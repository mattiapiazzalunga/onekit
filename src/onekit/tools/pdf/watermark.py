# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Add a translucent text watermark while retaining PDF text and graphics."""
import base64
import io
import math
import re

from ...models import Artifact, OneKitError, Result
from . import pages_option

FONTS = ("Helvetica", "Helvetica-Bold", "Times-Roman", "Courier")
POSITIONS = ("center", "top-left", "top-center", "top-right", "middle-left", "middle-right", "bottom-left", "bottom-center", "bottom-right")


def settings(options):
    kind = options.get("watermark_type", "text")
    if kind not in ("text", "image"):
        raise OneKitError("Choose a text or image watermark.")
    image = None
    if kind == "image":
        from PIL import Image
        from reportlab.lib.utils import ImageReader
        raw = options.get("image_base64", "")
        if not isinstance(raw, str) or not raw or len(raw) > 2796204:
            raise OneKitError("Choose a PNG or JPEG watermark up to 2 MiB.")
        try:
            decoded = base64.b64decode(raw, validate=True)
            if len(decoded) > 2*1024*1024:
                raise ValueError("Image too large")
            with Image.open(io.BytesIO(decoded)) as source:
                if source.format not in ("PNG", "JPEG") or source.width*source.height > 4000000:
                    raise ValueError("Unsupported watermark image")
                source.load()
                image = ImageReader(source.convert("RGBA"))
        except Exception as exc:
            raise OneKitError("Choose a valid PNG or JPEG watermark with at most 4 million pixels.") from exc
    text = options.get("text", "DRAFT") if kind == "text" else "DRAFT"
    if not isinstance(text, str):
        raise OneKitError("Watermark text must be a string.")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip() or len(text) > 200 or len(text.split("\n")) > 5:
        raise OneKitError("Enter 1–200 watermark characters, on at most 5 lines.")
    try:
        text.encode("cp1252")
    except UnicodeEncodeError as exc:
        raise OneKitError("Watermark fonts support Western European text and punctuation. Remove unsupported characters.") from exc
    if any((ord(char) < 32 and char != "\n") or 127 <= ord(char) <= 159 for char in text):
        raise OneKitError("Watermark text contains unsupported control characters.")
    font, position, layout = options.get("font", "Helvetica-Bold"), options.get("position", "center"), options.get("layout", "single")
    if font not in FONTS or position not in POSITIONS or layout not in ("single", "repeat"):
        raise OneKitError("Choose a supported watermark font, position and layout.")
    numbers = {}
    for name, default, low, high in (("font_size", 48, 8, 160), ("opacity", .25, .05, 1), ("angle", 45, -180, 180), ("margin", 24, 0, 144), ("image_width", 144, 24, 400)):
        raw = options.get(name, default)
        value = float(raw)
        if isinstance(raw, bool) or not math.isfinite(value) or not low <= value <= high:
            raise OneKitError(f"Watermark {name} must be between {low} and {high}.")
        numbers[name] = value
    color = options.get("color", "#666666")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise OneKitError("Watermark color must be a six-digit hexadecimal color.")
    return {"image": image, "text": text, "font": font, "position": position, "layout": layout, "color": color, **numbers}


