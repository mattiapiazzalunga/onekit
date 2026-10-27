# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io

import pytest
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DecodedStreamObject, DictionaryObject, NameObject, NumberObject, TextStringObject
from reportlab.pdfgen import canvas

from onekit import Artifact, execute
from onekit.models import OneKitError


def nested_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.beginForm('Stamp');c.setFont('Helvetica',30);c.drawString(10,10,'DRAFT');c.endForm()
    c.beginForm('Outer');c.doForm('Stamp');c.endForm()
    for number in (1,2):
        c.drawString(20,700,f'Keep page {number}');c.doForm('Outer');c.showPage()
    c.save()
    return Artifact('nested.pdf',buffer.getvalue())


def report(file):
    return execute('pdf-remove-watermark',[file],{'mode':'inspect'}).details['objects']


def reader(result):
    return PdfReader(io.BytesIO(result.files[0].data))


def test_nested_forms_exact_text_removal():
    file = nested_pdf()
    objects = report(file)
    assert [item['text'] for item in objects if item['type']=='text'].count('DRAFT') == 2
    result = execute('pdf-remove-watermark',[file],{'text':'DRAFT'})
    output = reader(result)
    assert output.pages[0].extract_text().strip() == 'Keep page 1'
    assert output.pages[1].extract_text().strip() == 'Keep page 2'
    assert result.details['removedObjects'] == 2


def test_select_one_invocation_preserves_shared_form_on_other_page():
    file = nested_pdf()
    stamp = next(item for item in report(file) if item.get('text')=='DRAFT')
    result = execute('pdf-remove-watermark',[file],{'objects':[stamp['id']]})
    output = reader(result)
    assert 'DRAFT' not in output.pages[0].extract_text()
    assert 'DRAFT' in output.pages[1].extract_text()
    assert 'Keep page 1' in output.pages[0].extract_text()


def test_parent_and_child_selections_do_not_conflict():
    file = nested_pdf()
    objects = [item['id'] for item in report(file) if item['page']==1 and item['type'] in ('form','text') and item.get('text')!='Keep page 1']
    result = execute('pdf-remove-watermark',[file],{'objects':objects})
    assert 'DRAFT' not in reader(result).pages[0].extract_text()
    assert 'DRAFT' in reader(result).pages[1].extract_text()


def dictionary(**values):
    return DictionaryObject({NameObject('/'+key):value for key,value in values.items()})


def write(writer):
    buffer = io.BytesIO();writer.write(buffer)
    return Artifact('objects.pdf',buffer.getvalue())


def test_identity_h_font_decodes_hex_glyphs_for_matching():
    writer = PdfWriter();page=writer.add_blank_page(200,300)
    cmap = DecodedStreamObject();cmap.set_data(b'/CIDInit /ProcSet findresource begin 12 dict begin begincmap /CIDSystemInfo << /Registry (Test) /Ordering (Test) /Supplement 0 >> def /CMapName /Test def /CMapType 2 def 1 begincodespacerange <0000> <FFFF> endcodespacerange 2 beginbfchar <0001> <0057> <0002> <004D> endbfchar endcmap CMapName currentdict /CMap defineresource pop end end')
    descendant = dictionary(Type=NameObject('/Font'),Subtype=NameObject('/CIDFontType2'),BaseFont=NameObject('/Test'),CIDSystemInfo=dictionary(Registry=TextStringObject('Test'),Ordering=TextStringObject('Test'),Supplement=NumberObject(0)),DW=NumberObject(1000))
    font = dictionary(Type=NameObject('/Font'),Subtype=NameObject('/Type0'),BaseFont=NameObject('/Test'),Encoding=NameObject('/Identity-H'),DescendantFonts=ArrayObject([writer._add_object(descendant)]),ToUnicode=writer._add_object(cmap))
    page[NameObject('/Resources')] = dictionary(Font=dictionary(F1=writer._add_object(font)))
    stream=DecodedStreamObject();stream.set_data(b'BT /F1 20 Tf 10 100 Td <00010002> Tj ET')
    page[NameObject('/Contents')]=writer._add_object(stream)
    file=write(writer)
    assert report(file)[0]['text']=='WM'
    result=execute('pdf-remove-watermark',[file],{'text':'WM'})
    assert reader(result).pages[0].extract_text().strip()==''


def test_selected_image_invocation_is_removed_without_removing_other_drawing():
    writer=PdfWriter();page=writer.add_blank_page(200,300)
    image=DecodedStreamObject();image.set_data(b'\xff\x00\x00');image.update(dictionary(Type=NameObject('/XObject'),Subtype=NameObject('/Image'),Width=NumberObject(1),Height=NumberObject(1),BitsPerComponent=NumberObject(8),ColorSpace=NameObject('/DeviceRGB')))
    page[NameObject('/Resources')]=dictionary(XObject=dictionary(Im=writer._add_object(image)))
    stream=DecodedStreamObject();stream.set_data(b'q 10 0 0 10 50 50 cm /Im Do Q 0 0 20 20 re S')
    page[NameObject('/Contents')]=writer._add_object(stream);file=write(writer)
    image_id=next(item['id'] for item in report(file) if item['type']=='image')
    result=execute('pdf-remove-watermark',[file],{'objects':[image_id]})
    content=reader(result).pages[0].get_contents().get_data()
    assert b' Do' not in content and b'20 20 re' in content


def test_selection_inside_tagged_artifact_and_named_properties():
    writer=PdfWriter();page=writer.add_blank_page(200,300)
    page[NameObject('/Resources')]=dictionary(Properties=dictionary(WM=dictionary(Subtype=NameObject('/Watermark'))))
    stream=DecodedStreamObject();stream.set_data(b'/Artifact /WM BDC BT (Logo) Tj ET EMC 0 0 20 20 re S')
    page[NameObject('/Contents')]=writer._add_object(stream);file=write(writer)
    result=execute('pdf-remove-watermark',[file],{'objects':[report(file)[0]['id']]})
    assert b'Logo' not in reader(result).pages[0].get_contents().get_data()


def test_removed_text_preserves_advance_and_following_text():
    buffer=io.BytesIO();c=canvas.Canvas(buffer);c.setFont('Helvetica',12);text=c.beginText(20,100);text.textOut('DRAFT');c.drawText(text);text=c.beginText();text.textOut('Keep');c.drawText(text);c.save()
    file=Artifact('advance.pdf',buffer.getvalue())
    before=[];PdfReader(io.BytesIO(file.data)).pages[0].extract_text(visitor_text=lambda text,cm,tm,font,size:before.append((text,tm[:])) if 'Keep' in text else None)
    result=execute('pdf-remove-watermark',[file],{'text':'DRAFT'})
    after=[];reader(result).pages[0].extract_text(visitor_text=lambda text,cm,tm,font,size:after.append((text,tm[:])) if 'Keep' in text else None)
    assert before==after
    assert b'DRAFT' not in reader(result).pages[0].get_contents().get_data()


@pytest.mark.parametrize('options',[{'objects':['p99/t0']},{'objects':'{}'},{'mode':'unknown'}])
def test_invalid_selection_fails_explicitly(options):
    with pytest.raises(OneKitError):execute('pdf-remove-watermark',[nested_pdf()],options)
