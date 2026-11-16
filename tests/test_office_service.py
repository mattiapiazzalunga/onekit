import io

import pytest
from docx import Document
from pypdf import PdfWriter

from onekit.api import execute
from onekit.execution import ExecutionContext, DocumentLimits
from onekit.models import Artifact, OneKitError
from onekit.tools.office import conversion_request


def word():
    stream = io.BytesIO()
    document = Document()
    document.add_paragraph('Caffè. 中文测试。 हिन्दी परीक्षण।')
    document.save(stream)
    return Artifact('document.docx', stream.getvalue())


def pdf(pages=1):
    stream = io.BytesIO()
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=595, height=842)
    writer.write(stream)
    return stream.getvalue()


def test_office_service_uses_shared_dispatcher_and_validates_pdf():
    seen = []
    def service(request):
        seen.append(request)
        return {'data': pdf(2)}
    result = execute('docx-to-pdf', [word()], context=ExecutionContext(document_converter=service))
    assert result.files[0].name == 'document.pdf'
    assert result.details['pages'] == 2
    assert result.details['engine'] == 'LibreOffice'
    assert seen[0]['format'] == 'docx'
    assert seen[0]['output'] == 'pdf'


@pytest.mark.parametrize('response', [None, {}, {'data': b'not a PDF'}, {'data': b'%PDF-1.7\ntruncated'}])
def test_office_rejects_invalid_engine_output(response):
    with pytest.raises(OneKitError, match='Document conversion failed'):
        execute('docx-to-pdf', [word()], context=ExecutionContext(document_converter=lambda request: response))


def test_office_enforces_page_budget():
    with pytest.raises(OneKitError, match='Document conversion failed'):
        execute('docx-to-pdf', [word()], context=ExecutionContext(
            document_converter=lambda request: {'data': pdf(2)}, document_limits=DocumentLimits(max_pages=1)))


def test_office_rejects_fake_docx_before_engine():
    with pytest.raises(OneKitError):
        conversion_request(Artifact('fake.docx', b'PK\x03\x04not an Office document'))
