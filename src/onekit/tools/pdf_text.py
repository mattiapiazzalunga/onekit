# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io

from ..models import OneKitError, Result, output
from .pdf import pages_option


def run(tool, files, options):
    from pypdf import PdfReader
    file = files[0];reader = PdfReader(io.BytesIO(file.data))
    if reader.is_encrypted:
        raise OneKitError('Unlock the PDF before extracting text.')
    selected = pages_option(options.get('pages') or 'all',len(reader.pages))
    if len(selected)>256:
        raise OneKitError('Extract text from at most 256 pages at a time.')
    mode = options.get('layout','plain')
    if mode not in ('plain','layout'):
        raise OneKitError('Choose plain text or layout-preserving text.')
    parts = []
    characters = 0
    for index in selected:
        text = reader.pages[index].extract_text(extraction_mode='layout' if mode=='layout' else 'plain') or ''
        characters += len(text)
        if characters>8*1024*1024:
            raise OneKitError('Extracted text exceeds 8 MiB. Select fewer pages.')
        parts.append(text)
    text = '\n\n'.join(parts)
    warnings = ['No selectable text was found. Use OCR for scanned PDFs.'] if not text.strip() else []
    return Result([output(file,'txt',text)],warnings,{'pages':[index+1 for index in selected],'characters':len(text),'ocr':False})
