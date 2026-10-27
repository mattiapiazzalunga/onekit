# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Portable metadata editing without recompressing JPEG/PNG image data."""
import io
import struct
import zlib

from ..models import OneKitError, Result, output

FIELDS = {"title": "Title", "author": "Author", "subject": "Subject", "keywords": "Keywords", "comment": "Comment"}


def _xmp_fields(data):
    from xml.etree import ElementTree
    if not data:
        return {}
    if len(data) > 1024 * 1024:
        raise OneKitError('XMP metadata exceeds the text limit.')
    text = data.decode('utf-8-sig') if isinstance(data, bytes) else data
    if '<!doctype' in text.lower() or '<!entity' in text.lower():
        raise OneKitError('XMP document declarations are unsupported.')
    root = ElementTree.fromstring(text)
    dc, rdf = '{http://purl.org/dc/elements/1.1/}', '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
    result = {}
    for name, tag in {'Title': 'title', 'Author': 'creator', 'Subject': 'description', 'Keywords': 'subject'}.items():
        element = root.find('.//' + dc + tag)
        if element is None:
            continue
        items = element.findall('.//' + rdf + 'li')
        if name in ('Title', 'Subject'):
            items = [next((item for item in items if item.get('{http://www.w3.org/XML/1998/namespace}lang') == 'x-default'), items[0])] if items else []
        value = '; '.join(''.join(item.itertext()) for item in items) if items else (element.text or '')
        if value:
            result[name] = value
    keyword = '{http://ns.adobe.com/pdf/1.3/}Keywords'
    element = root.find('.//' + keyword)
    value = element.text if element is not None else next((node.get(keyword) for node in root.iter() if node.get(keyword)), None)
    if value is not None:
        result['Keywords'] = value
    return result


def _exif_fields(exif):
    result = {}
    for name, tag in {"Title": 40091, "Comment": 40092, "Author": 40093, "Keywords": 40094, "Subject": 40095}.items():
        value = exif.get(tag)
        if isinstance(value, (bytes, tuple, list)):
            value = bytes(value).decode('utf-16-le', errors='replace').rstrip('\0')
        if isinstance(value, str):
            result[name] = value
    for name, tag in {'Title': 270, 'Author': 315}.items():
        value = exif.get(tag)
        if name not in result and isinstance(value, str):
            result[name] = value.rstrip('\0')
    return result


def _pdf_fields(reader):
    from xml.etree.ElementTree import ParseError
    from xml.parsers.expat import ExpatError

    from pypdf.errors import PdfReadError
    if reader.is_encrypted:
        raise OneKitError('Unlock the PDF before reading its metadata.')
    info = reader.metadata or {}
    result = {name: str(info['/' + name]) for name in FIELDS.values() if info.get('/' + name) is not None}
    try:
        xmp = reader.xmp_metadata
        if xmp:
            def localized(value):
                return value.get('x-default', next(iter(value.values()), '')) if value else ''
            fallback = {'Title': localized(xmp.dc_title), 'Author': '; '.join(xmp.dc_creator or []),
                        'Subject': localized(xmp.dc_description), 'Keywords': xmp.pdf_keywords or '; '.join(xmp.dc_subject or [])}
            for name, value in fallback.items():
                if name not in result and value:
                    result[name] = value
    except (ValueError, PdfReadError, ParseError, ExpatError):
        # Malformed optional XMP must not block readable document-info fields.
        return result
    return result


