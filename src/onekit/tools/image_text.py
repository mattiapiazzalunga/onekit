# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Add text to an image; shared by native and embedded Python hosts."""
import re

from ..models import OneKitError, Result, output
from .images import encode, open_image
from .video_edit import number


def run(tool, files, options):
    boxes = options.get("text_boxes")
    if boxes is None:
        boxes = [options]
    elif not isinstance(boxes, list) or not 1 <= len(boxes) <= 50 or any(not isinstance(box, dict) for box in boxes):
        raise OneKitError("Provide 1–50 text boxes as objects.")
    image = open_image(files[0]).convert("RGBA")
    fonts = {}
    for box in boxes:
        _draw_text(image, box, fonts)
    return Result([output(files[0], "png", encode(image, "png"))])


def _draw_text(image, options, fonts):
    from PIL import ImageDraw, ImageFont
    text = options.get("text", "")
    if not isinstance(text, str) or not text.strip() or len(text) > 500:
        raise OneKitError("Enter 1–500 characters of text.")
    # Pillow's bundled scalable font is available in native and WASM builds.
    try:
        text.encode("cp1252")
    except UnicodeEncodeError:
        raise OneKitError("Use Western European text and punctuation.") from None
    size = number(options, "font_size", 32, 8, 3000, integer=True)
    color = options.get("color", "#ffffff")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise OneKitError("Choose a six-digit hexadecimal text color.")
    position = options.get("position", "bottom-center")
    if position not in ("top-left", "top-center", "top-right", "center", "bottom-left", "bottom-center", "bottom-right"):
        raise OneKitError("Choose a supported text position.")
    margin = number(options, "margin", 16, 0, 1000, integer=True)
    if size not in fonts:
        fonts[size] = ImageFont.load_default(size=size)
    font = fonts[size]
    draw = ImageDraw.Draw(image)
    box = draw.multiline_textbbox((0, 0), text, font=font, spacing=4)
    width, height = box[2]-box[0], box[3]-box[1]
    custom = 'x' in options or 'y' in options
    if custom and not ('x' in options and 'y' in options):
        raise OneKitError("Provide both x and y coordinates for the text box.")
    padding = 0 if custom else margin
    if width+2*padding > image.width or height+2*padding > image.height:
        raise OneKitError("The text does not fit. Reduce text size, text length or margin.")
    x = margin if position.endswith("left") else image.width-margin-width if position.endswith("right") else (image.width-width)/2
    y = margin if position.startswith("top") else image.height-margin-height if position.startswith("bottom") else (image.height-height)/2
    if custom:
        x = min(number(options, 'x', 0, 0, image.width), image.width-width)
        y = min(number(options, 'y', 0, 0, image.height), image.height-height)
    draw.multiline_text((x-box[0], y-box[1]), text, font=font, fill=color, spacing=4, align="center")
