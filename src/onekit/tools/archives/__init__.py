# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
import io
import tarfile
import zipfile
from pathlib import PurePosixPath

from ...models import Artifact, OneKitError, Result, output

LIMIT = 128 * 1024 * 1024


def tar_payload(data, limit):
    # Bound decompression before tarfile parses PAX/sparse metadata or member sizes.
    budget = limit + 4096 * 1024
    if data.startswith(b"\x1f\x8b"):
        import zlib
        decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
        payload = decoder.decompress(data, budget + 1)
    elif data.startswith(b"BZh"):
        import bz2
        decoder = bz2.BZ2Decompressor()
        payload = decoder.decompress(data, max_length=budget + 1)
    elif data.startswith(b"\xfd7zXZ\x00"):
        import lzma
        decoder = lzma.LZMADecompressor(memlimit=max(limit, 16 * 1024 * 1024))
        payload = decoder.decompress(data, max_length=budget + 1)
    else:
        if len(data) > budget:
            raise OneKitError("TAR expansion exceeds safety limits.")
        return data
    if len(payload) > budget or not decoder.eof:
        raise OneKitError("Archive expansion exceeds safety limits or the compressed stream is incomplete.")
    if decoder.unused_data.strip(b"\0"):
        raise OneKitError("Concatenated compressed archive streams are not supported.")
    return payload


def safe_name(name):
    path = PurePosixPath(name.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts or ":" in name:
        raise OneKitError("Archive contains an unsafe path.")
    return str(path)


def unpack(data, *, limit=LIMIT):
    files, total = [], 0
    if zipfile.is_zipfile(io.BytesIO(data)):
        from ...validation import validate_zip
        validate_zip(data, limit)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            if len(entries) > 4096:
                raise OneKitError("Archive contains too many entries.")
            for entry in entries:
                name = safe_name(entry.filename)
                if entry.is_dir():
                    continue
                if entry.external_attr >> 16 & 0o170000 == 0o120000:
                    raise OneKitError("Archive symlinks are not supported.")
                total += entry.file_size
                if total > limit or entry.file_size > max(entry.compress_size, 1) * 1000:
                    raise OneKitError("Archive expansion exceeds safety limits.")
                files.append(Artifact(name, archive.read(entry)))
    else:
        with tarfile.open(fileobj=io.BytesIO(tar_payload(data, limit)), mode="r:") as archive:
            seen = set()
            for index, entry in enumerate(archive):
                if index >= 4096:
                    raise OneKitError("Archive contains too many entries.")
                name = safe_name(entry.name)
                if name in seen:
                    raise OneKitError("Archive contains duplicate paths.")
                seen.add(name)
                if entry.isdir():
                    continue
                if not entry.isfile():
                    raise OneKitError("Archive links and devices are not supported.")
                total += entry.size
                if total > limit:
                    raise OneKitError("Archive expansion exceeds safety limits.")
                stream = archive.extractfile(entry)
                content = stream.read(limit + 1)
                if len(content) != entry.size:
                    raise OneKitError("The archive entry is truncated or exceeds its declared size.")
                files.append(Artifact(name, content))
    return files


def pack(files, format="zip"):
    names = [safe_name(file.name) for file in files]
    if len(set(names)) != len(names):
        raise OneKitError("Archive inputs must have unique paths.")
    stream = io.BytesIO()
    if format == "zip":
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file in files:
                archive.writestr(safe_name(file.name), file.data)
    else:
        modes = {"tar": "w", "tar.gz": "w:gz", "tar.bz2": "w:bz2", "tar.xz": "w:xz"}
        if format not in modes:
            raise OneKitError("Supported archive formats: zip, tar, tar.gz, tar.bz2, tar.xz.")
        with tarfile.open(fileobj=stream, mode=modes[format]) as archive:
            for file in files:
                info = tarfile.TarInfo(safe_name(file.name))
                info.size = len(file.data)
                info.mode = 0o600
                archive.addfile(info, io.BytesIO(file.data))
    return stream.getvalue()


def run(tool, files, options):
    return Result([output(files[0], options.get("format", "zip"), pack(unpack(files[0].data, limit=options.get("_max_expanded_bytes", LIMIT)), options.get("format", "zip")))])
