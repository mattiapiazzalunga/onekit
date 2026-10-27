# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import datetime
import hashlib
import io
import re
from functools import lru_cache

import pytest
from asn1crypto import cms, keys, x509
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC, RSA
from Crypto.Signature import DSS, pkcs1_15, pss
from PIL import Image
from pypdf import PdfWriter
from pypdf.generic import ArrayObject, ByteStringObject, DictionaryObject, NameObject, NumberObject, TextStringObject

from onekit import Artifact, OneKitError, execute

IDS = ['file-checksum','signature-verify','pdf-to-text','gif-to-images','png-to-svg']


@lru_cache
def material(algorithm='rsa'):
    key = RSA.generate(2048) if algorithm=='rsa' else ECC.generate(curve='P-224' if algorithm=='ec224' else 'P-256')
    public = key.public_key().export_key(format='DER')
    name = x509.Name.build({'common_name':'OneKit synthetic test signer'})
    signature_algorithm = 'sha256_rsa' if algorithm=='rsa' else 'sha256_ecdsa'
    tbs = x509.TbsCertificate({'version':'v3','serial_number':1,'signature':{'algorithm':signature_algorithm},
                             'issuer':name,'subject':name,'subject_public_key_info':keys.PublicKeyInfo.load(public),
                             'validity':{'not_before':x509.Time({'utc_time':datetime.datetime(2020,1,1,tzinfo=datetime.UTC)}),
                                         'not_after':x509.Time({'utc_time':datetime.datetime(2035,1,1,tzinfo=datetime.UTC)})}})
    digest = SHA256.new(tbs.dump())
    signature = pkcs1_15.new(key).sign(digest) if algorithm=='rsa' else DSS.new(key,'fips-186-3',encoding='der').sign(digest)
    cert = x509.Certificate({'tbs_certificate':tbs,'signature_algorithm':{'algorithm':signature_algorithm},'signature_value':signature})
    return key,cert


def signed_cms(data, *, attached=True, algorithm='rsa', use_pss=False):
    key,cert = material(algorithm)
    attrs = cms.CMSAttributes([{'type':'content_type','values':['data']},{'type':'message_digest','values':[hashlib.sha256(data).digest()]}])
    digest = SHA256.new(attrs.dump())
    if use_pss:
        signature = pss.new(key,salt_bytes=32).sign(digest)
        alg = {'algorithm':'rsassa_pss','parameters':{'hash_algorithm':{'algorithm':'sha256'},'mask_gen_algorithm':{'algorithm':'mgf1','parameters':{'algorithm':'sha256'}},'salt_length':32}}
    elif algorithm=='rsa':
        signature = pkcs1_15.new(key).sign(digest);alg = {'algorithm':'rsassa_pkcs1v15'}
    else:
        signature = DSS.new(key,'fips-186-3',encoding='der').sign(digest);alg = {'algorithm':'sha256_ecdsa'}
    signer = cms.SignerInfo({'version':'v1','sid':{'issuer_and_serial_number':{'issuer':cert.issuer,'serial_number':cert.serial_number}},
                            'digest_algorithm':{'algorithm':'sha256'},'signed_attrs':attrs,'signature_algorithm':alg,'signature':signature})
    return cms.ContentInfo({'content_type':'signed_data','content':{'version':'v1','digest_algorithms':[{'algorithm':'sha256'}],
                           'encap_content_info':{'content_type':'data',**({'content':data} if attached else {})},
                           'certificates':[cert],'signer_infos':[signer]}}).dump()


def signed_pdf():
    writer = PdfWriter();writer.add_blank_page(width=300,height=400)
    signature = DictionaryObject({NameObject('/Type'):NameObject('/Sig'),NameObject('/Filter'):NameObject('/Adobe.PPKLite'),
                                  NameObject('/SubFilter'):NameObject('/adbe.pkcs7.detached'),
                                  NameObject('/ByteRange'):ArrayObject([NumberObject(v) for v in [0,1111111111,2222222222,3333333333]]),
                                  NameObject('/Contents'):ByteStringObject(bytes(8192))})
    field = DictionaryObject({NameObject('/FT'):NameObject('/Sig'),NameObject('/T'):TextStringObject('TestSignature'),NameObject('/V'):writer._add_object(signature)})
    writer._root_object[NameObject('/AcroForm')] = DictionaryObject({NameObject('/Fields'):ArrayObject([writer._add_object(field)])})
    stream = io.BytesIO();writer.write(stream);data = stream.getvalue()
    match = re.search(rb'/Contents\s*(<[0-9a-fA-F]+>)',data);start,end = match.span(1)
    values = re.search(rb'/ByteRange \[ 0 1111111111 2222222222 3333333333 \]',data)
    replacement = f'/ByteRange [ 0 {start:010d} {end:010d} {len(data)-end:010d} ]'.encode()
    assert len(replacement)==values.end()-values.start()
    data = data[:values.start()]+replacement+data[values.end():]
    encoded = signed_cms(data[:start]+data[end:],attached=False).hex().encode()
    return data[:start]+b'<'+encoded+b'0'*(end-start-2-len(encoded))+b'>'+data[end:]


