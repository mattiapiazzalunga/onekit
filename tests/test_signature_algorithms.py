import asyncio
import datetime
from functools import lru_cache

import pytest
from asn1crypto import keys
from asn1crypto import x509 as asn1x509
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dsa, ec, ed25519, ed448, rsa
from test_signature_validation import local_policy, pki

from onekit import Artifact, execute

ALGORITHMS = ['ed25519', 'ed448', 'dsa', 'brainpool', 'sha224-rsa', 'sha3-rsa', 'sha3-ecdsa', 'ml-dsa-44']


@lru_cache
def algorithm_inputs(algorithm):
    from pyhanko.sign.signers import SimpleSigner
    from pyhanko.sign.signers.pdf_cms import select_suitable_signing_md
    from pyhanko_certvalidator.registry import SimpleCertificateStore
    root_key, root, template, content, _ = pki()
    if algorithm == 'ed25519':
        key = ed25519.Ed25519PrivateKey.generate()
    elif algorithm == 'ed448':
        key = ed448.Ed448PrivateKey.generate()
    elif algorithm == 'dsa':
        key = dsa.generate_private_key(2048)
    elif algorithm == 'brainpool':
        key = ec.generate_private_key(ec.BrainpoolP256R1())
    elif algorithm == 'sha3-ecdsa':
        key = ec.generate_private_key(ec.SECP256R1())
    elif algorithm == 'ml-dsa-44':
        from cryptography.hazmat.primitives.asymmetric.mldsa import MLDSA44PrivateKey
        key = MLDSA44PrivateKey.generate()
    else:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    now = datetime.datetime.now(datetime.UTC)
    builder = (x509.CertificateBuilder().subject_name(template.subject).issuer_name(root.subject)
               .serial_number(7).public_key(key.public_key()).not_valid_before(now-datetime.timedelta(days=1))
               .not_valid_after(now+datetime.timedelta(days=1)))
    for extension in template.extensions:
        builder = builder.add_extension(extension.value, extension.critical)
    certificate = builder.sign(root_key, hashes.SHA256())
    store = SimpleCertificateStore(); store.register(asn1x509.Certificate.load(root.public_bytes(serialization.Encoding.DER)))
    from asn1crypto import algos
    signer = SimpleSigner(asn1x509.Certificate.load(certificate.public_bytes(serialization.Encoding.DER)),
        keys.PrivateKeyInfo.load(key.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8,
                                                 serialization.NoEncryption())), store,
        signature_mechanism=algos.SignedDigestAlgorithm({'algorithm': 'rsassa_pkcs1v15'}) if algorithm == 'sha3-rsa' else None)
    digest = 'sha224' if algorithm == 'sha224-rsa' else 'sha3_256' if algorithm.startswith('sha3-') else select_suitable_signing_md(signer.signing_cert.public_key)
    signature = asyncio.run(signer.async_sign_general_data(content, digest, use_cades=True)).dump()
    return [Artifact('signature.p7s', signature), Artifact('original.bin', content)]


@pytest.mark.parametrize('algorithm', ALGORITHMS)
@pytest.mark.parametrize('altered', [False, True])
def test_additional_algorithms_verify_the_actual_content(monkeypatch, algorithm, altered):
    local_policy(monkeypatch)
    files = algorithm_inputs(algorithm)
    if altered:
        files = [files[0], Artifact('original.bin', b'changed')]
    report = execute('signature-verify', files).details
    assert report['verdict'] == ('mismatch' if altered else 'cryptographic_match'), report
    assert 'reason' not in report['validation'], report['validation']
    if altered:
        assert report['validation']['indication'] == 'TOTAL_FAILED'
    elif algorithm in ('ed25519', 'ed448', 'ml-dsa-44'):
        assert report['validation']['signatures'][0]['subindication'] == 'CRYPTO_CONSTRAINTS_FAILURE'
    else:
        assert report['validation']['indication'] == 'TOTAL_PASSED', report['validation']
