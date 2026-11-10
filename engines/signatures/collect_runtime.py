# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Collect original Maven binaries, sources, inherited POMs and their digests.

Offline authoring only; run Maven dependency:sources first. Missing source or
license metadata is a build error, never inferred permission to distribute.
This inventory does not replace a review of the applicable license obligations.
"""
import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
from xml.etree import ElementTree


def digest(path):
    with path.open('rb') as stream:
        value = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'sha256': value, 'bytes': path.stat().st_size}


def read_pom(path):
    tree = ElementTree.parse(path)
    for element in tree.iter():
        element.tag = element.tag.split('}')[-1]
    return tree.getroot()


def collect(classpath, repository, output):
    repository = repository.resolve()
    output.mkdir(parents=True, exist_ok=True)
    rows = []

    def copy(path):
        relative = path.resolve().relative_to(repository)
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        return {'path': relative.as_posix(), **digest(path)}

    def pom_metadata(path, seen=None):
        seen = set() if seen is None else seen
        if path in seen or len(seen) >= 32:
            raise ValueError('pom_parent_cycle')
        seen.add(path)
        pom = read_pom(path)
        files = [copy(path)]
        licenses = [{'name': item.findtext('name'), 'url': item.findtext('url')}
                    for item in pom.findall('./licenses/license')]
        parent = pom.find('parent')
        if parent is not None:
            group, artifact, version = (parent.findtext(key) for key in ('groupId', 'artifactId', 'version'))
            if not all((group, artifact, version)) or any('${' in value for value in (group, artifact, version)):
                raise ValueError('pom_parent_unresolved')
            parent_path = repository / group.replace('.', '/') / artifact / version / f'{artifact}-{version}.pom'
            inherited, parent_files = pom_metadata(parent_path, seen)
            files.extend(parent_files)
            licenses = licenses or inherited
        if not licenses or any(not item['name'] for item in licenses):
            raise ValueError(f'license_metadata_missing:{path.name}')
        return licenses, files

    for item in classpath.read_text(encoding='utf-8').strip().split(os.pathsep):
        binary = Path(item).resolve()
        relative = binary.relative_to(repository)
        version, artifact = relative.parts[-2], relative.parts[-3]
        group = '.'.join(relative.parts[:-3])
        source = binary.with_name(binary.stem + '-sources.jar')
        if not source.is_file():
            raise ValueError(f'corresponding_source_missing:{group}:{artifact}:{version}')
        licenses, poms = pom_metadata(binary.with_suffix('.pom'))
        rows.append({'coordinate': f'{group}:{artifact}:{version}', 'binary': copy(binary),
                     'source': copy(source), 'poms': poms, 'licenses': licenses})
    manifest = {'schema': 'onekit-dss-java-dependencies-v1', 'dssVersion': '6.5.1',
                'licenseReview': 'required', 'components': sorted(rows, key=lambda row: row['coordinate'])}
    locked = json.loads(Path(__file__).with_name('dependencies.lock.json').read_text(encoding='utf-8'))
    if manifest['components'] != locked['components']:
        raise ValueError('dependency_lock_mismatch')
    (output / 'dependencies.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--classpath', required=True, type=Path)
    parser.add_argument('--repository', type=Path, default=Path.home() / '.m2/repository')
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    result = collect(arguments.classpath, arguments.repository, arguments.output)
    print(json.dumps({'components': len(result['components']), 'licenseReview': result['licenseReview']}))
