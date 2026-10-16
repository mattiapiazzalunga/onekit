# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
"""Bounded input contracts shared by CLI, Python callers and browser workers."""
import codecs
import io
import re
import struct
import warnings
import zipfile
from xml.etree import ElementTree

from .models import Artifact, OneKitError, parse_json

MAX_FILES = 256
MAX_BYTES = 128 * 1024 * 1024
BROWSER_BYTES = 32 * 1024 * 1024
MAX_PIXELS = 40_000_000
TEXT_CONTROLS = re.compile(r"[\x00-\x08\x0b\x0e-\x1f\x7f]")
TEXT_BYTES = bytes(value for value in range(256) if value not in (*range(9), 11, *range(14, 32), 127))


def check_batch(files, *, browser=False, output=False):
    limit = BROWSER_BYTES if browser else MAX_BYTES
    if not isinstance(files, (list, tuple)) or any(not isinstance(file, Artifact) or not isinstance(file.data, bytes) for file in files):
        raise OneKitError("Inputs must be a list of files containing byte data.")
    if len(files) > MAX_FILES or sum(len(file.data) for file in files) > limit:
        raise OneKitError(f"{'Output' if output else 'Input'} exceeds {MAX_FILES} files or {limit // 1024 // 1024} MiB.")


def validate_inputs(tool, files, options, *, browser=False):
    check_batch(files, browser=browser)
    if not files:
        raise OneKitError("Choose at least one input file.")
    if tool.max_files == 1 and len(files) != 1:
        raise OneKitError("This tool accepts one input file.")
    if not tool.min_files <= len(files) <= tool.max_files:
        raise OneKitError(f"{tool.name} requires {'exactly ' + str(tool.min_files) if tool.min_files == tool.max_files else str(tool.min_files) + '–' + str(tool.max_files)} input file(s).")
    total_limit = min(tool.max_total_bytes, tool.browser_max_total_bytes) if browser else tool.max_total_bytes
    file_limit = min(tool.max_file_bytes, tool.browser_max_file_bytes) if browser else tool.max_file_bytes
    if sum(len(file.data) for file in files) > total_limit:
        raise OneKitError(f"Inputs exceed this tool's total limit of {total_limit // 1024 // 1024} MiB.")
    for file in files:
        if len(file.data) > file_limit:
            raise OneKitError(f"'{file.name}' exceeds this tool's per-file limit of {file_limit:,} bytes.")
        if tool.accepts != ("*",) and file.kind not in tool.accepts:
            raise OneKitError(f"Expected file types: {', '.join(kind or '(extensionless text)' for kind in tool.accepts)}. Rejected '{file.name}'.")
        if tool.input_mode == "any":
            continue  # Inspection, metadata and encryption intentionally accept arbitrary bytes.
        if tool.input_mode in ("text", "encoded-text"):
            encoding = options.get("source_encoding", "utf-8-sig") if tool.input_mode == "encoded-text" else "utf-8-sig"
            text = file.text() if tool.input_mode == "text" else file.data.decode(encoding)
            # UTF-8 continuation bytes cannot hide ASCII controls. A C byte-table
            # scan avoids an expensive regex pass while retaining full UTF-8 decoding.
            utf8 = codecs.lookup(encoding).name in ("utf-8", "utf-8-sig")
            controls = bool(file.data.translate(None, TEXT_BYTES)) if utf8 else bool(TEXT_CONTROLS.search(text))
            if controls or binary_signature(file.data):
                raise OneKitError(f"'{file.name}' contains binary data; this tool requires text.")
            if tool.id == "diff-notebook":
                notebook = parse_json(text)
                if not isinstance(notebook, dict) or not isinstance(notebook.get("cells"), list):
                    raise OneKitError("Expected a Jupyter notebook with a cells array.")
            continue
        validate_binary(file, tool, total_limit)


