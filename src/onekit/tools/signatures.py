# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Offline signature cryptography; never infer certificate trust or revocation."""
import asyncio
import datetime
import hashlib
import hmac
import io
import json
import re
import zipfile

from ..models import Artifact, OneKitError, Result
from .signature_algorithms import content_digest

LIMITATION = 'Cryptographic integrity and AdES validation are separate results. Validation uses local evidence and authenticated EU trust lists. Missing evidence is indeterminate. Equivalence with DSS is not certified.'


def verify_value(certificate, signer, data, content_type='data'):
    from Crypto.Hash import SHA1, SHA3_224, SHA3_256, SHA3_384, SHA3_512, SHA224, SHA256, SHA384, SHA512
    from Crypto.PublicKey import DSA, ECC, RSA
    from Crypto.Signature import DSS, eddsa, pkcs1_15, pss
    from cryptography.exceptions import InvalidSignature
    hashes = {'sha1':SHA1,'sha224':SHA224,'sha256':SHA256,'sha384':SHA384,'sha512':SHA512,
              'sha3_224':SHA3_224,'sha3_256':SHA3_256,'sha3_384':SHA3_384,'sha3_512':SHA3_512}
    digest_name = signer['digest_algorithm']['algorithm'].native
    if digest_name not in hashes and digest_name not in ('shake256', 'shake256_len'):
        return {'status':'not_checked','reason':'Unsupported digest algorithm.'}
    if digest_name == 'shake256_len' and signer['digest_algorithm']['parameters'].native != 512:
        return {'status':'not_checked','reason':'Unsupported digest algorithm.'}
    attrs = signer['signed_attrs']
    message = data
    if attrs.native is not None:
        values = {}
        for attr in attrs:
            name = attr['type'].native
            if name in values or name in ('message_digest','content_type') and len(attr['values'])!=1:
                return {'status':'invalid','reason':'Duplicate or malformed signed attributes.'}
            values[name] = attr['values']
        if 'message_digest' not in values or 'content_type' not in values or values['content_type'][0].native!=content_type:
            return {'status':'not_checked','reason':'Required CMS signed attributes are missing or unsupported.'}
        if not hmac.compare_digest(values['message_digest'][0].native,content_digest(digest_name,data)):
            return {'status':'invalid','reason':'The signed content digest does not match.'}
        message = attrs.untag().dump()
    signature = signer['signature'].native
    algorithm = signer['signature_algorithm']['algorithm'].native
    digest = hashes[digest_name].new(message) if digest_name in hashes else None
    key_bytes = certificate.public_key.dump()
    try:
        if algorithm == 'rsassa_pkcs1v15' or algorithm.removesuffix('_rsa') in hashes and algorithm.endswith('_rsa'):
            if digest is None or algorithm!='rsassa_pkcs1v15' and algorithm.removesuffix('_rsa')!=digest_name:
                return {'status':'invalid','reason':'Signature and digest algorithms disagree.'}
            try:
                key = RSA.import_key(key_bytes)
            except (ValueError,TypeError,IndexError):
                return {'status':'not_checked','reason':'Unsupported RSA public key encoding.'}
            if key.size_in_bits()>8192:
                return {'status':'not_checked','reason':'RSA key exceeds the supported verification limit.'}
            pkcs1_15.new(key).verify(digest,signature)
        elif algorithm == 'rsassa_pss':
            params = signer['signature_algorithm']['parameters'].native
            if digest is None or not params or params['hash_algorithm']['algorithm']!=digest_name or params['mask_gen_algorithm']['algorithm']!='mgf1' or params['trailer_field']!='trailer_field_bc':
                return {'status':'not_checked','reason':'Unsupported RSA-PSS parameters.'}
            mgf = hashes.get(params['mask_gen_algorithm']['parameters']['algorithm'])
            if mgf is None:
                return {'status':'not_checked','reason':'Unsupported RSA-PSS mask digest.'}
            try:
                key = RSA.import_key(key_bytes)
            except (ValueError,TypeError,IndexError):
                return {'status':'not_checked','reason':'Unsupported RSA public key encoding.'}
            if key.size_in_bits()>8192:
                return {'status':'not_checked','reason':'RSA key exceeds the supported verification limit.'}
            pss.new(key,salt_bytes=params['salt_length'],mask_func=lambda seed,length:pss.MGF1(seed,length,mgf)).verify(digest,signature)
        elif algorithm.endswith('_ecdsa') and algorithm.removesuffix('_ecdsa') in hashes:
            if algorithm.removesuffix('_ecdsa')!=digest_name:
                return {'status':'invalid','reason':'Signature and digest algorithms disagree.'}
            try:
                key = ECC.import_key(key_bytes)
            except (ValueError,TypeError,IndexError):
                from cryptography.hazmat.primitives import hashes as crypto_hashes
                from cryptography.hazmat.primitives.asymmetric import ec
                from cryptography.hazmat.primitives.serialization import load_der_public_key
                key = load_der_public_key(key_bytes)
                if not isinstance(key, ec.EllipticCurvePublicKey) or key.key_size > 1024:
                    return {'status':'not_checked','reason':'Unsupported ECDSA public key encoding.'}
                key.verify(signature, message, ec.ECDSA(getattr(crypto_hashes, digest_name.upper())()))
            else:
                DSS.new(key,'fips-186-3',encoding='der').verify(digest,signature)
        elif algorithm in ('ed25519', 'ed448'):
            expected_digest = 'sha512' if algorithm == 'ed25519' else 'shake256'
            if (digest_name != expected_digest and not (algorithm == 'ed448' and digest_name == 'shake256_len')) or certificate.public_key.algorithm != algorithm:
                return {'status':'invalid','reason':'Signature and digest algorithms disagree.'}
            key = ECC.import_key(key_bytes)
            eddsa.new(key, 'rfc8032').verify(message, signature)
        elif algorithm == 'dsa' or algorithm.endswith('_dsa') and algorithm.removesuffix('_dsa') in hashes:
            if digest is None or algorithm != 'dsa' and algorithm.removesuffix('_dsa') != digest_name:
                return {'status':'invalid','reason':'Signature and digest algorithms disagree.'}
            key = DSA.import_key(key_bytes)
            if key.p.bit_length() > 8192:
                return {'status':'not_checked','reason':'Unsupported signature algorithm.'}
            DSS.new(key, 'fips-186-3', encoding='der').verify(digest, signature)
        elif algorithm in ('mldsa44', 'mldsa65', 'mldsa87'):
            from cryptography.hazmat.primitives.serialization import load_der_public_key
            if certificate.public_key.algorithm != algorithm:
                return {'status':'invalid','reason':'Signature and digest algorithms disagree.'}
            load_der_public_key(key_bytes).verify(signature, message)
        else:
            return {'status':'not_checked','reason':'Unsupported signature algorithm.'}
    except (ValueError,TypeError,InvalidSignature):
        return {'status':'invalid','reason':'The cryptographic signature does not match.'}
    return {'status':'match','digest':digest_name,'signatureAlgorithm':algorithm,'weakDigest':digest_name=='sha1'}


