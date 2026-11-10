# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Fetch public, signed EU trust lists; no documents or signer data are sent."""
import argparse
import base64
import datetime
import io
import json
import ssl
import sys
import urllib.parse
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .tools.signature_validation import MAX_EVIDENCE, SCHEMA, authenticated_registry

LOTL_URL = 'https://ec.europa.eu/tools/lotl/eu-lotl.xml'


def build_issuer_index(files, manifest):
    """An availability hint only: validation still authenticates the signed XML."""
    import hashlib

    from asn1crypto import x509
    from lxml import etree
    index = {}
    for item in manifest['trusted_lists']:
        territory = Path(item['path']).stem
        root = etree.fromstring(files[item['path']], parser=etree.XMLParser(resolve_entities=False, no_network=True))
        for element in root.iter():
            if not isinstance(element.tag, str) or etree.QName(element).localname != 'X509Certificate' or not element.text:
                continue
            try:
                cert = x509.Certificate.load(base64.b64decode(element.text))
                names = [cert.subject.dump()]
                try:
                    names.append(cert.subject.hashable.encode('utf-8'))
                except ValueError:
                    pass
            except ValueError:
                continue
            for name in names:
                index.setdefault(hashlib.sha256(name).hexdigest(), set()).add(territory)
    return {key: sorted(value) for key, value in index.items()}


def fetch_public(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ('https', 'http') or parsed.username or parsed.password:
        raise ValueError('Unsupported trusted-list location.')
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OneKit trust-list updater)', 'Accept': '*/*'})
    context = None
    if sys.platform == 'win32':
        try:
            import truststore
        except ImportError:
            pass
        else:
            # Windows builds a verified chain using the OS certificate store,
            # including intermediate retrieval. Never disable TLS verification.
            context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    with urllib.request.urlopen(request, timeout=30, context=context) as response:
        data = response.read(MAX_EVIDENCE + 1)
    if len(data) > MAX_EVIDENCE:
        raise ValueError('Trusted list exceeds the evidence budget.')
    return data


def collect(territories=None):
    from pyhanko.sign.validation.qualified.eutl_parse import LOTL_RULE, latest_known_lotl_tlso_certs, parse_lotl_unsafe

    from .tools.signature_validation import _fresh_signed_list
    now = datetime.datetime.now(datetime.UTC)
    lotl = fetch_public(LOTL_URL)
    verified, _ = _fresh_signed_list(lotl.decode('utf-8-sig'), latest_known_lotl_tlso_certs(), now)
    references = [ref for ref in parse_lotl_unsafe(verified).references if LOTL_RULE not in ref.scheme_rules]
    if territories:
        references = [ref for ref in references if ref.territory in territories]
    files = {'lotl.xml': lotl}
    manifest = {'schema': SCHEMA, 'lotl': 'lotl.xml', 'trusted_lists': [], 'certificates': [], 'crls': [], 'ocsps': []}
    def download(reference):
        try:
            return reference, fetch_public(reference.location_uri)
        except OSError:
            return reference, None
    with ThreadPoolExecutor(max_workers=4) as pool:
        for reference, data in pool.map(download, references):
            if data is None:
                continue  # Omitted territories remain untrusted; never fabricate data.
            try:
                _fresh_signed_list(data.decode('utf-8-sig'), reference.tlso_certs, now)
            except ValueError:
                continue
            path = f'tl/{reference.territory}.xml'
            if path in files:
                raise ValueError('Duplicate trust-list territory.')
            files[path] = data
            manifest['trusted_lists'].append({'url': reference.location_uri, 'path': path})
            if sum(len(value) for value in files.values()) > MAX_EVIDENCE:
                raise ValueError('Trusted lists exceed the evidence budget.')
    _, status = authenticated_registry(files, manifest, now)
    manifest['issuer_index'] = build_issuer_index(files, manifest)
    files['manifest.json'] = json.dumps(manifest, sort_keys=True).encode()
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path, data in sorted(files.items()):
            archive.writestr(path, data)
    return output.getvalue(), status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--territory', action='append', help='ISO territory code; repeat to limit the snapshot.')
    args = parser.parse_args()
    data, status = collect(set(args.territory) if args.territory else None)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print(json.dumps(status, sort_keys=True))


if __name__ == '__main__':
    main()
