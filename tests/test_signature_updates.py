import datetime as dt
import importlib.util
import json
from pathlib import Path
import zipfile

import pytest

spec = importlib.util.spec_from_file_location('signature_updates', Path(__file__).resolve().parents[1] / 'scripts/check_signature_updates.py')
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)
NOW = dt.datetime(2026, 10, 30, tzinfo=dt.UTC)


def xml(date, extra=''):
    return f'<TrustServiceStatusList xmlns="http://uri.etsi.org/02231/v2#"><SchemeInformation><NextUpdate><dateTime>{date}</dateTime></NextUpdate></SchemeInformation>{extra}</TrustServiceStatusList>'.encode()


def fixture(root):
    engine = root / 'engines/signatures'
    engine.mkdir(parents=True)
    (engine / 'pom.xml').write_text('<project xmlns="http://maven.apache.org/POM/4.0.0"><properties><dss.version>6.5.1</dss.version></properties></project>')
    (engine / 'dependencies.lock.json').write_text('{"dssVersion":"6.5.1"}')
    directory = root / 'src/onekit/data'
    directory.mkdir(parents=True)
    data = xml('2026-12-01T00:00:00Z')
    with zipfile.ZipFile(directory / 'eu-trust-lists.zip', 'w') as archive:
        archive.writestr('manifest.json', json.dumps({'lotl': 'lotl.xml', 'trusted_lists': [{'path': 'tl/IT.xml', 'url': 'https://example.org/it.xml'}]}))
        archive.writestr('lotl.xml', data)
        archive.writestr('tl/IT.xml', data)
    return {monitor.RELEASE: b'{"tag_name":"6.5.1","prerelease":false}', monitor.LOTL: data, 'https://example.org/it.xml': data}


def test_unchanged_fresh_dependencies_do_not_alert(tmp_path):
    remote = fixture(tmp_path)
    assert monitor.check(tmp_path, remote.__getitem__, NOW)['attention'] is False


def test_release_and_xml_changes_only_alert_and_never_modify_snapshot(tmp_path):
    remote = fixture(tmp_path)
    snapshot = tmp_path / 'src/onekit/data/eu-trust-lists.zip'
    original = snapshot.read_bytes()
    remote[monitor.RELEASE] = b'{"tag_name":"6.6","prerelease":false}'
    remote['https://example.org/it.xml'] = xml('2026-12-02T00:00:00Z', '<Changed/>')
    result = monitor.check(tmp_path, remote.__getitem__, NOW)
    assert result['attention'] and not result['failed']
    assert result['rows'][0]['attention']
    assert next(row for row in result['rows'] if row['source'] == 'tl/IT.xml')['changed']
    assert snapshot.read_bytes() == original


@pytest.mark.parametrize('remote_value', [xml('2026-11-02T00:00:00Z'), b'<TrustServiceStatusList xmlns="http://uri.etsi.org/02231/v2#"/>'])
def test_expiring_or_unknown_dates_alert(tmp_path, remote_value):
    remote = fixture(tmp_path)
    remote[monitor.LOTL] = remote_value
    assert monitor.check(tmp_path, remote.__getitem__, NOW)['attention']


def test_expiry_alerts_even_when_the_remote_bytes_have_not_changed(tmp_path):
    remote = fixture(tmp_path)
    result = monitor.check(tmp_path, remote.__getitem__, dt.datetime(2026, 11, 27, tzinfo=dt.UTC))
    assert result['attention'] and not result['failed']
    assert all(not row['changed'] for row in result['rows'][1:])


def test_partial_network_failure_alerts_but_preserves_successful_checks(tmp_path):
    remote = fixture(tmp_path)
    del remote['https://example.org/it.xml']
    result = monitor.check(tmp_path, remote.__getitem__, NOW)
    assert result['attention'] and result['failed']
    assert len(result['rows']) == 2
    monitor.write_report(result, tmp_path / 'reports')
    assert 'Failed checks' in (tmp_path / 'reports/signature-updates.md').read_text()


def test_missing_configuration_and_mismatched_lock_fail_visibly(tmp_path):
    assert monitor.check(tmp_path, lambda _: b'{}', NOW)['failed']
    remote = fixture(tmp_path)
    (tmp_path / 'engines/signatures/dependencies.lock.json').write_text('{"dssVersion":"6.5"}')
    assert monitor.check(tmp_path, remote.__getitem__, NOW)['failed']


def test_xml_restrictions_dates_and_release_versions():
    with pytest.raises(ValueError):
        monitor.expiry(b'<!DOCTYPE x [<!ENTITY y "payload">]><x/>')
    with pytest.raises(ValueError):
        monitor.expiry(xml('2026-12-01T00:00:00'))
    with pytest.raises(ValueError):
        monitor.version('6.6-RC1')
    assert monitor.version('v6.5.0') == monitor.version('6.5')
    assert monitor.version('6.5.1') > monitor.version('6.5')


def test_public_download_retries_connection_failure_once_and_keeps_tls_defaults(monkeypatch):
    import io
    calls = []
    def open_url(request, **options):
        calls.append((request, options))
        if len(calls) == 1:
            raise ConnectionResetError('Transient source connection reset')
        return io.BytesIO(b'public source')
    monkeypatch.setattr(monitor.urllib.request, 'urlopen', open_url)
    assert monitor.fetch_public('https://example.org/list.xml') == b'public source'
    assert len(calls) == 2
    assert all(options == {'timeout': 30} for _, options in calls)
