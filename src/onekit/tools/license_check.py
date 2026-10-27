# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Local, evidence-first inspection. Never determines ownership or permission."""
from __future__ import annotations

import hashlib
import io
import json
import re
import stat
import tarfile
import tomllib
import zipfile
import zlib
from functools import lru_cache
from pathlib import PurePosixPath

from license_expression import ExpressionError

from ..models import Artifact, OneKitError, Result, parse_json

DISCLAIMER = (
    "This is an estimate from unverified declarations, metadata and limited text recognition. "
    "It is not a copyright certificate, a determination of ownership, legal advice or permission to use the work. "
    "Verify the original source, license scope and rights holder before use. "
    "Missing metadata never means public domain or free to use. An author is not necessarily the copyright owner."
)
REFERENCES = [
    {"name": "SPDX license identifiers and expressions", "url": "https://spdx.org/licenses/"},
    {"name": "REUSE licensing declarations", "url": "https://reuse.software/spec/"},
    {"name": "IPTC photo rights metadata", "url": "https://iptc.org/std/photometadata/documentation/userguide/"},
    {"name": "Creative Commons licenses", "url": "https://creativecommons.org/share-your-work/cclicenses/"},
    {"name": "OpenType name records (copyright and licensing)", "url": "https://learn.microsoft.com/en-us/typography/opentype/spec/name"},
    {"name": "EPUB package metadata", "url": "https://www.w3.org/TR/epub-33/#sec-opf-dcmes-optional"},
]
MAX_ENTRY = 2 * 1024 * 1024
TEXT_TOTAL = 8 * 1024 * 1024
RIGHTS = {"license", "licence", "licensedeclared", "licenseconcluded", "licenseexpression", "spdxlicenseidentifier", "licenses", "usageterms", "rights", "rightsusage", "rightsstatement", "webstatement", "licensorurl"}
COPYRIGHT = {"copyright", "copyrightnotice", "copyrightowner", "copyrightownername", "filecopyrighttext", "spdxfilecopyrighttext"}
CREATOR = {"creator", "author", "artist", "byline", "authors", "creators", "initialcreator"}


@lru_cache(maxsize=1)
def spdx_licensing():
    """Reuse the public SPDX symbol index, never file contents or reports."""
    from license_expression import get_spdx_licensing
    licensing = get_spdx_licensing()
    licensing.get_advanced_tokenizer()
    return licensing


def key(value):
    return re.sub(r"[^a-z]", "", str(value).split("}")[-1].split(":")[-1].lower())


def text_value(value):
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


