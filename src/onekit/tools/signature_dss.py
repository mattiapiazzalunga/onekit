# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import asyncio
import base64
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from xml.etree import ElementTree

from ..models import Artifact, OneKitError, Result

_runtime = None
_SIMPLE = 'http://dss.esig.europa.eu/validation/simple-report'
_DIAGNOSTIC = 'http://dss.esig.europa.eu/validation/diagnostic'
_REPORTS = ('simple.xml', 'detailed.xml', 'diagnostic.xml', 'etsi.xml')
_MAX_REPORT = 64 * 1024 * 1024
RUNTIME_PACKAGES = ('pypdf', 'asn1crypto', 'pycryptodome', 'cryptography')


def install_runtime(callback):
    global _runtime
    if callback is not None and not callable(callback):
        raise TypeError('dss_runtime_callback')
    _runtime = callback


def configured_runtime():
    if _runtime is not None:
        return _runtime
    if sys.platform != 'emscripten' and os.environ.get('ONEKIT_DSS_MODEL'):
        return native_runtime
    return None


async def native_runtime(request):
    if os.environ.get('ONEKIT_ALLOW_COPYLEFT') == '0':
        raise OneKitError('A required engine is disabled by ONEKIT_ALLOW_COPYLEFT=0.')
    executable = shutil.which('node')
    if executable is None:
        raise OneKitError('DSS validation requires Node.js 24 or later.')
    script = Path(__file__).resolve().parents[1] / 'data/signatures/node_worker.mjs'
    with tempfile.TemporaryDirectory(prefix='onekit-dss-') as temporary:
        directory = Path(temporary)
        metadata = {}
        for key in ('document', 'detached'):
            if request.get(key) is not None:
                item = request[key]
                path = directory / (key + '.bin')
                path.write_bytes(item['data'])
                metadata[key] = {'name': item.get('name', path.name), 'path': str(path)}
        for key in ('certificates', 'crls', 'ocsps'):
            metadata[key] = []
            for index, data in enumerate(request.get(key, [])):
                path = directory / f'{key}-{index}.bin'
                path.write_bytes(data)
                metadata[key].append(str(path))
        if request.get('trustedLists') is not None:
            lists = request['trustedLists']
            path = directory / 'lotl.xml';path.write_bytes(lists['lotl'])
            metadata['trustedLists'] = {'lotl': str(path), 'lists': []}
            for index, item in enumerate(lists['lists']):
                path = directory / f'tl-{index}.xml';path.write_bytes(item['data'])
                metadata['trustedLists']['lists'].append({'url': item['url'], 'path': str(path)})
        process = await asyncio.create_subprocess_exec(executable, str(script), os.environ['ONEKIT_DSS_MODEL'],
            str(directory), stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(json.dumps(metadata).encode('utf-8')),
                timeout=1830 if request.get('trustedLists') else 330)
        except BaseException:
            process.kill()
            await process.wait()
            raise
        if len(stdout) > 16384:
            raise OneKitError('The local DSS signature model is unavailable or failed its integrity check.')
        result = json.loads(stdout)
        if os.environ.get('ONEKIT_DSS_DEBUG') == '1' and stderr:
            sys.stderr.write(stderr.decode('utf-8', errors='replace'))
        if result.get('reason') in ('validation_failed', 'validation_timeout', 'engine_failed'):
            raise RuntimeError('dss_validation_failed')
        if process.returncode:
            raise OneKitError('The local DSS signature model is unavailable or failed its integrity check.')
        if result.get('status') != 'done':
            raise ValueError('dss_worker_result')
        reports = {}
        for name in _REPORTS:
            path = directory / ('output-' + name)
            if path.stat().st_size > _MAX_REPORT:
                raise ValueError('dss_report_size')
            reports[name] = path.read_bytes()
        return reports


def _xml(data, root, namespace):
    if not isinstance(data, bytes) or len(data) > _MAX_REPORT:
        raise ValueError('dss_report_size')
    text = data.decode('utf-8-sig')
    if '<!DOCTYPE' in text or '<!ENTITY' in text:
        raise ValueError('dss_report_doctype')
    tree = ElementTree.fromstring(text)
    if tree.tag != '{' + namespace + '}' + root:
        raise ValueError('dss_report_schema')
    return tree


