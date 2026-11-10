"""Differential samples, not a claim of exhaustive DSS/eIDAS equivalence.

Build tests/dss_reference with Maven, then set ONEKIT_DSS_CLASSPATH to its
target/classes plus the Maven dependency classpath. The oracle is offline and
has no trust anchors, so the generated self-signed test identities stay unknown.
"""
import os
import subprocess

import pytest
from test_integrity_tools import signed_cms, signed_pdf
from test_signature_validation import local_policy, pki, timestamped_inputs

from onekit import Artifact, execute

CLASSPATH = os.environ.get('ONEKIT_DSS_CLASSPATH')
pytestmark = pytest.mark.skipif(not CLASSPATH, reason='DSS reference classpath is not configured')


@pytest.mark.parametrize('algorithm,use_pss', [('rsa', False), ('rsa', True), ('ec', False)])
@pytest.mark.parametrize('altered', [False, True])
def test_detached_cms_main_indication_matches_dss(tmp_path, algorithm, use_pss, altered):
    signature = Artifact('signature.p7s', signed_cms(b'original', attached=False, algorithm=algorithm, use_pss=use_pss))
    original = Artifact('original.bin', b'altered' if altered else b'original')
    compare(tmp_path, [signature, original])


def test_attached_cms_main_indication_matches_dss(tmp_path):
    compare(tmp_path, [Artifact('signed.p7m', signed_cms(b'original'))])


@pytest.mark.parametrize('change', ['none', 'tampered', 'later_bytes'])
def test_pdf_main_indication_matches_dss(tmp_path, change):
    data = signed_pdf()
    if change == 'tampered':
        data = data.replace(b'/Producer (pypdf)', b'/Producer (Qypdf)', 1)
    elif change == 'later_bytes':
        data += b'\n%later bytes'
    compare(tmp_path, [Artifact('signed.pdf', data)])


@pytest.mark.parametrize('revoked,stale,use_ocsp,empty', [
    (False, False, False, False), (False, False, True, False),
    (True, False, False, False), (True, False, True, False),
    (False, True, False, False), (False, False, False, True),
])
def test_trusted_chain_and_revocation_match_dss(tmp_path, monkeypatch, revoked, stale, use_ocsp, empty):
    import datetime

    from cryptography.hazmat.primitives import serialization

    from onekit.tools import signature_validation
    local_policy(monkeypatch, revoked=revoked, stale=stale, use_ocsp=use_ocsp, empty=empty)
    _, root, _, content, signature = pki()
    spec, _ = signature_validation.validation_spec(None, datetime.datetime.now(datetime.UTC))
    root_path = tmp_path / 'root.der'; root_path.write_bytes(root.public_bytes(serialization.Encoding.DER))
    crl_path = tmp_path / 'evidence.crl'; ocsp_path = tmp_path / 'evidence.ocsp'
    if spec.local_knowledge.known_crls:
        crl_path.write_bytes(spec.local_knowledge.known_crls[0].crl_data.dump())
    if spec.local_knowledge.known_ocsps:
        ocsp_path.write_bytes(spec.local_knowledge.known_ocsps[0].ocsp_response_data.dump())
    compare(tmp_path, [Artifact('signature.p7s', signature), Artifact('original.bin', content)],
            [str(root_path), str(crl_path) if crl_path.exists() else '-', str(ocsp_path) if ocsp_path.exists() else '-'])


def compare(directory, files, trust_args=None):
    paths = []
    for file in files:
        path = directory / file.name
        path.write_bytes(file.data)
        paths.append(str(path))
    if trust_args:
        if len(paths) == 1:
            paths.append('-')
        paths.extend(trust_args)
    result = subprocess.run(['java', '-cp', CLASSPATH, 'Reference', *paths],
                            capture_output=True, text=True, check=False, timeout=60)
    assert result.returncode == 0, result.stderr
    rows = [line.split('=', 1)[1].split('|')[0] for line in result.stdout.splitlines()
            if line.startswith('ONEKIT_DSS_RESULT=')]
    ours = execute('signature-verify', files).details['validation']
    assert 'reason' not in ours, ours
    assert rows and all(row == ours['indication'] for row in rows), (rows, ours)
    return result.stdout


@pytest.mark.parametrize('container_format,profile', [
    ('cms', 'CAdES-BASELINE-T'), ('pdf-b', 'PAdES-BASELINE-B'),
    ('pdf', 'PAdES-BASELINE-T'), ('pdf-lt', 'PAdES-BASELINE-LT'),
    ('pdf-lta', 'PAdES-BASELINE-LTA'),
])
def test_trusted_timestamp_matches_dss(tmp_path, monkeypatch, container_format, profile):
    import datetime

    from cryptography.hazmat.primitives import serialization

    from onekit.tools import signature_validation
    local_policy(monkeypatch)
    files = timestamped_inputs(container_format)
    _, root, _, _, _ = pki()
    spec, _ = signature_validation.validation_spec(None, datetime.datetime.now(datetime.UTC))
    root_path = tmp_path / 'root.der'; root_path.write_bytes(root.public_bytes(serialization.Encoding.DER))
    crl_path = tmp_path / 'evidence.crl'; crl_path.write_bytes(spec.local_knowledge.known_crls[0].crl_data.dump())
    output = compare(tmp_path, files, [str(root_path), str(crl_path), '-'])
    assert f'ONEKIT_DSS_DETAILS={profile}|' in output


@pytest.mark.parametrize('algorithm', ['ed25519', 'ed448', 'dsa', 'brainpool', 'sha224-rsa', 'sha3-rsa', 'sha3-ecdsa'])
@pytest.mark.parametrize('altered', [False, True])
def test_trusted_additional_algorithms_match_dss(tmp_path, monkeypatch, algorithm, altered):
    import datetime

    from cryptography.hazmat.primitives import serialization
    from test_signature_algorithms import algorithm_inputs

    from onekit.tools import signature_validation
    local_policy(monkeypatch)
    files = algorithm_inputs(algorithm)
    if altered:
        files = [files[0], Artifact('original.bin', b'changed')]
    _, root, _, _, _ = pki()
    spec, _ = signature_validation.validation_spec(None, datetime.datetime.now(datetime.UTC))
    root_path = tmp_path / 'root.der'; root_path.write_bytes(root.public_bytes(serialization.Encoding.DER))
    crl_path = tmp_path / 'evidence.crl'; crl_path.write_bytes(spec.local_knowledge.known_crls[0].crl_data.dump())
    compare(tmp_path, files, [str(root_path), str(crl_path), '-'])
