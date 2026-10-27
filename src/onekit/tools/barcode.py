# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Standard linear barcode generation and image reading, entirely local."""
import io
import json
import math
import re

from ..models import Artifact, OneKitError, Result

FORMATS = {"code128", "code39", "ean13", "ean8", "upca", "itf", "isbn13"}


def make_symbol(raw, kind):
    import barcode
    if kind not in FORMATS:
        raise OneKitError("Choose code128, code39, ean13, ean8, upca, itf or isbn13.")
    value = raw.rstrip("\r\n")
    if not value or len(value) > 80:
        raise OneKitError("Enter 1–80 characters for the barcode.")
    if kind == "code128" and (len(value) > 60 or not re.fullmatch(r"[\x20-\x7e]+", value)):
        raise OneKitError("Code 128 accepts 1–60 printable ASCII characters.")
    if kind == "code39" and (len(value) > 48 or not re.fullmatch(r"[A-Z0-9 .$/+%-]+", value)):
        raise OneKitError("Code 39 accepts 1–48 uppercase letters, digits, spaces and . $ / + % -.")
    digits = {"ean13": 12, "ean8": 7, "upca": 11, "isbn13": 12}
    if kind in digits:
        length = digits[kind]
        if not re.fullmatch(r"[0-9]+", value) or len(value) not in (length, length+1):
            raise OneKitError(f"{kind.upper()} requires {length} digits, or {length+1} with a valid check digit.")
        if kind == "isbn13" and not value.startswith(("978", "979")):
            raise OneKitError("ISBN-13 must start with 978 or 979.")
    if kind == "itf" and (not re.fullmatch(r"[0-9]+", value) or len(value) % 2):
        raise OneKitError("ITF requires an even number of digits, at most 80.")
    options = {"add_checksum": False} if kind == "code39" else {}
    symbol = barcode.get("ean13" if kind == "isbn13" else kind, value, options=options)
    full = symbol.get_fullcode()
    if kind in digits and len(value) == digits[kind]+1 and full != value:
        raise OneKitError(f"Invalid check digit: expected {full[-1]}. The supplied code was not changed.")
    return symbol, full


def numeric(options, name, default, low, high):
    value = float(options.get(name, default))
    if not math.isfinite(value) or not low <= value <= high:
        raise OneKitError(f"{name} must be between {low} and {high}.")
    return value


def run(tool, files, options):
    if tool.id in ("scan-barcode", "barcode-to-text"):
        from ..execution import current_context
        reader = current_context().symbol_reader
        if reader is not None:
            return decode_result(tool.id, reader(files[0], "linear"))
        from .symbols import input_image, read_native
        results = read_native(input_image(files[0], max_pixels=16000000), 'linear')
        codes = []
        for result in results:
            code = {"text": result.text, "format": str(result.format).replace(" ", "").replace("-", "").upper()}
            # UPC-A and a zero-prefixed EAN-13 have the same bars. Match common scanners.
            if code["format"] == "EAN13" and len(code["text"]) == 13 and code["text"].startswith("0"):
                code = {"text": code["text"][1:], "format": "UPCA"}
            if result.valid and code not in codes:
                codes.append(code)
        return decode_result(tool.id, codes)
    from barcode.writer import ImageWriter, SVGWriter
    kind, fmt = options.get("barcode_type", "code128"), options.get("format", "png")
    if fmt not in ("png", "jpeg", "svg"):
        raise OneKitError("Choose PNG, JPEG or SVG output.")
    symbol, payload = make_symbol(files[0].text(), kind)
    width = numeric(options, "module_width", .3, .2, 1)
    height = numeric(options, "height", 25, 10, 80)
    quiet = numeric(options, "quiet_zone", 6.5, max(2.5, 10*width), 30)
    dpi = numeric(options, "dpi", 300, 150, 600)
    font_size = numeric(options, "font_size", 10, 6, 24)
    show_text = options.get("show_text", True)
    if show_text not in (True, False, "true", "false"):
        raise OneKitError("show_text must be true or false.")
    writer = SVGWriter() if fmt == "svg" else ImageWriter()
    symbol.writer = writer
    settings = {"module_width": width, "module_height": height, "quiet_zone": quiet, "font_size": font_size,
                "write_text": show_text in (True, "true"), "dpi": int(dpi), "background": "white", "foreground": "black"}
    # Bound raster allocation before Pillow creates an image, including caption space.
    columns = max(len(row) for row in symbol.build())
    if ((columns*width+2*quiet)*dpi/25.4)*((height+30)*dpi/25.4) > 16000000:
        raise OneKitError("Output would exceed 16 million pixels. Reduce DPI, module width, height or content length.")
    stream = io.BytesIO()
    symbol.write(stream, settings)
    if fmt == "jpeg":
        from PIL import Image
        with Image.open(io.BytesIO(stream.getvalue())) as image:
            stream = io.BytesIO()
            image.convert("RGB").save(stream, format="JPEG", quality=95, subsampling=0, dpi=(int(dpi), int(dpi)))
    return Result([Artifact(f"barcode.{fmt}", stream.getvalue())], details={"payload": payload, "symbology": kind.upper(), "bytes": len(payload.encode()), "checkDigitAdded": payload != files[0].text().rstrip("\r\n")})


def decode_result(tool_id, readings):
    codes = []
    for reading in readings:
        format = str(reading['format']).replace(' ', '').replace('-', '').upper()
        format = {'CODE39STD': 'CODE39', 'CODE39EXT': 'CODE39', 'ITF14': 'ITF', 'ISBN': 'EAN13'}.get(format, format)
        code = {"text": reading["text"], "format": format}
        if code["format"] == "EAN13" and len(code["text"]) == 13 and code["text"].startswith("0"):
            code = {"text": code["text"][1:], "format": "UPCA"}
        if code not in codes:
            codes.append(code)
    if not codes:
        raise OneKitError("No readable barcode found. Use a sharp image with the complete bars and clear side margins.")
    report = {"count": len(codes), "codes": codes}
    content = "\n".join(code["text"] for code in codes) if tool_id == "barcode-to-text" else json.dumps(report, indent=2)
    return Result([Artifact("decoded.txt" if tool_id == "barcode-to-text" else "decoded.json", content.encode())], details=report)
