# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Inspect and remove explicit PDF drawing objects, including nested forms.

Object identifiers address an invocation, not a shared resource. Modified forms
are copied so choosing one page never changes another use of the same resource.
"""
import json

from ..models import OneKitError, Result, output, parse_json

SHOW = (b'Tj', b'TJ', b"'", b'"')


def normalize(text):
    return ' '.join(text.split())


def process(writer, text='', objects=(), inspect=False):
    from pypdf.generic import ArrayObject, ContentStream, DecodedStreamObject, DictionaryObject, FloatObject, NameObject
    from pypdf.generic._font import Font

    from .pdf.editing import font_codec

    selected, matched, candidates = set(objects), set(), []
    count, budget = 0, 0
    target = normalize(text)

    def resolve(value):
        return value.get_object() if hasattr(value, 'get_object') else value

    def add(item):
        if inspect:
            if len(candidates) >= 2000:
                raise OneKitError('More than 2,000 selectable objects. Split the PDF into smaller documents first.')
            candidates.append(item)

    def rewrite(source, inherited, path, page_number, ancestors=(), inherited_font=None):
        nonlocal count, budget
        if len(ancestors) > 12:
            raise OneKitError('Nested PDF forms exceed the supported depth of 12.')
        resources = DictionaryObject(dict(resolve(inherited)))
        xobjects = DictionaryObject(dict(resolve(resources.get('/XObject', {}))))
        fonts = resolve(resources.get('/Font', {}))
        properties = resolve(resources.get('/Properties', {}))
        stream = ContentStream(source, writer, 'bytes')
        operations, kept, block, parts = stream.operations, [], [], []
        font, stack, codecs = inherited_font, [], {}
        size, char_space, word_space = 12., 0., 0.
        replacements, replacement_error = [], False
        depth, skipped, changed, start, readable = 0, None, False, 0, True

        def decoded(values, op):
            nonlocal readable
            raw_parts = values[0] if op == b'TJ' else values[-1:]
            raw = b''.join(bytes(part) for part in raw_parts if isinstance(part, bytes))
            try:
                if font not in fonts:
                    readable = False
                    return ''
                if font not in codecs:
                    codecs[font] = (*font_codec(resolve(fonts[font])), Font.from_font_resource(resolve(fonts[font])))
                return codecs[font][0](raw)
            except (UnicodeError, ValueError, KeyError, TypeError, NotImplementedError):
                readable = False
                return ''

        def empty_show(args, op):
            # Keep the original text advance without retaining invisible glyphs.
            if font not in codecs or size <= 0:
                raise ValueError('Font metrics unavailable')
            _, _, encoding, metric = codecs[font]
            values = args[0] if op == b'TJ' else args[-1:]
            advances = []
            for value in values:
                if isinstance(value, bytes):
                    codes = ''.join(chr(code) for code in value) if isinstance(encoding, dict) else value.decode(encoding)
                    width = metric.get_text_width(codes) + (len(codes)*char_space+value.count(b' ')*word_space)*1000/size
                    advances.append(FloatObject(-width))
                else:
                    advances.append(value)
            before = []
            if op == b'"':
                before = [([args[0]], b'Tw'), ([args[1]], b'Tc')]
            if op in (b"'", b'"'):
                before.append(([], b'T*'))
            return [*before, ([ArrayObject(advances)], b'TJ')]

        def acknowledge(index, op):
            identifier = f"{path}/{'t' if op == b'BT' else 'o'}{index}"
            if identifier in selected:
                matched.add(identifier)
            if op == b'Do':
                matched.update(item for item in selected if item.startswith(identifier+'/'))

        for index, (args, op) in enumerate(operations):
            budget += 1
            if budget > 300000:
                raise OneKitError('PDF drawing complexity exceeds 300,000 operations. Split the PDF first.')
            if op in (b'BDC', b'BMC'):
                tagged = False
                if op == b'BDC' and len(args) > 1 and args[0] == '/Artifact':
                    prop = resolve(properties.get(args[1], {})) if isinstance(args[1], NameObject) else resolve(args[1])
                    tagged = hasattr(prop, 'get') and prop.get('/Subtype') == '/Watermark'
                if tagged and skipped is None and not inspect:
                    skipped, changed = depth, True
                    count += 1
                depth += 1
                if skipped is not None:
                    continue
            elif op == b'EMC':
                depth -= 1
                if depth < 0:
                    raise OneKitError('Unbalanced marked PDF content.')
                if skipped is not None:
                    if depth == skipped:
                        skipped = None
                    continue
            if skipped is not None:
                if op in (b'BT', b'Do'):
                    acknowledge(index, op)
                continue
            if op == b'q':
                stack.append((font, size, char_space, word_space))
            elif op == b'Q' and stack:
                font, size, char_space, word_space = stack.pop()
            elif op == b'Tf' and args:
                font, size = str(args[0]), float(args[1])
            elif op == b'Tc':
                char_space = float(args[0])
            elif op == b'Tw':
                word_space = float(args[0])
            elif op == b'"':
                word_space, char_space = float(args[0]), float(args[1])
            if op == b'BT':
                if block:
                    raise OneKitError('Nested PDF text objects are unsupported.')
                start, block, parts, readable = index, [(args, op)], [], True
                replacements, replacement_error = [(args, op)], False
                continue
            if block:
                block.append((args, op))
                if op in SHOW:
                    parts.append(decoded(args, op))
                    try:
                        replacements.extend(empty_show(args, op))
                    except (UnicodeError, ValueError, KeyError, TypeError, NotImplementedError):
                        replacement_error = True
                else:
                    replacements.append((args, op))
                if op != b'ET':
                    continue
                label, identifier = normalize(''.join(parts)), f'{path}/t{start}'
                if any(operator in SHOW for _, operator in block):
                    add({'id':identifier, 'page':page_number, 'type':'text', 'text':label[:1000], 'readable':readable})
                remove = identifier in selected or target and readable and label == target
                if remove and not inspect:
                    if identifier in selected:
                        matched.add(identifier)
                    if replacement_error:
                        raise OneKitError('Cannot safely remove text with unavailable font metrics. Select its enclosing graphic group instead.')
                    kept.extend(replacements)
                    count += 1
                    changed = True
                else:
                    kept.extend(block)
                block = []
                continue
            if op == b'Do' and args and args[0] in xobjects:
                obj = resolve(xobjects[args[0]])
                kind = obj.get('/Subtype')
                identifier = f'{path}/o{index}'
                if kind in ('/Image', '/Form'):
                    add({'id':identifier, 'page':page_number, 'type':'image' if kind == '/Image' else 'form', 'resource':str(args[0]),
                         **({'width':int(obj.get('/Width',0)), 'height':int(obj.get('/Height',0))} if kind == '/Image' else {})})
                    if identifier in selected and not inspect:
                        acknowledge(index, op)
                        count += 1
                        changed = True
                        continue
                if kind == '/Form':
                    identity = id(obj)
                    if identity in ancestors:
                        raise OneKitError('Cyclic PDF form references are unsupported.')
                    nested, nested_resources, edited = rewrite(obj, obj.get('/Resources', resources), identifier, page_number, (*ancestors, identity), font)
                    if edited and not inspect:
                        clone = DecodedStreamObject()
                        clone.update({key:value for key,value in obj.items() if key not in ('/Length','/Filter','/DecodeParms')})
                        clone.set_data(nested.get_data())
                        clone[NameObject('/Resources')] = nested_resources
                        name = '/OneKitClean'
                        while name in xobjects:
                            name += 'X'
                        xobjects[NameObject(name)] = writer._add_object(clone)
                        args = [NameObject(name)]
                        changed = True
            kept.append((args, op))
        if depth or skipped is not None or block:
            raise OneKitError('Unbalanced PDF content; repair the PDF first.')
        if changed:
            stream.operations = kept
            if xobjects:
                resources[NameObject('/XObject')] = xobjects
        return stream, resources, changed

    for number, page in enumerate(writer.pages, 1):
        source = page.get_contents()
        if source is not None:
            stream, resources, edited = rewrite(source, page.get('/Resources', {}), f'p{number}', number)
            if edited and not inspect:
                page[NameObject('/Contents')] = writer._add_object(stream)
                page[NameObject('/Resources')] = resources
        annotations = page.get('/Annots')
        if annotations and not inspect:
            clean = ArrayObject()
            for reference in annotations:
                if reference.get_object().get('/Subtype') == '/Watermark':
                    count += 1
                else:
                    clean.append(reference)
            page[NameObject('/Annots')] = clean
    if selected-matched and not inspect:
        raise OneKitError('Some selected object IDs no longer match this PDF. Inspect the same original PDF again.')
    return count, candidates


def run(writer, file, options):
    import io
    mode = options.get('mode', 'remove')
    if mode not in ('inspect', 'remove'):
        raise OneKitError('Choose inspect or remove mode.')
    text = options.get('text', '')
    if not isinstance(text, str) or len(text) > 500:
        raise OneKitError('Watermark text must contain at most 500 characters.')
    objects = options.get('objects', [])
    if isinstance(objects, str):
        objects = parse_json(objects)
    if not isinstance(objects, list) or len(objects)>2000 or any(not isinstance(item,str) or len(item)>256 for item in objects):
        raise OneKitError('objects must be an array of up to 2,000 inspected object IDs.')
    count, candidates = process(writer, text.strip(), objects, inspect=mode=='inspect')
    if mode == 'inspect':
        report = {'objects':candidates, 'pages':len(writer.pages)}
        return Result([output(file, 'watermarks.json', json.dumps(report, ensure_ascii=False, indent=2))], details=report,
                      warnings=['These are selectable drawing objects, not confirmed watermarks. Select only objects you recognize. Flattened marks cannot be separated from their image.'])
    if not count:
        raise OneKitError('No matching watermark objects found. Inspect the PDF and select the text, image or form to remove, or enter its exact text. Marks merged into a scanned image cannot be separated by object removal.')
    buffer = io.BytesIO()
    writer.write(buffer)
    return Result([output(file, 'pdf', buffer.getvalue())], details={'removedObjects':count},
                  warnings=['Removes selected drawing objects, exact matching text, tagged watermark artifacts and watermark annotations, including nested forms. Original files stay unchanged. Review all pages: selecting document content removes that content.'])
