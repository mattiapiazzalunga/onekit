import io

import pytest
from PIL import Image, PngImagePlugin
from pypdf import PdfReader
from test_core import pdf

from onekit import Artifact, OneKitError, execute
from onekit.tools.file_metadata import read_metadata


@pytest.mark.parametrize('kind', ['png', 'jpeg', 'pdf'])
def test_reads_existing_editable_metadata_without_modifying_the_file(kind):
    if kind == 'pdf':
        file = pdf()
    else:
        stream = io.BytesIO()
        Image.new('RGB', (24, 16), 'red').save(stream, format=kind.upper())
        file = Artifact('sample.' + kind, stream.getvalue())
    expected = {'Title': 'Caffè Ω', 'Author': 'OneKit', 'Subject': 'Subject', 'Keywords': 'one; two', 'Comment': 'Hello'}
    edited = execute('file-metadata-set', [file], {'metadata': expected}).files[0]
    original_bytes = edited.data
    assert read_metadata(edited) == expected
    assert edited.data == original_bytes


def test_reads_legacy_exif_and_compressed_png_text():
    stream = io.BytesIO()
    exif = Image.Exif()
    exif[270], exif[315] = 'Existing description', 'Existing artist'
    Image.new('RGB', (4, 4)).save(stream, format='JPEG', exif=exif)
    assert read_metadata(Artifact('legacy.jpg', stream.getvalue())) == {'Title': 'Existing description', 'Author': 'Existing artist'}
    stream = io.BytesIO()
    info = PngImagePlugin.PngInfo()
    info.add_text('Title', 'Compressed', zip=True)
    info.add_itxt('Author', 'Caffè Ω', zip=True)
    Image.new('RGB', (4, 4)).save(stream, format='PNG', pnginfo=info)
    assert read_metadata(Artifact('compressed.png', stream.getvalue())) == {'Title': 'Compressed', 'Author': 'Caffè Ω'}


def test_metadata_reader_rejects_unsupported_files_and_text_expansion():
    with pytest.raises(OneKitError, match='supports PDF'):
        read_metadata(Artifact('file.txt', b'text'))
    stream = io.BytesIO()
    info = PngImagePlugin.PngInfo()
    info.add_text('Title', 'x' * (1024 * 1024 + 1), zip=True)
    Image.new('RGB', (4, 4)).save(stream, format='PNG', pnginfo=info)
    with pytest.raises(OneKitError, match='text limit'):
        read_metadata(Artifact('expansion.png', stream.getvalue()))


def test_xmp_and_pdf_document_info_use_standard_field_precedence():
    from pypdf import PdfWriter
    from pypdf.generic import DecodedStreamObject, NameObject

    from onekit.tools.file_metadata import _xmp_fields
    xmp = b'''<x:xmpmeta xmlns:x="adobe:ns:meta/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/"><rdf:RDF><rdf:Description><dc:title><rdf:Alt><rdf:li xml:lang="x-default">XMP title</rdf:li></rdf:Alt></dc:title><dc:creator><rdf:Seq><rdf:li>Existing author</rdf:li></rdf:Seq></dc:creator></rdf:Description></rdf:RDF></x:xmpmeta>'''
    assert _xmp_fields(xmp) == {'Title': 'XMP title', 'Author': 'Existing author'}
    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(pdf().data)))
    writer.metadata = None
    writer.add_metadata({'/Title': 'Document title'})
    stream = DecodedStreamObject()
    stream.set_data(xmp)
    writer.root_object[NameObject('/Metadata')] = writer._add_object(stream)
    output = io.BytesIO()
    writer.write(output)
    original = Artifact('xmp.pdf', output.getvalue())
    assert read_metadata(original) == {'Title': 'Document title', 'Author': 'Existing author'}
    edited = execute('file-metadata-set', [original], {'metadata': {'Title': 'Changed'}}).files[0]
    assert read_metadata(edited) == {'Title': 'Changed', 'Author': 'Existing author'}
    with pytest.raises(OneKitError, match='declarations'):
        _xmp_fields('<!DOCTYPE x [<!ENTITY e "value">]><x>&e;</x>')


