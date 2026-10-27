# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import hashlib
import hmac
import json
import re

from ..models import Artifact, OneKitError, Result


def run(tool, files, options):
    algorithm = options.get('algorithm','sha256')
    if algorithm not in ('sha256','sha512','sha1','md5'):
        raise OneKitError('Choose SHA-256, SHA-512, SHA-1 or MD5.')
    expected = options.get('expected','')
    if not isinstance(expected,str):
        raise OneKitError('Enter an expected checksum as hexadecimal text.')
    expected = expected.strip().lower()
    if expected and (len(files)!=1 or not re.fullmatch(r'[0-9a-f]{'+str(hashlib.new(algorithm).digest_size*2)+r'}',expected)):
        raise OneKitError('Compare one file at a time and enter a complete hexadecimal checksum for the selected algorithm.')
    rows = []
    for file in files:
        digest = hashlib.new(algorithm,file.data).hexdigest()
        rows.append({'name':file.name,'bytes':len(file.data),'checksum':digest,
                     **({'matches':hmac.compare_digest(digest,expected)} if expected else {})})
    details = {'algorithm':algorithm,'files':rows}
    warnings = ['MD5 and SHA-1 are legacy checksums; use SHA-256 or SHA-512 for integrity checks.'] if algorithm in ('md5','sha1') else []
    return Result([Artifact('checksums.json',json.dumps(details,ensure_ascii=False,indent=2).encode())],warnings,details)
