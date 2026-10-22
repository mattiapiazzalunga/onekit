# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Destructive redaction by rebuilding from already-masked raster pixels."""
import io
import math

from ..models import Artifact, OneKitError, Result, parse_json


def regions_option(value):
    if isinstance(value, str):
        value = parse_json(value)
    if not isinstance(value, list) or not 1 <= len(value) <= 500:
        raise OneKitError("Select between 1 and 500 redaction areas.")
    regions = []
    for item in value:
        if not isinstance(item, dict) or set(item) - {"page", "x", "y", "width", "height"}:
            raise OneKitError("Each area needs page, x, y, width and height; coordinates are normalized from 0 to 1.")
        page = item.get("page", 1)
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise OneKitError("Redaction page numbers must be positive integers.")
        values = [item.get(key) for key in ("x", "y", "width", "height")]
        if any(isinstance(part, bool) or not isinstance(part, (int, float)) or not math.isfinite(part) for part in values):
            raise OneKitError("Redaction coordinates must be finite numbers.")
        x, y, width, height = values
        if x < 0 or y < 0 or width <= 0 or height <= 0 or x+width > 1+1e-9 or y+height > 1+1e-9:
            raise OneKitError("Redaction rectangles must fit completely inside the page or image (0–1 coordinates).")
        regions.append({"page": page, "x": x, "y": y, "width": width, "height": height})
    return regions


def pixel_box(region, width, height):
    # Expand outward by a pixel to cover antialiased edges; never leave fractional gaps.
    return (max(0, math.floor(region["x"]*width)-1), max(0, math.floor(region["y"]*height)-1),
            min(width, math.ceil((region["x"]+region["width"])*width)+1),
            min(height, math.ceil((region["y"]+region["height"])*height)+1))


def mask_image(image, regions):
    from PIL import Image, ImageDraw
    # A fresh RGB allocation carries no EXIF, comments, palette or hidden alpha pixels.
    clean = Image.new("RGB", image.size, "white")
    rgba = image.convert("RGBA")
    clean.paste(rgba, mask=rgba.getchannel("A"))
    draw = ImageDraw.Draw(clean)
    for region in regions:
        left, top, right, bottom = pixel_box(region, *clean.size)
        draw.rectangle((left, top, right-1, bottom-1), fill="black")
    return clean


def run(tool, files, options):
    regions = regions_option(options.get("regions"))
    if tool.id == "image-redact":
        from PIL import Image, ImageOps
        if any(region["page"] != 1 for region in regions):
            raise OneKitError("Image redaction areas must use page 1.")
        with Image.open(io.BytesIO(files[0].data)) as source:
            if getattr(source, "n_frames", 1) != 1:
                raise OneKitError("Animated or multi-frame images are not supported. Export a single frame first.")
            image = mask_image(ImageOps.exif_transpose(source), regions)
            stream = io.BytesIO()
            image.save(stream, format="PNG", optimize=True)
        return Result([Artifact("redacted.png", stream.getvalue())], details={"areas": len(regions), "metadataRemoved": True, "flattened": True})
    import pypdfium2 as pdfium
    from pypdf import PdfReader, PdfWriter
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    dpi = options.get("dpi", 144)
    if isinstance(dpi, str) and dpi.isdecimal():
        dpi = int(dpi)
    if isinstance(dpi, bool) or not isinstance(dpi, int) or not 72 <= dpi <= 300:
        raise OneKitError("PDF redaction DPI must be an integer between 72 and 300.")
    limit = options.get("_max_expanded_bytes", 128*1024*1024)
    stream = io.BytesIO()
    writer = canvas.Canvas(stream, pageCompression=1)
    encoded_total = 0
    with pdfium.PdfDocument(files[0].data) as document:
        count = len(document)
        if not 1 <= count <= 256:
            raise OneKitError("Redact at most 256 PDF pages at a time.")
        if any(region["page"] > count for region in regions):
            raise OneKitError(f"Redaction page numbers must be between 1 and {count}.")
        for index in range(count):
            page = document[index]
            try:
                width, height = page.get_size()
                if math.ceil(width*dpi/72)*math.ceil(height*dpi/72) > 40000000:
                    raise OneKitError("A rendered page exceeds 40 million pixels. Reduce DPI.")
                # Preserve visible annotation covers before discarding annotation objects.
                bitmap = page.render(scale=dpi/72, draw_annots=True)
                try:
                    image = mask_image(bitmap.to_pil(), [region for region in regions if region["page"] == index+1])
                finally:
                    bitmap.close()
                png = io.BytesIO()
                image.save(png, format="PNG")
                encoded_total += png.tell()
                if encoded_total > limit:
                    raise OneKitError("Redacted PDF images exceed the output limit. Reduce DPI or split the document first.")
                writer.setPageSize((width, height))
                writer.drawImage(ImageReader(png), 0, 0, width=width, height=height)
                writer.showPage()
                image.close()
            finally:
                page.close()
    writer.save()
    # Only the newly rendered pages are copied. No original PDF objects are reused.
    clean = PdfWriter()
    for page in PdfReader(io.BytesIO(stream.getvalue())).pages:
        clean.add_page(page)
    clean.metadata = None
    output = io.BytesIO()
    clean.write(output)
    if output.tell() > limit:
        raise OneKitError("Redacted PDF exceeds the output limit. Reduce DPI or split the document first.")
    return Result([Artifact("redacted.pdf", output.getvalue())], warnings=["All pages are rasterized. Selectable text, forms, annotations, attachments and original metadata are removed."], details={"pages": count, "areas": len(regions), "dpi": dpi, "flattened": True, "metadataRemoved": True})