def placements(width, height, config):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    lines = config["text"].split("\n")
    margin = config["margin"]
    usable_width, usable_height = width-2*margin, height-2*margin
    if usable_width <= 0 or usable_height <= 0:
        raise OneKitError("The watermark margin is too large for a selected page.")
    columns, rows = (3, 4) if config["layout"] == "repeat" else (1, 1)
    cell_width, cell_height = usable_width/columns, usable_height/rows
    radians = math.radians(config["angle"])
    cosine, sine = abs(math.cos(radians)), abs(math.sin(radians))
    size = config["font_size"]
    text_width = max(stringWidth(line, config["font"], size) for line in lines)
    text_height = size*1.2*len(lines)
    if config["image"]:
        image_width, image_height = config["image"].getSize()
        text_width = config["image_width"]
        text_height = text_width*image_height/image_width
    bound_width, bound_height = text_width*cosine+text_height*sine, text_width*sine+text_height*cosine
    fit = min(1, cell_width/max(bound_width, 1), cell_height/max(bound_height, 1))
    size *= fit
    if size < 6 and not config["image"]:
        raise OneKitError("Watermark text is too long to fit legibly. Shorten it or use the single layout.")
    if config["layout"] == "repeat":
        centers = [(margin+(column+.5)*cell_width, margin+(row+.5)*cell_height) for row in range(rows) for column in range(columns)]
    else:
        position = config["position"]
        x = margin+bound_width*fit/2 if position.endswith("left") else width-margin-bound_width*fit/2 if position.endswith("right") else width/2
        y = height-margin-bound_height*fit/2 if position.startswith("top") else margin+bound_height*fit/2 if position.startswith("bottom") else height/2
        centers = [(x, y)]
    return size, centers, lines


def run(tool, files, options):
    from pypdf import PdfReader, PdfWriter, Transformation
    from reportlab.lib.colors import HexColor
    from reportlab.pdfgen import canvas
    config = settings(options)
    reader = PdfReader(io.BytesIO(files[0].data))
    if reader.is_encrypted:
        raise OneKitError("Unlock the PDF before adding a watermark.")
    if not 1 <= len(reader.pages) <= 512:
        raise OneKitError("Watermark at most 512 PDF pages at a time.")
    page_value = options.get("pages")
    selected = sorted(set(pages_option(page_value if page_value else None, len(reader.pages))))
    writer = PdfWriter(clone_from=reader)
    for index in selected:
        page = writer.pages[index]
        crop = page.cropbox
        raw_width, raw_height = float(crop.width), float(crop.height)
        left, bottom = float(crop.left), float(crop.bottom)
        rotation = page.rotation % 360
        transforms = {0: (1, 0, 0, 1, left, bottom), 90: (0, 1, -1, 0, left+raw_width, bottom),
                      180: (-1, 0, 0, -1, left+raw_width, bottom+raw_height), 270: (0, -1, 1, 0, left, bottom+raw_height)}
        if rotation not in transforms:
            raise OneKitError("The PDF page has an unsupported rotation.")
        width, height = (raw_height, raw_width) if rotation in (90, 270) else (raw_width, raw_height)
        size, centers, lines = placements(width, height, config)
        stream = io.BytesIO()
        overlay = canvas.Canvas(stream, pagesize=(width, height))
        overlay.setFillColor(HexColor(config["color"]))
        overlay.setFillAlpha(config["opacity"])
        overlay.setFont(config["font"], size)
        for x, y in centers:
            overlay.saveState()
            overlay.translate(x, y)
            overlay.rotate(config["angle"])
            if config["image"]:
                original_width, original_height = config["image"].getSize()
                stamp_width = config["image_width"]*size/config["font_size"]
                stamp_height = stamp_width*original_height/original_width
                overlay.drawImage(config["image"], -stamp_width/2, -stamp_height/2, width=stamp_width, height=stamp_height, mask="auto")
            else:
                for number, line in enumerate(lines):
                    baseline = ((len(lines)-1)/2-number)*size*1.2-size*.35
                    overlay.drawCentredString(0, baseline, line)
            overlay.restoreState()
        overlay.save()
        stamp = PdfReader(io.BytesIO(stream.getvalue())).pages[0]
        page.merge_transformed_page(stamp, Transformation(transforms[rotation]), over=True)
    output = io.BytesIO()
    writer.write(output)
    fields = reader.get_fields() or {}
    warnings = ["Adding a watermark changes the PDF; existing digital signatures will no longer verify."] if any(field.get("/FT") == "/Sig" for field in fields.values()) else []
    return Result([Artifact("watermarked.pdf", output.getvalue())], warnings=warnings, details={"pages": len(reader.pages), "watermarkedPages": [index+1 for index in selected], "text": config["text"], "layout": config["layout"], "opacity": config["opacity"]})