class Inspection:
    def __init__(self, tool, files, options):
        self.licensing = spdx_licensing()
        self.files = files
        self.options = options
        self.scanned = 0
        self.text_bytes = 0
        self.seen = set()
        self.warnings = []
        self.records = {"declared_licenses": [], "estimated_license_matches": [], "copyright_notices": [], "declared_creators": [], "source_links": []}
        self.coverage = {"files_inspected": 0, "skipped": [], "complete": False,
                         "scope": "Embedded metadata, SPDX/REUSE declarations and bounded text; basic MIT, Apache-2.0 and BSD-3-Clause text patterns only; no reverse search, legal verification, dependency resolution or execution."}
        self.tool = tool

    def skip(self, location, reason):
        if len(self.coverage["skipped"]) < 100:
            self.coverage["skipped"].append({"location": str(location)[:300], "reason": reason})

    def add(self, category, value, location, method="declared metadata"):
        value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text_value(value)).strip()
        if not value or len(self.seen) >= 500:
            return
        value = value[:2000]
        identity = (category, value, location)
        if identity in self.seen:
            return
        self.seen.add(identity)
        record = {"value": value, "location": str(location)[:500], "method": method, "verified": False}
        if category in ("declared_licenses", "estimated_license_matches"):
            record.update({"spdx_expression": None, "spdx_syntax_valid": False, "license_ids": [], "official_license_links": []})
            expression = value
            match = re.search(r"https?://(?:www\.)?creativecommons\.org/(licenses/([a-z-]+)/([0-9.]+)|publicdomain/(zero|mark)/([0-9.]+))/?", value, re.IGNORECASE)
            if match:
                expression = ("CC-" + match[2].upper() + "-" + match[3]) if match[2] else "CC0-1.0" if match[4] == "zero" else ""
                record["official_license_links"].append(match[0])
            try:
                parsed = self.licensing.parse(expression, validate=True, strict=True)
                if parsed is not None:
                    identifiers = self.licensing.license_keys(parsed)
                    record.update(spdx_expression=str(parsed), spdx_syntax_valid=True, license_ids=identifiers)
                    record["official_license_links"].extend("https://spdx.org/licenses/" + identifier + ".html" for identifier in identifiers if not identifier.startswith("LicenseRef-"))
            except (ExpressionError, ValueError, TypeError):
                pass
            record["interpretation"] = "Tentative text-pattern match; verify against the full source license." if category == "estimated_license_matches" else "A declaration only. Valid SPDX syntax does not establish a valid grant or ownership."
        self.records[category].append(record)

    def field(self, name, value, location):
        field = key(name)
        if isinstance(value, (list, tuple)):
            for part in value[:40]:
                self.field(name, part, location)
            return
        if isinstance(value, dict):
            for child, part in list(value.items())[:40]:
                self.field(name if field in RIGHTS | COPYRIGHT | CREATOR else child, part, location + "/" + str(child))
            return
        if value is None or not isinstance(value, (str, bytes, int, float)):
            return
        if field in CREATOR:
            self.add("declared_creators", value, location)
        elif field in COPYRIGHT or "copyright" in field:
            self.add("copyright_notices", value, location)
        elif field in RIGHTS or field.endswith(("license", "licence")):
            self.add("declared_licenses", value, location)
        if field in RIGHTS | COPYRIGHT and isinstance(value, str):
            for url in re.findall(r"https?://[^\s<>\"']{1,1000}", value)[:8]:
                self.add("source_links", url.rstrip(".,);"), location, "URL declared in rights metadata; not opened")

    def scan_text(self, text, location, *, license_document=False):
        if not isinstance(text, str):
            return
        amount = len(text.encode("utf-8"))
        if amount > MAX_ENTRY or self.text_bytes + amount > TEXT_TOTAL:
            self.skip(location, "Text inspection limit reached (2 MiB per entry, 8 MiB total).")
            return
        self.text_bytes += amount
        text = re.sub(r"REUSE-IgnoreStart.*?REUSE-IgnoreEnd", "", text, flags=re.DOTALL)
        line, previous = 1, 0
        for match in re.finditer(r"(?im)^\s*(?:[#/*;!<\-]\s*)*SPDX-License-Identifier:\s*([^\r\n]+)", text):
            line += text.count('\n', previous, match.start())
            previous = match.start()
            self.add("declared_licenses", match[1].strip().removesuffix("*/").removesuffix("-->").strip(), location + f":line {line}", "SPDX declaration")
            if len(self.seen) >= 500:
                break
        for match in re.finditer(r"(?im)^\s*(?:[#/*;!<\-]\s*)*(?:SPDX-FileCopyrightText:|Copyright\b|©)\s*([^\r\n]{1,800})", text):
            self.add("copyright_notices", match.group(0).strip(), location, "Unverified copyright notice in text")
        for match in re.finditer(r"(?i)\blicen[sc]ed\s+under\s+(?:the\s+)?([a-z0-9][a-z0-9.+-]{1,70})(?:\s+licen[sc]e)?", text):
            value = match[1]
            try:
                self.licensing.parse(value, validate=True, strict=True)
            except (ExpressionError, ValueError, TypeError):
                continue
            self.add("declared_licenses", value, location, "Explicit licensing statement in text; scope unverified")
        for url in re.findall(r"https?://(?:www\.)?(?:creativecommons\.org/(?:licenses|publicdomain)/[^\s<>\"']+|spdx\.org/licenses/[^\s<>\"']+)", text, flags=re.IGNORECASE)[:20]:
            self.add("source_links", url.rstrip(".,);"), location, "License reference in text; not opened")
            if "creativecommons.org" in url:
                self.add("declared_licenses", url.rstrip(".,);"), location, "License URL reference; applicability unverified")
        if license_document:
            normalized = " ".join(text.lower().split())
            if all(phrase in normalized for phrase in ("permission is hereby granted", "without restriction", "the software is provided", "as is")):
                self.add("estimated_license_matches", "MIT", location, "Heuristic text-pattern recognition; not a full SPDX text match")
            if "apache license" in normalized and "version 2.0" in normalized and "limitations under the license" in normalized:
                self.add("estimated_license_matches", "Apache-2.0", location, "Heuristic text-pattern recognition")
            if "redistribution and use in source and binary forms" in normalized and "neither the name" in normalized and "this software is provided" in normalized:
                self.add("estimated_license_matches", "BSD-3-Clause", location, "Heuristic text-pattern recognition")
            if "all rights reserved" in normalized:
                self.add("copyright_notices", "All rights reserved", location, "Restriction notice; not a complete license")

    def xml(self, data, location, *, body=False):
        from defusedxml import ElementTree
        if len(data) > MAX_ENTRY:
            self.skip(location, "XML entry exceeds 2 MiB.")
            return
        root = ElementTree.fromstring(data)
        pending = [(root, "")]
        nodes = 0
        fragments = []
        while pending:
            node, context = pending.pop()
            nodes += 1
            if nodes > 40000:
                self.skip(location, "XML node limit reached.")
                break
            label = key(node.attrib.get("name", node.tag))
            scope = label if label in RIGHTS | COPYRIGHT | CREATOR or "copyright" in label else context
            if node.text and node.text.strip():
                if scope:
                    self.field(scope, node.text, location + "/" + str(node.tag).split("}")[-1])
                if body:
                    fragments.append(node.text.strip())
            for attr, value in node.attrib.items():
                if key(attr) in RIGHTS | COPYRIGHT | CREATOR:
                    self.field(attr, value, location + "/@" + str(attr).split("}")[-1])
                elif scope and key(attr) in ("resource", "href"):
                    self.field(scope, value, location + "/@" + key(attr))
            pending.extend((child, scope) for child in reversed(list(node)))
        if body:
            self.scan_text("\n".join(fragments), location)

    def structured(self, value, location):
        pending = [(value, location, 0)]
        nodes = 0
        while pending:
            value, path, depth = pending.pop()
            nodes += 1
            if nodes > 12000 or depth > 20:
                self.skip(path, "Structured metadata inspection limit reached.")
                break
            if isinstance(value, dict):
                for name, part in value.items():
                    if key(name) in RIGHTS | COPYRIGHT | CREATOR:
                        self.field(name, part, path + "/" + str(name))
                    elif key(name) not in ("data", "rows", "records", "features") and isinstance(part, (dict, list)):
                        pending.append((part, path + "/" + str(name), depth + 1))
            elif isinstance(value, list):
                pending.extend((part, path + f"/{index}", depth + 1) for index, part in enumerate(value[:1000]) if isinstance(part, (dict, list)))

    def text_file(self, name, data):
        if len(data) > MAX_ENTRY:
            self.skip(name, "Text entry exceeds 2 MiB.")
            return
        try:
            text = data.decode("utf-16" if data.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")
        except UnicodeError:
            self.skip(name, "Not UTF-8/UTF-16 text; binary content was not scanned.")
            return
        base = PurePosixPath(name.rsplit("!", 1)[-1]).name.lower()
        # A source module such as license_check.py may contain the detector's
        # own reference phrases. Its name alone does not make it a license text.
        document_suffix = PurePosixPath(base).suffix in ("", ".txt", ".md", ".rst", ".html", ".htm", ".license")
        license_document = bool(document_suffix and (re.match(r"^(licen[sc]e|copying|copyright|notice)([._-]|$)", base) or base.endswith(".license")))
        if base.endswith(".csv"):
            text = "\n".join(line for line in text.splitlines()[:40] if line.lstrip().startswith("#"))
        if not base.endswith((".json", ".jsonld")):
            self.scan_text(text, name, license_document=license_document)
        if base.endswith((".json", ".jsonld")):
            try:
                value = parse_json(text)
                if self.tool.id == "license-dataset" and isinstance(value, list):
                    self.skip(name, "Dataset rows are not license metadata. Include a metadata object or sidecar.")
                else:
                    self.structured(value, name)
            except (ValueError, RecursionError):
                self.skip(name, "Could not read structured JSON metadata.")
        elif base.endswith(".toml"):
            try:
                self.structured(tomllib.loads(text), name)
            except ValueError:
                self.skip(name, "Could not read TOML metadata.")
        elif base.endswith(".csv"):
            # CSV cells and column names are data, not licensing evidence.
            self.skip(name, "CSV rows are not treated as a license. Include a LICENSE or metadata sidecar when available.")
        elif base in ("license", "licence", "copying") and len(text.strip()) < 100:
            self.field("license", text.strip(), name)

    def entries(self, file):
        limit = min(64 * 1024 * 1024, self.options.get("_max_expanded_bytes", 64 * 1024 * 1024))
        if zipfile.is_zipfile(io.BytesIO(file.data)):
            with zipfile.ZipFile(io.BytesIO(file.data)) as archive:
                infos = archive.infolist()
                if len(infos) > 2048 or sum(info.file_size for info in infos) > limit:
                    raise OneKitError("Archive exceeds 2048 entries or the expanded-byte limit. Upload a smaller project.")
                seen = set()
                from ..license_sources import candidate_rank
                for info in sorted(infos, key=lambda item: (candidate_rank(item.filename), item.filename)):
                    name = safe_entry(info.filename)
                    if name in seen:
                        raise OneKitError("Archive contains duplicate paths.")
                    seen.add(name)
                    if info.is_dir():
                        continue
                    if stat.S_ISLNK(info.external_attr >> 16):
                        self.skip(name, "Archive links are not followed.")
                        continue
                    if info.flag_bits & 1:
                        self.skip(name, "Encrypted archive entry.")
                        continue
                    if info.file_size > MAX_ENTRY:
                        self.skip(name, "Entry exceeds 2 MiB.")
                        continue
                    with archive.open(info) as stream:
                        data = stream.read(MAX_ENTRY + 1)
                    if len(data) > MAX_ENTRY:
                        raise OneKitError("Expanded archive entry exceeds its limit.")
                    yield name, data
            return
        data = file.data
        # Bound decompression before tarfile reads extended/PAX headers.
        if data.startswith(b"\x1f\x8b"):
            decoder = zlib.decompressobj(31)
            data = decoder.decompress(data, limit + 1)
        elif data.startswith(b"BZh"):
            import bz2
            decoder = bz2.BZ2Decompressor()
            data = decoder.decompress(data, max_length=limit + 1)
        elif data.startswith(b"\xfd7zXZ\x00"):
            import lzma
            decoder = lzma.LZMADecompressor(memlimit=128 * 1024 * 1024)
            data = decoder.decompress(data, max_length=limit + 1)
        else:
            decoder = None
        if len(data) > limit:
            raise OneKitError("Expanded TAR exceeds the local inspection limit.")
        if decoder is not None and (not decoder.eof or decoder.unused_data):
            raise OneKitError("Use one complete TAR stream, without concatenated compressed members.")
        try:
            archive = tarfile.open(fileobj=io.BytesIO(data), mode="r:")  # noqa: SIM115 - closed immediately below
        except tarfile.TarError as exc:
            raise OneKitError("Use a ZIP/TAR project archive or upload individual source files.") from exc
        with archive:
            total = 0
            for index, info in enumerate(archive):
                name = safe_entry(info.name)
                total += info.size
                if index >= 2048 or total > limit:
                    raise OneKitError("Archive exceeds 2048 entries or its expanded-byte limit.")
                if not info.isfile():
                    if not info.isdir():
                        self.skip(name, "Archive links and special files are not followed.")
                    continue
                if info.size > MAX_ENTRY:
                    self.skip(name, "Entry exceeds 2 MiB.")
                    continue
                with archive.extractfile(info) as stream:
                    data = stream.read(MAX_ENTRY + 1)
                if len(data) > MAX_ENTRY:
                    raise OneKitError("Expanded archive entry exceeds its limit.")
                yield name, data

    def office(self, file, kind):
        if file.data.startswith(b"\xd0\xcf\x11\xe0"):
            import olefile
            with olefile.OleFileIO(io.BytesIO(file.data)) as document:
                metadata = document.get_metadata()
                for name in ("author", "last_saved_by", "comments"):
                    value = getattr(metadata, name, None)
                    if value:
                        self.field("author" if name == "author" else "description", value, file.name + "/OLE/" + name)
                        self.scan_text(text_value(value), file.name + "/OLE/" + name)
            self.skip(file.name, "Legacy Office inspection covers OLE metadata only. Embedded document text and macros are not executed or scanned.")
            return
        if not zipfile.is_zipfile(io.BytesIO(file.data)):
            raise OneKitError("Expected an Office Open XML, EPUB or legacy Office file.")
        prefix = {"word": "word/", "powerpoint": "ppt/", "excel": "xl/"}.get(kind)
        matched = False
        epub_package = False
        for name, data in self.entries(file):
            if prefix and name.startswith(prefix):
                matched = True
            if name.endswith(".opf"):
                epub_package = True
            selected = name.startswith("docProps/") or name.endswith(".opf") or kind == "epub" and name.endswith((".xhtml", ".html")) or prefix and name.startswith(prefix) and name.endswith(".xml") and "/media/" not in name
            if selected and self.scanned < 160:
                self.scanned += 1
                try:
                    self.xml(data, file.name + "!" + name, body=True)
                except (ValueError, TypeError) as exc:
                    self.skip(name, "XML could not be inspected: " + str(exc)[:120])
            elif selected:
                self.skip(name, "Document-part inspection limit reached.")
        if prefix and not matched:
            raise OneKitError("The archive does not contain the selected Office document format.")
        if kind == "epub" and not epub_package:
            raise OneKitError("Expected an EPUB archive with package metadata (.opf).")

    def pdf(self, file):
        from pypdf import PdfReader, apply_configuration
        with apply_configuration(zlib_maximum_output_length=MAX_ENTRY, lzw_maximum_output_length=MAX_ENTRY,
                                 run_length_maximum_output_length=MAX_ENTRY, brotli_maximum_output_length=MAX_ENTRY,
                                 stream_decoding_work_maximum_length=8 * MAX_ENTRY, page_tree_maximum_entries=1000):
            reader = PdfReader(io.BytesIO(file.data), strict=False)
            if reader.is_encrypted and not reader.decrypt(""):
                raise OneKitError("Unlock this PDF before checking its license declarations.")
            for name, value in (reader.metadata or {}).items():
                # PDF /Creator identifies creating software, unlike XMP dc:creator.
                if name not in ("/Creator", "/Producer"):
                    self.field(name.lstrip("/"), value, file.name + "/metadata/" + name)
                if isinstance(value, str):
                    self.scan_text(value, file.name + "/metadata/" + name)
            metadata = reader.trailer["/Root"].get("/Metadata")
            if metadata:
                self.xml(metadata.get_object().get_data(), file.name + "/XMP")
            for index, page in enumerate(reader.pages):
                if index >= 5:
                    self.skip(file.name, "Only the first 5 PDF pages were inspected for text.")
                    break
                try:
                    self.scan_text(page.extract_text()[:MAX_ENTRY], file.name + f"/page {index+1}")
                except Exception as exc:  # noqa: BLE001 - report incomplete text extraction without certifying it
                    self.skip(file.name + f"/page {index+1}", "Text could not be inspected: " + str(exc)[:120])
        self.skip(file.name, "No OCR, signature validation or ownership verification was performed.")

    def image(self, file):
        if file.kind == "svg":
            self.xml(file.data, file.name, body=True)
            return
        from PIL import ExifTags, Image, IptcImagePlugin
        with Image.open(io.BytesIO(file.data)) as image:
            for name, value in image.info.items():
                if key(name) in ("xmp", "xmlxmp") and isinstance(value, (bytes, str)):
                    self.xml(value, file.name + "/XMP")
                else:
                    self.field(name, value, file.name + "/image metadata/" + name)
            for number, value in image.getexif().items():
                name = ExifTags.TAGS.get(number, str(number))
                if number == 700 and isinstance(value, bytes):
                    self.xml(value, file.name + "/EXIF XMP")
                else:
                    self.field(name, value, file.name + "/EXIF/" + name)
            iptc = IptcImagePlugin.getiptcinfo(image) or {}
            for identifier, name in {(2, 80): "author", (2, 116): "copyright", (2, 120): "rightsusage"}.items():
                if identifier in iptc:
                    if identifier == (2, 120):
                        self.scan_text(text_value(iptc[identifier]), file.name + "/IPTC caption")
                    else:
                        self.field(name, iptc[identifier], file.name + "/IPTC/" + name)
        self.skip(file.name, "Pixels, watermarks and Content Credentials signatures were not analyzed. Metadata can be missing or altered.")

    def font(self, file):
        from fontTools.ttLib import TTFont

        from .font_brotli import font_brotli
        if file.data.startswith((b"wOFF", b"wOF2")) and int.from_bytes(file.data[16:20], "big") > 32 * 1024 * 1024:
            raise OneKitError("Expanded webfont exceeds the 32 MiB metadata inspection limit.")
        with font_brotli(), TTFont(io.BytesIO(file.data), lazy=True) as font:
            if "name" not in font:
                return
            for entry in font["name"].names[:512]:
                if entry.nameID in (0, 8, 9, 13, 14):
                    name = {0: "copyright", 8: "manufacturer", 9: "author", 13: "license", 14: "license"}[entry.nameID]
                    self.field(name, entry.toUnicode(), file.name + f"/OpenType name ID {entry.nameID}")
        self.skip(file.name, "Font metadata is a declaration. Embedding, webfont and redistribution permissions require checking the full license.")

    def media(self, file):
        from .native import inspect_media
        metadata = inspect_media(file)
        streams = metadata.get("streams", [])
        if self.tool.id == "license-video" and not any(stream.get("codec_type") == "video" for stream in streams):
            raise OneKitError("Choose a file containing a video stream.")
        if self.tool.id == "license-audio" and not any(stream.get("codec_type") == "audio" for stream in streams):
            raise OneKitError("Choose a file containing an audio stream.")
        parts = [("container", metadata.get("format", {})), *((f"stream {index}", stream) for index, stream in enumerate(streams[:64]))]
        for location, part in parts:
            for name, value in part.get("tags", {}).items():
                self.field(name, value, file.name + "/" + location + "/" + name)
                if isinstance(value, str):
                    self.scan_text(value[:MAX_ENTRY], file.name + "/" + location + "/" + name)
        self.skip(file.name, "Only embedded tags were inspected. Audio, video frames, watermarks and music identification were not analyzed.")

    def inspect(self, file):
        kind = self.tool.id.removeprefix("license-")
        self.coverage["files_inspected"] += 1
        if kind == "pdf":
            self.pdf(file)
        elif kind in ("word", "powerpoint", "excel", "epub"):
            self.office(file, kind)
        elif kind == "image":
            self.image(file)
        elif kind == "font":
            self.font(file)
        elif kind in ("audio", "video"):
            self.media(file)
        elif kind == "code" and (zipfile.is_zipfile(io.BytesIO(file.data)) or file.name.lower().endswith((".tar", ".gz", ".tgz", ".bz2", ".xz"))):
            for name, data in self.entries(file):
                if self.scanned >= 256:
                    self.skip(name, "Only 256 archive files were inspected.")
                    continue
                self.scanned += 1
                if any(part in (".git", "node_modules", ".venv") for part in PurePosixPath(name).parts):
                    self.skip(name, "Dependency and VCS directories are not scanned.")
                    continue
                self.text_file(file.name + "!" + name, data)
        else:
            self.text_file(file.name, file.data)


def safe_entry(name):
    normalized = name.replace("\\", "/")
    if not normalized or normalized.startswith("/") or ":" in normalized or ".." in normalized.split("/") or any(ord(char) < 32 for char in normalized):
        raise OneKitError("Unsafe archive path; no files were extracted.")
    return normalized


def run(tool, files, options):
    inspection = Inspection(tool, files, options)
    for file in files:
        inspection.inspect(file)
    records = inspection.records
    found = bool(records["declared_licenses"] or records["copyright_notices"])
    if len(records["declared_licenses"]) > 1:
        inspection.warnings.append("Multiple declarations were found. They may cover different files or components; their scope requires manual checking.")
    source = options.get("_source", {})
    if not isinstance(source, dict):
        source = {}
    if source.get("coverage"):
        inspection.coverage["source_download"] = str(source["coverage"])[:1000]
    report = {
        "schema": "onekit-license-estimate/v1", "tool": tool.id,
        "status": "unverified-declarations-found" if found else "rights-undetermined",
        "is_estimate": True, "requires_manual_verification": True, "permission_to_use": "not-determined",
        "disclaimer": DISCLAIMER, "analysis": "local-only",
        "source": {name: str(source[name])[:2048] for name in ("url", "download_url", "coverage", "revision") if name in source},
        "files": [{"name": file.name, "bytes": len(file.data), "sha256": hashlib.sha256(file.data).hexdigest()} for file in files],
        **records, "coverage": inspection.coverage,
        "limitations": ["Metadata and text may be inaccurate, outdated, removed or forged.",
                        "No ownership, identity, license scope, permission, trademark, model/property release or rights in depicted works was verified.",
                        "A project license does not automatically cover all dependencies or assets. No dependencies were downloaded or executed.",
                        "Official references below explain standards; they do not validate this particular file."],
        "next_steps": ["Open the original source and confirm that the license applies to this exact file and version.",
                       "Read the complete terms and check attribution, commercial use, modifications and redistribution for your intended use.",
                       "Resolve missing or ambiguous information with the rights holder before use."],
        "tools_used": ["license-expression (SPDX syntax)", "defusedxml", {"pdf": "pypdf", "image": "Pillow / IPTC / XMP", "font": "fontTools", "audio": "FFprobe", "video": "FFprobe"}.get(tool.id.removeprefix("license-"), "Python standard-library container and text readers")],
        "official_references": REFERENCES,
    }
    warnings = [DISCLAIMER, *inspection.warnings]
    name = files[0].stem if len(files) == 1 else "project"
    return Result([Artifact(name + ".license-report.json", json.dumps(report, ensure_ascii=False, indent=2).encode())], warnings, report)
