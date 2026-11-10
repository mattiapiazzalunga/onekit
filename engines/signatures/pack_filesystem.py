# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Author a v86 v3 filesystem with full SHA-256 content-addressed files."""
import argparse
import hashlib
import json
import os
import shutil
import stat
from pathlib import Path


def pack(root, output, excluded):
    root, output = root.resolve(), output.resolve()
    if output.is_relative_to(root):
        raise ValueError('output_inside_filesystem')
    content = output / 'fs'
    content.mkdir(parents=True, exist_ok=True)
    total = 0

    def directory(path):
        nonlocal total
        rows = []
        for item in sorted(path.iterdir(), key=lambda item: item.name):
            relative = '/' + item.relative_to(root).as_posix()
            if relative in excluded:
                continue
            info = item.lstat()
            mode = info.st_mode
            if stat.S_ISLNK(mode):
                payload = os.readlink(item)
            elif stat.S_ISDIR(mode):
                payload = directory(item)
            elif stat.S_ISREG(mode):
                with item.open('rb') as stream:
                    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                payload = digest + '.bin'
                target = content / payload
                if not target.exists():
                    shutil.copyfile(item, target)
                else:
                    with target.open('rb') as stream:
                        if hashlib.file_digest(stream, 'sha256').hexdigest() != digest:
                            raise ValueError('content_integrity')
            else:
                continue
            total += info.st_size
            rows.append([item.name, info.st_size, int(info.st_mtime), mode, info.st_uid, info.st_gid, payload])
        return rows

    tree = directory(root)
    result = {'fsroot': tree, 'version': 3, 'size': total}
    (output / 'fs.json').write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--exclude', action='append', default=[])
    args = parser.parse_args()
    pack(args.root, args.output, set(args.exclude))
