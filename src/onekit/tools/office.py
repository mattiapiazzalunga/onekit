# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
# Validate output from a trusted, local Office PDF engine primitive.
import io

from ..execution import current_context
from ..models import OneKitError, Result, output


def conversion_request(file):
    from ..validation import validate_zip
    if file.kind != 'docx' or len(file.data) > 16 * 1024 * 1024:
        raise OneKitError('Document conversion failed.')
    validate_zip(file.data, 32 * 1024 * 1024, 'docx')
    return {'format': 'docx', 'output': 'pdf', 'data': file.data}


def convert(file, service):
    response = service(conversion_request(file))
    try:
        data = bytes(response['data'])
        if not data.startswith(b'%PDF-') or len(data) > 32 * 1024 * 1024:
            raise ValueError()
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(data), strict=True)
        if reader.is_encrypted or not 1 <= len(reader.pages) <= current_context().document_limits.max_pages:
            raise ValueError()
    except Exception as exc:
        raise OneKitError('Document conversion failed.') from exc
    return Result([output(file, 'pdf', data)], details={'engine': 'LibreOffice', 'distribution': 'libreoffice-wasm', 'pages': len(reader.pages)})
