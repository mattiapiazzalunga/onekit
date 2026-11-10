"""Reproducible memory selection for the separately authored original-DSS VM."""
import importlib.util
import json
from pathlib import Path

import pytest


def builder():
    path = Path(__file__).resolve().parents[1] / 'engines/signatures/make_manifest.py'
    spec = importlib.util.spec_from_file_location('dss_manifest_builder', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('memory_mib', [384, 512])
def test_manifest_records_supported_memory_without_changing_engine_bytes(tmp_path, memory_mib):
    for name in ('v86.wasm', 'libv86.mjs', 'seabios.bin', 'vgabios.bin', 'kernel.bin', 'initrd.cpio.gz'):
        (tmp_path / name).write_bytes(b'public-build-fixture')
    (tmp_path / 'fs.json').write_text(json.dumps({'fsroot': []}))
    result = builder().make(tmp_path, memory_mib)
    assert result['memoryBytes'] == memory_mib * 1024 * 1024
    assert result['dssVersion'] == '6.5.1'
    assert result['files']['v86.wasm']['bytes'] == len(b'public-build-fixture')
    assert json.loads((tmp_path / 'engine-manifest.json').read_bytes()) == result


def test_manifest_rejects_untested_memory_before_writing(tmp_path):
    with pytest.raises(ValueError, match='engine_memory_profile'):
        builder().make(tmp_path, 256)
    assert not (tmp_path / 'engine-manifest.json').exists()
