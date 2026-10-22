# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Local image effects on the whole image or selected normalized rectangles."""
import io
import math
import re

from ..models import Artifact, OneKitError, Result
from .redaction import mask_image, pixel_box, regions_option


def run(tool, files, options):
    from PIL import Image, ImageFilter, ImageOps
    effect = options.get("effect", "blur")
    scope = options.get("scope", "all")
    if effect not in ("blur", "pixelate", "box-blur", "solid", "grayscale"):
        raise OneKitError("Choose blur, pixelate, box-blur, solid or grayscale.")
    if scope not in ("all", "selected"):
        raise OneKitError("Choose the whole image or selected areas.")
    raw = options.get("strength", 12)
    try:
        strength = float(raw)
    except (TypeError, ValueError, OverflowError) as exc:
        raise OneKitError("Effect intensity must be an integer from 1 to 100 pixels.") from exc
    if isinstance(raw, bool) or not math.isfinite(strength) or not strength.is_integer() or not 1 <= strength <= 100:
        raise OneKitError("Effect intensity must be an integer from 1 to 100 pixels.")
    strength = int(strength)
    if effect == "pixelate" and strength < 2:
        raise OneKitError("Pixelation block size must be at least 2 pixels.")
    color = options.get("color", "#000000")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise OneKitError("Cover color must be a six-digit hexadecimal color.")
    regions = [{"page": 1, "x": 0, "y": 0, "width": 1, "height": 1}] if scope == "all" else regions_option(options.get("regions"))
    if any(region["page"] != 1 for region in regions):
        raise OneKitError("Image effect areas must use page 1.")
    with Image.open(io.BytesIO(files[0].data)) as image:
        if getattr(image, "n_frames", 1) != 1:
            raise OneKitError("Animated or multi-frame images are not supported. Export a single frame first.")
        original = mask_image(ImageOps.exif_transpose(image), [])
    output = original.copy()
    boxes = [pixel_box(region, *original.size) for region in regions]
    if sum((right-left)*(bottom-top) for left, top, right, bottom in boxes) > 80000000:
        raise OneKitError("Selected areas exceed the effect processing limit. Reduce overlapping areas or use the whole-image scope.")
    for box in boxes:
        part = original.crop(box)
        if effect == "blur":
            filtered = part.filter(ImageFilter.GaussianBlur(strength))
        elif effect == "box-blur":
            filtered = part.filter(ImageFilter.BoxBlur(strength))
        elif effect == "pixelate":
            small = part.resize((max(1, math.ceil(part.width/strength)), max(1, math.ceil(part.height/strength))), Image.Resampling.BOX)
            filtered = small.resize(part.size, Image.Resampling.NEAREST)
            small.close()
        elif effect == "solid":
            filtered = Image.new("RGB", part.size, color)
        else:
            filtered = ImageOps.grayscale(part).convert("RGB")
        output.paste(filtered, box)
        part.close()
        filtered.close()
    stream = io.BytesIO()
    output.save(stream, format="PNG", optimize=True)
    original.close()
    output.close()
    warnings = ["Blur and pixelation are visual effects, not guaranteed permanent removal of sensitive details."] if effect in ("blur", "box-blur", "pixelate") else []
    return Result([Artifact("image-effects.png", stream.getvalue())], warnings=warnings,
                  details={"effect": effect, "scope": scope, "strength": strength, "areas": len(regions), "metadataRemoved": True})
