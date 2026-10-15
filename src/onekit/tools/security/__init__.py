# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
import os

from ...models import Artifact, OneKitError, Result, output, require

MAGIC = b"ONEKIT\x01"


def run(tool, files, options):
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import scrypt
    from ..archives import pack, unpack
    password = str(require(options, "password")).encode("utf-8")
    if len(password) < 12:
        raise OneKitError("Use a password with at least 12 characters.")
    if tool.id == "security-encrypt":
        salt, nonce = os.urandom(16), os.urandom(12)
        key = scrypt(password, salt, 32, N=2**15, r=8, p=1)
        header = MAGIC + salt + nonce
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        cipher.update(header)
        ciphertext, tag = cipher.encrypt_and_digest(pack(files))
        encrypted = ciphertext + tag
        return Result([output(files[0], "onekit", header + encrypted)])
    data = files[0].data
    if not data.startswith(MAGIC) or len(data) < len(MAGIC) + 44:
        raise OneKitError("This is not a supported OneKit encrypted archive.")
    offset = len(MAGIC)
    salt, nonce = data[offset:offset+16], data[offset+16:offset+28]
    key = scrypt(password, salt, 32, N=2**15, r=8, p=1)
    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        cipher.update(data[:offset+28])
        plaintext = cipher.decrypt_and_verify(data[offset+28:-16], data[-16:])
    except ValueError as exc:
        raise OneKitError("Wrong password or damaged encrypted file.") from exc
    return Result(unpack(plaintext))
