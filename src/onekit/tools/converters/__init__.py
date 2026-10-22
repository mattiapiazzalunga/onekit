# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import base64
import csv
import html
import io
import json
import re

from ...models import OneKitError, Result, output, parse_json


def pdf_images(file, format="png", dpi=144):
    import pypdfium2 as pdfium
    from ..images import encode
    if not 36 <= int(dpi) <= 300:
        raise OneKitError("dpi must be between 36 and 300.")
    result = []
    with pdfium.PdfDocument(file.data) as document:
        if len(document) > 256:
            raise OneKitError("Render at most 256 pages at a time.")
        for index in range(len(document)):
            page = document[index]
            width, height = page.get_size()
            if width * height * (dpi / 72) ** 2 > 40_000_000:
                raise OneKitError("A rendered page exceeds 40 million pixels; reduce dpi.")
            bitmap = page.render(scale=dpi / 72)
            result.append(output(file, f"page-{index+1}.{format}", encode(bitmap.to_pil(), format)))
            bitmap.close()
            page.close()
    return result


def add_image_slide(presentation, data):
    from PIL import Image
    with Image.open(io.BytesIO(data)) as image:
        width, height = image.size
    scale = min(presentation.slide_width / width, presentation.slide_height / height)
    width, height = round(width * scale), round(height * scale)
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    slide.shapes.add_picture(io.BytesIO(data), (presentation.slide_width-width)//2,
                             (presentation.slide_height-height)//2, width=width, height=height)


def text_document(text, file, target):
    if target == "docx":
        from docx import Document
        document = Document()
        for paragraph in text.split("\n"):
            document.add_paragraph(paragraph)
        buffer = io.BytesIO()
        document.save(buffer)
        return output(file, "docx", buffer.getvalue())
    if target == "html":
        return output(file, "html", '<!doctype html><meta charset="utf-8"><pre>' + html.escape(text) + "</pre>")
    if target == "latex":
        escape = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}"}
        return output(file, "tex", "\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\begin{document}\n" + "".join(escape.get(char, char) for char in text) + "\n\\end{document}\n")
    return output(file, target, text)


def run(tool, files, options):
    file = files[0]
    source, target = tool.id.split("-to-")
    if source == "image":
        if target == "base64":
            return Result([output(file, "base64", base64.b64encode(file.data))])
        if target == "pdf":
            from ..images import open_image, encode
            return Result([output(file, "pdf", encode(open_image(file), "pdf"))])
        from pptx import Presentation
        from ..images import open_image, encode
        image = open_image(file)
        presentation = Presentation()
        add_image_slide(presentation, encode(image, "png"))
        buffer = io.BytesIO()
        presentation.save(buffer)
        return Result([output(file, "pptx", buffer.getvalue())])
    if source == "base64":
        value = file.text().strip()
        if value.startswith("data:"):
            value = value.split(",", 1)[1]
        data = base64.b64decode(re.sub(r"\s+", "", value), validate=True)
        from ..inspector import SIGNATURES
        mime = next((mime for signature, mime in SIGNATURES if data.startswith(signature) and mime.startswith("image/")), None)
        if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
            mime = "image/webp"
        if mime is None:
            raise OneKitError("Base64 does not contain a recognized PNG, JPEG or GIF image.")
        return Result([output(file, mime.split("/")[1], data)])
    if source in ("csv", "json", "xlsx"):
        return tables(file, source, target, options)
    if source == "pdf":
        if target in ("png", "jpeg", "webp", "tiff"):
            return Result(pdf_images(file, target, int(options.get("dpi", 144))))
        if target == "pptx":
            from pptx import Presentation
            presentation = Presentation()
            images = pdf_images(file, dpi=int(options.get("dpi", 144)))
            for image in images:
                add_image_slide(presentation, image.data)
            buffer = io.BytesIO()
            presentation.save(buffer)
            return Result([output(file, "pptx", buffer.getvalue())], details={"pages": len(images), "dpi": int(options.get("dpi", 144))})
        if target == "pdfa":
            from ..native import pdfa
            return pdfa(file, options)
        from pypdf import PdfReader
        text = "\n\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(file.data)).pages)
        return Result([text_document(text, file, target)])
    if source == "md":
        if target == "json":
            return Result([output(file, "json", json.dumps({"content": file.text()}, ensure_ascii=False, indent=2))])
        if target == "html":
            from markdown_it import MarkdownIt
            rendered = MarkdownIt("commonmark", {"html": False}).render(file.text())
            return Result([output(file, "html", '<!doctype html><html lang="en"><meta charset="utf-8"><title>' + html.escape(file.stem) + "</title><body>" + rendered + "</body></html>")])
    if source == "html":
        if target == "json":
            from html.parser import HTMLParser
            class Parser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.events = []
                def handle_starttag(self, tag, attrs):
                    self.events.append({"type": "element", "tag": tag, "attributes": dict(attrs)})
                def handle_data(self, data):
                    if data.strip():
                        self.events.append({"type": "text", "value": data})
            parser = Parser()
            parser.feed(file.text())
            return Result([output(file, "json", json.dumps(parser.events, ensure_ascii=False, indent=2))])
        if target == "md":
            from markdownify import markdownify
            return Result([output(file, "md", markdownify(file.text(), heading_style="ATX"))])
    from ..native import convert_document
    return convert_document(file, source, target, options)


