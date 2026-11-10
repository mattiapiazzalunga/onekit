"""Exercise strict revocation and shared sync/async contracts with synthetic PKI."""
import asyncio
import datetime
import io
import json
import zipfile
from functools import lru_cache

import pytest
from asn1crypto import tsp
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import ocsp
from cryptography.x509.oid import AuthorityInformationAccessOID, ExtendedKeyUsageOID, NameOID

from onekit import Artifact, execute, execute_async
from onekit.tools import signature_validation as validation

# Register ESS/timestamp OIDs before any test builds CMS's reverse OID cache.
assert tsp.TSTInfo


@lru_cache
def pki():
    now = datetime.datetime.now(datetime.UTC)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    leaf_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Synthetic CA')])
    root = (x509.CertificateBuilder().subject_name(name).issuer_name(name).serial_number(1)
            .public_key(key.public_key()).not_valid_before(now-datetime.timedelta(days=2))
            .not_valid_after(now+datetime.timedelta(days=2))
            .add_extension(x509.BasicConstraints(ca=True, path_length=1), critical=True)
            .add_extension(x509.KeyUsage(False, False, False, False, False, True, True, False, False), critical=True)
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
            .sign(key, hashes.SHA256()))
    leaf_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Synthetic signer')])
    leaf = (x509.CertificateBuilder().subject_name(leaf_name).issuer_name(name).serial_number(2)
            .public_key(leaf_key.public_key()).not_valid_before(now-datetime.timedelta(days=1))
            .not_valid_after(now+datetime.timedelta(days=1))
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .add_extension(x509.KeyUsage(True, True, False, False, False, False, False, False, False), critical=True)
            .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(key.public_key()), critical=False)
            .add_extension(x509.AuthorityInformationAccess([x509.AccessDescription(
                AuthorityInformationAccessOID.OCSP, x509.UniformResourceIdentifier('https://never-contact.invalid/ocsp'))]), critical=False)
            .add_extension(x509.CRLDistributionPoints([x509.DistributionPoint(
                full_name=[x509.UniformResourceIdentifier('https://never-contact.invalid/ca.crl')], relative_name=None,
                reasons=None, crl_issuer=None)]), critical=False)
            .sign(key, hashes.SHA256()))
    content = b'OneKit local validation fixture'
    from asn1crypto import keys
    from asn1crypto import x509 as asn1x509
    from pyhanko.sign.signers import SimpleSigner
    from pyhanko_certvalidator.registry import SimpleCertificateStore
    store = SimpleCertificateStore()
    store.register(asn1x509.Certificate.load(root.public_bytes(serialization.Encoding.DER)))
    signer = SimpleSigner(asn1x509.Certificate.load(leaf.public_bytes(serialization.Encoding.DER)),
                          keys.PrivateKeyInfo.load(leaf_key.private_bytes(serialization.Encoding.DER,
                              serialization.PrivateFormat.PKCS8, serialization.NoEncryption())), store)
    signature = asyncio.run(signer.async_sign_general_data(content, 'sha256', use_cades=True)).dump()
    pki.signer_key = leaf_key
    return key, root, leaf, content, signature


