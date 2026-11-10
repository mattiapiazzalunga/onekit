"""Original-DSS offline worker integration; opt in with its compiled classpath."""
import datetime
import hashlib
import os
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

import pytest
from test_integrity_tools import signed_cms, signed_pdf
from test_signature_validation import pki

CLASSPATH = os.environ.get('ONEKIT_DSS_ENGINE_CLASSPATH')
pytestmark = pytest.mark.skipif(not CLASSPATH, reason='DSS engine classpath is not configured')
ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def trust_asset(tmp_path_factory):
    directory = tmp_path_factory.mktemp('dss-authenticated-trust')
    subprocess.run([sys.executable, str(ROOT / 'engines/signatures/prepare_trust.py'), str(directory)],
                   check=True, capture_output=True, timeout=120)
    asset = directory / 'trust.ser.gz'
    result = subprocess.run(['java', '-Dorg.slf4j.simpleLogger.defaultLogLevel=off', '-cp', CLASSPATH,
                             'org.onekit.signatures.TrustSnapshotBuilder', str(directory), str(asset)],
                            check=True, capture_output=True, text=True, timeout=120)
    assert 'ONEKIT_TRUST=30|' in result.stdout
    return asset, hashlib.sha256(asset.read_bytes()).hexdigest()


def invoke(trust_asset, jobs, commands, digest=None):
    asset, expected = trust_asset
    return subprocess.run(['java', '-Xmx256m', '-Djava.awt.headless=true',
                           '-Dorg.slf4j.simpleLogger.defaultLogLevel=off', '-cp', CLASSPATH,
                           'org.onekit.signatures.OfflineEngine', str(asset), digest or expected, str(jobs)],
                          check=False, input=commands, capture_output=True, text=True, timeout=120)


def job(directory, **values):
    directory.mkdir(parents=True, exist_ok=True)
    moment = datetime.datetime.now(datetime.UTC).isoformat()
    properties = {'document': 'signature.p7m', 'validationTime': moment, **values}
    (directory / 'request.properties').write_text(
        ''.join(f'{key}={value}\n' for key, value in properties.items()), encoding='utf-8')
    return directory


def indications(path):
    tree = ElementTree.fromstring(path.read_bytes())
    return [node.text for node in tree.iter() if node.tag.endswith('}Indication')]


def test_evidence_certificate_cannot_become_a_trust_anchor(tmp_path, trust_asset):
    from cryptography.hazmat.primitives import serialization

    _, root, _, content, signature = pki()
    directory = job(tmp_path / 'unknown', detached='original.bin',
                    **{'certificate.count': 1, 'certificate.0': 'root.der'})
    (directory / 'signature.p7m').write_bytes(signature)
    (directory / 'original.bin').write_bytes(content)
    (directory / 'root.der').write_bytes(root.public_bytes(serialization.Encoding.DER))
    result = invoke(trust_asset, tmp_path, 'RUN unknown\n')
    assert result.returncode == 0, result.stderr
    assert 'ONEKIT_DSS_DONE=unknown' in result.stdout
    assert indications(directory / 'simple.xml') == ['INDETERMINATE']
    for report in ('simple', 'detailed', 'diagnostic', 'etsi'):
        ElementTree.fromstring((directory / f'{report}.xml').read_bytes())


@pytest.mark.parametrize('pdf', [False, True])
def test_tampered_document_is_never_successful(tmp_path, trust_asset, pdf):
    directory = job(tmp_path / 'tampered', document='signature.pdf' if pdf else 'signature.p7m')
    if pdf:
        data = signed_pdf().replace(b'/Producer (pypdf)', b'/Producer (Qypdf)', 1)
        (directory / 'signature.pdf').write_bytes(data)
    else:
        (directory / 'signature.p7m').write_bytes(signed_cms(b'original', attached=False))
        (directory / 'original.bin').write_bytes(b'changed')
        with (directory / 'request.properties').open('a', encoding='utf-8') as stream:
            stream.write('detached=original.bin\n')
    result = invoke(trust_asset, tmp_path, 'RUN tampered\n')
    assert result.returncode == 0, result.stderr
    assert 'ONEKIT_DSS_DONE=tampered' in result.stdout
    assert indications(directory / 'simple.xml') == ['TOTAL_FAILED']


@pytest.mark.parametrize('moment', ['2000-01-01T00:00:00Z', '2100-01-01T00:00:00Z'])
def test_trust_cache_is_not_valid_outside_its_window(tmp_path, trust_asset, moment):
    directory = job(tmp_path / 'expired', validationTime=moment)
    (directory / 'signature.p7m').write_bytes(signed_cms(b'original'))
    result = invoke(trust_asset, tmp_path, 'RUN expired\n')
    assert result.returncode == 0, result.stderr
    assert 'ONEKIT_DSS_ERROR=expired' in result.stdout
    assert not (directory / 'simple.xml').exists()


def test_modified_trust_cache_is_rejected_before_deserialization(tmp_path, trust_asset):
    result = invoke(trust_asset, tmp_path, '', digest='0' * 64)
    assert result.returncode != 0
    assert 'trust_asset_digest' in result.stderr
    assert 'ONEKIT_DSS_READY' not in result.stdout


def test_request_cannot_read_files_outside_its_job(tmp_path, trust_asset):
    directory = job(tmp_path / 'escape', document='../outside.p7m')
    (tmp_path / 'outside.p7m').write_bytes(signed_cms(b'outside'))
    result = invoke(trust_asset, tmp_path, 'RUN escape\n')
    assert result.returncode == 0, result.stderr
    assert 'ONEKIT_DSS_ERROR=escape' in result.stdout
    assert not (directory / 'simple.xml').exists()


