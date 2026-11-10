# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Author digest-pinned 64 KiB ranges for lazy guest filesystem reads.

Java's modules image is large; reading a page must not download the whole file.
The original logical file digest and exact bytes are retained in the manifest.
"""
import argparse
import hashlib
import json
from pathlib import Path

CHUNK_SIZE = 65536


def chunk_filesystem(manifest_path, filesystem_root, output):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('schema') != 'onekit-dss-vm-v1':
        raise ValueError('engine_manifest')
    chunk_directory = output / 'chunks'
    chunk_directory.mkdir(parents=True, exist_ok=True)
    rows = list(manifest['files'].items())
    for name, descriptor in rows:
        if not name.startswith('fs/') or descriptor['bytes'] <= CHUNK_SIZE:
            continue
        basename = name.removeprefix('fs/')
        if Path(basename).name != basename or '\\' in basename:
            raise ValueError('filesystem_path')
        source = filesystem_root / basename
        total = 0
        whole = hashlib.sha256()
        chunks = []
        with source.open('rb') as stream:
            while data := stream.read(CHUNK_SIZE):
                whole.update(data)
                total += len(data)
                digest = hashlib.sha256(data).hexdigest()
                target = chunk_directory / f'{digest}.bin'
                target.write_bytes(data)
                key = f'chunks/{digest}.bin'
                manifest['files'][key] = {'sha256': digest, 'bytes': len(data)}
                chunks.append(key)
        if whole.hexdigest() != descriptor['sha256'] or total != descriptor['bytes']:
            raise ValueError('filesystem_integrity')
        descriptor.update(chunks=chunks, chunkSize=CHUNK_SIZE)
    target = output / 'engine-manifest.json'
    temporary = target.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(manifest, separators=(',', ':')) + '\n', encoding='utf-8')
    temporary.replace(target)
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--filesystem-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = chunk_filesystem(args.manifest, args.filesystem_root, args.output)
    print(json.dumps({'files': len(result['files'])}))