def local_policy(monkeypatch, *, revoked=False, stale=False, use_ocsp=False, empty=False):
    from dataclasses import replace

    from asn1crypto import crl as asn1crl
    from asn1crypto import ocsp as asn1ocsp
    from asn1crypto import x509 as asn1x509
    from pyhanko.sign.validation.policy_decl import LocalKnowledge
    from pyhanko_certvalidator.registry import SimpleTrustManager
    from pyhanko_certvalidator.revinfo.archival import CRLContainer, OCSPContainer
    key, root, leaf, _, _ = pki()
    now = datetime.datetime.now(datetime.UTC)
    spec, _ = validation.validation_spec(None, now)
    manager = SimpleTrustManager.build([asn1x509.Certificate.load(root.public_bytes(serialization.Encoding.DER))])
    if use_ocsp:
        response = (ocsp.OCSPResponseBuilder().add_response(cert=leaf, issuer=root, algorithm=hashes.SHA1(),
                    cert_status=ocsp.OCSPCertStatus.REVOKED if revoked else ocsp.OCSPCertStatus.GOOD,
                    this_update=now-datetime.timedelta(hours=1), next_update=now+datetime.timedelta(hours=1),
                    revocation_time=now-datetime.timedelta(minutes=30) if revoked else None,
                    revocation_reason=x509.ReasonFlags.key_compromise if revoked else None)
                    .responder_id(ocsp.OCSPResponderEncoding.HASH, root).sign(key, hashes.SHA256()))
        knowledge = LocalKnowledge(known_ocsps=OCSPContainer.load_multi(asn1ocsp.OCSPResponse.load(response.public_bytes(serialization.Encoding.DER))))
    else:
        builder = (x509.CertificateRevocationListBuilder().issuer_name(root.subject)
                   .last_update(now-datetime.timedelta(days=2) if stale else now-datetime.timedelta(hours=1))
                   .next_update(now-datetime.timedelta(days=1) if stale else now+datetime.timedelta(hours=1)))
        if revoked:
            builder = builder.add_revoked_certificate(x509.RevokedCertificateBuilder().serial_number(leaf.serial_number)
                                                     .revocation_date(now-datetime.timedelta(minutes=30)).build())
        encoded = builder.sign(key, hashes.SHA256()).public_bytes(serialization.Encoding.DER)
        knowledge = LocalKnowledge(known_crls=[CRLContainer(asn1crl.CertificateList.load(encoded))])
    if empty:
        knowledge = LocalKnowledge()
    spec = replace(spec, cert_validation_policy=replace(spec.cert_validation_policy, trust_manager=manager), local_knowledge=knowledge)
    monkeypatch.setattr(validation, 'validation_spec', lambda evidence, moment, certificate_names=None: (spec, {'status': 'synthetic-test-only'}))


@pytest.mark.parametrize('use_ocsp', [False, True])
@pytest.mark.parametrize('revoked', [False, True])
def test_signed_revocation_evidence_is_enforced(monkeypatch, revoked, use_ocsp):
    local_policy(monkeypatch, revoked=revoked, use_ocsp=use_ocsp)
    _, _, _, content, signature = pki()
    result = execute('signature-verify', [Artifact('test.p7s', signature), Artifact('original.bin', content)])
    report = result.details['validation']
    if revoked:
        assert report['indication'] != 'TOTAL_PASSED'
        assert 'REVOKED' in report['signatures'][0]['subindication']
    else:
        assert report['indication'] == 'TOTAL_PASSED', report
        assert report['signatures'][0]['trusted']


@pytest.mark.parametrize('stale,empty', [(True, False), (False, True)])
def test_missing_or_stale_revocation_is_never_success(monkeypatch, stale, empty):
    local_policy(monkeypatch, stale=stale, empty=empty)
    _, _, _, content, signature = pki()
    report = execute('signature-verify', [Artifact('test.p7s', signature), Artifact('original.bin', content)]).details['validation']
    assert report['indication'] == 'INDETERMINATE'


def test_sync_and_async_share_validation_and_bounds():
    _, _, _, content, signature = pki()
    files = [Artifact('test.p7s', signature), Artifact('original.bin', content)]
    sync = execute('signature-verify', files).details
    asynchronous = asyncio.run(execute_async('signature-verify', files)).details
    sync['validation'].pop('validationTime'); asynchronous['validation'].pop('validationTime')
    assert sync == asynchronous
    assert sync['validation']['indication'] == 'INDETERMINATE'
    assert sync['validation']['dssEquivalence'] == 'not_established'