def parse_reports(reports, pdf_size=None):
    if set(reports) != set(_REPORTS) or sum(map(len, reports.values())) > 2 * _MAX_REPORT:
        raise ValueError('dss_reports')
    simple = _xml(reports['simple.xml'], 'SimpleReport', _SIMPLE)
    diagnostic = _xml(reports['diagnostic.xml'], 'DiagnosticData', _DIAGNOSTIC)
    _xml(reports['detailed.xml'], 'DetailedReport', 'http://dss.esig.europa.eu/validation/detailed-report')
    _xml(reports['etsi.xml'], 'ValidationReport', 'http://uri.etsi.org/19102/v1.4.1#')
    namespace = {'s': _SIMPLE, 'd': _DIAGNOSTIC}
    diagnostic_rows = {node.get('Id'): node for node in diagnostic.findall('d:Signatures/d:Signature', namespace)}
    diagnostic_rows.update({node.get('Id'): node for node in diagnostic.findall('d:UsedTimestamps/d:Timestamp', namespace)})
    rows, timestamps, cryptographic = [], [], []

    def text(node, path):
        return node.findtext(path, namespaces=namespace)

    def boolean(node, path):
        value = text(node, path)
        if value is None:
            return None
        if value not in ('true', 'false'):
            raise ValueError('dss_report_boolean')
        return value == 'true'

    for token in list(simple.findall('s:Signature', namespace)) + list(simple.findall('s:Timestamp', namespace)):
        identity = token.get('Id')
        indication = text(token, 's:Indication')
        normalized = {'TOTAL_PASSED': 'PASSED', 'TOTAL_FAILED': 'FAILED', 'INDETERMINATE': 'INDETERMINATE'}
        if indication not in normalized or not identity:
            raise ValueError('dss_report_indication')
        is_timestamp = token.tag == '{' + _SIMPLE + '}Timestamp'
        row = {'id': identity, 'indication': normalized[indication], 'dssIndication': indication,
               'subindication': text(token, 's:SubIndication'), 'profile': token.get('SignatureFormat'),
               'bestSignatureTime': text(token, 's:BestSignatureTime')}
        level = text(token, 's:TimestampLevel' if is_timestamp else 's:SignatureLevel')
        row['qualification'] = {'dssLevel': level}
        row['trusted'] = True if indication == 'TOTAL_PASSED' else None
        nested_timestamps = token.findall('s:Timestamps/s:Timestamp', namespace)
        row['timestamp'] = ('passed' if all(text(item, 's:Indication') == 'TOTAL_PASSED' for item in nested_timestamps)
                            else 'indeterminate') if nested_timestamps else 'absent'
        row['revoked'] = True if row['subindication'] in ('REVOKED', 'REVOKED_NO_POE', 'REVOKED_CA_NO_POE') else None
        source = diagnostic_rows.get(identity)
        raw = {'id': identity, 'status': 'not_checked'}
        if source is not None:
            intact = boolean(source, 'd:BasicSignature/d:SignatureIntact')
            valid = boolean(source, 'd:BasicSignature/d:SignatureValid')
            matchers = source.findall('d:DigestMatchers/d:DigestMatcher', namespace)
            found = [boolean(item, 'd:DataFound') for item in matchers]
            matched = [boolean(item, 'd:DataIntact') for item in matchers]
            integrity = False if False in [intact, *matched] else (
                True if all(value is True for value in [intact, *matched]) else None)
            row.update(integrity=integrity, cryptography=valid)
            if source.find('d:SigningCertificate', namespace) is not None:
                if intact is False or valid is False or False in matched:
                    raw['status'] = 'invalid'
                elif intact is True and valid is True and all(value is True for value in found + matched):
                    raw['status'] = 'match'
            field = source.find('d:PDFRevision/d:SignatureField', namespace)
            if field is not None:
                raw['field'] = row['field'] = field.get('name')
            bounds = source.find('d:PDFRevision/d:PDFSignatureDictionary/d:SignatureByteRange', namespace)
            if bounds is not None and pdf_size is not None:
                numbers = [int(number) for number in (bounds.text or '').split()]
                if len(numbers) == 4:
                    end = numbers[2] + numbers[3]
                    raw.update(coversCurrentFile=end == pdf_size, signedRevisionBytes=end,
                               laterChanges='none' if end == pdf_size else 'not_checked')
                if bounds.get('valid') == 'false':
                    raw['status'] = 'invalid'
        cryptographic.append(raw)
        (timestamps if is_timestamp else rows).append(row)
    if len(rows) + len(timestamps) > 20:
        raise ValueError('dss_signature_count')
    if len(rows) != int(text(simple, 's:SignaturesCount') or '0'):
        raise ValueError('dss_signature_count')
    primary = rows or timestamps
    indication = 'TOTAL_FAILED' if any(row['indication'] == 'FAILED' for row in primary) else (
        'TOTAL_PASSED' if primary and all(row['indication'] == 'PASSED' for row in primary) else 'INDETERMINATE')
    validation = {'engine': 'DSS', 'engineVersion': '6.5.1', 'policy': 'dss-6.5.1-default-local-evidence',
                  'network': 'disabled', 'dssEquivalence': 'same_engine', 'indication': indication,
                  'validationTime': simple.get('ValidationTime'), 'signatures': rows, 'timestamps': timestamps}
    verdict = 'unsigned' if not cryptographic else 'mismatch' if any(row['status'] == 'invalid' for row in cryptographic) else (
        'cryptographic_match' if all(row['status'] == 'match' for row in cryptographic) else 'not_checked')
    if verdict == 'cryptographic_match' and pdf_size is not None and not any(row.get('coversCurrentFile') for row in cryptographic):
        verdict = 'partial_coverage'
    return {'verdict': verdict, 'signatures': cryptographic, 'certificateTrust': 'not_checked',
            'revocation': 'not_checked', 'trustedTimestamp': 'not_checked', 'validation': validation}


