# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json
import re

from ...models import OneKitError, Result, output


def run(tool, files, options):
    from ...execution import current_context
    from ..converters import pdf_images
    file = files[0]
    target = tool.produces
    language = str(options.get("language", "eng"))
    if not re.fullmatch(r"[a-zA-Z_]+(?:\+[a-zA-Z_]+)*", language):
        raise OneKitError("Use installed Tesseract language codes, such as eng or eng+ita.")
    reader = current_context().ocr_reader
    if reader is not None:
        pages = reader(file, language, int(options.get("dpi", 200)), target == "pdf")
        return recognition_result(file, target, language, pages)
    import pytesseract
    from PIL import Image
    images = pdf_images(file, dpi=int(options.get("dpi", 200))) if file.kind == "pdf" else [file]
    pages = []
    for image in images:
        opened = Image.open(io.BytesIO(image.data))
        if opened.width * opened.height > 40_000_000:
            raise OneKitError("Image exceeds 40 million pixels.")
        if target == "pdf":
            pages.append({"pdf": pytesseract.image_to_pdf_or_hocr(opened, extension="pdf", lang=language, timeout=120)})
        else:
            pages.append({"text": pytesseract.image_to_string(opened, lang=language, timeout=120)})
    return recognition_result(file, target, language, pages)


def recognition_result(file, target, language, pages):
    from ..converters import text_document
    texts = [re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", page.get("text", "")) for page in pages]
    if target == "pdf":
        from pypdf import PdfReader, PdfWriter

        from ..pdf import save
        writer = PdfWriter()
        for recognized in pages:
            part = PdfReader(io.BytesIO(recognized["pdf"]))
            for page in part.pages:
                if recognized.get("width") and recognized.get("height"):
                    page.scale_to(recognized["width"], recognized["height"])
                writer.add_page(page)
        artifact = output(file, "pdf", save(writer))
    elif target == "json":
        artifact = output(file, "json", json.dumps({"pages": texts, "language": language}, ensure_ascii=False, indent=2))
    else:
        artifact = text_document("\n\n".join(texts), file, target)
    return Result([artifact])
