# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Exact quarter turns and reflections after applying EXIF orientation."""
import io

from PIL import Image, ImageOps

from ..models import Artifact, OneKitError, Result


def run(tool, files, options):
    angle, flip = str(options.get("angle", "90")), options.get("flip", "none")
    if angle not in ("0", "90", "180", "270") or flip not in ("none", "horizontal", "vertical", "both"):
        raise OneKitError("Choose a clockwise rotation of 0, 90, 180 or 270 degrees and a supported reflection.")
    with Image.open(io.BytesIO(files[0].data)) as source:
        if getattr(source, "n_frames", 1) != 1:
            raise OneKitError("Choose a single-frame image; animated and multipage images are not transformed.")
        ImageOps.exif_transpose(source, in_place=True)
        image = source if source.mode == "RGBA" else source.convert("RGBA")
        if image is not source:
            source.close()
        try:
            operations = []
            if angle != "0":
                operations.append({"90": Image.Transpose.ROTATE_270, "180": Image.Transpose.ROTATE_180, "270": Image.Transpose.ROTATE_90}[angle])
            if flip in ("horizontal", "both"):
                operations.append(Image.Transpose.FLIP_LEFT_RIGHT)
            if flip in ("vertical", "both"):
                operations.append(Image.Transpose.FLIP_TOP_BOTTOM)
            for operation in operations:
                previous = image
                image = image.transpose(operation)
                previous.close()
            # Avoid a full image.tobytes()/frombytes() copy just to drop metadata.
            image.info.clear()
            width, height = image.size
            stream = io.BytesIO()
            image.save(stream, format="PNG")
        finally:
            image.close()
    return Result([Artifact(files[0].stem + "-transformed.png", stream.getvalue())],
                  details={"width": width, "height": height, "clockwise_degrees": int(angle), "flip_after_rotation": flip})
