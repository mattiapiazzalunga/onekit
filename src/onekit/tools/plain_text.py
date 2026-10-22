# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Local text-only exports; markup is parsed, never rendered or executed."""
import io
import re
import zipfile
from html.parser import HTMLParser

from ..models import Artifact, OneKitError, Result
from ..validation import binary_signature, validate_zip

LIMIT = 8 * 1024 * 1024


class PlainHTML(HTMLParser):
    blocks = frozenset({"p", "div", "section", "article", "header", "footer", "main", "aside", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "dl", "dt", "dd", "table", "tr", "pre", "hr"})
    ignored = frozenset({"head", "script", "style", "template", "noscript", "iframe", "object", "svg"})

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.stack = [], []
        self.pre = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.stack:
            if tag == self.stack[-1]:
                self.stack.append(tag)
            return
        if tag in self.ignored or "hidden" in attrs or (attrs.get("aria-hidden") or "").lower() == "true":
            if tag not in ("br", "hr", "img", "input", "meta", "link", "source", "wbr", "area", "embed"):
                self.stack.append(tag)
            return
        if tag == "br" or tag in self.blocks:
            self.parts.append("\n")
        elif tag in ("td", "th") and self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\t")
        if tag == "pre":
            self.pre += 1

    def handle_endtag(self, tag):
        if self.stack:
            if tag == self.stack[-1]:
                self.stack.pop()
            return
        if tag in self.blocks:
            self.parts.append("\n")
        if tag == "pre":
            self.pre = max(0, self.pre - 1)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        if not self.stack:
            self.parts.append(data if self.pre else re.sub(r"\s+", " ", data))

    def result(self):
        text = "".join(self.parts).replace("\xa0", " ")
        text = re.sub(r" *\n *", "\n", text)
        return re.sub(r"\n{3,}", "\n\n", text).strip("\n")


def html_text(text):
    parser = PlainHTML()
    parser.feed(text)
    parser.close()
    return parser.result()


def docx_text(data):
    from defusedxml import ElementTree
    validate_zip(data, 32 * 1024 * 1024, "docx")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        info = archive.getinfo("word/document.xml")
        if info.file_size > 4 * 1024 * 1024:
            raise OneKitError("Word document text XML exceeds the 4 MiB inspection limit.")
        root = ElementTree.fromstring(archive.read(info))
    parts, pending, count = [], [(root, False)], 0
    while pending:
        node, closing = pending.pop()
        tag = node.tag.split("}")[-1]
        if closing:
            if tag == "p":
                parts.append("\n")
            elif tag == "tc":
                if parts and parts[-1] == "\n":
                    parts.pop()
                parts.append("\t")
            elif tag == "tr":
                if parts and parts[-1] == "\t":
                    parts.pop()
                parts.append("\n")
            continue
        count += 1
        if count > 100000:
            raise OneKitError("Word document exceeds the 100,000-node text limit.")
        if tag in ("del", "instrText"):
            continue
        if tag == "t":
            parts.append(node.text or "")
        elif tag == "tab":
            parts.append("\t")
        elif tag in ("br", "cr"):
            parts.append("\n")
        pending.append((node, True))
        pending.extend((child, False) for child in reversed(list(node)))
    return "".join(parts).rstrip("\n")


def run(tool, files, options):
    file = files[0]
    format = options.get("input_format", "auto")
    if format not in ("auto", "plain", "html", "markdown", "docx"):
        raise OneKitError("Choose automatic, plain text, HTML, Markdown or Word DOCX input.")
    if len(file.data) > LIMIT:
        raise OneKitError("Text cleanup supports inputs up to 8 MiB.")
    if format == "auto":
        format = {"html": "html", "md": "markdown", "docx": "docx"}.get(file.kind, "plain")
    warnings = []
    if format == "docx":
        text = docx_text(file.data)
        warnings.append("Word body text only: images, headers, footers, comments and automatic list numbering are not exported. No OCR is performed.")
    else:
        data = file.data
        try:
            text = data.decode("utf-16" if data.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")
        except UnicodeError as error:
            raise OneKitError("Use UTF-8 or UTF-16 with a byte-order mark, or convert the file encoding first.") from error
        if any(ord(char) < 32 and char not in "\n\r\t\f" for char in text) or binary_signature(data):
            raise OneKitError("Choose a text, HTML, Markdown or DOCX file; other binary files are not supported.")
        if format == "markdown":
            from markdown_it import MarkdownIt
            text = html_text(MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"]).render(text))
        elif format == "html":
            text = html_text(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
    if not text.strip():
        warnings.append("No readable text was found. This tool does not use OCR.")
    return Result([Artifact(file.stem + "-plain.txt", text.encode("utf-8"))], warnings,
                  {"input_format": format, "output_encoding": "UTF-8", "characters": len(text), "lines": len(text.splitlines())})
