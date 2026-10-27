# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Extract aligned text tables from digital PDFs; never claim OCR accuracy."""
import csv
import io
import re

from ..models import OneKitError, Result, output
from .pdf import pages_option


def page_tables(page):
    text = page.extract_text(extraction_mode='layout')
    if len(text)>2000000:
        raise OneKitError('A PDF page contains too much text for table extraction.')
    groups, current, positions, last_line = [], [], None, None
    for index,line in enumerate(text.splitlines()):
        if not line.strip():
            continue
        cells = [(match.start(),match.group().strip()) for match in re.finditer(r'\S+(?: \S+)*',line)]
        aligned = positions is not None and len(cells)==len(positions) and all(abs(cell[0]-x)<=3 for cell,x in zip(cells,positions))
        nearby = last_line is not None and index-last_line<6
        if len(cells)<2 or not aligned or not nearby:
            if len(current)>=2:
                groups.append(current)
            current, positions = [], None
        if len(cells)>=2:
            current.append([value for x,value in cells]);positions = [x for x,value in cells];last_line = index
    if len(current)>=2:
        groups.append(current)
    return groups


def run(tool, files, options):
    from pypdf import PdfReader
    file = files[0]
    reader = PdfReader(io.BytesIO(file.data))
    if reader.is_encrypted:
        raise OneKitError('Unlock the PDF before extracting tables.')
    count = len(reader.pages)
    selected = pages_option(options.get('pages') or 'all',count)
    if len(selected)>100:
        raise OneKitError('Extract tables from at most 100 pages at a time.')
    tables = []
    for page_number in sorted(selected):
        for rows in page_tables(reader.pages[page_number]):
            if len(tables)>=100:
                raise OneKitError('Extract at most 100 tables at a time.')
            tables.append((page_number+1,rows))
    if not tables:
        raise OneKitError('No aligned text tables were found. Scanned PDFs require OCR; complex or unaligned tables may need manual extraction.')
    if tool.produces == 'csv':
        artifacts = []
        for index,(page,rows) in enumerate(tables,1):
            stream = io.StringIO(newline='');csv.writer(stream).writerows(rows)
            artifacts.append(output(file,f'page-{page}-table-{index}.csv',stream.getvalue()))
    else:
        from openpyxl import Workbook
        book = Workbook();book.remove(book.active)
        for index,(page,rows) in enumerate(tables,1):
            sheet = book.create_sheet(f'Page {page} Table {index}')
            for row in rows:
                sheet.append(row)
            for row in sheet:
                for cell in row:
                    cell.data_type = 's'
        stream = io.BytesIO();book.save(stream)
        artifacts = [output(file,'xlsx',stream.getvalue())]
    return Result(artifacts,warnings=['Table detection is based on aligned selectable text. Review column alignment, merged cells and values. CSV values must be imported as text when untrusted.'],
                  details={'tables':len(tables),'pages':sorted({page for page,rows in tables})})
