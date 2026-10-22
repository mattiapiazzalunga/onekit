# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json

from ...models import OneKitError, Result, output, require


def pages_option(value, count):
    if value is None or value == "all":
        return list(range(count))
    result = []
    for section in str(value).split(","):
        bounds = section.strip().split("-")
        if len(bounds) not in (1, 2):
            raise OneKitError("Use page numbers such as 1,3-5 (one based).")
        start, end = int(bounds[0]), int(bounds[-1])
        if not 1 <= start <= end <= count:
            raise OneKitError(f"Page ranges must be between 1 and {count}.")
        result.extend(range(start - 1, end))
    return result


def save(writer):
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def run(tool, files, options):
    op = tool.id.removeprefix("pdf-")
    if op == "sign":
        from pyhanko.sign import signers
        from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
        signer = signers.SimpleSigner.load_pkcs12(require(options, "certificate"), passphrase=str(require(options, "password")).encode())
        if signer is None:
            raise OneKitError("Cannot load the certificate; check its password and format.")
        stream = io.BytesIO()
        signers.sign_pdf(IncrementalPdfFileWriter(io.BytesIO(files[0].data)), signature_meta=signers.PdfSignatureMetadata(field_name="OneKitSignature"), signer=signer, output=stream)
        return Result([output(files[0], "signed.pdf", stream.getvalue())])
    if op == "validate-pdfa":
        from ..native import run_verapdf
        return run_verapdf(files[0])
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(io.BytesIO(files[0].data), strict=False)
    if reader.is_encrypted:
        password = options.get("password", "")
        if not reader.decrypt(password):
            raise OneKitError("The PDF is encrypted. Supply its correct password.")
    if op == "compress":
        from .compression import compress_pdf
        return compress_pdf(reader, files[0], options)
    if op == "edit" and ("edits" in options or "mode" in options):
        from .editing import edit_pdf
        return edit_pdf(reader, files[0], options)
    writer = PdfWriter()
    if op == "merge":
        for file in files:
            part = PdfReader(io.BytesIO(file.data))
            if part.is_encrypted and not part.decrypt(options.get("password", "")):
                raise OneKitError(f"A correct password is required for {file.name}.")
            writer.append(part)
    elif op == "split":
        result = []
        for index, page in enumerate(reader.pages):
            part = PdfWriter()
            part.add_page(page)
            result.append(output(files[0], f"page-{index+1}.pdf", save(part)))
        return Result(result)
    elif op in ("organize", "extract-pages", "remove-pages"):
        selected = pages_option(require(options, "pages"), len(reader.pages))
        if op == "remove-pages":
            removed = set(selected)
            selected = [index for index in range(len(reader.pages)) if index not in removed]
        if not selected:
            raise OneKitError("The result must contain at least one page.")
        for index in selected:
            writer.add_page(reader.pages[index])
    else:
        writer.append(reader)
        if op == "rotate":
            angle = int(options.get("angle", 90))
            if angle % 90:
                raise OneKitError("Rotation must be a multiple of 90 degrees.")
            for index in pages_option(options.get("pages"), len(writer.pages)):
                writer.pages[index].rotate(angle)
        elif op == "protect":
            password = str(require(options, "password"))
            if len(password) < 8:
                raise OneKitError("Use a password with at least 8 characters.")
            writer.encrypt(password, algorithm="AES-256")
        elif op == "edit":
            from reportlab.pdfgen import canvas
            index = int(options.get("page", 1)) - 1
            if not 0 <= index < len(writer.pages):
                raise OneKitError("The selected page does not exist.")
            page = writer.pages[index]
            stream = io.BytesIO()
            overlay = canvas.Canvas(stream, pagesize=(float(page.mediabox.width), float(page.mediabox.height)))
            overlay.drawString(float(options.get("x", 36)), float(options.get("y", 36)), str(require(options, "text")))
            overlay.save()
            page.merge_page(PdfReader(io.BytesIO(stream.getvalue())).pages[0])
    data = save(writer)
    return Result([output(files[0], "pdf", data)])
