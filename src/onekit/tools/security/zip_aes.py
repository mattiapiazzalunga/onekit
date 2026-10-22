# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""WinZip AES ZIP interoperability using the stream-zip/unzip implementations."""
import io
import struct
import zipfile
from datetime import datetime
from itertools import pairwise

from ...models import Artifact, OneKitError
from ...validation import validate_zip
from ..archives import safe_name


def encrypt_zip(files, password):
    from stream_zip import NO_COMPRESSION_32, stream_zip

    names = [safe_name(file.name) for file in files]
    if len(names) != len(set(names)):
        raise OneKitError("Archive inputs must have unique paths.")
    # STORE avoids double compression of PDFs/images and expansion-ratio surprises.
    members = ((name, datetime(2026, 1, 1), 0o100600, NO_COMPRESSION_32, (file.data,))
               for name, file in zip(names, files))
    return b"".join(stream_zip(members, password=password, extended_timestamps=False))


def aes_extra(extra):
    while extra:
        if len(extra) < 4:
            raise OneKitError("The encrypted ZIP extra fields are damaged.")
        kind, size = struct.unpack_from("<HH", extra)
        if size > len(extra) - 4:
            raise OneKitError("The encrypted ZIP extra fields are damaged.")
        value, extra = extra[4:4 + size], extra[4 + size:]
        if kind == 0x9901:
            if len(value) != 7:
                raise OneKitError("The encrypted ZIP AES header is damaged.")
            return value
    return None


def decrypt_zip(data, password, limit):
    from stream_unzip import UnzipError, stream_unzip

    validate_zip(data, limit, allow_encrypted=True)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        directory_start = archive.start_dir
    expected, spans = {}, []
    for entry in entries:
        safe_name(entry.filename)
        if not entry.is_dir():
            extra = aes_extra(entry.extra)
            if not entry.flag_bits & 1 or entry.compress_type != 99 or extra is None:
                raise OneKitError("Choose a ZIP encrypted with AES-256; unencrypted ZIP and ZipCrypto are unsupported.")
            version, vendor, strength, method = struct.unpack("<H2sBH", extra)
            if version not in (1, 2) or vendor != b"AE" or strength != 3 or method not in (0, 8, 9):
                raise OneKitError("Supported encrypted ZIP format: WinZip AES-256 with Store, Deflate or Deflate64.")
        start = entry.header_offset
        if start < 0 or start + 30 > directory_start or data[start:start + 4] != b"PK\x03\x04":
            raise OneKitError("The encrypted ZIP local header is damaged.")
        flags, method = struct.unpack_from("<HH", data, start + 6)
        name_size, extra_size = struct.unpack_from("<HH", data, start + 26)
        body = start + 30 + name_size + extra_size
        raw_name = data[start + 30:start + 30 + name_size]
        encoding = "utf-8" if flags & 0x800 else "cp437"
        if (body + entry.compress_size > directory_start or flags != entry.flag_bits
                or method != entry.compress_type or raw_name.decode(encoding) != entry.filename
                or aes_extra(data[start + 30 + name_size:body]) != aes_extra(entry.extra)):
            raise OneKitError("The encrypted ZIP local header and directory do not match.")
        expected[raw_name] = entry
        spans.append((start, body + entry.compress_size))
    spans.sort()
    if any(end > following for (_, end), (following, _) in pairwise(spans)):
        raise OneKitError("The encrypted ZIP contains overlapping entries.")
    files, seen, total = [], set(), 0
    try:
        for raw_name, _, chunks in stream_unzip((data,), password=password, allow_zip64=False):
            entry = expected.get(raw_name)
            if entry is None or raw_name in seen:
                raise OneKitError("The encrypted ZIP entries do not match its directory.")
            seen.add(raw_name)
            content, length = [], 0
            for chunk in chunks:
                length += len(chunk)
                total += len(chunk)
                if total > limit or length > entry.file_size:
                    raise OneKitError("Archive expansion exceeds safety limits or its declared size.")
                content.append(chunk)
            if length != entry.file_size:
                raise OneKitError("The encrypted ZIP entry size is damaged.")
            if not entry.is_dir():
                files.append(Artifact(safe_name(entry.filename), b"".join(content)))
    except UnzipError as exc:
        raise OneKitError("Wrong password or damaged encrypted ZIP.") from exc
    if seen != set(expected):
        raise OneKitError("The encrypted ZIP is missing entries or is damaged.")
    return files
