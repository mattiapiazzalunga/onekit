# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Attach verified snapshot and trust provenance to an authored asset manifest."""
import argparse
import hashlib
import json
from pathlib import Path


def attach(assets, snapshot, metadata, trust_metadata):
    manifest = json.loads((assets / 'engine-manifest.json').read_text(encoding='utf-8'))
    with snapshot.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    if digest != metadata['sha256'] or snapshot.stat().st_size != metadata['bytes']:
        raise ValueError('snapshot_integrity')
    if not snapshot.resolve().is_relative_to(assets.resolve()):
        raise ValueError('snapshot_asset_path')
    name = snapshot.relative_to(assets).as_posix()
    manifest.update(state=name, stateCompression=metadata['compression'],
                    stateExpandedBytes=metadata['expandedBytes'], stateExpandedSha256=metadata['expandedSha256'],
                    trustLists=trust_metadata)
    manifest['files'][name] = {'sha256': digest, 'bytes': metadata['bytes']}
    (assets / 'engine-manifest.json').write_text(json.dumps(manifest, separators=(',', ':')) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--assets', required=True, type=Path)
    parser.add_argument('--snapshot', required=True, type=Path)
    parser.add_argument('--metadata', required=True, type=Path)
    parser.add_argument('--trust-metadata', required=True, type=Path)
    args = parser.parse_args()
    attach(args.assets, args.snapshot, json.loads(args.metadata.read_text(encoding='utf-8')),
           json.loads(args.trust_metadata.read_text(encoding='utf-8')))
