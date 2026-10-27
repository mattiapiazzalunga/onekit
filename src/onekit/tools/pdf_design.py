# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Editable AcroForm fields and conservative object-based watermark removal."""
import io
import math
import re

from ..models import OneKitError, Result, output, parse_json


def field_specs(value):
    if isinstance(value, str):
        value = parse_json(value)
    if not isinstance(value, list) or not 1 <= len(value) <= 200:
        raise OneKitError("Add 1–200 form fields.")
    names, clean = set(), []
    for item in value:
        if not isinstance(item, dict):
            raise OneKitError("Each field must be an object.")
        name, kind, page = item.get("name"), item.get("type", "text"), item.get("page", 1)
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", name) or name in names:
            raise OneKitError("Use unique field names: a letter followed by letters, digits, hyphens or underscores, up to 64 characters.")
        names.add(name)
        if kind not in ("text", "checkbox", "choice") or isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise OneKitError("Choose text, checkbox or choice and a positive page number.")
        values = [item.get(key) for key in ("x", "y", "width", "height")]
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
            raise OneKitError("Field coordinates must be finite normalized numbers.")
        x, y, w, h = values
        if min(x, y) < 0 or min(w, h) <= 0 or x+w > 1+1e-9 or y+h > 1+1e-9:
            raise OneKitError("Fields must fit inside the displayed page (0–1 coordinates).")
        choices = item.get("choices", [])
        if kind == "choice" and (not isinstance(choices, list) or not 1 <= len(choices) <= 100 or any(not isinstance(choice, str) or not choice or len(choice) > 200 for choice in choices)):
            raise OneKitError("Choice fields need 1–100 options, up to 200 characters each.")
        for flag in ("required", "multiline"):
            if flag in item and not isinstance(item[flag], bool):
                raise OneKitError(f"{flag} must be true or false.")
        clean.append({**item, "name": name, "type": kind, "page": page, "choices": choices})
    return clean


def field_rectangle(page, field):
    box = page.cropbox
    w, h, left, bottom = float(box.width), float(box.height), float(box.left), float(box.bottom)
    x, y, rw, rh = (field[key] for key in ("x", "y", "width", "height"))
    rotation = page.rotation % 360
    def point(u, v):
        if rotation == 0:
            return left+u*w, bottom+(1-v)*h
        if rotation == 90:
            return left+v*w, bottom+u*h
        if rotation == 180:
            return left+(1-u)*w, bottom+v*h
        return left+(1-v)*w, bottom+(1-u)*h
    corners = [point(x, y), point(x+rw, y+rh)]
    return [min(p[0] for p in corners), min(p[1] for p in corners), max(p[0] for p in corners), max(p[1] for p in corners)]