def samples(tool):
    if tool.id=='file-checksum':
        return [Artifact('sample.bin',b'OneKit')],{}
    if tool.id=='signature-verify':
        return [Artifact('signed.p7m',signed_cms(b'OneKit signed fixture'))],{}
    if tool.id=='pdf-to-text':
        from test_core import pdf
        return [pdf()],{}
    if tool.id=='png-to-svg':
        stream = io.BytesIO();Image.new('RGB',(16,12),'blue').save(stream,'PNG')
        return [Artifact('image.png',stream.getvalue())],{}
    stream = io.BytesIO()
    Image.new('RGBA',(16,12),'red').save(stream,'GIF',save_all=True,append_images=[Image.new('RGBA',(16,12),'blue')],duration=[100,200],loop=0,disposal=2)
    return [Artifact('animation.gif',stream.getvalue())],{}


@pytest.mark.parametrize('algorithm',['sha256','sha512','sha1','md5'])
def test_checksums_match_known_digests_and_compare_expected(algorithm):
    expected = hashlib.new(algorithm,b'abc').hexdigest()
    result = execute('file-checksum',[Artifact('sample.bin',b'abc')],{'algorithm':algorithm,'expected':expected.upper()})
    assert result.details['files'][0]['checksum']==expected and result.details['files'][0]['matches']
    mismatch = execute('file-checksum',[Artifact('sample.bin',b'abd')],{'algorithm':algorithm,'expected':expected})
    assert mismatch.details['files'][0]['matches'] is False


@pytest.mark.parametrize('algorithm,use_pss',[('rsa',False),('rsa',True),('ec',False)])
def test_cms_verifies_rsa_pss_and_ecdsa_and_detects_changed_content(algorithm,use_pss):
    signature = Artifact('signed.p7s',signed_cms(b'original',attached=False,algorithm=algorithm,use_pss=use_pss))
    result = execute('signature-verify',[signature,Artifact('original.bin',b'original')])
    assert result.details['verdict']=='cryptographic_match'
    assert result.details['certificateTrust']=='not_checked' and result.details['revocation']=='not_checked'
    altered = execute('signature-verify',[signature,Artifact('original.bin',b'changed')])
    assert altered.details['verdict']=='mismatch'
    with pytest.raises(OneKitError,match='original'):
        execute('signature-verify',[signature])


def test_pdf_signature_detects_tampering_and_reports_uncovered_later_bytes():
    data = signed_pdf()
    report = execute('signature-verify',[Artifact('signed.pdf',data)]).details
    assert report['verdict']=='cryptographic_match' and report['signatures'][0]['coversCurrentFile']
    altered = data.replace(b'/Producer (pypdf)',b'/Producer (Qypdf)',1)
    assert altered!=data
    assert execute('signature-verify',[Artifact('signed.pdf',altered)]).details['verdict']=='mismatch'
    later = execute('signature-verify',[Artifact('signed.pdf',data+b'\n%later bytes')]).details
    assert later['verdict']=='partial_coverage'
    assert later['signatures'][0]['coversCurrentFile'] is False
    assert later['signatures'][0]['laterChanges']=='not_checked'


def test_gif_frames_have_composed_pixels_and_durations():
    from onekit.catalog import TOOLS
    files,_ = samples(TOOLS['gif-to-images'])
    result = execute('gif-to-images',files)
    assert result.details['durationsMs']==[100,200] and len(result.files)==2
    assert Image.open(io.BytesIO(result.files[0].data)).convert('RGB').getpixel((5,5))==(255,0,0)
    assert Image.open(io.BytesIO(result.files[1].data)).convert('RGB').getpixel((5,5))==(0,0,255)


def test_pdf_text_page_selection_and_png_vector_output():
    from onekit.catalog import TOOLS
    files,_ = samples(TOOLS['pdf-to-text'])
    result = execute('pdf-to-text',files,{'pages':'2'})
    assert 'Second page' in result.files[0].text() and 'regression document' not in result.files[0].text()
    files,_ = samples(TOOLS['png-to-svg'])
    result = execute('png-to-svg',files)
    assert '<path' in result.files[0].text() and '<image' not in result.files[0].text()


def test_unsupported_ecdsa_curve_is_not_reported_as_a_broken_signature():
    signature = Artifact('signed.p7m',signed_cms(b'original',algorithm='ec224'))
    result = execute('signature-verify',[signature])
    assert result.details['verdict']=='not_checked'
    assert result.details['signatures'][0]['reason']=='Unsupported ECDSA curve.'
