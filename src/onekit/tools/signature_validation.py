# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Local AdES validation shared by synchronous and asynchronous processing hosts.

Trust is established only through authenticated EU trusted lists. Certificates
inside the document or an evidence archive never become trust anchors by fiat.
No network I/O is performed by validation. Missing evidence is indeterminate.
"""
import copy
import datetime
import hashlib
import io
import json
import zipfile
from collections import OrderedDict
from pathlib import Path

from ..models import OneKitError
from .signature_algorithms import content_digest

SCHEMA = 'onekit-signature-evidence-v1'
MAX_EVIDENCE = 32 * 1024 * 1024
MAX_MEMBERS = 256
_TRUST_CACHE = OrderedDict()
ENGINE_VERSIONS = {'pyhanko': '0.38.0', 'pyhanko-certvalidator': '0.33.0', 'cryptography': '50.0.2',
                   'signxml': '5.2.0', 'xsdata': '26.10'}


def evidence_files(data, certificate_names=None):
    """Read a bounded archive in memory; never extract paths to the filesystem."""
    if len(data) > MAX_EVIDENCE:
        raise ValueError('evidence_size')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        if len(entries) > MAX_MEMBERS or sum(item.file_size for item in entries) > MAX_EVIDENCE:
            raise ValueError('evidence_size')
        names = [item.filename for item in entries]
        if len(set(names)) != len(names) or any(item.flag_bits & 1 for item in entries):
            raise ValueError('evidence_members')
        manifest = json.loads(archive.read('manifest.json'))
        if not isinstance(manifest, dict) or manifest.get('schema') != SCHEMA:
            raise ValueError('evidence_schema')
        for key in ('trusted_lists', 'certificates', 'crls', 'ocsps'):
            values = manifest.get(key, [])
            if not isinstance(values, list) or len(values) > 100:
                raise ValueError('evidence_count')
        for item in manifest.get('trusted_lists', []):
            if not isinstance(item, dict) or not isinstance(item.get('url'), str) or not isinstance(item.get('path'), str):
                raise TypeError('evidence_members')
        if any(not isinstance(path, str) for key in ('certificates', 'crls', 'ocsps') for path in manifest.get(key, [])):
            raise TypeError('evidence_members')
        index = manifest.get('issuer_index', {})
        if not isinstance(index, dict) or len(index) > 20000 or any(
                not isinstance(value, list) or len(value) > 32 or any(not isinstance(territory, str) for territory in value)
                for value in index.values()):
            raise ValueError('evidence_index')
        selected = None
        if 'issuer_index' in manifest and certificate_names is not None:
            selected = {territory for name in certificate_names for territory in index.get(name, [])}
        needed = {'manifest.json'}
        if manifest.get('lotl'):
            needed.add(manifest['lotl'])
        for item in manifest.get('trusted_lists', []):
            if selected is None or item.get('territory', Path(item['path']).stem) in selected:
                needed.add(item['path'])
        needed.update(path for key in ('certificates', 'crls', 'ocsps') for path in manifest.get(key, []))
        files = {name: archive.read(name) for name in needed}
    return files, manifest


def _fresh_signed_list(xml, certificates, moment):
    # Pinning pyHanko is required: these lower-level entry points let us enforce
    # expiry on exactly the XML subtree authenticated by its wrapping-safe verifier.
    from pyhanko.sign.validation.qualified.eutl_parse import (
        _raw_tl_parse,
        _validate_and_extract_tl_data_multiple_certs,
    )
    verified = _validate_and_extract_tl_data_multiple_certs(xml, certificates, validation_time=moment)
    parsed = _raw_tl_parse(verified)
    info = parsed.scheme_information
    if info.list_issue_date_time is None or info.next_update is None or info.next_update.date_time is None:
        raise ValueError('trust_list_dates_missing')
    issued = info.list_issue_date_time.to_datetime()
    expiry = info.next_update.date_time.to_datetime()
    if issued.tzinfo is None or expiry.tzinfo is None or not issued <= moment < expiry:
        raise ValueError('trust_list_expired_or_future')
    return verified, expiry


def authenticated_registry(files, manifest, moment, selected_territories=None):
    from pyhanko.sign.validation.qualified.eutl_parse import (
        LOTL_RULE,
        latest_known_lotl_tlso_certs,
        parse_lotl_unsafe,
    )
    from pyhanko.sign.validation.qualified.tsp import TSPRegistry
    xml, expiry = _fresh_signed_list(files[manifest['lotl']].decode('utf-8-sig'), latest_known_lotl_tlso_certs(), moment)
    lotl = parse_lotl_unsafe(xml)
    if lotl.errors:
        raise ValueError('lotl_parse_errors')
    allowed = {ref.location_uri: ref for ref in lotl.references if LOTL_RULE not in ref.scheme_rules}
    registry = TSPRegistry()
    territories = []
    skipped = 0
    taken_over = 0
    for item in manifest.get('trusted_lists', []):
        reference = allowed[item['url']]
        if selected_territories is not None and reference.territory not in selected_territories:
            continue
        signed, end = _fresh_signed_list(files[item['path']].decode('utf-8-sig'), reference.tlso_certs, moment)
        from .signature_trust import add_authenticated_services
        errors, supported_takeovers = add_authenticated_services(signed, registry)
        taken_over += supported_takeovers
        # Upstream rejects individual services with unknown critical extensions.
        # Keep those exclusions visible; never reinterpret their qualifiers.
        skipped += len(errors)
        expiry = min(expiry, end)
        territories.append(reference.territory)
    supplied = {allowed[item['url']].territory for item in manifest.get('trusted_lists', [])}
    missing = sorted({ref.territory for ref in allowed.values()} - supplied)
    return registry, {'status': 'authenticated_partial' if skipped or missing else 'authenticated',
                      'territories': sorted(set(territories)), 'missingTerritories': missing,
                      'expires': expiry.isoformat(), 'skippedServices': skipped,
                      'supportedTakeovers': taken_over}


def cached_registry(evidence, files, manifest, moment, territories=None):
    key = hashlib.sha256(evidence).digest(), None if territories is None else tuple(sorted(territories))
    if key in _TRUST_CACHE:
        registry, status, verified_at = _TRUST_CACHE[key]
        if not verified_at <= moment < datetime.datetime.fromisoformat(status['expires']):
            del _TRUST_CACHE[key]
        else:
            _TRUST_CACHE.move_to_end(key)
            return registry, copy.deepcopy(status)
    registry, status = authenticated_registry(files, manifest, moment, territories)
    _TRUST_CACHE[key] = registry, copy.deepcopy(status), moment
    while len(_TRUST_CACHE) > 2:
        _TRUST_CACHE.popitem(last=False)
    return registry, status


def validation_spec(evidence, moment, certificate_names=None):
    from asn1crypto import crl, ocsp, x509
    from pyhanko.sign.validation.policy_decl import (
        CertificateFetchingRule,
        LocalKnowledge,
        RevinfoOnlineFetchingRule,
        RevocationInfoGatheringSpec,
        SignatureValidationSpec,
    )
    from pyhanko.sign.validation.qualified.tsp import TSPRegistry, TSPTrustManager
    from pyhanko.sign.validation.settings import KeyUsageConstraints
    from pyhanko_certvalidator.context import CertValidationPolicySpec
    from pyhanko_certvalidator.policy_decl import REQUIRE_REVINFO, CertRevTrustPolicy
    from pyhanko_certvalidator.revinfo.archival import CRLContainer, OCSPContainer

    from .signature_policy import DSSAlgorithmPolicy
    files, manifest = ({}, {}) if evidence is None else evidence_files(evidence, certificate_names)
    registry = TSPRegistry()
    trust = {'status': 'unavailable', 'territories': []}
    if manifest.get('lotl'):
        selection = None
        index = manifest.get('issuer_index')
        if isinstance(index, dict) and certificate_names is not None:
            selection = {territory for name in certificate_names for territory in index.get(name, [])}
        registry, trust = cached_registry(evidence, files, manifest, moment, selection)
    knowledge = LocalKnowledge(
        known_certs=[x509.Certificate.load(files[path], strict=True) for path in manifest.get('certificates', [])],
        known_crls=[CRLContainer(crl.CertificateList.load(files[path], strict=True)) for path in manifest.get('crls', [])],
        known_ocsps=[item for path in manifest.get('ocsps', []) for item in OCSPContainer.load_multi(ocsp.OCSPResponse.load(files[path], strict=True))],
    )
    spec = SignatureValidationSpec(
        cert_validation_policy=CertValidationPolicySpec(TSPTrustManager(registry), CertRevTrustPolicy(REQUIRE_REVINFO),
                                                       algorithm_usage_policy=DSSAlgorithmPolicy()),
        revinfo_gathering_policy=RevocationInfoGatheringSpec(
            online_fetching_rule=RevinfoOnlineFetchingRule.LOCAL_ONLY,
            certificate_fetching_rule=CertificateFetchingRule.NEVER_FETCH,
        ),
        local_knowledge=knowledge,
        key_usage_settings=KeyUsageConstraints(key_usage=('digital_signature', 'non_repudiation')),
    )
    return spec, trust


def certificate_name_keys(certificates):
    keys = set()
    for cert in certificates:
        for name in (cert.subject, cert.issuer):
            keys.add(hashlib.sha256(name.dump()).hexdigest())
            try:
                keys.add(hashlib.sha256(name.hashable.encode('utf-8')).hexdigest())
            except ValueError:
                pass  # Invalid legacy DN encodings still receive a DER lookup.
    return keys


def cms_certificates(signed, depth=0):
    if depth > 4 or len(signed['certificates']) > 100 or len(signed['signer_infos']) > 20:
        raise ValueError('signature_evidence_depth')
    certificates = [choice.chosen for choice in signed['certificates'] if choice.name == 'certificate']
    for signer in signed['signer_infos']:
        if len(signer['signed_attrs']) > 64 or len(signer['unsigned_attrs']) > 32:
            raise ValueError('signature_attribute_count')
        for attr in signer['unsigned_attrs']:
            if attr['type'].native == 'signature_time_stamp_token':
                if len(attr['values']) > 4:
                    raise ValueError('signature_timestamp_count')
                for value in attr['values']:
                    certificates.extend(cms_certificates(value['content'], depth + 1))
    if len(certificates) > 200:
        raise ValueError('signature_evidence_count')
    return certificates


def _result_row(outcome, registry, field=None):
    indication = outcome.ades_subindic
    status = outcome.api_status
    row = {'indication': indication.status.name, 'subindication': indication.name}
    if field is not None:
        row['field'] = field
    if status is not None:
        row.update(integrity=bool(status.intact), cryptography=bool(status.valid), trusted=bool(status.trusted))
        timestamp = getattr(status, 'timestamp_validity', None)
        row['timestamp'] = ('passed' if timestamp.intact and timestamp.valid and timestamp.trusted else 'indeterminate') if timestamp else 'absent'
        row['revoked'] = bool(status.revoked)
        from pyhanko.sign.validation.settings import KeyUsageConstraints
        from pyhanko_certvalidator.errors import InvalidCertificateError
        try:
            KeyUsageConstraints(key_usage=('digital_signature', 'non_repudiation')).validate(status.signing_cert)
        except InvalidCertificateError:
            row['signerKeyUsage'] = 'not_permitted'
            if row['indication'] == 'PASSED':
                row.update(indication='INDETERMINATE', subindication='SIG_CONSTRAINTS_FAILURE')
        if hasattr(status, 'docmdp_ok'):
            row['modificationPolicy'] = status.docmdp_ok
            if status.docmdp_ok is False:
                row.update(indication='FAILED', subindication='DOCUMENT_MODIFIED')
            elif status.docmdp_ok is None and row['indication'] == 'PASSED':
                row.update(indication='INDETERMINATE', subindication='MODIFICATIONS_NOT_DETERMINED')
        path = status.validation_path
        if path is not None and status.trusted:
            row['path'] = [hashlib.sha256(cert.dump()).hexdigest() for cert in path]
            # A successful trusted path does not by itself establish QES/QSeal.
            from pyhanko.sign.validation.qualified.assess import QualificationAssessor
            if registry is not None:
                qualified = QualificationAssessor(registry).check_entity_cert_qualified(path, status.validation_time)
                row['qualification'] = {'qualifiedCertificate': qualified.status.qualified,
                                        'type': getattr(qualified.status.qc_type, 'name', None),
                                        'keySecurity': qualified.status.qc_key_security.name}
                row['serviceTakeovers'] = [copy.deepcopy(item) for item in getattr(registry, '_onekit_takeovers', [])
                                          if set(item['certificateSha256']).intersection(row['path'])]
    return row


async def validate(files, evidence=None):
    """Validate using pyHanko's AdES engine, without hidden network fallbacks."""
    from importlib.metadata import version
    if any(version(name) != pin for name, pin in ENGINE_VERSIONS.items()):
        raise OneKitError('Signature validation requires the pinned verification dependencies. Reinstall the verification extra.')
    from asn1crypto import cms, pem
    from pyhanko.pdf_utils.reader import PdfFileReader
    from pyhanko.sign.validation import ades
    from pyhanko.sign.validation.policy_decl import PdfSignatureValidationSpec
    from pyhanko_certvalidator.ltv.types import ValidationTimingInfo
    moment = datetime.datetime.now(datetime.UTC)
    timing = ValidationTimingInfo(validation_time=moment, best_signature_time=moment, point_in_time_validation=False)
    rows = []
    containers = [file for file in files if file.kind in ('p7m', 'p7s', 'cms', 'der')]
    if containers:
        encoded = containers[0].data
        if pem.detect(encoded):
            _, _, encoded = pem.unarmor(encoded)
        signed = cms.ContentInfo.load(encoded)['content']
        spec, trust = validation_spec(evidence, moment, certificate_name_keys(cms_certificates(signed)))
        original = next((file for file in files if file is not containers[0]), None)
        content = original.data if original else signed['encap_content_info']['content'].native
        if content is None:
            raise OneKitError('Provide the original file together with this detached signature.')
        # The AdES API handles one signer at a time. Never silently ignore extras.
        for signer in signed['signer_infos']:
            individual = cms.SignedData.load(signed.untag().dump())
            individual['signer_infos'] = [signer]
            digest = (content_digest(signer['digest_algorithm']['algorithm'].native, content)
                      if signed['encap_content_info']['content'].native is None else None)
            has_timestamp = any(attr['type'].native == 'signature_time_stamp_token' for attr in signer['unsigned_attrs'])
            engine = ades.ades_with_time_validation if has_timestamp else ades.ades_basic_validation
            outcome = await engine(individual, spec, timing_info=timing, raw_digest=digest)
            rows.append(_result_row(outcome, getattr(spec.cert_validation_policy.trust_manager, 'tsp_registry', None)))
    else:
        reader = PdfFileReader(io.BytesIO(files[0].data), strict=True)
        if len(reader.embedded_signatures) > 20:
            raise ValueError('signature_count')
        certificates = [cert for signature in reader.embedded_signatures for cert in cms_certificates(signature.signed_data)]
        from pyhanko.sign.validation.dss import DocumentSecurityStore, NoDSSFoundError
        store = None
        try:
            store = DocumentSecurityStore.read_dss(reader)
            certificates.extend(store.load_certs())
        except NoDSSFoundError:
            pass
        spec, trust = validation_spec(evidence, moment, certificate_name_keys(certificates))
        if store is not None:
            from dataclasses import replace

            # DSS entries are PDF stream references, not decoded ASN.1 objects.
            # Use the pinned engine's decoder, including its decode-purpose limits.
            embedded_knowledge = ades._dss_to_local_knowledge(reader)
            spec = replace(spec, local_knowledge=replace(spec.local_knowledge,
                known_certs=spec.local_knowledge.known_certs + embedded_knowledge.known_certs,
                known_crls=spec.local_knowledge.known_crls + embedded_knowledge.known_crls,
                known_ocsps=spec.local_knowledge.known_ocsps + embedded_knowledge.known_ocsps))
        for signature in reader.embedded_regular_signatures:
            if reader.embedded_timestamp_signatures:
                outcome = await ades.ades_lta_validation(signature, PdfSignatureValidationSpec(spec), timing_info=timing)
            else:
                from pyhanko.sign.diff_analysis import DEFAULT_DIFF_POLICY
                signature.compute_integrity_info(diff_policy=DEFAULT_DIFF_POLICY)
                has_timestamp = any(attr['type'].native == 'signature_time_stamp_token' for attr in signature.signer_info['unsigned_attrs'])
                engine = ades.ades_with_time_validation if has_timestamp else ades.ades_basic_validation
                outcome = await engine(signature.signed_data, spec, timing_info=timing,
                    raw_digest=signature.compute_digest())
            row = _result_row(outcome, getattr(spec.cert_validation_policy.trust_manager, 'tsp_registry', None), signature.field_name)
            integrity = signature.summarise_integrity_info()
            row['modificationPolicy'] = integrity['docmdp_ok']
            if integrity['docmdp_ok'] is False:
                row.update(indication='FAILED', subindication='DOCUMENT_MODIFIED')
            elif integrity['docmdp_ok'] is None and row['indication'] == 'PASSED':
                row.update(indication='INDETERMINATE', subindication='MODIFICATIONS_NOT_DETERMINED')
            rows.append(row)
        for signature in reader.embedded_timestamp_signatures:
            outcome = await ades.ades_timestamp_validation(signature.signed_data, spec,
                expected_tst_imprint=signature.compute_digest, timing_info=timing)
            row = _result_row(outcome, None, signature.field_name)
            rows.append(row)
    indication = 'TOTAL_FAILED' if any(row['indication'] == 'FAILED' for row in rows) else (
        'TOTAL_PASSED' if rows and all(row['indication'] == 'PASSED' for row in rows) else 'INDETERMINATE')
    return {'engine': 'pyhanko', 'engineVersion': '0.38.0', 'policy': 'dss-6.5.1-local-evidence-v2',
            'indication': indication, 'signatures': rows, 'trustLists': trust,
            'network': 'disabled', 'dssEquivalence': 'not_established', 'validationTime': moment.isoformat()}


def default_evidence():
    path = Path(__file__).resolve().parents[1] / 'data' / 'eu-trust-lists.zip'
    return path.read_bytes() if path.is_file() else None
