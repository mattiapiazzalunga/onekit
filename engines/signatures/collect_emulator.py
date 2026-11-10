# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Collect the pinned emulator source and original third-party notices offline."""
import argparse
import gzip
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

COMMIT = 'cc37f35c43bf14865d74ad76879ecf9410f69eb1'
ZSTD_LICENSE = '2c1a7fa704df8f3a606f6fc010b8b5aaebf403f3aeec339a12048f1ba7331a0b'


def collect(repository, output):
    repository = repository.resolve()
    commit = subprocess.check_output(['git', '-C', str(repository), 'rev-parse', COMMIT], text=True).strip()
    if commit != COMMIT:
        raise ValueError('emulator_source_commit')
    archived = subprocess.check_output(['git', '-C', str(repository), 'archive', '--format=tar', COMMIT])
    output.mkdir(parents=True, exist_ok=True)
    source = output / 'v86-source.tar.gz'
    # The engine uses Debian SeaBIOS with separately collected corresponding
    # Debian sources. Do not redistribute the upstream tree's unrelated old
    # prebuilt BIOS images as though this archive supplied their source.
    with (source.open('wb') as stream,
          gzip.GzipFile(fileobj=stream, mode='wb', mtime=0) as compressed,
          tarfile.open(fileobj=compressed, mode='w|') as target,
          tarfile.open(fileobj=io.BytesIO(archived)) as original):
        for member in original:
            if member.name.startswith('bios/') and member.name.endswith('.bin'):
                continue
            member.uid = member.gid = 0
            member.uname = member.gname = ''
            target.addfile(member, original.extractfile(member) if member.isfile() else None)
    rows = []

    def record(path, origin):
        rows.append({'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'bytes': path.stat().st_size, 'origin': origin})

    record(source, f'https://github.com/copy/v86/tree/{COMMIT}')
    for name, destination in (('LICENSE', 'V86-LICENSE.txt'), ('LICENSE.MIT', 'V86-FLOPPY-LICENSE.txt'),
                              ('lib/softfloat/softfloat.c', 'SOFTFLOAT-SOURCE-NOTICE.c')):
        data = subprocess.check_output(['git', '-C', str(repository), 'show', f'{COMMIT}:{name}'])
        path = output / destination;path.write_bytes(data)
        record(path, f'https://github.com/copy/v86/blob/{COMMIT}/{name}')
    license_data = Path(__file__).with_name('third-party').joinpath('ZSTD-LICENSE.txt').read_bytes()
    if hashlib.sha256(license_data).hexdigest() != ZSTD_LICENSE:
        raise ValueError('zstd_license_integrity')
    path = output / 'ZSTD-LICENSE.txt';path.write_bytes(license_data)
    record(path, 'https://github.com/facebook/zstd/blob/v1.4.5/LICENSE')
    metadata = {'schema': 'onekit-dss-emulator-sources-v1', 'version': '0.5.472', 'commit': COMMIT,
                'zstdLicenseChoice': 'BSD-3-Clause', 'files': rows}
    (output / 'emulator-sources.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    return metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(collect(args.repository, args.output)))
