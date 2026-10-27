# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Bounded, offline markup exports without native document executables.

This is an intentionally small document model, not a CSS or TeX renderer.
No URL is resolved, and all source text is escaped before writing output.
"""
import io
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path

from ..execution import current_context
from ..models import OneKitError, Result, output

IGNORED = {'script', 'style', 'head', 'iframe', 'object', 'embed', 'template'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
BLOCKS = {'p', 'div', 'section', 'article', 'main', 'header', 'footer', 'blockquote', 'pre',
          'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {'tag': 'root', 'children': []}
        self.stack = [self.root]
        self.count = 0

    def add(self, value):
        self.count += 1
        if self.count > current_context().document_limits.max_nodes:
            raise OneKitError('Document is too complex; split it into smaller files.')
        self.stack[-1]['children'].append(value)

    def handle_starttag(self, tag, attrs):
        element = {'tag': tag, 'attrs': dict(attrs), 'children': []}
        self.add(element)
        if tag not in VOID:
            if len(self.stack) >= current_context().document_limits.max_depth:
                raise OneKitError('Document nesting is too complex.')
            self.stack.append(element)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack)-1, 0, -1):
            if self.stack[index]['tag'] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.add(data)


def plain(value):
    if isinstance(value, str):
        return value
    if value['tag'] in IGNORED:
        return ''
    return ''.join(plain(child) for child in value['children'])


def latex_escape(text):
    special = {'\\': r'\textbackslash{}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(special.get(char, '\\'+char if char in '{}#$%&_' else char) for char in text)


def read_document(text, source):
    if re.search(r'[\x00-\x08\x0b\x0e-\x1f\x7f]', text):
        raise OneKitError('Binary content is not accepted by this text tool.')
    if source == 'md':
        from markdown_it import MarkdownIt
        text = MarkdownIt('commonmark', {'html': False, 'maxNesting': 32}).render(text)
    reader = Reader()
    reader.feed(text)
    reader.close()
    return reader.root


def document_blocks(root):
    """Flatten structural containers while retaining lists, code and headings."""
    blocks = []
    warnings = set()

    def visit(elements, quote=False, level=0):
        pending = []

        def flush():
            if any(plain(item).strip() for item in pending):
                blocks.append(('blockquote' if quote else 'p', list(pending), level))
            pending.clear()

        for element in elements:
            if isinstance(element, str):
                pending.append(element)
                continue
            tag = element['tag']
            children = element['children']
            if tag in IGNORED:
                warnings.add('Active content is omitted.')
                continue
            if tag == 'img':
                warnings.add('Images are represented by their alternative text; remote images are not fetched.')
                pending.append(element['attrs'].get('alt') or '[image]')
            elif tag not in BLOCKS:
                pending.append(element)
            else:
                flush()
                if tag in {'p', 'pre', 'hr'} or re.fullmatch(r'h[1-6]', tag):
                    blocks.append((tag, children, level))
                elif tag in {'ul', 'ol'}:
                    try:
                        first = int(element['attrs'].get('start', 1))
                    except (ValueError, TypeError):
                        first = 1
                    items = [item for item in children if isinstance(item, dict) and item['tag'] == 'li']
                    for index, item in enumerate(items):
                        marker = f'{first+index}. ' if tag == 'ol' else '• '
                        first_block = len(blocks)
                        visit(item['children'], quote, level+1)
                        if len(blocks) > first_block and blocks[first_block][0] != 'pre':
                            blocks[first_block][1].insert(0, marker)
                        else:
                            blocks.insert(first_block, ('p', [marker], level+1))
                elif tag == 'tr':
                    warnings.add('Tables are represented by text rows.')
                    blocks.append(('p', [' | '.join(plain(cell).strip() for cell in children if isinstance(cell, dict))], level))
                else:
                    visit(children, quote or tag == 'blockquote', level)
        flush()
        if len(blocks) > current_context().document_limits.max_blocks:
            raise OneKitError('Document has too many text blocks.')

    visit(root['children'])
    return blocks, sorted(warnings)


def inline(values, target):
    result = []
    esc = latex_escape if target == 'latex' else escape
    for value in values:
        if isinstance(value, str):
            result.append(esc(re.sub(r'\s+', ' ', value)))
            continue
        tag = value['tag']
        if tag in IGNORED:
            continue
        if tag == 'br':
            result.append('\\\\\n' if target == 'latex' else '<br/>')
            continue
        if tag == 'img':
            result.append(esc(value['attrs'].get('alt') or '[image]'))
            continue
        content = inline(value['children'], target)
        style = {'strong': 'b', 'b': 'b', 'em': 'i', 'i': 'i', 'code': 'code'}.get(tag)
        if style and target == 'latex':
            command = {'b': 'textbf', 'i': 'emph', 'code': 'texttt'}[style]
            content = '\\'+command+'{'+content+'}'
        elif style in {'b', 'i'}:
            content = f'<{style}>{content}</{style}>'
        # Links remain inert text. In particular no PDF writer receives source URLs.
        result.append(content)
    return ''.join(result)


def write_latex(blocks):
    lines = [r'\documentclass{article}', r'\usepackage[utf8]{inputenc}', r'\usepackage[T1]{fontenc}', r'\begin{document}']
    for tag, values, level in blocks:
        if tag == 'pre':
            lines.append(r'\par\begingroup\ttfamily\obeyspaces'+'\n'+latex_escape(''.join(plain(item) for item in values)).replace('\n', '\\\\\n')+'\n'+r'\par\endgroup')
        elif tag == 'hr':
            lines.append(r'\par\noindent\rule{\linewidth}{0.4pt}')
        elif re.fullmatch(r'h[1-6]', tag):
            command = ['section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph', 'subparagraph'][int(tag[1])-1]
            lines.append('\\'+command+'*{'+inline(values, 'latex').strip()+'}')
        else:
            lines.append(inline(values, 'latex').strip()+'\n')
    return '\n'.join([*lines, r'\end{document}', ''])


def write_pdf(blocks):
    import reportlab
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import HRFlowable, Paragraph, Preformatted, SimpleDocTemplate

    font_dir = Path(reportlab.__file__).parent/'fonts'
    for name, filename in [('PortableRegular', 'Vera.ttf'), ('PortableBold', 'VeraBd.ttf'), ('PortableItalic', 'VeraIt.ttf'), ('PortableBoldItalic', 'VeraBI.ttf')]:
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(font_dir/filename)))
    pdfmetrics.registerFontFamily('PortableRegular', normal='PortableRegular', bold='PortableBold', italic='PortableItalic', boldItalic='PortableBoldItalic')
    supported = pdfmetrics.getFont('PortableRegular').face.charToGlyph
    story = []
    for tag, values, level in blocks:
        for char in ''.join(plain(value) for value in values):
            if not char.isspace() and ord(char) not in supported:
                raise OneKitError(f'The document font does not support U+{ord(char):04X}. Export LaTeX instead.')
        heading = bool(re.fullmatch(r'h[1-6]', tag))
        size = max(12, 24-(int(tag[1])-1)*2) if heading else 10 if tag == 'pre' else 11
        style = ParagraphStyle('portable', fontName='PortableBold' if heading else 'PortableRegular',
                               fontSize=size, leading=size*1.4, spaceAfter=7,
                               leftIndent=min(level, 6)*18+(18 if tag == 'blockquote' else 0), splitLongWords=True)
        if tag == 'hr':
            story.append(HRFlowable(width='100%', spaceAfter=14))
        elif tag == 'pre':
            story.append(Preformatted(''.join(plain(value) for value in values), style, maxLineLength=70))
        else:
            story.append(Paragraph(inline(values, 'pdf'), style))
    stream = io.BytesIO()
    document = SimpleDocTemplate(stream, pagesize=(595.28, 841.89), leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    pages = 0

    def page(canvas, document):
        nonlocal pages
        pages += 1
        if pages > current_context().document_limits.max_pages:
            raise OneKitError(f'Export at most {current_context().document_limits.max_pages} pages. Shorten the document.')

    if not story:
        story.append(Paragraph(' ', ParagraphStyle('empty', fontName='PortableRegular')))
    document.build(story, onFirstPage=page, onLaterPages=page)
    return stream.getvalue(), pages


def convert(file, source, target):
    if source not in {'md', 'html'} or target not in {'pdf', 'latex'}:
        raise OneKitError('Unsupported portable document conversion.')
    blocks, warnings = document_blocks(read_document(file.text(), source))
    if target == 'latex':
        return Result([output(file, 'tex', write_latex(blocks))], warnings=warnings)
    data, pages = write_pdf(blocks)
    return Result([output(file, 'pdf', data)], warnings=warnings, details={'pages': pages})
