# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io

from ..models import Artifact, OneKitError, Result


def run(tool, files, options):
    from PIL import Image, ImageOps
    scale = options.get("scale", 2)
    if isinstance(scale, bool) or str(scale) not in ("2", "3", "4"):
        raise OneKitError("Choose an upscale factor of 2, 3 or 4.")
    with Image.open(io.BytesIO(files[0].data)) as source:
        if getattr(source, "n_frames", 1) != 1:
            raise OneKitError("Upscaling supports single-frame images only.")
        image = ImageOps.exif_transpose(source).convert("RGBA")
        size = (image.width * int(scale), image.height * int(scale))
        if size[0] * size[1] > 40_000_000:
            raise OneKitError("Upscaled output exceeds 40 million pixels. Choose a smaller factor or source.")
        image = image.resize(size, Image.Resampling.LANCZOS)
        output = io.BytesIO()
        image.save(output, format="PNG")
    return Result([Artifact(f"{files[0].stem}-upscaled.png", output.getvalue())],
                  details={"width": size[0], "height": size[1], "scale": int(scale)})
