# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Bounded PDF optimization for the CLI and Python API."""
import io

from ...models import OneKitError, Result, output

PRESETS = {
    "light": {"deflate": 1, "edge": None, "quality": None},
    "balanced": {"deflate": 6, "edge": 2000, "quality": 82},
    "maximum": {"deflate": 9, "edge": 1400, "quality": 60},
}


def image_objects(resources, path=(), visited=None):
    """Inspect image dictionaries before asking Pillow to decode any pixels."""
    visited = set() if visited is None else visited
    if len(path) > 16 or not resources:
        return
    resources = resources.get_object()
    xobjects = resources.get("/XObject", {})
    if hasattr(xobjects, "get_object"):
        xobjects = xobjects.get_object()
    for name, reference in xobjects.items():
        obj = reference.get_object()
        identity = id(obj)
        if identity in visited:
            continue
        visited.add(identity)
        if obj.get("/Subtype") == "/Image":
            yield (*path, name), obj
        elif obj.get("/Subtype") == "/Form":
            yield from image_objects(obj.get("/Resources"), (*path, name), visited)


def optimize_images(writer, preset):
    if preset["edge"] is None:
        return 0, 0
    from PIL import Image

    processed, optimized, skipped, pixels = set(), 0, 0, 0
    for page in writer.pages:
        for path, obj in image_objects(page.get("/Resources")):
            reference = getattr(obj, "indirect_reference", None)
            if reference is None or reference.idnum in processed:
                continue
            processed.add(reference.idnum)
            width, height = int(obj.get("/Width", 0)), int(obj.get("/Height", 0))
            # Keep masks, uncommon color spaces and small artwork untouched.
            if any(key in obj for key in ("/SMask", "/Mask", "/Decode")) or obj.get("/ImageMask"):
                skipped += 1
                continue
            if obj.get("/ColorSpace") not in ("/DeviceRGB", "/DeviceGray") or obj.get("/BitsPerComponent") != 8:
                skipped += 1
                continue
            if min(width, height) < 256:
                continue
            if width * height > 16_000_000 or pixels + width * height > 64_000_000 or len(processed) > 1000:
                skipped += 1
                continue
            pixels += width * height
            original = replacement = None
            try:
                image = page.images[list(path) if len(path) > 1 else path[0]]
                original = image.image
                if original is None or original.mode not in ("RGB", "L"):
                    skipped += 1
                    continue
                replacement = original.copy()
                replacement.thumbnail((preset["edge"], preset["edge"]), Image.Resampling.LANCZOS)
                candidate = io.BytesIO()
                replacement.save(candidate, "JPEG", quality=preset["quality"], optimize=True)
                # Do not replace an embedded image with a larger encoding.
                if len(candidate.getvalue()) >= len(image.data):
                    continue
                image.replace(replacement, quality=preset["quality"], optimize=True)
                optimized += 1
            except (OSError, ValueError, TypeError, NotImplementedError):
                skipped += 1
            finally:
                if replacement is not None:
                    replacement.close()
                if original is not None:
                    original.close()
    return optimized, skipped


def compress_pdf(reader, source, options):
    from pypdf import PdfWriter

    level = options.get("compression_level", "balanced")
    if not isinstance(level, str) or level not in PRESETS:
        raise OneKitError("Choose light, balanced or maximum compression.")
    preset = PRESETS[level]
    writer = PdfWriter(clone_from=reader)
    optimized, skipped = optimize_images(writer, preset)
    for page in writer.pages:
        page.compress_content_streams(level=preset["deflate"])
    # Deduplicate only after changing streams; shared streams must not be mutated.
    writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    stream = io.BytesIO()
    writer.write(stream)
    candidate = stream.getvalue()
    retained = len(candidate) >= len(source.data)
    data = source.data if retained else candidate
    warnings = []
    if retained:
        warnings.append("No smaller version was found. The original file has been kept unchanged.")
    elif optimized:
        warnings.append("Embedded images were optimized and may have lower quality or resolution. Text and vector graphics were not rasterized.")
    if skipped:
        warnings.append("Some images were left unchanged to preserve compatibility or stay within local processing limits.")
    return Result([output(source, "pdf", data)], warnings=warnings, details={
        "inputBytes": len(source.data), "outputBytes": len(data),
        "originalRetained": retained, "compressionLevel": level,
        "imagesOptimized": 0 if retained else optimized,
    })
