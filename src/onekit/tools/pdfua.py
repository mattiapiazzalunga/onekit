# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Tagged PDF/UA-1 text export; semantics come from the supplied plain text."""
import io
import re
from html import escape
from pathlib import Path

from ..execution import current_context
from ..models import OneKitError, Result, output


def run(tool, files, options):
    import reportlab
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import (ArrayObject, BooleanObject, DecodedStreamObject,
                               DictionaryObject, NameObject, NumberObject, TextStringObject)

    file = files[0]
    title = str(options.get('title', file.stem)).strip()
    language = str(options.get('language', 'en')).strip()
    text = file.text()
    if (not title or len(title) > 300 or re.search(r'[\x00-\x1f\x7f]', title)
            or not re.fullmatch(r'[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*', language)):
        raise OneKitError('Choose a document title and a valid language tag.')
    if len(text.encode('utf-8')) > 256 * 1024 or not text.strip():
        raise OneKitError('Use a non-empty text file up to 256 KiB.')
    font = 'OneKitAccessible'
    if font not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(font, str(Path(reportlab.__file__).parent / 'fonts/Vera.ttf')))
    supported = pdfmetrics.getFont(font).face.charToGlyph
    if any(ord(char) not in supported and char not in '\n\r\t' for char in title + text):
        raise OneKitError('The PDF font does not support this text. Choose text with supported characters.')
    tags = []
    counts = {}

    class TaggedParagraph(Paragraph):
        def __init__(self, *args, role='P', **kwargs):
            self.role = role
            super().__init__(*args, **kwargs)

        def split(self, *args):
            parts = super().split(*args)
            for part in parts:
                part.role = self.role
            return parts

        def draw(self):
            page = self.canv.getPageNumber() - 1
            mcid = counts.get(page, 0)
            counts[page] = mcid + 1
            tags.append((page, mcid, self.role))
            self.canv._code.append('/%s <</MCID %d>> BDC' % (self.role, mcid))
            super().draw()
            self.canv._code.append('EMC')

    style = ParagraphStyle('accessible', fontName=font, fontSize=11, leading=16, spaceAfter=9)
    heading = ParagraphStyle('title', parent=style, fontSize=20, leading=26, spaceAfter=16)
    story = [TaggedParagraph(escape(title), heading, role='H1')]
    # Blank lines delimit paragraphs; single line breaks are preserved explicitly.
    for paragraph in re.split(r'\n\s*\n', text.replace('\r\n', '\n').replace('\r', '\n')):
        if paragraph.strip():
            if len(story) >= current_context().document_limits.max_blocks:
                raise OneKitError('Document is too complex; split it into smaller files.')
            story.append(TaggedParagraph(escape(paragraph.expandtabs(4)).replace('\n', '<br/>'), style))
    stream = io.BytesIO()

    def page(canvas, document):
        if canvas.getPageNumber() > current_context().document_limits.max_pages:
            raise OneKitError('Document has too many pages.')

    document = SimpleDocTemplate(stream, title=title, initialFontName=font, pagesize=(595.28, 841.89),
                                 leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    document.build(story, onFirstPage=page, onLaterPages=page)
    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(stream.getvalue())))
    # ReportLab reserves byte zero for .notdef and maps that unused glyph to
    # U+0000. No source controls are accepted; use the Unicode replacement
    # character for .notdef so the exported CMap has no prohibited mapping.
    for page_object in writer.pages:
        for ref in page_object['/Resources'].get('/Font', {}).values():
            cmap = ref.get_object().get('/ToUnicode')
            if cmap is not None:
                cmap = cmap.get_object()
                cmap.set_data(re.sub(rb'(<[0-9A-Fa-f]{2}>\s*)<0000>', rb'\1<FFFD>', cmap.get_data()))
    root = writer.root_object
    tree = DictionaryObject({NameObject('/Type'): NameObject('/StructTreeRoot')})
    tree_ref = writer._add_object(tree)
    document_tag = DictionaryObject({NameObject('/Type'): NameObject('/StructElem'),
        NameObject('/S'): NameObject('/Document'), NameObject('/P'): tree_ref})
    document_ref = writer._add_object(document_tag)
    kids = ArrayObject()
    parent_arrays = [ArrayObject() for _ in writer.pages]
    for page_index, mcid, role in tags:
        element = DictionaryObject({NameObject('/Type'): NameObject('/StructElem'),
            NameObject('/S'): NameObject('/' + role), NameObject('/P'): document_ref,
            NameObject('/Pg'): writer.pages[page_index].indirect_reference,
            NameObject('/K'): NumberObject(mcid)})
        ref = writer._add_object(element)
        kids.append(ref)
        parent_arrays[page_index].append(ref)
    document_tag[NameObject('/K')] = kids
    nums = ArrayObject()
    for index, page_object in enumerate(writer.pages):
        page_object[NameObject('/StructParents')] = NumberObject(index)
        page_object[NameObject('/Tabs')] = NameObject('/S')
        nums.extend([NumberObject(index), parent_arrays[index]])
    tree.update({NameObject('/K'): ArrayObject([document_ref]),
                 NameObject('/ParentTree'): writer._add_object(DictionaryObject({NameObject('/Nums'): nums})),
                 NameObject('/ParentTreeNextKey'): NumberObject(len(writer.pages))})
    root.update({NameObject('/StructTreeRoot'): tree_ref, NameObject('/Lang'): TextStringObject(language),
                 NameObject('/MarkInfo'): DictionaryObject({NameObject('/Marked'): BooleanObject(True)}),
                 NameObject('/ViewerPreferences'): DictionaryObject({NameObject('/DisplayDocTitle'): BooleanObject(True)})})
    metadata = DecodedStreamObject()
    metadata.set_data(('<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>'
        '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
        '<rdf:Description rdf:about="" xmlns:pdfuaid="http://www.aiim.org/pdfua/ns/id/" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/"><pdfuaid:part>1</pdfuaid:part>'
        '<dc:title><rdf:Alt><rdf:li xml:lang="x-default">' + escape(title) + '</rdf:li></rdf:Alt></dc:title>'
        '<dc:language><rdf:Bag><rdf:li>' + escape(language) + '</rdf:li></rdf:Bag></dc:language>'
        '</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>').encode('utf-8'))
    metadata.update({NameObject('/Type'): NameObject('/Metadata'), NameObject('/Subtype'): NameObject('/XML')})
    root[NameObject('/Metadata')] = writer._add_object(metadata)
    writer.add_metadata({'/Title': title, '/Producer': 'OneKit'})
    result = io.BytesIO()
    writer.write(result)
    return Result([output(file, 'pdf', result.getvalue())], details={'profile': 'ua1',
                   'verdict': 'not_checked', 'compliant': None, 'requires_manual_review': True})
