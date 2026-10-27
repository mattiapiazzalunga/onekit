# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json
from xml.etree import ElementTree

import pytest
from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject

from onekit import Artifact, execute
from onekit.models import OneKitError
from onekit.tools.pdf_design import field_rectangle


def picture(image, fmt='PNG'):
    buffer = io.BytesIO()
    image.save(buffer, fmt)
    return Artifact('sample.jpg' if fmt == 'JPEG' else 'sample.png', buffer.getvalue())


def pdf(content=None):
    writer = PdfWriter()
    page = writer.add_blank_page(200, 300)
    if content:
        stream = DecodedStreamObject()
        stream.set_data(content)
        page[NameObject('/Contents')] = writer._add_object(stream)
    buffer = io.BytesIO()
    writer.write(buffer)
    return Artifact('sample.pdf', buffer.getvalue())


def test_picker_and_palette():
    image = Image.new('RGBA', (10, 10), (255, 0, 0, 255))
    ImageDraw.Draw(image).rectangle((0, 0, 4, 9), fill=(0, 0, 255, 255))
    artifact = picture(image)
    assert execute('color-picker', [artifact], {'x':0, 'y':0}).details['hex'] == '#0000FF'
    assert execute('color-picker', [Artifact('color.txt', b'#123456')]).details['rgb'] == [18, 52, 86]
    colors = execute('image-extract-colors', [artifact], {'colors':2}).details['colors']
    assert {c['hex'] for c in colors} == {'#FF0000', '#0000FF'}
    assert [c['fraction'] for c in colors] == [.5, .5]
    transparent = picture(Image.new('RGBA', (2, 2)))
    with pytest.raises(OneKitError, match='no visible'):
        execute('image-extract-colors', [transparent])
    assert execute('color-picker', [transparent]).details['hex'] == '#FFFFFF'


def test_vector_paths_without_bitmap():
    result = execute('jpg-to-svg', [picture(Image.new('RGB', (32, 24), 'blue'), 'JPEG')])
    root = ElementTree.fromstring(result.files[0].data)
    assert root.findall('{http://www.w3.org/2000/svg}path')
    assert b'base64' not in result.files[0].data and b'<image' not in result.files[0].data
    assert result.details['shapes'] == 1


@pytest.mark.parametrize('tool', ['image-repair', 'image-remove-watermark'])
def test_local_repair_preserves_outside_and_alpha(tool):
    image = Image.new('RGBA', (32, 32), (30, 90, 150, 180))
    ImageDraw.Draw(image).rectangle((12, 12, 15, 15), fill=(255, 255, 255, 180))
    region = {'x':12/32, 'y':12/32, 'width':4/32, 'height':4/32}
    result = execute(tool, [picture(image)], {'regions':[region]})
    output = Image.open(io.BytesIO(result.files[0].data))
    assert output.getpixel((13, 13)) == (30, 90, 150, 180)
    assert output.getpixel((11, 12)) == image.getpixel((11, 12))
    assert output.getchannel('A').tobytes() == image.getchannel('A').tobytes()


def test_median_and_sharpen_methods():
    image = Image.new('RGBA', (16, 16), (40, 80, 120, 170))
    image.putpixel((8, 8), (255, 255, 255, 170))
    output = execute('image-repair', [picture(image)], {'regions':'[]'})
    assert Image.open(io.BytesIO(output.files[0].data)).getpixel((8, 8)) == (40, 80, 120, 170)
    for method in ['unsharp', 'deconvolution']:
        result = execute('image-sharpen', [picture(image)], {'method':method, 'iterations':2})
        repaired = Image.open(io.BytesIO(result.files[0].data))
        assert repaired.size == image.size
        assert repaired.getchannel('A').tobytes() == image.getchannel('A').tobytes()


@pytest.mark.parametrize('tool,opts', [('color-picker', {'x':True}), ('image-extract-colors', {'colors':1}), ('image-sharpen', {'radius':float('nan')}), ('image-remove-watermark', {'regions':[]})])
def test_invalid_image_options(tool, opts):
    with pytest.raises(OneKitError):
        execute(tool, [picture(Image.new('RGB', (10, 10)))], opts)


def test_fillable_fields_survive_roundtrip_and_can_be_filled():
    fields = [{'name':name, 'type':kind, 'x':.1, 'y':.1+i*.2, 'width':.4, 'height':.1, **({'choices':['One','Two']} if kind=='choice' else {})} for i,(name,kind) in enumerate([('Name','text'),('Consent','checkbox'),('Select','choice')])]
    result = execute('pdf-make-fillable', [pdf()], {'fields':json.dumps(fields)})
    reader = PdfReader(io.BytesIO(result.files[0].data))
    assert set(reader.get_fields()) == {'Name','Consent','Select'}
    assert all('/AP' in ref.get_object() for ref in reader.pages[0]['/Annots'])
    writer = PdfWriter(clone_from=reader)
    writer.update_page_form_field_values(writer.pages[0], {'Name':'Example', 'Consent':'/Yes', 'Select':'Two'}, auto_regenerate=False)
    out = io.BytesIO(); writer.write(out)
    updated = PdfReader(io.BytesIO(out.getvalue())).get_fields()
    assert updated['Name']['/V'] == 'Example'
    assert updated['Consent']['/V'] == '/Yes'
    assert updated['Select']['/V'] == 'Two'
    more = execute('pdf-make-fillable', result.files, {'fields':[{'name':'Extra', 'x':.1,'y':.8,'width':.4,'height':.1}]})
    assert len(PdfReader(io.BytesIO(more.files[0].data)).get_fields()) == 4
    with pytest.raises(OneKitError, match='already exists'):
        execute('pdf-make-fillable', result.files, {'fields':fields})


@pytest.mark.parametrize('rotation,expected', [(0,[20,210,80,240]),(90,[40,30,60,120]),(180,[120,60,180,90]),(270,[140,180,160,270])])
def test_form_display_coordinates(rotation, expected):
    writer = PdfWriter(); page = writer.add_blank_page(200,300);page.rotate(rotation)
    assert field_rectangle(page, {'x':.1,'y':.2,'width':.3,'height':.1}) == pytest.approx(expected)


def test_tagged_watermark_removal_preserves_other_objects():
    source = pdf(b'q 0 0 10 10 re f Q /Artifact << /Subtype /Watermark >> BDC q 1 1 5 5 re f Q EMC q 20 20 10 10 re S Q')
    result = execute('pdf-remove-watermark', [source])
    content = PdfReader(io.BytesIO(result.files[0].data)).pages[0].get_contents().get_data()
    assert b'Watermark' not in content
    assert b'20 20 10 10 re' in content and b'0 0 10 10 re' in content
    assert result.details['removedObjects'] == 1
    with pytest.raises(OneKitError, match='No matching'):
        execute('pdf-remove-watermark', [pdf()])


def test_exact_text_watermark_only():
    from reportlab.pdfgen import canvas
    buffer = io.BytesIO(); c=canvas.Canvas(buffer);c.drawString(10,100,'WATERMARK');c.drawString(10,50,'Keep WATERMARK context');c.save()
    result = execute('pdf-remove-watermark', [Artifact('source.pdf',buffer.getvalue())], {'text':'WATERMARK'})
    text = PdfReader(io.BytesIO(result.files[0].data)).pages[0].extract_text()
    assert text.strip() == 'Keep WATERMARK context'