def test_malformed_optional_xmp_does_not_block_pdf_metadata_editing():
    from pypdf import PdfWriter
    from pypdf.generic import DecodedStreamObject, NameObject
    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(pdf().data)))
    writer.metadata = None
    writer.add_metadata({'/Author': 'Keep this author'})
    xmp = DecodedStreamObject()
    xmp.set_data(b'<invalid')
    writer.root_object[NameObject('/Metadata')] = writer._add_object(xmp)
    stream = io.BytesIO()
    writer.write(stream)
    file = Artifact('broken-xmp.pdf', stream.getvalue())
    assert read_metadata(file) == {'Author': 'Keep this author'}
    edited = execute('file-metadata-set', [file], {'metadata': {'Title': 'New title'}}).files[0]
    assert read_metadata(edited) == {'Title': 'New title', 'Author': 'Keep this author'}


@pytest.mark.parametrize('kind', ['png', 'jpeg', 'pdf'])
def test_metadata_roundtrip_preserves_content(kind):
    if kind == 'pdf':
        file = pdf()
    else:
        stream = io.BytesIO()
        image = Image.new('RGB', (24, 16), 'red')
        info = PngImagePlugin.PngInfo()
        info.add_text('Private', 'secret')
        image.save(stream, format=kind.upper(), **({'pnginfo': info} if kind == 'png' else {}))
        file = Artifact('sample.' + kind, stream.getvalue())
    edited = execute('file-metadata-set', [file], {'metadata': {'Title': 'Caffè', 'Author': 'OneKit'}}).files[0]
    cleaned = execute('file-metadata-remove', [edited]).files[0]
    if kind == 'pdf':
        before, after = PdfReader(io.BytesIO(edited.data)), PdfReader(io.BytesIO(cleaned.data))
        assert before.metadata.title == 'Caffè'
        assert not after.metadata
        assert [p.extract_text() for p in before.pages] == [p.extract_text() for p in after.pages]
    else:
        original = Image.open(io.BytesIO(file.data))
        before, after = Image.open(io.BytesIO(edited.data)), Image.open(io.BytesIO(cleaned.data))
        assert original.tobytes() == before.tobytes() == after.tobytes()
        if kind == 'png':
            assert before.info['Title'] == 'Caffè'
            assert before.info['Private'] == 'secret'
            assert not after.info
        else:
            assert before.getexif()[40091].decode('utf-16-le').rstrip('\0') == 'Caffè'
            assert not after.getexif()
            assert file.data[file.data.index(b'\xff\xda'):] == cleaned.data[cleaned.data.index(b'\xff\xda'):]


def test_metadata_rejects_invalid_fields_and_corrupt_png():
    with pytest.raises(OneKitError, match='Supported text fields'):
        execute('file-metadata-set', [pdf()], {'metadata': {'Title': {'nested': True}}})
    with pytest.raises(OneKitError, match='Provide a metadata object'):
        execute('file-metadata-set', [pdf()])
    from onekit.tools.file_metadata import png
    with pytest.raises(OneKitError, match='Truncated'):
        png(b'\x89PNG\r\n\x1a\n\x00', {}, True)


def test_pdf_removal_does_not_leave_detached_xmp_bytes():
    from pypdf import PdfWriter
    from pypdf.generic import DecodedStreamObject, NameObject
    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(pdf().data)))
    xmp = DecodedStreamObject()
    xmp.set_data(b'<private>SECRET-XMP-LOCATION</private>')
    reference = writer._add_object(xmp)
    writer.root_object[NameObject('/Metadata')] = reference
    writer.pages[0][NameObject('/Metadata')] = reference
    stream = io.BytesIO()
    writer.write(stream)
    cleaned = execute('file-metadata-remove', [Artifact('private.pdf', stream.getvalue())]).files[0]
    assert b'SECRET-XMP-LOCATION' not in cleaned.data


def test_progressive_jpeg_removal_clears_comments_after_scan():
    stream = io.BytesIO()
    Image.new('RGB', (32, 32), 'blue').save(stream, format='JPEG', progressive=True)
    data = stream.getvalue()
    secret = b'SECRET-LATE-COMMENT'
    comment = b'\xff\xfe' + (len(secret) + 2).to_bytes(2, 'big') + secret
    file = Artifact('progressive.jpg', data[:-2] + comment + data[-2:])
    cleaned = execute('file-metadata-remove', [file]).files[0]
    assert secret not in cleaned.data
    assert Image.open(io.BytesIO(cleaned.data)).tobytes() == Image.open(io.BytesIO(data)).tobytes()