def cms_signatures(encoded, content=None, content_type='data'):
    from asn1crypto import cms, pem
    if pem.detect(encoded):
        _,_,encoded = pem.unarmor(encoded)
    info = cms.ContentInfo.load(encoded)
    if info['content_type'].native!='signed_data':
        raise OneKitError('Choose a CMS/PKCS#7 signed-data file.')
    signed = info['content'];embedded_value = signed['encap_content_info']['content']
    embedded = embedded_value.native if content_type == 'data' else embedded_value.contents
    if signed['encap_content_info']['content_type'].native!=content_type:
        return [{'status':'not_checked','reason':'Unsupported CMS content type.'}]
    if content is None:
        content = embedded
    elif embedded is not None and embedded!=content:
        return [{'status':'invalid','reason':'The supplied original differs from the attached signed content.'}]
    if content is None:
        raise OneKitError('Provide the original file together with this detached signature.')
    if len(signed['certificates'])>100 or len(signed['signer_infos'])>20:
        raise OneKitError('Verify at most 20 signers and 100 embedded certificates at a time.')
    certs = [choice.chosen for choice in signed['certificates'] if choice.name=='certificate']
    results = []
    now = datetime.datetime.now(datetime.UTC)
    for signer in signed['signer_infos']:
        sid = signer['sid'];certificate = None
        for cert in certs:
            if sid.name=='issuer_and_serial_number':
                if cert.serial_number==sid.chosen['serial_number'].native and cert.issuer.dump()==sid.chosen['issuer'].dump():
                    certificate = cert;break
            elif sid.name=='subject_key_identifier' and cert.key_identifier==sid.chosen.native:
                certificate = cert;break
        if certificate is None:
            results.append({'status':'not_checked','reason':'The signer certificate is not embedded.'});continue
        result = verify_value(certificate,signer,content,content_type)
        validity = certificate['tbs_certificate']['validity']
        before,after = validity['not_before'].native,validity['not_after'].native
        result.update({'certificateSubject':certificate.subject.human_friendly,'certificateIssuer':certificate.issuer.human_friendly,
                       'certificateSha256':hashlib.sha256(certificate.dump()).hexdigest(),
                       'certificateNotBefore':before.isoformat(),'certificateNotAfter':after.isoformat(),
                       'certificateWithinValidityPeriod':before<=now<=after,
                       'certificateTrust':'not_checked','revocation':'not_checked','trustedTimestamp':'not_checked'})
        results.append(result)
    return results


