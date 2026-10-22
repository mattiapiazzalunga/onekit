# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io

import pytest
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
from reportlab.pdfgen import canvas

from onekit.api import execute
from onekit.models import Artifact, OneKitError


def document(shared=False, form=False):
    data = io.BytesIO()
    pdf = canvas.Canvas(data, pagesize=(400, 300))
    pdf.setTitle('Keep this title')
    for number in range(2):
        pdf.setFillColorRGB(.1, .6, .2)
        pdf.rect(10, 10, 380, 280, fill=1)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont('Helvetica', 18)
        pdf.drawString(40, 240, 'Hello world')
        pdf.drawString(40, 180, 'Keep this line')
        if form and number == 0:
            pdf.beginForm('reusable')
            pdf.drawString(40, 90, 'Inside form')
            pdf.endForm()
            pdf.doForm('reusable')
        pdf.showPage()
    pdf.save()
    if shared:
        writer = PdfWriter(clone_from=PdfReader(io.BytesIO(data.getvalue())))
        writer.pages[1][NameObject('/Contents')] = writer.pages[0].raw_get('/Contents')
        data = io.BytesIO()
        writer.write(data)
    return Artifact('editable.pdf', data.getvalue())


def inspect(file):
    return execute('pdf-edit', [file], {'mode': 'inspect'}).details


def edit(file, text='Changed text', page=1):
    run = inspect(file)['pages'][page-1]['runs'][0]
    return execute('pdf-edit', [file], {'edits': [{'page': page, 'id': run['id'],
                    'original': run['text'], 'text': text}]})


@pytest.mark.parametrize('shared', [False, True])
@pytest.mark.parametrize('text', ['Changed text', 'Much longer text that must stay inside the original box', '', 'Caffè'])
def test_replaces_original_keeps_other_page_graphics_metadata(shared, text):
    source = document(shared)
    result = edit(source, text)
    output = PdfReader(io.BytesIO(result.files[0].data))
    assert output.metadata.title == 'Keep this title'
    assert text in output.pages[0].extract_text()
    assert 'Hello world' not in output.pages[0].extract_text()
    assert 'Keep this line' in output.pages[0].extract_text()
    assert 'Hello world' in output.pages[1].extract_text()
    assert output.pages[0].mediabox == [0, 0, 400, 300]
    assert b're' in output.pages[0].get_contents().get_data()
    assert result.details['textBoxesEdited'] == 1


def test_unavailable_glyph_rejected_without_silent_substitution():
    with pytest.raises(OneKitError, match='original font'):
        edit(document(), 'Hello 😀')


def test_stale_original_invalid_page_duplicate_and_multiline_rejected():
    source = document()
    run = inspect(source)['pages'][0]['runs'][0]
    change = {'page': 1, 'id': run['id'], 'original': run['text'], 'text': 'New text'}
    for changes in [[dict(change, original='stale')], [dict(change, page=3)],
                    [change, change], [dict(change, text='two\nlines')]]:
        with pytest.raises(OneKitError):
            execute('pdf-edit', [source], {'edits': changes})


def test_inspect_does_not_offer_reusable_form_text():
    source = document(form=True)
    assert all('Inside form' not in run['text'] for run in inspect(source)['pages'][0]['runs'])


def test_blank_page_and_json_protocol():
    writer = PdfWriter()
    writer.add_blank_page(400, 300)
    buffer = io.BytesIO()
    writer.write(buffer)
    assert inspect(Artifact('blank.pdf', buffer.getvalue()))['editableRuns'] == 0
    source = document()
    import json
    run = inspect(source)['pages'][0]['runs'][0]
    result = execute('pdf-edit', [source], {'edits': json.dumps([
        {'page': 1, 'id': run['id'], 'original': run['text'], 'text': 'JSON edit'}])})
    assert 'JSON edit' in PdfReader(io.BytesIO(result.files[0].data)).pages[0].extract_text()


