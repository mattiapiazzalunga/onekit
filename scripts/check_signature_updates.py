# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Maintenance alerts only: never install or trust downloaded material."""
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.parse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LOTL = 'https://ec.europa.eu/tools/lotl/eu-lotl.xml'
RELEASE = 'https://api.github.com/repos/esig/dss/releases/latest'
MAX_BYTES = 16 * 1024 * 1024
NS = {'t': 'http://uri.etsi.org/02231/v2#', 'm': 'http://maven.apache.org/POM/4.0.0'}


def fetch_public(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Invalid public source URL')
    request = urllib.request.Request(url, headers={'User-Agent': 'OneKit-signature-maintenance', 'Accept': '*/*'})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read(MAX_BYTES + 1)
            break
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt:
                raise
    if len(data) > MAX_BYTES:
        raise ValueError('Public source exceeds the download limit')
    return data


def parse_xml(data):
    if len(data) > MAX_BYTES or re.search(br'<!\s*(?:DOCTYPE|ENTITY)\b', data, re.I):
        raise ValueError('Unsafe or oversized XML')
    return ET.fromstring(data)


def expiry(data):
    value = parse_xml(data).findtext('t:SchemeInformation/t:NextUpdate/t:dateTime', namespaces=NS)
    if not value:
        return None
    instant = dt.datetime.fromisoformat(value.strip().replace('Z', '+00:00'))
    if instant.tzinfo is None:
        raise ValueError('Trust-list expiry has no timezone')
    return instant.astimezone(dt.UTC)


def version(value):
    match = re.fullmatch(r'v?(\d+(?:\.\d+)+)', value)
    if not match:
        raise ValueError('Expected a stable numeric DSS version')
    parts = list(map(int, match[1].split('.')))
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


def check(root=ROOT, fetcher=fetch_public, now=None):
    now = now or dt.datetime.now(dt.UTC)
    rows, errors = [], []
    try:
        current = parse_xml((root / 'engines/signatures/pom.xml').read_bytes()).findtext('m:properties/m:dss.version', namespaces=NS)
        lock = json.loads((root / 'engines/signatures/dependencies.lock.json').read_text())
        if lock['dssVersion'] != current:
            errors.append('DSS dependency lock differs from the Maven version; rebuild and review the engine.')
        release = json.loads(fetcher(RELEASE))
        if release.get('prerelease') or release.get('draft'):
            raise ValueError('The release endpoint did not return a stable release')
        latest = release['tag_name']
        rows.append({'source': 'DSS', 'current': current, 'latest': latest, 'attention': version(latest) > version(current)})
    except Exception as error:
        errors.append(f'DSS check failed: {type(error).__name__}: {error}')
    try:
        with zipfile.ZipFile(root / 'src/onekit/data/eu-trust-lists.zip') as archive:
            manifest = json.loads(archive.read('manifest.json'))
            sources = [{'path': manifest['lotl'], 'url': LOTL}, *manifest['trusted_lists']]
            def inspect(source):
                path, url = source['path'], source['url']
                try:
                    if archive.getinfo(path).file_size > MAX_BYTES:
                        raise ValueError('Bundled list exceeds the inspection limit')
                    bundled = archive.read(path)
                    due = expiry(bundled)
                    remote = fetcher(url)
                    remote_due = expiry(remote)
                    changed = hashlib.sha256(bundled).digest() != hashlib.sha256(remote).digest()
                    return {'source': path, 'url': url, 'changed': changed,
                            'bundled_expiry': due.isoformat() if due else None,
                            'remote_expiry': remote_due.isoformat() if remote_due else None,
                            'attention': changed or due is None or remote_due is None or min(due, remote_due) <= now + dt.timedelta(days=7)}, None
                except Exception as error:
                    return None, f'{path}: {type(error).__name__}: {error}'
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                for row, error in pool.map(inspect, sources):
                    if row:
                        rows.append(row)
                    if error:
                        errors.append(error)
    except Exception as error:
        errors.append(f'Bundled trust-list inspection failed: {type(error).__name__}: {error}')
    return {'checked_at': now.isoformat(), 'attention': bool(errors) or any(row['attention'] for row in rows),
            'failed': bool(errors), 'rows': rows, 'errors': errors}


def write_report(result, directory):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'signature-updates.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    lines = ['# Signature dependency maintenance', '', f"Checked: {result['checked_at']}", '',
             'Alerts only. Remote XML is NOT authenticated by this monitor and is never installed or used for signature validation.',
             'Changed lists must pass the authenticated updater before integration. DSS updates require a rebuild, matching dependency hashes, license/source review and regression tests.', '',
             '| Source | State | Bundled expiry / version | Remote expiry / version |', '|---|---|---|---|']
    for row in result['rows']:
        current = row.get('current', row.get('bundled_expiry')) or 'unknown'
        latest = row.get('latest', row.get('remote_expiry')) or 'unknown'
        state = 'Review required' if row['attention'] else 'No change or impending expiry detected'
        if row.get('changed'):
            state += ' (XML changed)'
        lines.append(f"| {row['source']} | {state} | {current} | {latest} |")
    if result['errors']:
        lines += ['', '## Failed checks', '', *['- ' + error.replace('\n', ' ') for error in result['errors']]]
    (directory / 'signature-updates.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    result = check()
    write_report(result, Path('.artifacts/signature-maintenance'))
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
            output.write(f"attention={str(result['attention']).lower()}\nfailed={str(result['failed']).lower()}\n")
    print(json.dumps({key: result[key] for key in ('attention', 'failed', 'checked_at')}))
    raise SystemExit(1 if result['failed'] else 0)