def tables(file, source, target, options):
    if source == "csv":
        reader = csv.DictReader(io.StringIO(file.text()), delimiter=str(options.get("delimiter", ",")))
        if reader.fieldnames and len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise OneKitError("CSV column headers must be unique.")
        keys = reader.fieldnames or []
        rows = bounded_rows(reader)
        if any(None in row for row in rows):
            raise OneKitError("CSV rows contain more fields than their header.")
    elif source == "json":
        rows = parse_json(file.text())
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise OneKitError("Expected a JSON array of objects.")
        keys = list(dict.fromkeys(key for row in rows for key in row))
    else:
        from openpyxl import load_workbook
        book = load_workbook(io.BytesIO(file.data), read_only=True, data_only=True)
        try:
            sheet = book[options["sheet"]] if options.get("sheet") else book.active
            values = sheet.iter_rows(values_only=True)
            keys = [str(value) if value is not None else f"Column {index+1}" for index, value in enumerate(next(values, []))]
            if len(set(keys)) != len(keys):
                raise OneKitError("Column headers must be unique.")
            rows = bounded_rows(dict(zip(keys, row)) for row in values)
        finally:
            book.close()
    if len(rows) > 100000:
        raise OneKitError("Tables may contain at most 100,000 rows.")
    if target == "json":
        return Result([output(file, "json", json.dumps(rows, ensure_ascii=False, indent=2, default=str))])
    if target == "csv":
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
        return Result([output(file, "csv", stream.getvalue())], ["CSV values are preserved. Import untrusted data as text to avoid spreadsheet formula execution."])
    if target == "pdf":
        from ..native import convert_document
        return convert_document(file, source, target, options)
    from openpyxl import Workbook
    book = Workbook()
    sheet = book.active
    sheet.append(keys)
    for row in rows:
        sheet.append([json.dumps(row.get(key), ensure_ascii=False) if isinstance(row.get(key), (dict, list)) else row.get(key) for key in keys])
    # Never turn untrusted JSON/CSV into spreadsheet formulas.
    for row in sheet:
        for cell in row:
            if isinstance(cell.value, str) and cell.value.startswith(("=", "+", "-", "@")):
                cell.data_type = "s"
    buffer = io.BytesIO()
    book.save(buffer)
    return Result([output(file, "xlsx", buffer.getvalue())])


def bounded_rows(rows):
    result = []
    for row in rows:
        if len(result) >= 100000:
            raise OneKitError("Tables may contain at most 100,000 rows.")
        result.append(row)
    return result
