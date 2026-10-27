# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import zipfile

import pytest

from onekit import Artifact, OneKitError
from onekit.tools import structured_data, text_converters
from onekit.tools.epub_pdf import epub_html


@pytest.mark.parametrize('value', ['Plain text', 'Caffè 漢字 😀', '\t\n\r', '\x7f\x85', '\ufffd', '\U0010ffff'])
def test_text_scanners_keep_valid_unicode(value):
    assert structured_data.xml_text(value) == value
    assert text_converters.read_text(Artifact('a.txt', value.encode()), {}) == value.replace('\r', '\n')


@pytest.mark.parametrize('character', [chr(i) for i in range(32) if i not in (9, 10, 13)])
def test_text_scanners_reject_binary_controls(character):
    value = 'valid Unicode é' + character + ' tail'
    with pytest.raises(OneKitError, match='XML cannot represent'):
        structured_data.xml_text(value)
    with pytest.raises(OneKitError, match='binary control'):
        text_converters.read_text(Artifact('a.txt', value.encode()), {})


@pytest.mark.parametrize('character', ['\ud800', '\udbff', '\udc00', '\udfff', '\ufffe', '\uffff'])
def test_xml_scanner_rejects_invalid_unicode(character):
    with pytest.raises(OneKitError, match='XML cannot represent'):
        structured_data.xml_text('prefix' + character + 'suffix')


def epub(chapters):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('mimetype', 'application/epub+zip')
        archive.writestr('META-INF/container.xml', '<container><rootfile full-path="book.opf"/></container>')
        manifest = ''.join(f'<item id="c{i}" href="c{i}.html" media-type="text/html"/>' for i in range(len(chapters)))
        spine = ''.join(f'<itemref idref="c{i}"/>' for i in range(len(chapters)))
        archive.writestr('book.opf', f'<package><manifest>{manifest}</manifest><spine>{spine}</spine></package>')
        for i, chapter in enumerate(chapters):
            archive.writestr(f'c{i}.html', chapter)
    return Artifact('book.epub', stream.getvalue())


def test_epub_budget_counts_bytes_and_excludes_join_separator():
    chapters = ['é'.encode() * (2 * 1024 * 1024)] * 2
    text, count = epub_html(epub(chapters))
    assert count == 2 and text == '\n'.join(chapter.decode() for chapter in chapters)
    with pytest.raises(OneKitError, match='exceeds 8 MiB'):
        epub_html(epub([*chapters[:-1], chapters[-1] + b'x']))


def test_slide_budget_counts_characters_and_preserves_separators(monkeypatch):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as archive:
        archive.writestr('ppt/presentation.xml', '<presentation xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sldId r:id="a"/><sldId r:id="b"/></presentation>')
        archive.writestr('ppt/_rels/presentation.xml.rels', '<Relationships><Relationship Id="a" Target="slides/a.xml"/><Relationship Id="b" Target="slides/b.xml"/></Relationships>')
        for name, text in [('a', 'Aé'), ('b', 'BCD')]:
            archive.writestr(f'ppt/slides/{name}.xml', f'<slide xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:p><a:t>{text}</a:t></a:p></slide>')
    file = Artifact('slides.pptx', stream.getvalue())
    monkeypatch.setattr(text_converters, 'MAX_TEXT', 5)
    assert text_converters.slide_text(file) == ('Aé\n\nBCD', 2)
    monkeypatch.setattr(text_converters, 'MAX_TEXT', 4)
    with pytest.raises(OneKitError, match='8 MiB'):
        text_converters.slide_text(file)
