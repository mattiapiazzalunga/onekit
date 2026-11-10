# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import hashlib


def content_digest(name, content):
    # RFC 8419 specifies a 512-bit SHAKE256 output for Ed448 CMS message digests.
    if name in ('shake256', 'shake256_len'):
        return hashlib.shake_256(content).digest(64)
    return hashlib.new(name, content).digest()
