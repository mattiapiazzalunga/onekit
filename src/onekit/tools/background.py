# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io

from ..models import Artifact, OneKitError, Result

MODEL = {
    'name': 'u2net',
    'url': 'https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx',
    'sha256': '8d10d2f3bb75ae3b6d527c77944fc5e7dcd94b29809d47a739a7a728a912b491',
}


def prepare_foreground(image):
    """Return the U2Net input tensor, independent of the inference runtime."""
    import numpy as np
    from PIL import Image

    pixels = np.asarray(image.convert('RGB').resize((320, 320), Image.Resampling.LANCZOS), dtype=np.float32)
    pixels /= max(float(pixels.max()), 1e-6)
    pixels = (pixels - np.array([.485, .456, .406], dtype=np.float32)) / np.array([.229, .224, .225], dtype=np.float32)
    return np.ascontiguousarray(pixels.transpose(2, 0, 1)[None, ...], dtype='<f4')


def prediction_mask(prediction, size):
    """Normalize the model's first output and restore the original image size."""
    import numpy as np
    from PIL import Image

    prediction = np.asarray(prediction, dtype=np.float32).reshape(320, 320)
    if not np.isfinite(prediction).all():
        raise ValueError('U2Net returned an invalid mask.')
    low, high = float(prediction.min()), float(prediction.max())
    mask = (prediction - low) / (high - low) if high > low else np.zeros_like(prediction)
    return Image.fromarray((mask.clip(0, 1) * 255).astype('uint8')).resize(size, Image.Resampling.LANCZOS)


def foreground_input(file):
    from PIL import Image, ImageOps
    with Image.open(io.BytesIO(file.data)) as source:
        if getattr(source, 'n_frames', 1) != 1:
            raise OneKitError('Background removal supports single-frame images only.')
        image = ImageOps.exif_transpose(source)
        return {'data': prepare_foreground(image).tobytes(), 'shape': [1, 3, 320, 320], 'model': MODEL}


def foreground_output(file, prediction):
    import numpy as np
    from PIL import Image, ImageOps
    values = np.frombuffer(bytes(prediction), dtype='<f4')
    with Image.open(io.BytesIO(file.data)) as source:
        mask = prediction_mask(values, ImageOps.exif_transpose(source).size)
        stream = io.BytesIO()
        mask.save(stream, format='PNG')
        return stream.getvalue()


def foreground_mask(image):
    """Run the public U2Net model locally using its ImageNet input contract."""
    import onnxruntime as ort
    import pooch

    model = pooch.retrieve(
        url=MODEL['url'],
        known_hash='sha256:'+MODEL['sha256'],
        fname="u2net.onnx", path=pooch.os_cache("onekit/models"),
    )
    session = ort.InferenceSession(str(model), providers=["CPUExecutionProvider"])
    tensor = prepare_foreground(image)
    prediction = session.run(None, {session.get_inputs()[0].name: tensor})[0][0, 0]
    return prediction_mask(prediction, image.size)


def run(tool, files, options):
    from PIL import Image, ImageChops, ImageOps

    with Image.open(io.BytesIO(files[0].data)) as source:
        if getattr(source, "n_frames", 1) != 1:
            raise OneKitError("Background removal supports single-frame images only.")
        image = ImageOps.exif_transpose(source).convert("RGBA")
        try:
            from ..execution import current_context
            reader = current_context().foreground_reader
            mask = Image.open(io.BytesIO(reader(files[0]))).convert("L") if reader else foreground_mask(image)
            if mask.size != image.size:
                raise ValueError("Foreground mask dimensions do not match the image.")
        except Exception as exc:
            raise OneKitError("Cannot load or run U2Net. On first use, allow the model download; later runs use the local cache.") from exc
        image.putalpha(ImageChops.multiply(image.getchannel("A"), mask))
        stream = io.BytesIO()
        image.save(stream, format="PNG")
    return Result([Artifact(f"{files[0].stem}-no-background.png", stream.getvalue())])