def read_metadata(file):
    """Read editable descriptive fields without changing the input artifact."""
    from ..validation import check_batch
    check_batch([file])
    if file.kind == 'pdf':
        from pypdf import PdfReader
        return _pdf_fields(PdfReader(io.BytesIO(file.data)))
    if file.kind == 'png':
        result, exif_fields, xmp_fields = {}, {}, {}
        text_bytes = 0
        for kind, payload, _ in _png_chunks(file.data):
            if kind == b'eXIf':
                from PIL import Image
                exif = Image.Exif()
                exif.load(b'Exif\0\0' + payload)
                exif_fields = _exif_fields(exif)
            if kind not in (b'tEXt', b'zTXt', b'iTXt'):
                continue
            keyword, _, body = payload.partition(b'\0')
            key = keyword.decode('latin-1').lower()
            name = FIELDS.get(key) or ('Subject' if key == 'description' else None)
            if name is None and key != 'xml:com.adobe.xmp':
                continue
            compressed = False
            if kind == b'zTXt':
                if not body or body[0] != 0:
                    raise OneKitError('Unsupported PNG text compression.')
                body, compressed = body[1:], True
            elif kind == b'iTXt':
                if len(body) < 2 or body[0] not in (0, 1) or body[1] != 0:
                    raise OneKitError('Invalid PNG international text.')
                compressed = bool(body[0])
                parts = body[2:].split(b'\0', 2)
                if len(parts) != 3:
                    raise OneKitError('Invalid PNG international text.')
                body = parts[2]
            if compressed:
                decoder = zlib.decompressobj()
                body = decoder.decompress(body, 1024 * 1024 + 1)
                if len(body) > 1024 * 1024 or not decoder.eof:
                    raise OneKitError('PNG metadata exceeds the text limit or is truncated.')
            if len(body) > 1024 * 1024:
                raise OneKitError('PNG metadata exceeds the text limit.')
            text_bytes += len(body)
            if text_bytes > 8 * 1024 * 1024:
                raise OneKitError('PNG metadata exceeds the total text limit.')
            value = body.decode('utf-8' if kind == b'iTXt' else 'latin-1')
            if key == 'xml:com.adobe.xmp':
                xmp_fields = _xmp_fields(value)
            elif name not in result or key == name.lower():
                result[name] = value
        return {**xmp_fields, **exif_fields, **result}
    if file.kind == 'jpeg':
        from PIL import Image
        with Image.open(io.BytesIO(file.data)) as image:
            result = {**_xmp_fields(image.info.get('xmp')), **_exif_fields(image.getexif())}
            if 'Comment' not in result and image.info.get('comment'):
                result['Comment'] = image.info['comment'].decode('utf-8', errors='replace')
            return result
    raise OneKitError('Metadata reading supports PDF, JPEG and PNG.')


def values(options):
    metadata = options.get("metadata", {})
    if not isinstance(metadata, dict) or not metadata or len(metadata) > 32:
        raise OneKitError("Provide a metadata object with 1–32 text fields.")
    result = {}
    for key, value in metadata.items():
        name = str(key).lstrip("/")
        if name.lower() not in FIELDS or not isinstance(value, str) or len(value) > 4000 or "\0" in value:
            raise OneKitError("Supported text fields: Title, Author, Subject, Keywords, Comment (up to 4000 characters each).")
        result[FIELDS[name.lower()]] = value
    return result


def _png_chunks(data):
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise OneKitError("Invalid PNG signature.")
    offset = 8
    while offset < len(data):
        if offset + 12 > len(data):
            raise OneKitError("Truncated PNG chunk.")
        size = struct.unpack_from(">I", data, offset)[0]
        end = offset + size + 12
        if end > len(data):
            raise OneKitError("Truncated PNG chunk.")
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:end - 4]
        if zlib.crc32(kind + payload) != struct.unpack_from(">I", data, end - 4)[0]:
            raise OneKitError("Invalid PNG chunk checksum.")
        yield kind, payload, data[offset:end]
        offset = end
        if kind == b'IEND':
            return
    raise OneKitError('PNG has no end chunk.')


def png(data, metadata, remove):
    result = bytearray(data[:8])
    replaced_keys = {key.lower() for key in metadata}
    for kind, payload, original in _png_chunks(data):
        key = payload.split(b"\0", 1)[0].decode("latin-1") if kind in (b"tEXt", b"zTXt", b"iTXt") else ""
        discard = kind in (b"tEXt", b"zTXt", b"iTXt") and (remove or key.lower() in replaced_keys)
        discard |= remove and kind in (b"eXIf", b"tIME")
        if kind == b"IEND":
            for name, value in metadata.items():
                body = name.encode("ascii") + b"\0\0\0\0\0" + value.encode("utf-8")
                chunk = b"iTXt" + body
                result.extend(struct.pack(">I", len(body)) + chunk + struct.pack(">I", zlib.crc32(chunk)))
        if not discard:
            result.extend(original)
    return bytes(result)


