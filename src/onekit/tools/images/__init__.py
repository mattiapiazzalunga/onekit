# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import warnings

from ...models import OneKitError, Result, output


def open_image(file):
    from PIL import Image, ImageOps
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        image = Image.open(io.BytesIO(file.data))
        if image.width * image.height > 40_000_000:
            raise OneKitError("Images must contain no more than 40 million pixels.")
        image.load()
        return ImageOps.exif_transpose(image)


def encode(image, format="png", **options):
    format = format.lower().replace("jpg", "jpeg")
    if format not in ("png", "jpeg", "webp", "tiff", "bmp", "ico", "gif", "pdf"):
        raise OneKitError("Supported formats: png, jpeg, webp, tiff, bmp, ico, gif, pdf.")
    if format in ("jpeg", "pdf") and image.mode != "RGB":
        from PIL import Image
        base = Image.new("RGB", image.size, "white")
        if "A" in image.getbands():
            base.paste(image, mask=image.getchannel("A"))
        else:
            base.paste(image.convert("RGB"))
        image = base
    buffer = io.BytesIO()
    image.save(buffer, format=format.upper(), **options)
    return buffer.getvalue()


def run(tool, files, options):
    file = files[0]
    if tool.id == "image-extract-pdf":
        from pypdf import PdfReader
        result = []
        for page_index, page in enumerate(PdfReader(io.BytesIO(file.data)).pages):
            for index, image in enumerate(page.images):
                result.append(output(file, f"{page_index+1}-{index+1}-{image.name}", image.data))
        if not result:
            raise OneKitError("This PDF contains no embedded raster images.")
        return Result(result)
    image = open_image(file)
    if tool.id == "image-crop":
        box = options.get("box")
        if not isinstance(box, (list, tuple)) or len(box) != 4:
            raise OneKitError("box must be [left, top, right, bottom] in pixels.")
        left, top, right, bottom = map(int, box)
        if not 0 <= left < right <= image.width or not 0 <= top < bottom <= image.height:
            raise OneKitError("Crop bounds must lie inside the image.")
        image = image.crop((left, top, right, bottom))
    format = options.get("format", file.kind if file.kind != "pdf" else "png")
    quality = int(options.get("quality", 82))
    if not 1 <= quality <= 100:
        raise OneKitError("quality must be between 1 and 100.")
    data = encode(image, format, optimize=True, quality=quality)
    return Result([output(file, format, data)], details={"inputBytes": len(file.data), "outputBytes": len(data)})