def binary_signature(data):
    return bool(re.match(rb"%PDF-[12]\.\d(?:\s|%)", data[:16])) or data.startswith((b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff", b"PK\x03\x04", b"\x1f\x8b", b"ONEKIT\x01", b"\x1aE\xdf\xa3"))


def validate_binary(file, tool, expanded_limit):
    data, kind = file.data, file.kind
    if not data:
        raise OneKitError(f"'{file.name}' is empty; provide a valid {kind.upper()} file.")
    if tool.group in ("audio", "video"):
        validate_media_header(data, kind)
        return
    if kind == "pdf":
        if not re.match(rb"%PDF-[12]\.\d(?:\s|%)", data[:16]):
            raise OneKitError(f"'{file.name}' is not a PDF: its content does not match its extension.")
        if tool.id != "pdf-repair":
            matches = list(re.finditer(rb"startxref\s+(\d+)\s+%%EOF", data[-65536:]))
            if not matches:
                raise OneKitError("The PDF is incomplete or invalid. Use PDF repair for damaged PDFs.")
            offset = int(matches[-1][1])
            if offset >= len(data) or not re.match(rb"(?:xref\b|\d+\s+\d+\s+obj\b)", data[offset:offset+64]):
                raise OneKitError("Invalid PDF cross-reference structure. Use PDF repair for damaged PDFs.")
    elif kind in ("png", "jpeg", "webp", "gif", "bmp", "tiff", "ico"):
        from PIL import Image
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data)) as image:
                actual = {"jpg": "jpeg", "tif": "tiff"}.get(image.format.lower(), image.format.lower())
                if actual != kind:
                    raise OneKitError(f"'{file.name}' contains {actual.upper()} data, not {kind.upper()}.")
                if image.width * image.height * getattr(image, "n_frames", 1) > MAX_PIXELS:
                    raise OneKitError("Decoded images must contain at most 40 million pixels in total.")
                image.verify()
            if tool.id == "image-to-base64":
                with Image.open(io.BytesIO(data)) as image:
                    image.load()
    elif kind in ("docx", "pptx", "xlsx", "zip"):
        validate_zip(data, expanded_limit, kind)
    elif kind in ("ttf", "otf", "woff", "woff2"):
        expected = {"ttf": (b"\x00\x01\x00\x00", b"true"), "otf": (b"OTTO",), "woff": (b"wOFF",), "woff2": (b"wOF2",)}[kind]
        minimum = {"ttf": 12, "otf": 12, "woff": 44, "woff2": 48}[kind]
        if len(data) < minimum or not data.startswith(expected):
            raise OneKitError(f"'{file.name}' does not contain a valid {kind.upper()} font header.")
        if kind.startswith("woff"):
            length, tables = struct.unpack_from(">IH", data, 8)
            expanded = int.from_bytes(data[16:20], "big")
            if length != len(data) or not 0 < tables <= 4096 or expanded < 12 + 16 * tables or expanded > tool.max_file_bytes:
                raise OneKitError("The compressed font header has invalid size or table counts.")
        else:
            tables = int.from_bytes(data[4:6], "big")
            if not tables or 12 + 16 * tables > len(data):
                raise OneKitError("The font table directory is invalid.")
            for index in range(tables):
                offset, length = struct.unpack_from(">II", data, 12 + 16 * index + 8)
                if offset + length > len(data):
                    raise OneKitError("A font table extends beyond the input file.")
    elif kind == "onekit":
        if len(data) < 51 or not data.startswith(b"ONEKIT\x01"):
            raise OneKitError("This is not a supported OneKit encrypted archive.")
    elif kind in ("tar", "gz", "bz2", "xz"):
        import tarfile
        signatures = {"gz": b"\x1f\x8b", "bz2": b"BZh", "xz": b"\xfd7zXZ\x00"}
        if kind in signatures and not data.startswith(signatures[kind]):
            raise OneKitError(f"'{file.name}' does not match its archive extension.")
        if kind == "tar":
            if len(data) < 512:
                raise OneKitError("The TAR header is incomplete.")
            if data[:512] != b"\0" * 512:
                tarfile.TarInfo.frombuf(data[:512], encoding="utf-8", errors="strict")
    else:
        raise OneKitError(f"No input validator is registered for {kind!r}.")


