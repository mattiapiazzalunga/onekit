from pathlib import Path
from types import SimpleNamespace


def test_missing_metadata_requires_exact_reviewed_license_and_version(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / 'scripts'))
    from check_licenses import verified_file_license
    license_file = tmp_path / 'resvg_py-0.5.0.dist-info/licenses/LICENSE'
    license_file.parent.mkdir(parents=True)
    content = (Path(__file__).parent / 'fixtures/resvg-py-0.5.0-LICENSE.txt').read_bytes().replace(b'\r\n', b'\n')
    distribution = SimpleNamespace(metadata={'Name': 'resvg_py'}, version='0.5.0',
                                   files=[license_file.relative_to(tmp_path)],
                                   locate_file=lambda file: tmp_path / file)
    for newline in (b'\n', b'\r\n'):
        license_file.write_bytes(content.replace(b'\n', newline))
        assert verified_file_license(distribution) == 'MIT'
    license_file.write_bytes(content + b'Altered terms')
    assert verified_file_license(distribution) is None
    license_file.write_bytes(content)
    distribution.version = '0.5.1'
    assert verified_file_license(distribution) is None
    distribution.version = '0.5.0'
    distribution.files = []
    assert verified_file_license(distribution) is None