def test_embedded_subset_font_unicode_and_missing_glyph():
    from pathlib import Path

    import reportlab
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont('OneKitTestVera', str(Path(reportlab.__file__).parent / 'fonts' / 'Vera.ttf')))
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont('OneKitTestVera', 14)
    pdf.drawString(40, 200, 'Caffè già pronto')
    pdf.save()
    source = Artifact('unicode.pdf', buffer.getvalue())
    assert inspect(source)['pages'][0]['runs'][0]['text'] == 'Caffè già pronto'
    result = edit(source, 'già Caffè')
    assert 'già Caffè' in PdfReader(io.BytesIO(result.files[0].data)).pages[0].extract_text()
    with pytest.raises(OneKitError, match='original font'):
        edit(source, 'Ω')


def test_replacement_keeps_following_inline_text_position_and_background():
    import pypdfium2 as pdfium
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(400, 300))
    pdf.setFillColorRGB(.1, .6, .2)
    pdf.rect(0, 0, 400, 300, fill=1, stroke=0)
    pdf.setFillColorRGB(0, 0, 0)
    text = pdf.beginText(30, 200)
    text.setFont('Helvetica', 16)
    text.setCharSpace(.5)
    text.textOut('Original ')
    text.textOut('Following')
    pdf.drawText(text)
    pdf.save()
    source = Artifact('inline.pdf', buffer.getvalue())
    result = edit(source, 'A much longer replacement')
    positions, backgrounds = [], []
    for data in [source.data, result.files[0].data]:
        with pdfium.PdfDocument(data) as document:
            page = document[0]
            textpage = page.get_textpage()
            extracted = textpage.get_text_range()
            positions.append(textpage.get_charbox(extracted.index('Following')))
            bitmap = page.render(scale=1)
            image = bitmap.to_pil()
            backgrounds.append(image.getpixel((20, 20)))
            image.close()
            bitmap.close()
            textpage.close()
            page.close()
    assert positions[0] == pytest.approx(positions[1], abs=.02)
    assert backgrounds[0] == backgrounds[1]


def test_tj_kerning_and_transformed_coordinates():
    from pypdf.generic import DecodedStreamObject
    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(document().data)))
    stream = DecodedStreamObject()
    stream.set_data(b'q 1 0 0 1 10 20 cm BT /F1 18 Tf 1 0 0 1 40 240 Tm [(Hello) -100 ( world)] TJ ET Q')
    writer.pages[0][NameObject('/Contents')] = writer._add_object(stream)
    buffer = io.BytesIO()
    writer.write(buffer)
    source = Artifact('kerning.pdf', buffer.getvalue())
    run = inspect(source)['pages'][0]['runs'][0]
    assert run['text'] == 'Hello world'
    assert (run['x'], run['y']) == (50, 260)
    result = edit(source, 'Changed kerning')
    assert 'Changed kerning' in PdfReader(io.BytesIO(result.files[0].data)).pages[0].extract_text()


def test_encrypted_pdf_can_be_inspected_and_edited_with_password():
    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(document().data)))
    writer.encrypt('edit-password')
    buffer = io.BytesIO()
    writer.write(buffer)
    source = Artifact('encrypted.pdf', buffer.getvalue())
    with pytest.raises(OneKitError, match='password'):
        inspect(source)
    run = execute('pdf-edit', [source], {'mode': 'inspect', 'password': 'edit-password'}).details['pages'][0]['runs'][0]
    result = execute('pdf-edit', [source], {'password': 'edit-password', 'edits': [
        {'page': 1, 'id': run['id'], 'original': run['text'], 'text': 'Edited protected PDF'}]})
    reader = PdfReader(io.BytesIO(result.files[0].data))
    assert 'Edited protected PDF' in reader.pages[0].extract_text()
    assert not reader.is_encrypted
    assert any('not password protected' in warning for warning in result.warnings)