def jpeg(data, metadata, remove):
    from PIL import Image
    if not data.startswith(b"\xff\xd8"):
        raise OneKitError("Invalid JPEG signature.")
    with Image.open(io.BytesIO(data)) as image:
        exif = image.getexif()
    tags = {"Title": 40091, "Comment": 40092, "Author": 40093, "Keywords": 40094, "Subject": 40095}
    for name, value in metadata.items():
        exif[tags[name]] = (value + "\0").encode("utf-16-le")
    result = bytearray(data[:2])
    if not remove:
        payload = exif.tobytes()
        if len(payload) > 65533:
            raise OneKitError("JPEG EXIF exceeds the segment size limit.")
        result.extend(b"\xff\xe1" + struct.pack(">H", len(payload) + 2) + payload)
    offset = 2
    while offset < len(data):
        start = offset
        if data[offset] != 255:
            raise OneKitError("Invalid JPEG marker.")
        while offset < len(data) and data[offset] == 255:
            offset += 1
        if offset >= len(data):
            raise OneKitError("Truncated JPEG marker.")
        marker = data[offset]
        offset += 1
        if marker == 0xD9:
            result.extend(data[start:offset])
            return bytes(result)
        if offset + 2 > len(data):
            raise OneKitError("Truncated JPEG segment.")
        size = struct.unpack_from(">H", data, offset)[0]
        if size < 2 or offset + size > len(data):
            raise OneKitError("Invalid JPEG segment size.")
        payload = data[offset + 2:offset + size]
        discard = marker == 0xE1 and (remove or payload.startswith(b"Exif\0\0"))
        discard |= remove and marker in (0xED, 0xFE)
        if not discard:
            result.extend(data[start:offset + size])
        offset += size
        if marker == 0xDA:
            # Entropy data can contain escaped FF bytes and restart markers.
            # Keep it verbatim, then inspect further segments in progressive JPEGs.
            scan = offset
            while True:
                boundary = data.find(b"\xff", scan)
                if boundary < 0:
                    raise OneKitError("JPEG has no end marker.")
                following = boundary + 1
                while following < len(data) and data[following] == 255:
                    following += 1
                if following >= len(data):
                    raise OneKitError("Truncated JPEG scan.")
                if data[following] == 0 or 0xD0 <= data[following] <= 0xD7:
                    scan = following + 1
                    continue
                result.extend(data[offset:boundary])
                offset = boundary
                break
    raise OneKitError("JPEG has no end marker.")


def run(tool, files, options):
    file = files[0]
    remove = tool.id.endswith("remove")
    metadata = {} if remove else values(options)
    warnings = ["Edits descriptive metadata only. Visible content and embedded files are not anonymized. Keep the original and inspect the downloaded result."]
    if file.kind == "pdf":
        from pypdf import PdfReader, PdfWriter

        from .pdf import save
        reader = PdfReader(io.BytesIO(file.data))
        writer = PdfWriter(clone_from=reader)
        if remove:
            writer.metadata = None
            writer.root_object.pop("/Metadata", None)
            for page in writer.pages:
                page.pop("/Metadata", None)
        else:
            writer.add_metadata({"/" + key: value for key, value in {**_pdf_fields(reader), **metadata}.items()})
            # Avoid conflicting old XMP values after editing document information.
            writer.root_object.pop("/Metadata", None)
        writer.compress_identical_objects(remove_duplicates=False, remove_unreferenced=True)
        data = save(writer)
        warnings.append("Rewriting a signed PDF invalidates its digital signatures. Attachments and embedded image metadata are retained.")
    elif file.kind == "png":
        data = png(file.data, metadata, remove)
        warnings.append("PNG pixels, animation and color profiles are preserved. Removal clears text, EXIF and modification-time chunks.")
    elif file.kind == "jpeg":
        data = jpeg(file.data, metadata, remove)
        warnings.append("JPEG compressed pixels and color profiles are preserved. Removal clears EXIF, XMP, IPTC and comments; removing EXIF orientation may change display rotation.")
    else:
        raise OneKitError("Portable metadata editing supports PDF, JPEG and PNG.")
    return Result([output(file, file.kind, data)], warnings)