def pdf_signatures(file):
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(file.data))
    if reader.is_encrypted:
        raise OneKitError('Unlock the PDF before checking its signatures.')
    results = []
    for name,field in (reader.get_fields() or {}).items():
        if field.get('/FT')!='/Sig' or not field.get('/V'):
            continue
        if len(results)>=20:
            raise OneKitError('Verify at most 20 PDF signatures at a time.')
        value = field['/V'].get_object()
        is_timestamp = value.get('/SubFilter') == '/ETSI.RFC3161'
        if value.get('/SubFilter') not in ('/adbe.pkcs7.detached','/ETSI.CAdES.detached','/ETSI.RFC3161'):
            results.append({'field':name,'status':'not_checked','reason':'Unsupported PDF signature format.'});continue
        bounds = value.get('/ByteRange',[])
        if len(bounds)!=4 or any(not isinstance(number,int) or isinstance(number,bool) for number in bounds):
            results.append({'field':name,'status':'invalid','reason':'Invalid PDF signature byte range.'});continue
        zero,length,second,tail = bounds
        if zero!=0 or not 0<length<second or tail<0 or second+tail>len(file.data):
            results.append({'field':name,'status':'invalid','reason':'Invalid PDF signature byte range.'});continue
        gap = file.data[length:second]
        if not re.fullmatch(rb'<[0-9a-fA-F\s]*>',gap):
            results.append({'field':name,'status':'not_checked','reason':'The excluded byte range is not a supported signature container.'});continue
        encoded = bytes.fromhex(gap[1:-1].decode('ascii'))
        contents = value.get('/Contents')
        contents = contents.original_bytes if hasattr(contents,'original_bytes') else bytes(contents or b'')
        if encoded!=contents:
            results.append({'field':name,'status':'invalid','reason':'The byte range excludes content other than the signature value.'});continue
        signed_bytes = file.data[:length]+file.data[second:second+tail]
        if is_timestamp:
            from asn1crypto import cms, tsp
            token = cms.ContentInfo.load(encoded)['content']['encap_content_info']['content']
            info = tsp.TSTInfo.load(token.contents)
            imprint = info['message_imprint']
            expected = content_digest(imprint['hash_algorithm']['algorithm'].native, signed_bytes)
            if not hmac.compare_digest(imprint['hashed_message'].native, expected):
                results.append({'field':name,'status':'invalid','reason':'The signed content digest does not match.'});continue
            checked = cms_signatures(encoded,content_type='tst_info')
        else:
            checked = cms_signatures(encoded,signed_bytes)
        for result in checked:
            result.update({'field':name,'coversCurrentFile':second+tail==len(file.data),
                           'signedRevisionBytes':second+tail,'laterChanges':'not_checked' if second+tail<len(file.data) else 'none'})
            results.append(result)
    return results


