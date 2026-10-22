# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import shutil
import struct
import subprocess
import zipfile
from pathlib import Path

import pytest

from onekit import Artifact, OneKitError, execute
from onekit.tools.archives import pack, unpack

PASSWORD = "a-long-zip-password"


def seven_zip():
    executable = shutil.which("7z") or shutil.which("7zz")
    if not executable and Path("C:/Program Files/7-Zip/7z.exe").is_file():
        executable = "C:/Program Files/7-Zip/7z.exe"
    if not executable:
        pytest.skip("7-Zip is required for the independent interoperability check.")
    return executable


def test_zip_aes256_metadata_and_unicode_filenames():
    files = [Artifact("nested/caffè.txt", b"private content"), Artifact("empty.txt", b"")]
    options = {"password": PASSWORD}
    encrypted = execute("security-encrypt", files, options)
    assert encrypted.files[0].name.endswith(".zip")
    with zipfile.ZipFile(io.BytesIO(encrypted.files[0].data)) as archive:
        for entry in archive.infolist():
            assert entry.flag_bits & 1
            assert entry.compress_type == 99
            assert struct.unpack("<HHH2sBH", entry.extra) == (0x9901, 7, 2, b"AE", 3, 0)
            with pytest.raises(RuntimeError):
                archive.read(entry)
    assert execute("security-decrypt", encrypted.files, options).files == files
    restored = execute("security-decrypt", encrypted.files, {**options, "restore": "zip"}).files[0]
    assert unpack(restored.data) == files


def test_onekit_archives_are_not_accepted_as_encrypted_files():
    with pytest.raises(OneKitError):
        execute("security-decrypt", [Artifact("legacy.onekit", b"ONEKIT\x01" + bytes(80))], {"password": PASSWORD})


def test_unencrypted_zip_and_expansion_over_budget_are_rejected():
    files = [Artifact("note.txt", b"private content")]
    with pytest.raises(OneKitError, match="AES-256"):
        execute("security-decrypt", [Artifact("plain.zip", pack(files))], {"password": PASSWORD})
    encrypted = execute("security-encrypt", files, {"password": PASSWORD}).files[0]
    from onekit.tools.security.zip_aes import decrypt_zip
    with pytest.raises(OneKitError, match="safety limits"):
        decrypt_zip(encrypted.data, PASSWORD.encode(), 2)


def test_7zip_reads_onekit_zip_and_onekit_reads_7zip(tmp_path):
    executable = seven_zip()
    password = PASSWORD
    data = b"\x00\xff private bytes " * 15
    encrypted = execute("security-encrypt", [Artifact("folder/note.bin", data)], {"password": password}).files[0]
    archive = tmp_path / "encrypted.zip"
    archive.write_bytes(encrypted.data)
    result = subprocess.run([executable, "x", "-so", f"-p{password}", str(archive), "folder/note.bin"],
                            capture_output=True, check=False)
    assert result.returncode == 0, result.stderr
    assert result.stdout == data
    (tmp_path / "folder").mkdir()
    (tmp_path / "folder/note.bin").write_bytes(data)
    external = tmp_path / "external.zip"
    result = subprocess.run([executable, "a", "-tzip", "-mem=AES256", "-pshort", str(external), "folder"],
                            cwd=tmp_path, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr
    restored = execute("security-decrypt", [Artifact("external.zip", external.read_bytes())], {"password": "short"})
    assert restored.files == [Artifact("folder/note.bin", data)]


def test_encryption_rejects_passwords_7zip_cannot_read():
    with pytest.raises(OneKitError, match="ASCII"):
        execute("security-encrypt", [Artifact("a.txt", b"a")], {"password": "una-password-秘密-è"})
