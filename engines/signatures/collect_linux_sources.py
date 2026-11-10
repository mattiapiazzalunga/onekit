# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Collect corresponding Debian source packages using authenticated APT indexes."""
import argparse
import hashlib
import json
import os
import re
import subprocess
from email.parser import Parser
from pathlib import Path


def collect(work):
    work = work.resolve()
    if not (work / '.onekit-dss-authoring').is_file():
        raise ValueError('build_directory_marker')
    environment = {**os.environ, 'APT_CONFIG': str(work / 'apt.conf')}
    sources = {}
    binaries = []
    for package in sorted((work / 'debs').glob('*.deb')):
        result = subprocess.run(['dpkg-deb', '-f', str(package)],
                                check=True, capture_output=True, text=True)
        metadata = Parser().parsestr(result.stdout)
        name, version, source = metadata['Package'], metadata['Version'], metadata.get('Source', '')
        match = re.fullmatch(r'([a-z0-9.+-]+)(?: \(([^()\s]+)\))?', source or name)
        if not match:
            raise ValueError('source_coordinate')
        source_name, source_version = match[1], match[2] or version
        if not re.fullmatch(r'[a-zA-Z0-9.+:~_-]+', source_version):
            raise ValueError('source_version')
        with package.open('rb') as stream:
            checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
        binaries.append({'package': name, 'version': version, 'file': package.name,
                         'sha256': checksum, 'bytes': package.stat().st_size,
                         'source': f'{source_name}={source_version}'})
        sources[f'{source_name}={source_version}'] = None
    destination = work / 'sources'
    destination.mkdir(exist_ok=True)
    for coordinate in sources:
        print('SOURCE', coordinate, flush=True)
        subprocess.run(['apt-get', 'source', '--download-only', '-y', coordinate],
                       env=environment, cwd=destination, check=True)
    files = []
    for path in sorted(destination.iterdir()):
        if not path.is_file():
            continue
        with path.open('rb') as stream:
            checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
        files.append({'file': path.name, 'sha256': checksum, 'bytes': path.stat().st_size})
    manifest = {'schema': 'onekit-dss-linux-dependencies-v1', 'architecture': 'i386',
                'distribution': 'debian-bookworm', 'licenseReview': 'required',
                'binaries': binaries, 'sources': files}
    (work / 'linux-dependencies.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('work', type=Path)
    collect(parser.parse_args().work)
