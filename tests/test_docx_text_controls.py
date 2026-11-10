import io

import pytest
from docx import Document
from docx.oxml.ns import qn

from onekit.models import Artifact, OneKitError
from onekit.tools.converters import text_document
from onekit import execute


def test_plain_text_form_feeds_become_word_page_breaks():
    result = execute('txt-to-docx', [Artifact('note.txt', 'Caffè\t一\nSecond line\fNext page'.encode())]).files[0]
    document = Document(io.BytesIO(result.data))
    assert [p.text for p in document.paragraphs] == ['Caffè\t一', 'Second line', '', 'Next page']
    assert len(document.element.findall('.//' + qn('w:br'))) == 1
    assert document.element.find('.//' + qn('w:br')).get(qn('w:type')) == 'page'


@pytest.mark.parametrize('control', ['\x00', '\x07', '\x0b', '\x1f', '\ufffe', '\uffff', '\ud800'])
def test_non_xml_text_gets_input_guidance_instead_of_lxml_failure(control):
    with pytest.raises(OneKitError, match='Binary content is not accepted'):
        text_document('Before' + control + 'After', Artifact('note.txt', b''), 'docx')