def cryptographic_report(tool, files, options):
    containers = [file for file in files if file.kind in ('p7m','p7s','cms','der')]
    if len(containers)>1:
        raise OneKitError('Choose one signed container and, for a detached signature, its original file.')
    try:
        if containers:
            signed = containers[0];original = next((file for file in files if file is not signed),None)
            rows = cms_signatures(signed.data,original.data if original else None)
        elif len(files)==1 and files[0].kind=='pdf':
            rows = pdf_signatures(files[0])
        else:
            raise OneKitError('Choose a signed PDF, P7M, P7S or CMS file. Detached signatures also require the original file.')
    except (ValueError,TypeError,KeyError,OverflowError) as error:
        if isinstance(error,OneKitError):
            raise
        raise OneKitError('Cannot read this signature. Check that the signed file is complete and uses a supported PDF or CMS format.') from error
    verdict = 'unsigned' if not rows else 'mismatch' if any(row['status']=='invalid' for row in rows) else 'cryptographic_match' if all(row['status']=='match' for row in rows) else 'not_checked'
    if verdict=='cryptographic_match' and any('coversCurrentFile' in row for row in rows) and not any(row.get('coversCurrentFile') for row in rows):
        verdict = 'partial_coverage'
    details = {'verdict':verdict,'signatures':rows,'certificateTrust':'not_checked','revocation':'not_checked','trustedTimestamp':'not_checked','limitations':LIMITATION}
    return Result([Artifact('signature-report.json',json.dumps(details,ensure_ascii=False,indent=2).encode())],[LIMITATION],details)


def _is_evidence_archive(file):
    from .signature_validation import MAX_EVIDENCE, SCHEMA
    if file.kind != 'zip' or len(file.data) > MAX_EVIDENCE:
        return False
    try:
        with zipfile.ZipFile(io.BytesIO(file.data)) as archive:
            if archive.getinfo('manifest.json').file_size > MAX_EVIDENCE:
                return False
            manifest = json.loads(archive.read('manifest.json'))
            return isinstance(manifest, dict) and manifest.get('schema') == SCHEMA
    except (ValueError, KeyError, OSError, RuntimeError, NotImplementedError, zipfile.BadZipFile):
        return False


async def run_async(tool, files, options):
    from .signature_validation import default_evidence, evidence_files, validate
    evidence = None
    documents = []
    for file in files:
        if _is_evidence_archive(file):
            if evidence is not None:
                raise OneKitError('Choose one signature evidence archive.')
            try:
                evidence_files(file.data)
            except (ValueError, TypeError, KeyError, zipfile.BadZipFile) as error:
                raise OneKitError('The signature evidence archive is invalid.') from error
            evidence = file.data
        else:
            documents.append(file)
    if not documents or len(documents) > 2:
        raise OneKitError('Choose a signed PDF, P7M, P7S or CMS file. Detached signatures also require the original file.')
    from ..execution import current_context
    if current_context().signature_certificate_only:
        return cryptographic_report(tool, documents, options)
    from .signature_dss import configured_runtime, run_original
    runtime = configured_runtime()
    if runtime is not None:
        containers = [file for file in documents if file.kind in ('p7m', 'p7s', 'cms', 'der')]
        if len(containers) > 1:
            raise OneKitError('Choose one signed container and, for a detached signature, its original file.')
        if not containers and not (len(documents) == 1 and documents[0].kind == 'pdf'):
            raise OneKitError('Choose a signed PDF, P7M, P7S or CMS file. Detached signatures also require the original file.')
        return await run_original(documents, evidence, runtime)
    from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
    from pyhanko.pdf_utils.misc import PdfReadError
    from pyhanko_certvalidator.errors import ValidationError

    result = cryptographic_report(tool, documents, options)
    try:
        result.details['validation'] = await validate(documents, evidence if evidence is not None else default_evidence())
        if result.details['validation']['indication'] == 'TOTAL_PASSED' and (
                len(result.details['validation']['signatures']) != len(result.details['signatures'])
                or any(row['status'] != 'match' for row in result.details['signatures'])):
            result.details['validation']['indication'] = 'INDETERMINATE'
    except OneKitError:
        raise
    except (ValueError, TypeError, KeyError, IndexError, OverflowError, OSError, RecursionError,
            InvalidSignature, UnsupportedAlgorithm, PdfReadError, ValidationError) as error:
        # Preserve the cryptographic result but never upgrade missing/invalid
        # evidence to a successful AdES validation. No raw certificate data leaks.
        result.details['validation'] = {'engine': 'pyhanko', 'engineVersion': '0.38.0',
                                        'indication': 'INDETERMINATE', 'reason': type(error).__name__,
                                        'network': 'disabled', 'dssEquivalence': 'not_established'}
    result.files[0] = Artifact('signature-report.json', json.dumps(result.details, ensure_ascii=False, indent=2).encode())
    return result


def run(tool, files, options):
    return asyncio.run(run_async(tool, files, options))
