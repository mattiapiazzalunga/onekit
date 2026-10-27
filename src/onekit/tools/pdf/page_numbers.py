# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Number visible PDF pages while retaining document contents."""
import io
import re

from ...models import OneKitError, Result, output
from ..video_edit import number
from . import pages_option


def run(tool, files, options):
    from pypdf import PdfReader, PdfWriter, Transformation
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.pdfgen import canvas
    reader = PdfReader(io.BytesIO(files[0].data))
    if reader.is_encrypted:
        raise OneKitError("Unlock the PDF before adding page numbers.")
    selected = pages_option(options.get("pages") or "all", len(reader.pages))
    start = number(options, "start_number", 1, 0, 1000000, integer=True)
    size = number(options, "font_size", 12, 6, 72)
    margin = number(options, "margin", 24, 0, 144)
    position = options.get("position", "bottom-center")
    if position not in ("top-left", "top-center", "top-right", "bottom-left", "bottom-center", "bottom-right"):
        raise OneKitError("Choose a supported page-number position.")
    style = options.get("number_style", "number")
    if style not in ("number", "page-of-total"):
        raise OneKitError("Choose a supported number style.")
    color = options.get("color", "#333333")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise OneKitError("Choose a six-digit hexadecimal color.")
    writer = PdfWriter(clone_from=reader)
    for offset, index in enumerate(selected):
        page = writer.pages[index]
        crop = page.cropbox
        w, h, left, bottom = map(float, (crop.width, crop.height, crop.left, crop.bottom))
        rotation = page.rotation % 360
        transforms = {0:(1,0,0,1,left,bottom),90:(0,1,-1,0,left+w,bottom),180:(-1,0,0,-1,left+w,bottom+h),270:(0,-1,1,0,left,bottom+h)}
        if rotation not in transforms:
            raise OneKitError("Unsupported PDF page rotation.")
        width, height = (h,w) if rotation in (90,270) else (w,h)
        text = str(start+offset) if style == "number" else f"{start+offset} / {start+len(selected)-1}"
        text_width = stringWidth(text, "Helvetica", size)
        if 2*margin+text_width > width or 2*margin+size > height:
            raise OneKitError("Page numbers do not fit; reduce font size or margin.")
        x = margin if position.endswith("left") else width-margin-text_width if position.endswith("right") else (width-text_width)/2
        y = height-margin-size if position.startswith("top") else margin
        stream = io.BytesIO()
        stamp = canvas.Canvas(stream, pagesize=(width,height))
        stamp.setFont("Helvetica", size)
        stamp.setFillColor(HexColor(color))
        stamp.drawString(x,y,text)
        stamp.save()
        page.merge_transformed_page(PdfReader(io.BytesIO(stream.getvalue())).pages[0], Transformation(transforms[rotation]))
    stream = io.BytesIO()
    writer.write(stream)
    return Result([output(files[0], "pdf", stream.getvalue())], warnings=["Adding page numbers invalidates existing digital signatures."], details={"numberedPages":[index+1 for index in selected]})
