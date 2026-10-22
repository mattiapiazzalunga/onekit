# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io

from ..models import Artifact, OneKitError, Result


def foreground_mask(image):
    """Run the public U2Net model locally using its ImageNet input contract."""
    import numpy as np
    import onnxruntime as ort
    import pooch
    from PIL import Image

    model = pooch.retrieve(
        url="https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx",
        known_hash="md5:60024c5c889badc19c04ad937298a77b",
        fname="u2net.onnx", path=pooch.os_cache("onekit/models"),
    )
    session = ort.InferenceSession(str(model), providers=["CPUExecutionProvider"])
    pixels = np.asarray(image.convert("RGB").resize((320, 320), Image.Resampling.LANCZOS), dtype=np.float32)
    pixels /= max(float(pixels.max()), 1e-6)
    pixels = (pixels - np.array([.485, .456, .406], dtype=np.float32)) / np.array([.229, .224, .225], dtype=np.float32)
    tensor = pixels.transpose(2, 0, 1)[None, ...]
    prediction = session.run(None, {session.get_inputs()[0].name: tensor})[0][0, 0]
    if prediction.ndim != 2 or not np.isfinite(prediction).all():
        raise ValueError("U2Net returned an invalid mask.")
    low, high = float(prediction.min()), float(prediction.max())
    mask = (prediction - low) / (high - low) if high > low else np.zeros_like(prediction)
    return Image.fromarray((mask.clip(0, 1) * 255).astype("uint8")).resize(image.size, Image.Resampling.LANCZOS)


def run(tool, files, options):
    from PIL import Image, ImageChops, ImageOps

    with Image.open(io.BytesIO(files[0].data)) as source:
        if getattr(source, "n_frames", 1) != 1:
            raise OneKitError("Background removal supports single-frame images only.")
        image = ImageOps.exif_transpose(source).convert("RGBA")
        try:
            mask = foreground_mask(image)
        except Exception as exc:
            raise OneKitError("Cannot load or run U2Net. On first use, allow the model download; later runs use the local cache.") from exc
        image.putalpha(ImageChops.multiply(image.getchannel("A"), mask))
        stream = io.BytesIO()
        image.save(stream, format="PNG")
    return Result([Artifact(f"{files[0].stem}-no-background.png", stream.getvalue())])
