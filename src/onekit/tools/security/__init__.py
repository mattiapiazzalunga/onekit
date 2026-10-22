# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
from ...models import Artifact, OneKitError, Result, output, require

def run(tool, files, options):
    from ..archives import pack
    restore = options.get("restore", "files")
    if tool.id == "security-decrypt" and restore not in ("files", "zip"):
        raise OneKitError("restore must be files or zip.")
    password_text = str(require(options, "password"))
    password = password_text.encode("utf-8")
    if tool.id == "security-encrypt" and len(password_text) < 12:
        raise OneKitError("Use a password with at least 12 characters.")
    if tool.id == "security-encrypt" and not all(32 <= ord(char) <= 126 for char in password_text):
        raise OneKitError("Use ASCII letters, numbers, spaces and symbols for a ZIP password compatible with 7-Zip.")
    if tool.id == "security-encrypt":
        from .zip_aes import encrypt_zip
        return Result([output(files[0], "zip", encrypt_zip(files, password))],
                      warnings=["ZIP encrypts file contents; file and folder names remain visible."])
    from .zip_aes import decrypt_zip
    restored = decrypt_zip(files[0].data, password, options.get("_max_expanded_bytes", 128 * 1024 * 1024))
    return Result([Artifact("restored.zip", pack(restored))] if restore == "zip" else restored)
