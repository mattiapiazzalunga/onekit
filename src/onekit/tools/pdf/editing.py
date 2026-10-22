# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Edit text drawing instructions without rasterizing or covering the page.

The inspect/edit protocol is used by the CLI and Python API. IDs identify original
page content operations; stale originals and unavailable glyphs fail explicitly.
Form XObjects and OCR are deliberately excluded from this first editable subset.
"""
import io
import json
import math

from pypdf import PdfWriter
from pypdf._cmap import get_encoding
from pypdf._text_extraction import mult
from pypdf.generic import ArrayObject, ByteStringObject, ContentStream, FloatObject, NameObject
from pypdf.generic._font import Font

from ...models import OneKitError, Result, output


def font_codec(resource):
    # Isolate pypdf's encoding adapter here (pypdf >=6.20.1,<7).
    if str(resource.get('/Encoding', '')).endswith('-V'):
        raise NotImplementedError('Vertical font encodings are not editable.')
    encoding, mapping = get_encoding(resource)
    reverse = {}
    if isinstance(encoding, dict):
        for code, char in encoding.items():
            if mapping and char not in mapping:
                continue
            char = mapping.get(char, char)
            if isinstance(char, str) and char:
                reverse.setdefault(char, bytes([code]))
    else:
        for code, char in mapping.items():
            if isinstance(code, str) and isinstance(char, str) and char:
                reverse.setdefault(char, code.encode(encoding, 'strict'))

    def decode(raw):
        if isinstance(encoding, dict):
            intermediate = ''.join(encoding.get(code, chr(code)) for code in raw)
        else:
            intermediate = raw.decode(encoding, 'strict')
        return ''.join(mapping.get(char, char) for char in intermediate)

    def encode(text):
        # A ToUnicode entry can represent a ligature, so consume longest first.
        keys = sorted(reverse, key=len, reverse=True)
        result, index = bytearray(), 0
        while index < len(text):
            key = next((key for key in keys if text.startswith(key, index)), None)
            if key is None:
                raise OneKitError(f"The original font does not contain {text[index]!r}. Choose different text.")
            result.extend(reverse[key])
            index += len(key)
        return bytes(result)

    return decode, encode, encoding


def page_runs(page, pdf):
    stream = ContentStream(page.get_contents(), pdf, 'bytes')
    resources = page.get('/Resources', {})
    if hasattr(resources, 'get_object'):
        resources = resources.get_object()
    fonts = resources.get('/Font', {})
    if hasattr(fonts, 'get_object'):
        fonts = fonts.get_object()
    state = {'font': None, 'size': 12., 'char': 0., 'word': 0., 'scale': 100., 'render': 0,
             'leading': 0., 'rise': 0., 'cm': [1., 0., 0., 1., 0., 0.]}
    tm = [1., 0., 0., 1., 0., 0.]
    line = list(tm)
    stack, runs, cache = [], [], {}
    for index, (args, op) in enumerate(stream.operations):
        if op == b'q':
            stack.append(dict(state))
        elif op == b'Q' and stack:
            state = stack.pop()
        elif op == b'Tf':
            state['font'], state['size'] = str(args[0]), float(args[1])
        elif op == b'cm':
            state['cm'] = mult([float(value) for value in args], state['cm'])
        elif op == b'BT':
            tm = [1., 0., 0., 1., 0., 0.]
            line = list(tm)
        elif op == b'Tm':
            tm = [float(value) for value in args]
            line = list(tm)
        elif op in (b'Td', b'TD'):
            tx, ty = map(float, args)
            if op == b'TD':
                state['leading'] = -ty
            line = [*line[:4], line[4] + tx * line[0] + ty * line[2],
                    line[5] + tx * line[1] + ty * line[3]]
            tm = list(line)
        elif op == b'T*':
            line = [*line[:4], line[4] - state['leading'] * line[2],
                    line[5] - state['leading'] * line[3]]
            tm = list(line)
        elif op in (b'Tc', b'Tw', b'Tz', b'Tr', b'TL', b'Ts'):
            state[{b'Tc': 'char', b'Tw': 'word', b'Tz': 'scale', b'Tr': 'render',
                   b'TL': 'leading', b'Ts': 'rise'}[op]] = float(args[0])
        if op in (b"'", b'"'):
            if op == b'"':
                state['word'], state['char'] = float(args[0]), float(args[1])
            line = [*line[:4], line[4] - state['leading'] * line[2],
                    line[5] - state['leading'] * line[3]]
            tm = list(line)
        if op in (b'Tj', b'TJ', b"'", b'"') and state['font'] in fonts:
            name = state['font']
            try:
                if name not in cache:
                    resource = fonts[name].get_object()
                    cache[name] = (*font_codec(resource), Font.from_font_resource(resource))
                decode, encode, encoding, font = cache[name]
                parts = args[0] if op == b'TJ' else args[-1:] if op == b'"' else args
                raw = b''.join(bytes(part) for part in parts if isinstance(part, bytes))
                text = decode(raw)
                if not math.isfinite(state['size']) or state['size'] <= 0:
                    continue

                def width(data, parts, size=state['size'], spacing=state['char'], word=state['word'],
                          font=font, encoding=encoding):
                    codes = ''.join(chr(code) for code in data) if isinstance(encoding, dict) else data.decode(encoding)
                    return (font.get_text_width(codes)
                            + (len(codes) * spacing + data.count(b' ') * word) * 1000 / size
                            - sum(float(part) for part in parts if not isinstance(part, bytes)))

                advance = width(raw, parts)
                matrix = mult(tm, state['cm'])
                if text.strip() and op in (b'Tj', b'TJ') and state['render'] in (0, 1, 2):
                    runs.append({'id': str(index), 'text': text, 'font': name, 'fontSize': state['size'],
                                 'x': matrix[4] + state['rise'] * matrix[2],
                                 'y': matrix[5] + state['rise'] * matrix[3],
                                 '_encode': encode, '_width': width, '_advance': advance,
                                 '_scale': state['scale']})
                distance = advance * state['size'] * state['scale'] / 100000
                tm = [*tm[:4], tm[4] + distance * tm[0], tm[5] + distance * tm[1]]
            except (UnicodeError, ValueError, KeyError, TypeError, NotImplementedError):
                continue
    return stream, runs


def edit_pdf(reader, source, options):
    mode = options.get('mode', 'edit')
    if mode not in ('inspect', 'edit'):
        raise OneKitError("Edit PDF mode must be inspect or edit.")
    writer = PdfWriter(clone_from=reader)
    edits = options.get('edits')
    if isinstance(edits, str):
        try:
            edits = json.loads(edits)
        except ValueError as exc:
            raise OneKitError('Edits must be a JSON array.') from exc
    if mode == 'edit' and (not isinstance(edits, list) or not edits or len(edits) > 2000):
        raise OneKitError('Select text in the page and edit at least one text box (up to 2000 edits).')
    pages, changed, seen = [], 0, set()
    for page_number, page in enumerate(writer.pages, 1):
        stream, runs = page_runs(page, writer)
        pages.append({'page': page_number, 'runs': [{key: value for key, value in run.items()
                                                    if not key.startswith('_')} for run in runs]})
        if mode == 'inspect':
            continue
        replacements = {}
        by_id = {run['id']: run for run in runs}
        for edit in edits:
            if not isinstance(edit, dict) or type(edit.get('page')) is not int:
                raise OneKitError('Each edit needs a page, id, original and text.')
            if edit['page'] != page_number:
                continue
            ident = str(edit.get('id'))
            run = by_id.get(ident)
            token = (page_number, ident)
            if token in seen or run is None or edit.get('original') != run['text']:
                raise OneKitError('This text box no longer matches the original PDF. Reopen the file.')
            seen.add(token)
            text = edit.get('text')
            if not isinstance(text, str) or len(text) > 10000 or any(ord(char) < 32 for char in text):
                raise OneKitError('Use a single line of text, up to 10000 characters per box.')
            raw = run['_encode'](text)
            new_width = run['_width'](raw, [])
            old_width = run['_advance']
            fit_width = old_width
            if 'fitIds' in edit:
                ids = edit['fitIds']
                if (not isinstance(ids, list) or not ids or len(ids) > 64
                        or len(set(ids)) != len(ids) or str(ids[0]) != ident):
                    raise OneKitError('Invalid combined text box.')
                group = [by_id.get(str(value)) for value in ids]
                if any(part is None or part['font'] != run['font']
                       or part['fontSize'] != run['fontSize'] for part in group):
                    raise OneKitError('Combined text boxes must use the same font and size.')
                fit_width = sum(part['_advance'] for part in group)
            ratio = min(1., fit_width / new_width) if fit_width > 0 and new_width > 0 else 1.
            scale = run['_scale']
            # Keep the original cursor advance so later text does not drift.
            adjustment = new_width - old_width / ratio
            instruction = ([ArrayObject([ByteStringObject(raw), FloatObject(adjustment)])], b'TJ')
            replacements[int(ident)] = [([FloatObject(scale * ratio)], b'Tz'), instruction,
                                         ([FloatObject(scale)], b'Tz')]
            changed += 1
        if replacements:
            stream.operations = [instruction for index, instruction in enumerate(stream.operations)
                                 for instruction in replacements.get(index, [instruction])]
            # replace_contents can overwrite a stream shared by other pages.
            page[NameObject('/Contents')] = writer._add_object(stream)
    if mode == 'inspect':
        details = {'pages': pages, 'editableRuns': sum(len(page['runs']) for page in pages)}
        return Result([output(source, 'text-boxes.json', json.dumps(details))], details=details)
    if changed != len(edits):
        raise OneKitError('An edit refers to a page that does not exist.')
    data = io.BytesIO()
    writer.write(data)
    warnings = ['The edited copy is not password protected. Protect it again if needed.'] if reader.is_encrypted else []
    return Result([output(source, 'edited.pdf', data.getvalue())], warnings=warnings,
                  details={'textBoxesEdited': changed})
