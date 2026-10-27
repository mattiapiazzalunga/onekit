# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import codecs
import hashlib
import io
import json
import re
import zipfile

from ...models import OneKitError, Result, output

TEXT_CONTROLS = re.compile(r"[\x00-\x08\x0b\x0e-\x1f]")

SIGNATURES = [(b"%PDF-", "application/pdf"), (b"\x89PNG\r\n\x1a\n", "image/png"), (b"\xff\xd8\xff", "image/jpeg"), (b"GIF8", "image/gif"), (b"BM", "image/bmp"), (b"II\x2a\x00", "image/tiff"), (b"MM\x00\x2a", "image/tiff"), (b"\x00\x00\x01\x00", "image/ico"), (b"PK\x03\x04", "application/zip"), (b"\x1f\x8b", "application/gzip"), (b"7z\xbc\xaf\x27\x1c", "application/x-7z-compressed"), (b"OggS", "audio/ogg"), (b"fLaC", "audio/flac"), (b"wOFF", "font/woff"), (b"wOF2", "font/woff2")]


def inspect(file):
    data = file.data
    kind = next((mime for signature, mime in SIGNATURES if data.startswith(signature)), "application/octet-stream")
    if data.startswith(b"RIFF"):
        kind = {b"WEBP": "image/webp", b"WAVE": "audio/wav", b"AVI ": "video/x-msvideo"}.get(data[8:12], kind)
    elif data[4:8] == b"ftyp" and len(data) >= 12:
        brand = data[8:12]
        kind = "audio/mp4" if brand in (b"M4A ", b"M4B ") else "image/avif" if brand in (b"avif", b"avis") else "video/quicktime" if brand == b"qt  " else "video/mp4"
    elif data.startswith(b"\x00\x01\x00\x00"):
        kind = "font/ttf"
    elif data.startswith(b"OTTO"):
        kind = "font/otf"
    elif data.startswith(b"ID3"):
        kind = "audio/mpeg"
    details = {"name": file.name, "bytes": len(data), "mime": kind, "sha256": hashlib.sha256(data).hexdigest(), "sha512": hashlib.sha512(data).hexdigest(), "encoding": None, "structure": None, "errors": [], "metadata": {}}
    try:
        text = data.decode("utf-8-sig")
        if kind == "application/octet-stream" and not TEXT_CONTROLS.search(text):
            details["encoding"] = "UTF-8"
            details["mime"] = "text/plain"
        if file.kind in ("json", "ipynb"):
            value = json.loads(text)
            details["structure"] = {"type": type(value).__name__, "items": len(value) if isinstance(value, (dict, list)) else 1}
    except UnicodeDecodeError:
        if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
            details["encoding"] = "UTF-16"
            if kind == "application/octet-stream":
                details["mime"] = "text/plain"
    except ValueError as exc:
        details["errors"].append(str(exc))
    if zipfile.is_zipfile(io.BytesIO(data)):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            details["structure"] = {"entries": [{"name": info.filename, "bytes": info.file_size} for info in archive.infolist()[:1000]]}
            names = archive.namelist()
            for prefix, mime in (("word/", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"), ("xl/", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"), ("ppt/", "application/vnd.openxmlformats-officedocument.presentationml.presentation")):
                if any(name.startswith(prefix) for name in names):
                    details["mime"] = mime
    if data.startswith(b"%PDF-"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            details["metadata"] = {str(k): str(v) for k, v in (reader.metadata or {}).items()}
            details["structure"] = {"pages": len(reader.pages), "encrypted": reader.is_encrypted}
        except ImportError:
            details["errors"].append("Install the pdf extra to inspect PDF structure.")
        except Exception as exc:
            details["errors"].append(str(exc)[:300])
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        details["mime"] = "image/webp"
    if details["mime"].startswith("image/"):
        try:
            from PIL import Image, ExifTags
            image = Image.open(io.BytesIO(data))
            details["structure"] = {"width": image.width, "height": image.height, "mode": image.mode, "frames": getattr(image, "n_frames", 1)}
            details["metadata"] = {str(ExifTags.TAGS.get(key, key)): str(value)[:500] for key, value in image.getexif().items()}
        except ImportError:
            details["errors"].append("Install the images extra to inspect image metadata.")
        except Exception as exc:
            details["errors"].append(str(exc)[:300])
    return details


def run(tool, files, options):
    file = files[0]
    if tool.id == "file-count":
        text = file.text()
        result = {"characters": len(text), "words": len(text.split()), "lines": len(text.splitlines()), "bytes": len(file.data)}
    elif tool.id == "file-encoding-convert":
        encoding = options.get("encoding", "utf-8")
        source_encoding = options.get("source_encoding", "utf-8-sig")
        return Result([output(file, file.kind or "txt", file.data.decode(source_encoding).encode(encoding))])
    elif tool.id.startswith("file-metadata"):
        if file.kind in ("pdf", "jpeg", "png"):
            from ..file_metadata import run as metadata_run
            return metadata_run(tool, files, options)
        from ..native import process_file
        arguments = ["-all="] if tool.id.endswith("remove") else []
        metadata = options.get("metadata", {})
        if not tool.id.endswith("remove") and not isinstance(metadata, dict):
            raise OneKitError("metadata must be a JSON object of tag/value pairs.")
        for key, value in metadata.items():
            if not key.replace("_", "").isalnum():
                raise OneKitError("Metadata keys may contain only letters, numbers and underscores.")
            arguments.append(f"-{key}={value}")
        return process_file(file, "exiftool", ["-overwrite_original", *arguments], in_place=True)
    else:
        result = inspect(file)
    return Result([output(file, "json", json.dumps(result, indent=2, ensure_ascii=False))], details=result)
