# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Offline signature cryptography; never infer certificate trust or revocation."""
import datetime
import hashlib
import hmac
import io
import json
import re

from ..models import Artifact, OneKitError, Result

LIMITATION = 'Offline cryptographic checks only. Certificate trust chains, revocation, qualified-signature status and trusted timestamps are not validated. A matching signature does not establish a trusted signer identity.'


def verify_value(certificate, signer, data):
    from Crypto.Hash import SHA1, SHA256, SHA384, SHA512
    from Crypto.PublicKey import ECC, RSA
    from Crypto.Signature import DSS, pkcs1_15, pss
    hashes = {'sha1':SHA1,'sha256':SHA256,'sha384':SHA384,'sha512':SHA512}
    digest_name = signer['digest_algorithm']['algorithm'].native
    if digest_name not in hashes:
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
        if 'message_digest' not in values or 'content_type' not in values or values['content_type'][0].native!='data':
            return {'status':'not_checked','reason':'Required CMS signed attributes are missing or unsupported.'}
        if not hmac.compare_digest(values['message_digest'][0].native,hashlib.new(digest_name,data).digest()):
            return {'status':'invalid','reason':'The signed content digest does not match.'}
        message = attrs.untag().dump()
    signature = signer['signature'].native
    algorithm = signer['signature_algorithm']['algorithm'].native
    digest = hashes[digest_name].new(message)
    key_bytes = certificate.public_key.dump()
    try:
        if algorithm in ('rsassa_pkcs1v15','sha1_rsa','sha256_rsa','sha384_rsa','sha512_rsa'):
            if algorithm!='rsassa_pkcs1v15' and algorithm.split('_')[0]!=digest_name:
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
            if not params or params['hash_algorithm']['algorithm']!=digest_name or params['mask_gen_algorithm']['algorithm']!='mgf1' or params['trailer_field']!='trailer_field_bc':
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
        elif algorithm in ('sha1_ecdsa','sha256_ecdsa','sha384_ecdsa','sha512_ecdsa'):
            if algorithm.split('_')[0]!=digest_name:
                return {'status':'invalid','reason':'Signature and digest algorithms disagree.'}
            try:
                key = ECC.import_key(key_bytes)
            except (ValueError,TypeError,IndexError):
                return {'status':'not_checked','reason':'Unsupported ECDSA public key encoding.'}
            if key.curve not in ('NIST P-256','NIST P-384','NIST P-521'):
                return {'status':'not_checked','reason':'Unsupported ECDSA curve.'}
            DSS.new(key,'fips-186-3',encoding='der').verify(digest,signature)
        else:
            return {'status':'not_checked','reason':'Unsupported signature algorithm.'}
    except (ValueError,TypeError):
        return {'status':'invalid','reason':'The cryptographic signature does not match.'}
    return {'status':'match','digest':digest_name,'signatureAlgorithm':algorithm,'weakDigest':digest_name=='sha1'}


def cms_signatures(encoded, content=None):
    from asn1crypto import cms, pem
    if pem.detect(encoded):
        _,_,encoded = pem.unarmor(encoded)
    info = cms.ContentInfo.load(encoded)
    if info['content_type'].native!='signed_data':
        raise OneKitError('Choose a CMS/PKCS#7 signed-data file.')
    signed = info['content'];embedded = signed['encap_content_info']['content'].native
    if signed['encap_content_info']['content_type'].native!='data':
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
        result = verify_value(certificate,signer,content)
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
        if value.get('/SubFilter') not in ('/adbe.pkcs7.detached','/ETSI.CAdES.detached'):
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
        for result in cms_signatures(encoded,signed_bytes):
            result.update({'field':name,'coversCurrentFile':second+tail==len(file.data),
                           'signedRevisionBytes':second+tail,'laterChanges':'not_checked' if second+tail<len(file.data) else 'none'})
            results.append(result)
    return results


def run(tool, files, options):
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