@pytest.mark.parametrize('ca_signer', [False, True])
def test_pdf_validation_checks_modification_policy_with_the_same_engine(monkeypatch, ca_signer):
    local_policy(monkeypatch)
    from asn1crypto import keys
    from asn1crypto import x509 as asn1x509
    from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
    from pyhanko.sign import signers
    from pyhanko_certvalidator.registry import SimpleCertificateStore
    from pypdf import PdfWriter
    key, root, leaf, _, _ = pki()
    store = SimpleCertificateStore()
    store.register(asn1x509.Certificate.load(root.public_bytes(serialization.Encoding.DER)))
    signer = signers.SimpleSigner(asn1x509.Certificate.load((root if ca_signer else leaf).public_bytes(serialization.Encoding.DER)),
        keys.PrivateKeyInfo.load((key if ca_signer else pki.signer_key).private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8,
                                                  serialization.NoEncryption())), store)
    writer = PdfWriter(); writer.add_blank_page(width=300, height=400)
    original = io.BytesIO(); writer.write(original); original.seek(0)
    signed = signers.sign_pdf(IncrementalPdfFileWriter(original),
        signers.PdfSignatureMetadata(field_name='Signature1'), signer=signer).getvalue()
    report = execute('signature-verify', [Artifact('signed.pdf', signed)]).details
    assert 'reason' not in report['validation'], report['validation']
    assert len(report['validation']['signatures']) == 1
    assert report['validation']['signatures'][0]['modificationPolicy'] is True
    if ca_signer:
        assert report['validation']['indication'] != 'TOTAL_PASSED'
    else:
        assert report['validation']['indication'] == 'TOTAL_PASSED'


def test_multiple_cms_signers_are_all_checked():
    from asn1crypto import cms
    _, _, _, content, signature = pki()
    container = cms.ContentInfo.load(signature)
    valid = container['content']['signer_infos'][0]
    invalid = cms.SignerInfo.load(valid.dump())
    value = invalid['signature'].native
    invalid['signature'] = value[:-1] + bytes([value[-1] ^ 1])
    container['content']['signer_infos'] = [valid, invalid]
    report = execute('signature-verify', [Artifact('signature.p7s', container.dump()), Artifact('original.bin', content)]).details
    assert report['verdict'] == 'mismatch'
    assert report['validation']['indication'] == 'TOTAL_FAILED'
    assert len(report['validation']['signatures']) == 2


