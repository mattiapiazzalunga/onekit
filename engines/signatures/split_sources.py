# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Prepare static source downloads below common static-host file-size limits."""
import argparse
import hashlib
import json
import shutil
import tarfile
from pathlib import Path


def split(archive, metadata, output):
    chunks = [];whole = hashlib.sha256();total = 0
    directory = output / 'chunks';directory.mkdir(parents=True, exist_ok=True)
    with archive.open('rb') as stream:
        while data := stream.read(4194304):
            digest = hashlib.sha256(data).hexdigest();whole.update(data);total += len(data)
            name = f'chunks/{digest}.bin';(output / name).write_bytes(data)
            chunks.append({'path': name, 'bytes': len(data), 'sha256': digest})
    if whole.hexdigest() != metadata['sha256'] or total != metadata['bytes']:
        raise ValueError('source_archive_integrity')
    index = {'schema': 'onekit-dss-source-download-v1', 'archive': 'onekit-dss-corresponding-source.tar.gz',
             'sha256': whole.hexdigest(), 'bytes': total, 'chunks': chunks,
             'restore': 'restore.py'}
    shutil.copyfile(Path(__file__).with_name('restore_sources.py'), output / 'restore.py')
    notices = [b'OneKit original-DSS runtime distribution\n\n',
        b'Original third-party license and copyright notices follow unchanged.\n',
        b'Corresponding sources and public rebuild tools are downloadable in full using sources.json and restore.py.\n',
        b'Download restore.py from the same directory as sources.json. Supply that HTTPS directory URL:\n',
        b'python restore.py HTTPS_SOURCE_DIRECTORY onekit-dss-corresponding-source.tar.gz\n\n']
    with tarfile.open(archive) as source:
        for member in source:
            if member.isfile() and (member.name.startswith('notices/') or '/third-party/' in member.name
                                   or member.name.endswith(('LICENSING.txt', 'V86-LICENSE.txt',
                                                            'V86-FLOPPY-LICENSE.txt', 'ZSTD-LICENSE.txt',
                                                            'SOFTFLOAT-SOURCE-NOTICE.c'))):
                notices.extend([b'\n===== ' + member.name.encode() + b' =====\n', source.extractfile(member).read(), b'\n'])
    (output / 'NOTICES.txt').write_bytes(b''.join(notices))
    index['assets'] = {name: {'bytes': (output / name).stat().st_size,
                             'sha256': hashlib.sha256((output / name).read_bytes()).hexdigest()}
                       for name in ('NOTICES.txt', 'restore.py')}
    (output / 'sources.json').write_text(json.dumps(index, indent=2) + '\n', encoding='utf-8')
    return {'bytes': total, 'chunks': len(chunks), 'files': len(chunks) + 3}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--metadata', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(split(args.archive, json.loads(args.metadata.read_text(encoding='utf-8')), args.output)))
