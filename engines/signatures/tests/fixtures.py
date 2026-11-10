"""Author synthetic inputs for the optional original-DSS VM integration test."""
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tests'))
from cryptography.hazmat.primitives import serialization
from test_signature_validation import pki

_, root, _, content, signature = pki()
encode = lambda value: base64.b64encode(value).decode('ascii')
Path(sys.argv[1]).write_text(json.dumps({
    'document': {'name': 'signature.p7s', 'data': encode(signature)},
    'detached': {'data': encode(content)},
    'certificates': [encode(root.public_bytes(serialization.Encoding.DER))],
}), encoding='utf-8')