def timestamped_inputs(container_format):
    assert tsp.TSTInfo  # Register timestamp and ESS ASN.1 types before CMS use.
    from asn1crypto import keys
    from asn1crypto import x509 as asn1x509
    from pyhanko.sign.signers import SimpleSigner
    from pyhanko.sign.timestamps import DummyTimeStamper
    from pyhanko_certvalidator.registry import SimpleCertificateStore
    key, root, leaf, content, _ = pki()
    now = datetime.datetime.now(datetime.UTC)
    tsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    tsa = (x509.CertificateBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Synthetic TSA')]))
           .issuer_name(root.subject).serial_number(3).public_key(tsa_key.public_key())
           .not_valid_before(now-datetime.timedelta(days=1)).not_valid_after(now+datetime.timedelta(days=1))
           .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
           .add_extension(x509.KeyUsage(True, False, False, False, False, False, False, False, False), critical=True)
           .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.TIME_STAMPING]), critical=True)
           .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(key.public_key()), critical=False)
           .add_extension(x509.CRLDistributionPoints([x509.DistributionPoint(
               full_name=[x509.UniformResourceIdentifier('https://never-contact.invalid/ca.crl')],
               relative_name=None, reasons=None, crl_issuer=None)]), critical=False).sign(key, hashes.SHA256()))
    def asncert(cert):
        return asn1x509.Certificate.load(cert.public_bytes(serialization.Encoding.DER))
    def asnkey(key):
        return keys.PrivateKeyInfo.load(key.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    store = SimpleCertificateStore(); store.register(asncert(root))
    signer = SimpleSigner(asncert(leaf), asnkey(pki.signer_key), store)
    timestamp = DummyTimeStamper(asncert(tsa), asnkey(tsa_key), certs_to_embed=store, fixed_dt=now)
    if container_format == 'cms':
        encoded = asyncio.run(signer.async_sign_general_data(content, 'sha256', use_cades=True, timestamper=timestamp)).dump()
        inputs = [Artifact('timestamped.p7s', encoded), Artifact('original.bin', content)]
    else:
        from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
        from pyhanko.sign import fields, signers
        from pypdf import PdfWriter
        writer = PdfWriter(); writer.add_blank_page(width=300, height=400)
        original = io.BytesIO(); writer.write(original); original.seek(0)
        encoded = signers.sign_pdf(IncrementalPdfFileWriter(original),
            signers.PdfSignatureMetadata(field_name='Signature1', subfilter=fields.SigSeedSubFilter.PADES),
            signer=signer, timestamper=None if container_format == 'pdf-b' else timestamp).getvalue()
        if container_format in ('pdf-lt', 'pdf-lta'):
            from pyhanko.sign.signers.pdf_signer import TimestampDSSContentSettings
            from pyhanko_certvalidator import ValidationContext
            spec, _ = validation.validation_spec(None, now)
            context = ValidationContext(trust_roots=[asncert(root)],
                crls=[value.crl_data for value in spec.local_knowledge.known_crls],
                allow_fetching=False, revocation_mode='require')
            encoded = signers.PdfTimeStamper(timestamp).timestamp_pdf(
                IncrementalPdfFileWriter(io.BytesIO(encoded)), 'sha256',
                validation_context=context,
                dss_settings=TimestampDSSContentSettings(include_vri=False, update_before_ts=True)
                    if container_format == 'pdf-lta' else TimestampDSSContentSettings()).getvalue()
        inputs = [Artifact('timestamped.pdf', encoded)]
    return inputs


@pytest.mark.parametrize('container_format', ['cms', 'pdf', 'pdf-lt', 'pdf-lta'])
def test_rfc3161_timestamp_is_cryptographically_bound_and_validated(monkeypatch, container_format):
    local_policy(monkeypatch)
    report = execute('signature-verify', timestamped_inputs(container_format)).details['validation']
    assert 'reason' not in report, report
    assert report['indication'] == 'TOTAL_PASSED', report
    assert report['signatures'][0]['timestamp'] == 'passed'


def test_valid_timestamp_from_another_signature_cannot_be_reused(monkeypatch):
    from asn1crypto import cms
    from pyhanko.pdf_utils.reader import PdfFileReader
    local_policy(monkeypatch)
    inputs = timestamped_inputs('cms')
    other = PdfFileReader(io.BytesIO(timestamped_inputs('pdf')[0].data))
    signed = cms.ContentInfo.load(inputs[0].data)
    signed['content']['signer_infos'][0]['unsigned_attrs'] = other.embedded_regular_signatures[0].signer_info['unsigned_attrs']
    inputs[0] = Artifact('swapped.p7s', signed.dump())
    report = execute('signature-verify', inputs).details
    assert report['verdict'] == 'cryptographic_match'
    assert report['validation']['indication'] != 'TOTAL_PASSED'
    assert report['validation']['signatures'][0]['timestamp'] != 'passed'


def test_document_timestamp_detects_changed_covered_bytes(monkeypatch):
    local_policy(monkeypatch)
    file = timestamped_inputs('pdf-lta')[0]
    changed = file.data.replace(b'/Producer (pypdf)', b'/Producer (Qypdf)', 1)
    assert changed != file.data
    report = execute('signature-verify', [Artifact(file.name, changed)]).details
    assert report['verdict'] == 'mismatch'
    assert report['validation']['indication'] == 'TOTAL_FAILED'


def test_evidence_never_accepts_roots_from_an_archive():
    _, root, _, _, _ = pki()
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w') as archive:
        archive.writestr('manifest.json', json.dumps({'schema': validation.SCHEMA, 'certificates': ['root.der']}))
        archive.writestr('root.der', root.public_bytes(serialization.Encoding.DER))
    spec, trust = validation.validation_spec(output.getvalue(), datetime.datetime.now(datetime.UTC))
    assert trust['status'] == 'unavailable'
    assert not list(spec.cert_validation_policy.trust_manager.tsp_registry.known_certificate_authorities)


def test_duplicate_archive_entries_are_rejected():
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w') as archive:
        archive.writestr('manifest.json', '{}')
        with pytest.warns(UserWarning):
            archive.writestr('manifest.json', '{}')
    with pytest.raises(ValueError, match='evidence_members'):
        validation.evidence_files(output.getvalue())


def test_real_eu_trust_snapshot_authenticates_selected_lists_and_rejects_tampering():
    evidence = validation.default_evidence()
    files, manifest = validation.evidence_files(evidence)
    moment = datetime.datetime(2026, 10, 29, 2, 0, tzinfo=datetime.UTC)
    registry, status = validation.authenticated_registry(files, manifest, moment, {'IT'})
    assert status['territories'] == ['IT']
    assert len(list(registry.known_certificate_authorities)) > 10
    assert status['skippedServices'] == 0
    assert status['supportedTakeovers'] > 0
    # Alter signed bytes while retaining well-formed XML and the signature.
    changed = dict(files)
    changed['lotl.xml'] = files['lotl.xml'].replace(b'European Commission', b'European CommissioN', 1)
    assert changed['lotl.xml'] != files['lotl.xml']
    with pytest.raises((ValueError, InvalidSignature)):
        validation.authenticated_registry(changed, manifest, moment, {'IT'})


def test_expired_trust_list_evidence_cannot_be_reused_from_cache():
    evidence = validation.default_evidence()
    files, manifest = validation.evidence_files(evidence)
    start = datetime.datetime(2026, 10, 29, 2, 0, tzinfo=datetime.UTC)
    _, status = validation.cached_registry(evidence, files, manifest, start, {'IT'})
    expired = datetime.datetime.fromisoformat(status['expires']) + datetime.timedelta(seconds=1)
    # Reports are caller-owned: changing their metadata must not extend a
    # registry's lifetime in the process-local cache.
    status['expires'] = '2099-01-01T00:00:00+00:00'
    with pytest.raises((ValueError, InvalidSignature)):
        validation.cached_registry(evidence, files, manifest, expired, {'IT'})


def test_indexed_evidence_does_not_decompress_unrelated_trust_lists():
    evidence = validation.default_evidence()
    files, manifest = validation.evidence_files(evidence, set())
    assert manifest['issuer_index']
    assert 'lotl.xml' in files
    assert not any(path.startswith('tl/') for path in files)
    assert sum(map(len, files.values())) < 2 * 1024 * 1024


def test_async_pipeline_preserves_multiple_outputs_and_resource_limits():
    from onekit import OneKitError, pipeline, pipeline_async
    from onekit.execution import ExecutionContext
    files = [Artifact('first.md', b'# First'), Artifact('second.md', b'# Second')]
    steps = [{'tool': 'md-to-html'}, {'tool': 'html-to-md'}]
    expected = pipeline(steps, files)
    actual = asyncio.run(pipeline_async(steps, files))
    assert [(file.name, file.data) for file in actual.files] == [(file.name, file.data) for file in expected.files]
    assert actual.details == expected.details
    assert actual.warnings == expected.warnings
    with pytest.raises(OneKitError):
        asyncio.run(pipeline_async(steps, files, context=ExecutionContext(max_batch_bytes=8)))


@pytest.mark.parametrize('with_evidence', [False, True])
def test_detached_signature_can_have_a_zip_original(with_evidence):
    from cryptography.hazmat.primitives.serialization import pkcs7
    _, _, leaf, _, _ = pki()
    original = io.BytesIO()
    with zipfile.ZipFile(original, 'w') as archive:
        archive.writestr('manifest.json', '{"application":"example"}')
        archive.writestr('document.txt', 'original')
    content = original.getvalue()
    signature = pkcs7.PKCS7SignatureBuilder().set_data(content).add_signer(
        leaf, pki.signer_key, hashes.SHA256()).sign(serialization.Encoding.DER, [pkcs7.PKCS7Options.DetachedSignature])
    files = [Artifact('signature.p7s', signature), Artifact('original.zip', content)]
    if with_evidence:
        evidence = io.BytesIO()
        with zipfile.ZipFile(evidence, 'w') as archive:
            archive.writestr('manifest.json', json.dumps({'schema': validation.SCHEMA}))
        files.append(Artifact('evidence.zip', evidence.getvalue()))
    report = execute('signature-verify', files).details
    assert report['verdict'] == 'cryptographic_match'