async def run_original(documents, evidence, runtime):
    from .signature_validation import evidence_files
    from .signatures import LIMITATION

    containers = [file for file in documents if file.kind in ('p7m', 'p7s', 'cms', 'der')]
    document = containers[0] if containers else documents[0]
    detached = next((file for file in documents if file is not document), None)
    request = {'document': {'name': document.name, 'data': document.data}}
    if detached is not None:
        request['detached'] = {'name': detached.name, 'data': detached.data}
    if evidence is not None:
        files, manifest = evidence_files(evidence)
        for key in ('certificates', 'crls', 'ocsps'):
            request[key] = [files[name] for name in manifest.get(key, [])]
        request['trustedLists'] = {'lotl': files[manifest['lotl']], 'lists': [
            {'url': item['url'], 'data': files[item['path']]} for item in manifest.get('trusted_lists', [])]}
    try:
        reports = await runtime(request)
        if isinstance(reports, str):
            payload = json.loads(reports)
            if payload.get('schema') != 'onekit-dss-reports-v1':
                raise ValueError('dss_reports_schema')
            if payload.get('error'):
                raise RuntimeError('dss_validation_failed')
            reports = {name: base64.b64decode(data, validate=True) for name, data in payload['reports'].items()}
        reports = {name: bytes(data) for name, data in reports.items()}
        details = parse_reports(reports, len(document.data) if document.kind == 'pdf' else None)
    except RuntimeError:
        from .signatures import cryptographic_report

        result = cryptographic_report('signature-verify', documents, {})
        result.details['validation'] = {'engine': 'DSS', 'engineVersion': '6.5.1', 'network': 'disabled',
            'indication': 'INDETERMINATE', 'dssEquivalence': 'not_established', 'reason': 'dss_validation_failed'}
        result.files[0] = Artifact('signature-report.json', json.dumps(result.details, ensure_ascii=False, indent=2).encode())
        return result
    details['limitations'] = LIMITATION
    details['validation']['reportSha256'] = {name: hashlib.sha256(data).hexdigest() for name, data in reports.items()}
    exported = {**details, 'dssReports': {name: data.decode('utf-8') for name, data in reports.items()}}
    artifacts = [Artifact('signature-report.json', json.dumps(exported, ensure_ascii=False, indent=2).encode())]
    return Result(artifacts, [LIMITATION], details)
