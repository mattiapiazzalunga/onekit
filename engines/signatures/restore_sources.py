# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Download and reconstruct the public corresponding-source archive.

Usage: python restore.py HTTPS_SOURCE_DIRECTORY output.tar.gz
No user document is read or uploaded. Existing output files are never replaced.
"""
import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def restore(base, output):
    url = urllib.parse.urlsplit(base)
    if url.scheme != 'https' or not url.hostname or url.username or url.password or url.query or url.fragment:
        raise ValueError('source_origin')
    base = base.rstrip('/') + '/'
    with urllib.request.urlopen(base + 'sources.json', timeout=60) as response:
        raw = response.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError('source_index_size')
    index = json.loads(raw)
    if index.get('schema') != 'onekit-dss-source-download-v1' or not 1 <= len(index['chunks']) <= 256:
        raise ValueError('source_index')
    total = 0;whole = hashlib.sha256()
    with Path(output).open('xb') as stream:
        for row in index['chunks']:
            if not re.fullmatch(r'chunks/[a-f0-9]{64}\.bin', row['path']) or not 0 < row['bytes'] <= 4194304:
                raise ValueError('source_chunk')
            with urllib.request.urlopen(base + row['path'], timeout=120) as response:
                data = response.read(row['bytes'] + 1)
            if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                raise ValueError('source_chunk_integrity')
            stream.write(data);whole.update(data);total += len(data)
    if total != index['bytes'] or whole.hexdigest() != index['sha256']:
        raise ValueError('source_archive_integrity')
    return {'bytes': total, 'sha256': whole.hexdigest()}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('python restore.py HTTPS_SOURCE_DIRECTORY output.tar.gz')
    print(json.dumps(restore(sys.argv[1], sys.argv[2])))
