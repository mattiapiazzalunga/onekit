# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
import io
import json
import re

from ...models import OneKitError, Result, output


def run(tool, files, options):
    import pytesseract
    from PIL import Image
    from ..converters import pdf_images, text_document
    file = files[0]
    target = tool.produces
    language = str(options.get("language", "eng"))
    if not re.fullmatch(r"[a-zA-Z_]+(?:\+[a-zA-Z_]+)*", language):
        raise OneKitError("Use installed Tesseract language codes, such as eng or eng+ita.")
    images = pdf_images(file, dpi=int(options.get("dpi", 200))) if file.kind == "pdf" else [file]
    texts, pdfs = [], []
    for image in images:
        opened = Image.open(io.BytesIO(image.data))
        if opened.width * opened.height > 40_000_000:
            raise OneKitError("Image exceeds 40 million pixels.")
        if target == "pdf":
            pdfs.append(pytesseract.image_to_pdf_or_hocr(opened, extension="pdf", lang=language, timeout=120))
        else:
            texts.append(pytesseract.image_to_string(opened, lang=language, timeout=120))
    if target == "pdf":
        from pypdf import PdfReader, PdfWriter
        from ..pdf import save
        writer = PdfWriter()
        for data in pdfs:
            writer.append(PdfReader(io.BytesIO(data)))
        artifact = output(file, "pdf", save(writer))
    elif target == "json":
        artifact = output(file, "json", json.dumps({"pages": texts, "language": language}, ensure_ascii=False, indent=2))
    else:
        artifact = text_document("\n\n".join(texts), file, target)
    return Result([artifact])