def make_fillable(writer, specs):
    from pypdf.generic import (
        ArrayObject,
        BooleanObject,
        DecodedStreamObject,
        DictionaryObject,
        FloatObject,
        NameObject,
        NumberObject,
        TextStringObject,
    )
    def dictionary(**values):
        return DictionaryObject({NameObject('/'+key): value for key, value in values.items()})
    existing = writer.get_fields() or {}
    if any(item["name"] in existing for item in specs):
        raise OneKitError("A field name already exists in this PDF. Choose another name.")
    root = writer._root_object
    if '/AcroForm' not in root:
        root[NameObject('/AcroForm')] = writer._add_object(dictionary(Fields=ArrayObject()))
    acro = root['/AcroForm'].get_object()
    if '/XFA' in acro:
        raise OneKitError("XFA forms are unsupported. Use a standard AcroForm PDF.")
    acro.setdefault(NameObject('/Fields'), ArrayObject())
    resources = acro.setdefault(NameObject('/DR'), DictionaryObject()).get_object()
    fonts = resources.setdefault(NameObject('/Font'), DictionaryObject()).get_object()
    font_name = '/OneKitHelv'
    while font_name in fonts:
        font_name += 'X'
    fonts[NameObject(font_name)] = writer._add_object(dictionary(Type=NameObject('/Font'), Subtype=NameObject('/Type1'), BaseFont=NameObject('/Helvetica'), Encoding=NameObject('/WinAnsiEncoding')))
    for item in specs:
        if item['page'] > len(writer.pages):
            raise OneKitError("A field refers to a page that does not exist.")
        page = writer.pages[item['page']-1]
        rect = field_rectangle(page, item)
        flags = (2 if item.get('required') else 0) | (4096 if item.get('multiline') and item['type'] == 'text' else 0)
        field = dictionary(Type=NameObject('/Annot'), Subtype=NameObject('/Widget'),
                           FT=NameObject({'text':'/Tx', 'checkbox':'/Btn', 'choice':'/Ch'}[item['type']]),
                           T=TextStringObject(item['name']), Rect=ArrayObject([FloatObject(v) for v in rect]),
                           F=NumberObject(4), Ff=NumberObject(flags), P=page.indirect_reference,
                           DA=TextStringObject(f'{font_name} 12 Tf 0 g'),
                           MK=dictionary(BC=ArrayObject([FloatObject(.25)]*3), R=NumberObject(page.rotation % 360)),
                           BS=dictionary(W=NumberObject(1), S=NameObject('/S')))
        if item['type'] == 'choice':
            field[NameObject('/Opt')] = ArrayObject([TextStringObject(choice) for choice in item['choices']])
            field[NameObject('/Ff')] = NumberObject(flags | 131072)
            field[NameObject('/V')] = TextStringObject(item['choices'][0])
        elif item['type'] == 'text':
            field[NameObject('/V')] = TextStringObject('')
        else:
            width, height = rect[2]-rect[0], rect[3]-rect[1]
            appearances = DictionaryObject()
            for state in ('Off', 'Yes'):
                stream = DecodedStreamObject()
                data = f'q 0.3 G 1 w 0.5 0.5 {max(0,width-1):.3f} {max(0,height-1):.3f} re S '
                if state == 'Yes':
                    data += f'0 G 2 w {width*.2:.3f} {height*.5:.3f} m {width*.45:.3f} {height*.2:.3f} l {width*.8:.3f} {height*.8:.3f} l S '
                stream.set_data((data+'Q').encode('ascii'))
                stream.update(dictionary(Type=NameObject('/XObject'), Subtype=NameObject('/Form'), BBox=ArrayObject([FloatObject(v) for v in (0,0,width,height)]), Resources=DictionaryObject()))
                appearances[NameObject('/'+state)] = writer._add_object(stream)
            field[NameObject('/AP')] = dictionary(N=appearances)
            field[NameObject('/AS')] = NameObject('/Off')
            field[NameObject('/V')] = NameObject('/Off')
        reference = writer._add_object(field)
        acro['/Fields'].append(reference)
        page.setdefault(NameObject('/Annots'), ArrayObject()).get_object().append(reference)
        if item['type'] != 'checkbox':
            writer.update_page_form_field_values(page, {item['name']:field['/V']}, auto_regenerate=False)
    acro[NameObject('/NeedAppearances')] = BooleanObject(False)


def run(tool, files, options):
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(io.BytesIO(files[0].data))
    if reader.is_encrypted:
        raise OneKitError("Unlock the PDF before processing it.")
    if not 1 <= len(reader.pages) <= 256:
        raise OneKitError("Process 1–256 PDF pages at a time.")
    writer = PdfWriter(clone_from=reader)
    if tool.id == 'pdf-make-fillable':
        specs = field_specs(options.get('fields'))
        make_fillable(writer, specs)
        details = {'fieldsAdded':len(specs)}
        warnings = ['Adds standard editable AcroForm fields. It does not automatically recognize blanks. Test the downloaded form in your PDF reader.']
    else:
        from .pdf_watermarks import run as remove
        return remove(writer, files[0], options)
    result = io.BytesIO()
    writer.write(result)
    return Result([output(files[0], 'pdf', result.getvalue())], details=details, warnings=warnings)