def test_serial_protocol_rejects_path_traversal_and_commands(tmp_path, trust_asset):
    result = invoke(trust_asset, tmp_path, 'RUN ../escape\nRUN x;echo-private\n')
    assert result.returncode == 0, result.stderr
    assert result.stdout.count('ONEKIT_DSS_PROTOCOL_ERROR=1') == 2
    assert 'echo-private' not in result.stdout


def test_failing_job_does_not_stop_the_next_validation(tmp_path, trust_asset):
    job(tmp_path / 'missing')
    valid = job(tmp_path / 'unknown')
    (valid / 'signature.p7m').write_bytes(signed_cms(b'original'))
    result = invoke(trust_asset, tmp_path, 'RUN missing\nRUN unknown\n')
    assert result.returncode == 0, result.stderr
    assert 'ONEKIT_DSS_ERROR=missing' in result.stdout
    assert 'ONEKIT_DSS_DONE=unknown' in result.stdout
    assert indications(valid / 'simple.xml') == ['INDETERMINATE']


def test_failed_reused_job_cannot_leave_a_stale_positive_report(tmp_path, trust_asset):
    directory = job(tmp_path / 'reused', document='missing.p7m')
    (directory / 'simple.xml').write_text('<stale>TOTAL_PASSED</stale>', encoding='utf-8')
    result = invoke(trust_asset, tmp_path, 'RUN reused\n')
    assert result.returncode == 0, result.stderr
    assert 'ONEKIT_DSS_ERROR=reused' in result.stdout
    assert not (directory / 'simple.xml').exists()


@pytest.mark.skipif(not os.environ.get('ONEKIT_DSS_HISTORICAL_UK_XML'), reason='Historical UK list is not configured')
@pytest.mark.parametrize('altered', [False, True])
def test_historical_uk_is_authenticated_by_original_dss(tmp_path, altered):
    historical = Path(os.environ['ONEKIT_DSS_HISTORICAL_UK_XML']).read_bytes()
    assert b'UKTSL31December2020' in historical
    if altered:
        historical = historical.replace(b'UKTSL31December2020', b'UKTSL31December2021', 1)
    path = tmp_path / 'historical.xml'
    path.write_bytes(historical)
    subprocess.run([sys.executable, str(ROOT / 'engines/signatures/prepare_trust.py'), str(tmp_path),
                    '--historical-uk', str(path)], check=True, capture_output=True, timeout=120)
    asset = tmp_path / 'trust.ser.gz'
    result = subprocess.run(['java', '-Dorg.slf4j.simpleLogger.defaultLogLevel=off', '-cp', CLASSPATH,
                             'org.onekit.signatures.TrustSnapshotBuilder', str(tmp_path), str(asset)],
                            check=False, capture_output=True, text=True, timeout=120)
    if altered:
        assert result.returncode != 0
        assert not asset.exists()
    else:
        assert result.returncode == 0, result.stderr
        assert 'ONEKIT_TL=UK|true|TOTAL_PASSED' in result.stdout
        assert 'ONEKIT_TRUST=31|' in result.stdout


@pytest.mark.skipif(not os.environ.get('ONEKIT_DSS_HISTORICAL_UK_XML'), reason='Historical UK list is not configured')
def test_authenticated_local_trust_overlay_uses_dss_and_not_user_roots(tmp_path, trust_asset):
    asset, _ = trust_asset
    directory = job(tmp_path / 'overlay', lotl='lotl.xml', **{
        'tl.count': 1, 'tl.0.url': 'https://ec.europa.eu/tools/lotl/Final_EU_TSL-UKsigned.xml',
        'tl.0.path': 'uk.xml'})
    (directory / 'lotl.xml').write_bytes((asset.parent / 'list-0.xml').read_bytes())
    (directory / 'uk.xml').write_bytes(Path(os.environ['ONEKIT_DSS_HISTORICAL_UK_XML']).read_bytes())
    (directory / 'signature.p7m').write_bytes(signed_cms(b'original'))
    result = invoke(trust_asset, tmp_path, 'RUN overlay\n')
    assert result.returncode == 0, result.stderr
    assert 'ONEKIT_DSS_DONE=overlay' in result.stdout, result.stdout
    assert indications(directory / 'simple.xml') == ['INDETERMINATE']


def test_invalid_trust_overlay_cannot_poison_the_next_job(tmp_path, trust_asset):
    asset, _ = trust_asset
    invalid = job(tmp_path / 'invalid', lotl='lotl.xml')
    data = (asset.parent / 'list-0.xml').read_bytes()
    (invalid / 'lotl.xml').write_bytes(data.replace(b'EUlistofthelists', b'EUlistoftheLISTS', 1))
    assert (invalid / 'lotl.xml').read_bytes() != data
    (invalid / 'signature.p7m').write_bytes(signed_cms(b'original'))
    valid = job(tmp_path / 'valid')
    (valid / 'signature.p7m').write_bytes(signed_cms(b'original'))
    result = invoke(trust_asset, tmp_path, 'RUN invalid\nRUN valid\n')
    assert result.returncode == 0, result.stderr
    assert 'ONEKIT_DSS_ERROR=invalid' in result.stdout
    assert 'ONEKIT_DSS_DONE=valid' in result.stdout
    assert not (invalid / 'simple.xml').exists()
    assert indications(valid / 'simple.xml') == ['INDETERMINATE']