def validate_zip(data, limit, kind="zip"):
    if not data.startswith((b"PK\x03\x04", b"PK\x05\x06")):
        raise OneKitError("The file does not contain a ZIP/Office container.")
    end = data.rfind(b"PK\x05\x06", max(0, len(data) - 65557))
    if end < 0 or end + 22 > len(data):
        raise OneKitError("The ZIP directory is missing or truncated.")
    _, disk, directory_disk, disk_count, count, size, offset, comment = struct.unpack_from("<4s4H2LH", data, end)
    if disk or directory_disk or disk_count != count or count > 4096 or offset + size != end or end + 22 + comment != len(data):
        raise OneKitError("Invalid, oversized, multi-volume or ZIP64 archive directory.")
    cursor, total, actual_count = offset, 0, 0
    # Inspect directory records before ZipFile allocates its complete entry table.
    while cursor < end:
        if actual_count >= 4096 or cursor + 46 > end or data[cursor:cursor+4] != b"PK\x01\x02":
            raise OneKitError("Invalid or oversized ZIP directory.")
        compressed, expanded = struct.unpack_from("<II", data, cursor + 20)
        lengths = struct.unpack_from("<3H", data, cursor + 28)
        total += expanded
        if total > limit or expanded > max(compressed, 1) * 1000:
            raise OneKitError("Archive expansion exceeds safety limits.")
        cursor += 46 + sum(lengths)
        actual_count += 1
    if cursor != end or actual_count != count:
        raise OneKitError("The ZIP directory entry counts or lengths do not match.")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        if len(entries) > 4096:
            raise OneKitError("Archive contains more than 4096 entries.")
        total, names = 0, set()
        for entry in entries:
            name = entry.filename.replace("\\", "/")
            if name in names or name.startswith("/") or ".." in name.split("/") or ":" in name or entry.flag_bits & 1 or entry.external_attr >> 16 & 0o170000 == 0o120000:
                raise OneKitError("Archive contains an unsafe path, duplicate, encrypted or linked entries.")
            names.add(name)
            total += entry.file_size
            if total > limit or entry.file_size > max(entry.compress_size, 1) * 1000:
                raise OneKitError("Archive expansion exceeds safety limits.")
        if kind == "zip":
            return
        root, tag = {"docx": ("word/document.xml", "document"), "xlsx": ("xl/workbook.xml", "workbook"), "pptx": ("ppt/presentation.xml", "presentation")}[kind]
        family = {"docx": "wordprocessingml", "xlsx": "spreadsheetml", "pptx": "presentationml"}[kind]
        if not {"[Content_Types].xml", "_rels/.rels", root} <= names:
            raise OneKitError(f"The ZIP container is not a {kind.upper()} document.")
        for path, expected in (("[Content_Types].xml", "Types"), ("_rels/.rels", "Relationships"), (root, tag)):
            with archive.open(path) as stream:
                parser = ElementTree.XMLPullParser(events=("start",))
                prefix = stream.read(65536)
                if b"<!DOCTYPE" in prefix.upper() or b"<!ENTITY" in prefix.upper():
                    raise OneKitError("Office XML cannot contain DTD or entity declarations.")
                parser.feed(prefix)
                element = next(parser.read_events(), (None, None))[1]
                namespaces = (f"http://schemas.openxmlformats.org/{family}/2006/main", f"http://purl.oclc.org/ooxml/{family}/main") if path == root else ("http://schemas.openxmlformats.org/package/2006/content-types" if expected == "Types" else "http://schemas.openxmlformats.org/package/2006/relationships",)
                if element is None or element.tag not in {"{" + namespace + "}" + expected for namespace in namespaces}:
                    raise OneKitError(f"Invalid {kind.upper()} document structure.")


def validate_media_header(data, kind):
    checks = {
        "gif": data.startswith((b"GIF87a", b"GIF89a")),
        "wav": data.startswith(b"RIFF") and data[8:12] == b"WAVE",
        "avi": data.startswith(b"RIFF") and data[8:12] == b"AVI ",
        "mp3": data.startswith(b"ID3") or len(data) > 2 and data[0] == 255 and data[1] & 0xE0 == 0xE0,
        "aac": len(data) > 2 and data[0] == 255 and data[1] & 0xF6 == 0xF0,
        "flac": data.startswith(b"fLaC"), "ogg": data.startswith(b"OggS"), "ogv": data.startswith(b"OggS"), "opus": data.startswith(b"OggS"),
        "webm": data.startswith(b"\x1aE\xdf\xa3"), "mkv": data.startswith(b"\x1aE\xdf\xa3"),
        "aif": data.startswith(b"FORM") and data[8:12] in (b"AIFF", b"AIFC"), "aiff": data.startswith(b"FORM") and data[8:12] in (b"AIFF", b"AIFC"),
        "wma": data.startswith(bytes.fromhex("3026b2758e66cf11a6d900aa0062ce6c")),
        "mpeg": data.startswith((b"\x00\x00\x01\xba", b"\x00\x00\x01\xb3")), "mpg": data.startswith((b"\x00\x00\x01\xba", b"\x00\x00\x01\xb3")),
        "ts": len(data) > 188 and data[0] == 0x47 and data[188] == 0x47,
    }
    valid = data[4:8] == b"ftyp" if kind in ("mp4", "m4a", "m4v") else data[4:8] in (b"ftyp", b"moov", b"mdat", b"wide", b"free") if kind == "mov" else checks.get(kind, False)
    if not valid:
        raise OneKitError(f"The file content does not match the {kind.upper()} media format.")
