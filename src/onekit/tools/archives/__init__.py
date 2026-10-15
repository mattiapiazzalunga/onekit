# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
import io
import tarfile
import zipfile
from pathlib import PurePosixPath

from ...models import Artifact, OneKitError, Result, output

LIMIT = 128 * 1024 * 1024


def safe_name(name):
    path = PurePosixPath(name.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts or ":" in name:
        raise OneKitError("Archive contains an unsafe path.")
    return str(path)


def unpack(data):
    files, total = [], 0
    if zipfile.is_zipfile(io.BytesIO(data)):
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
                if total > LIMIT or entry.file_size > max(entry.compress_size, 1) * 1000:
                    raise OneKitError("Archive expansion exceeds safety limits.")
                files.append(Artifact(name, archive.read(entry)))
    else:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as archive:
            for index, entry in enumerate(archive):
                name = safe_name(entry.name)
                if entry.isdir():
                    continue
                if not entry.isfile():
                    raise OneKitError("Archive links and devices are not supported.")
                total += entry.size
                if total > LIMIT or index > 4096:
                    raise OneKitError("Archive expansion exceeds safety limits.")
                stream = archive.extractfile(entry)
                files.append(Artifact(name, stream.read(LIMIT + 1)))
    return files


def pack(files, format="zip"):
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
    return Result([output(files[0], options.get("format", "zip"), pack(unpack(files[0].data), options.get("format", "zip")))])
