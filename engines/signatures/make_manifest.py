# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Pin every byte exposed to the guest before starting an authoring VM."""
import argparse
import hashlib
import json
from pathlib import Path


def descriptor(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'sha256': digest, 'bytes': path.stat().st_size}


def make(base, memory_mib=512):
    if memory_mib not in (384, 512):
        raise ValueError('engine_memory_profile')
    names = {'wasm': 'v86.wasm', 'runtime': 'libv86.mjs', 'bios': 'seabios.bin', 'vga': 'vgabios.bin',
             'kernel': 'kernel.bin', 'initrd': 'initrd.cpio.gz', 'filesystem': 'fs.json'}
    result = {'schema': 'onekit-dss-vm-v1', 'dssVersion': '6.5.1',
              'v86Version': '0.5.472+gcc37f35', 'memoryBytes': memory_mib * 1024 * 1024,
              'reportCommit': True, 'trustEvidence': True,
              **names, 'files': {name: descriptor(base / name) for name in names.values()}}

    def visit(rows):
        for row in rows:
            kind = row[3] & 0xf000
            if kind == 0x4000:
                visit(row[6])
            elif kind == 0x8000:
                filename = row[6]
                if Path(filename).name != filename or '\\' in filename:
                    raise ValueError('filesystem_content_path')
                item = descriptor(base / 'fs' / filename)
                if filename != item['sha256'] + '.bin':
                    raise ValueError('filesystem_content_digest')
                result['files']['fs/' + filename] = item
    visit(json.loads((base / 'fs.json').read_text(encoding='utf-8'))['fsroot'])
    (base / 'engine-manifest.json').write_text(json.dumps(result, separators=(',', ':')) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('assets', type=Path)
    parser.add_argument('--memory-mib', type=int, choices=(384, 512), default=512)
    args = parser.parse_args()
    make(args.assets, args.memory_mib)
