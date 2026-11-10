# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Assemble verified corresponding sources and original redistribution notices.

Build-time only. Input directories contain public third-party source/build
materials, never documents supplied to a running validation worker.
"""
import argparse
import gzip
import hashlib
import io
import json
import tarfile
import zipfile
from pathlib import Path, PurePosixPath


def package(linux, java, emulator, adapter, output):
    linux_manifest = json.loads((linux / 'linux-dependencies.json').read_text(encoding='utf-8'))
    java_manifest = json.loads((java / 'dependencies.json').read_text(encoding='utf-8'))
    emulator_manifest = json.loads((emulator / 'emulator-sources.json').read_text(encoding='utf-8'))
    locked = json.loads((adapter / 'dependencies.lock.json').read_text(encoding='utf-8'))
    if java_manifest['components'] != locked['components']:
        raise ValueError('dependency_lock_mismatch')
    entries = {}
    contents = {}

    def add(path, name, descriptor=None):
        pure = PurePosixPath(name)
        if pure.is_absolute() or '..' in pure.parts or '\\' in name:
            raise ValueError('source_archive_path')
        if name in entries:
            return
        with path.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        size = path.stat().st_size
        if descriptor is not None and (digest != descriptor['sha256'] or size != descriptor['bytes']):
            raise ValueError('corresponding_source_integrity')
        entries[name] = (path, {'sha256': digest, 'bytes': size})

    for row in linux_manifest['sources']:
        add(linux / 'sources' / row['file'], 'linux/sources/' + row['file'], row)
    add(linux / 'linux-dependencies.json', 'linux/dependencies.json')
    # Regular notices include the targets of Debian's intra-package symlinks.
    for path in sorted((linux / 'root/usr/share/doc').rglob('copyright')):
        if not path.is_symlink() and path.is_file():
            add(path, 'notices/linux/' + path.relative_to(linux / 'root/usr/share/doc').as_posix())
    for row in java_manifest['components']:
        for item in [row['source'], *row['poms']]:
            add(java / item['path'], 'java/' + item['path'], item)
        binary = row['binary']
        path = java / binary['path']
        with path.open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != binary['sha256']:
                raise ValueError('binary_notice_integrity')
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                basename = PurePosixPath(name).name.lower()
                if not name.endswith(('/', '.class')) and any(word in basename for word in ('license', 'notice', 'copying')):
                    target = 'notices/java/' + row['coordinate'].replace(':', '/') + '/' + name
                    if '..' in PurePosixPath(target).parts or '\\' in target:
                        raise ValueError('notice_path')
                    data = archive.read(name)
                    contents[target] = data
                    entries[target] = (None, {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
    add(java / 'dependencies.json', 'java/dependencies.json')
    for row in emulator_manifest['files']:
        add(emulator / row['file'], 'emulator/' + row['file'], row)
    add(emulator / 'emulator-sources.json', 'emulator/dependencies.json')
    for path in sorted(adapter.rglob('*')):
        relative = path.relative_to(adapter)
        if path.is_file() and not path.is_symlink() and not any(
                part in ('target', '__pycache__') for part in relative.parts) and path.name != 'classpath.txt':
            add(path, 'adapter/engines/signatures/' + relative.as_posix())
    core = adapter.parents[1]
    for name in ('LICENSE', 'NOTICE'):
        add(core / name, 'adapter/' + name)
    for name in ('host.mjs', 'browser.mjs', 'node_worker.mjs', 'LICENSING.txt'):
        add(core / 'src/onekit/data/signatures' / name, 'adapter/src/onekit/data/signatures/' + name)
    add(core / 'src/onekit/tools/signature_dss.py', 'adapter/src/onekit/tools/signature_dss.py')
    metadata = {'schema': 'onekit-dss-corresponding-source-v1', 'dssVersion': '6.5.1',
                'licenseReview': 'required',
                'files': {name: descriptor for name, (_, descriptor) in sorted(entries.items())}}
    index = json.dumps(metadata, indent=2).encode() + b'\n'
    output.parent.mkdir(parents=True, exist_ok=True)
    with (output.open('wb') as stream, gzip.GzipFile(fileobj=stream, mode='wb', mtime=0) as compressed,
          tarfile.open(fileobj=compressed, mode='w|') as archive):
        for name, (path, descriptor) in sorted(entries.items()):
            info = tarfile.TarInfo(name);info.size = descriptor['bytes']
            info.mode = 0o755 if name.endswith('.sh') else 0o644
            if path is None:
                archive.addfile(info, io.BytesIO(contents[name]))
            else:
                with path.open('rb') as source:
                    archive.addfile(info, source)
        info = tarfile.TarInfo('source-index.json');info.size = len(index);info.mode = 0o644
        archive.addfile(info, io.BytesIO(index))
    with output.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    result = {'sha256': digest, 'bytes': output.stat().st_size, 'files': len(entries)}
    output.with_suffix(output.suffix + '.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ('linux', 'java', 'emulator', 'adapter', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(package(args.linux, args.java, args.emulator, args.adapter, args.output)))
