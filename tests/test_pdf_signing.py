import asyncio
import base64
import datetime
import io

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature
from pyhanko_certvalidator import ValidationContext
from pypdf import PdfWriter

from onekit import Artifact, OneKitError, execute
from onekit.api import execute_async


def signing_case(algorithm='rsa'):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048) if algorithm == 'rsa' else ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'OneKit synthetic signing test')])
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(1).not_valid_before(datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC))
            .not_valid_after(datetime.datetime(2035, 1, 1, tzinfo=datetime.UTC)).sign(key, hashes.SHA256()))
    data = pkcs12.serialize_key_and_certificates(b'test', key, cert, None, serialization.BestAvailableEncryption(b'test-password'))
    writer = PdfWriter(); writer.add_blank_page(width=300, height=400)
    stream = io.BytesIO(); writer.write(stream)
    return [Artifact('document.pdf', stream.getvalue())], {'certificate_data': base64.b64encode(data).decode(), 'password': 'test-password'}


def assert_signed(result):
    assert result.files[0].name == 'document.signed.pdf'
    signatures = PdfFileReader(io.BytesIO(result.files[0].data)).embedded_signatures
    assert len(signatures) == 1
    status = validate_pdf_signature(signatures[0], signer_validation_context=ValidationContext(trust_roots=[signatures[0].signer_cert], allow_fetching=False))
    assert status.intact and status.valid


@pytest.mark.parametrize('algorithm', ['rsa', 'ec'])
def test_shared_sync_and_async_signing(algorithm):
    files, options = signing_case(algorithm)
    assert_signed(execute('pdf-sign', files, options))
    assert_signed(asyncio.run(execute_async('pdf-sign', files, options)))


def test_certificate_path_remains_supported(tmp_path):
    files, options = signing_case()
    path = tmp_path / 'signer.p12'; path.write_bytes(base64.b64decode(options.pop('certificate_data')))
    assert_signed(execute('pdf-sign', files, {**options, 'certificate': str(path)}))


@pytest.mark.parametrize('case', ['none', 'malformed', 'oversized', 'wrong-password'])
def test_invalid_credentials_produce_no_signed_output(case):
    files, options = signing_case()
    if case == 'none': options['certificate_data'] = None
    elif case == 'malformed': options['certificate_data'] = 'invalid!'
    elif case == 'oversized': options['certificate_data'] = base64.b64encode(b'x' * (1024 * 1024 + 1)).decode()
    else: options['password'] = 'incorrect'
    with pytest.raises(OneKitError):
        asyncio.run(execute_async('pdf-sign', files, options))
