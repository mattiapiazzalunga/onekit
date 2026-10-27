# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Local PDF/A processing without subprocesses or network access."""
from __future__ import annotations

import io
import json
import re
import tempfile
from pathlib import Path

from ..models import OneKitError, Result, output

SUPPORTED = ("1b", "2b", "3b")


def _normalize_type1_widths(document, directory, report):
    """Reconcile simple Type 1 width tables with their embedded font programs."""
    import pikepdf
    from fontTools.encodings.StandardEncoding import StandardEncoding
    from fontTools.misc.psLib import PSError
    from fontTools.pens.basePen import NullPen
    from fontTools.t1Lib import T1Error, T1Font

    repaired = False
    targets = set()
    for finding in report.findings:
        if 'glyph widths disagree with the font program' in finding.message:
            location = re.match(r'obj (\d+) (\d+) \(Font\)', finding.where)
            if location:
                targets.add(tuple(map(int, location.groups())))
    for index, objgen in enumerate(sorted(targets)):
        font = document.get_object(objgen)
        if not isinstance(font, pikepdf.Dictionary) or font.get('/Subtype') != pikepdf.Name.Type1:
            continue
        program = font.get('/FontDescriptor', {}).get('/FontFile')
        widths = font.get('/Widths')
        if not isinstance(program, pikepdf.Stream) or not isinstance(widths, pikepdf.Array):
            continue
        encoding = font.get('/Encoding')
        if isinstance(encoding, pikepdf.Dictionary):
            base = encoding.get('/BaseEncoding')
        else:
            base = encoding
        if base not in (None, pikepdf.Name.StandardEncoding):
            continue
        path = Path(directory, f'font-{index}.pfa')
        raw = program.read_bytes()
        # PDF Type 1 streams may omit the PFA padding/trailer.
        if b'cleartomark' not in raw[-1024:]:
            raw += b'\n' + b'0'*512 + b'\ncleartomark\n'
        path.write_bytes(raw)
        try:
            parsed = T1Font(path)
            names = list(StandardEncoding if base else parsed['Encoding'])
            if isinstance(encoding, pikepdf.Dictionary):
                code = 0
                for item in encoding.get('/Differences', []):
                    if isinstance(item, int):
                        code = item
                    else:
                        if 0 <= code < 256:
                            names[code] = str(item).lstrip('/')
                        code += 1
            matrix = parsed['FontMatrix']
            if matrix[1] or matrix[2]:
                continue
            glyphs = parsed.getGlyphSet()
            first = int(font.get('/FirstChar', 0))
            for offset, width in enumerate(widths):
                code = first+offset
                if not 0 <= code < len(names) or names[code] not in glyphs:
                    continue
                glyph = glyphs[names[code]]
                glyph.draw(NullPen())
                advance = float(glyph.width)*float(matrix[0])*1000
                if abs(float(width)-advance) > 1:
                    widths[offset] = advance
                    repaired = True
        except (ValueError, KeyError, TypeError, IndexError, RuntimeError, PSError, T1Error):
            # Unreadable font programs remain subject to strict final validation.
            continue
    return repaired


def _backend():
    import pikepdf
    from pikepdf import pdfa
    return pikepdf, pdfa


def _details(report):
    return {
        "compliant": report.passed,
        "verdict": report.verdict,
        "profile": report.flavour.value,
        "engine": "pikepdf",
        "reports": [{"rule": f.rule, "where": f.where, "message": f.message,
                     "kind": f.kind} for f in report.findings],
    }


def validate(file, options=None):
    pikepdf, pdfa = _backend()
    options = options or {}
    profile = str(options.get("profile", "auto")).lower()
    if profile != "auto" and profile not in SUPPORTED:
        raise OneKitError("Choose auto, 1b, 2b or 3b for PDF/A validation.")
    try:
        with pikepdf.open(io.BytesIO(file.data), inherit_page_attributes=False) as document:
            if profile == "auto":
                with document.open_metadata() as metadata:
                    profile = str(metadata.get("pdfaid:part", "")) + str(metadata.get("pdfaid:conformance", "")).lower()
    except (pikepdf.PdfError, pikepdf.PasswordError, ValueError) as error:
        raise OneKitError("Cannot validate this PDF. It is damaged or encrypted.") from error
    if profile not in SUPPORTED:
        details = {"compliant": False, "verdict": "not_checked", "profile": None,
                   "engine": "pikepdf", "reports": [],
                   "reason": "No supported PDF/A-1b, 2b or 3b declaration. Select a profile to check explicitly."}
    else:
        details = _details(pdfa.validate_written(io.BytesIO(file.data), profile))
    return Result([output(file, "validation.json", json.dumps(details, indent=2))], details=details)


def convert(file, options=None):
    """Embed fonts, normalize, then publish only bytes that pass validation."""
    from pdftopdfa import convert_to_pdfa
    from pdftopdfa.sanitizers import count_digital_signatures

    pikepdf, pdfa = _backend()
    options = options or {}
    profile = str(options.get("profile", "2b")).lower()
    if profile not in ("2b", "3b"):
        raise OneKitError("PDF/A conversion supports profiles 2b and 3b.")
    # The converter may choose CMYK and supply DefaultRGB for mixed documents.
    # Replacing that intent with sRGB would leave DeviceCMYK content uncalibrated.
    intent = None
    flattened_forms = False
    repaired_widths = False
    if options.get("icc_profile"):
        path = Path(options["icc_profile"])
        if not path.is_file() or path.stat().st_size > 4 * 1024 * 1024:
            raise OneKitError("Choose an ICC profile file no larger than 4 MiB.")
        intent = path.read_bytes()
    with tempfile.TemporaryDirectory(prefix="onekit-pdfa-") as directory:
        source, candidate = Path(directory, "input.pdf"), Path(directory, "candidate.pdf")
        source.write_bytes(file.data)
        try:
            with pikepdf.open(io.BytesIO(file.data)) as original:
                if original.is_encrypted:
                    raise OneKitError("Encrypted PDFs cannot be converted to PDF/A.")
                if count_digital_signatures(original):
                    raise OneKitError("Converting this signed PDF would invalidate its signatures.")
                form = original.Root.get('/AcroForm')
                if form is not None:
                    if '/XFA' in form:
                        raise OneKitError("XFA forms cannot be converted to PDF/A. Export a static PDF first.")
                    original.generate_appearance_streams()
                    for page in original.pages:
                        for annotation in page.obj.get('/Annots', []):
                            if annotation.get('/Subtype') != pikepdf.Name.Widget:
                                continue
                            appearance = annotation.get('/AP', {}).get('/N')
                            if not isinstance(appearance, pikepdf.Stream):
                                state = annotation.get('/AS')
                                if not isinstance(appearance, pikepdf.Dictionary) or state is None or state not in appearance:
                                    raise OneKitError("A form field has no usable appearance. Export a static PDF first.")
                    original.flatten_annotations()
                    if any(annotation.get('/Subtype') == pikepdf.Name.Widget
                           for page in original.pages for annotation in page.obj.get('/Annots', [])):
                        raise OneKitError("The PDF form could not be made static without losing its appearance.")
                    if '/AcroForm' in original.Root:
                        del original.Root['/AcroForm']
                    flattened_forms = True
                with original.open_metadata() as metadata:
                    claimed = "pdfaid:part" in metadata or "pdfaid:conformance" in metadata
                    # Never let an input claim trigger upstream's optional
                    # veraPDF subprocess pre-check. We validate locally instead.
                    for key in ("pdfaid:part", "pdfaid:conformance"):
                        if key in metadata:
                            del metadata[key]
                if claimed:
                    existing = pdfa.validate_written(io.BytesIO(file.data), profile)
                    if existing.passed and intent is None and not flattened_forms:
                        return Result([output(file, "pdf", file.data)],
                                      ["This PDF already passes the selected PDF/A profile; the original bytes are unchanged."], _details(existing))
                if claimed or flattened_forms:
                    original.save(source)
            conversion = convert_to_pdfa(source, candidate, level=profile, validate=False,
                                         allow_signature_invalidation=False)
            if not conversion.success or not candidate.is_file():
                raise OneKitError("This PDF could not be converted to PDF/A.")
            stream = io.BytesIO()
            with pikepdf.open(candidate) as document:
                if document.is_encrypted:
                    raise OneKitError("Encrypted PDFs cannot be converted to PDF/A.")
                # ReportLab writes an empty transition dictionary on ordinary pages.
                # An empty dictionary has no presentation effect.
                for page in document.pages:
                    transition = page.obj.get("/Trans")
                    if isinstance(transition, pikepdf.Dictionary) and not len(transition):
                        del page.obj["/Trans"]
                    resources = page.obj.get('/Resources')
                    if isinstance(resources, pikepdf.Dictionary) and '/Encoding' in resources:
                        del resources['/Encoding']
                # pdfTeX provenance keys are non-rendering private metadata.
                for obj in document.objects:
                    if isinstance(obj, pikepdf.Stream) and obj.get('/Subtype') == pikepdf.Name.Form:
                        resources = obj.get('/Resources')
                        # ReportLab also emits an unused, nonstandard resource
                        # category. Font encoding lives in each font dictionary.
                        if isinstance(resources, pikepdf.Dictionary) and '/Encoding' in resources:
                            del resources['/Encoding']
                        for key in ('/PTEX.FileName', '/PTEX.InfoDict', '/PTEX.PageNumber'):
                            if key in obj:
                                del obj[key]
                # Width reconciliation only applies to embedded simple Type 1
                # programs. Avoid a full compliance scan for other documents.
                has_type1 = any(
                    isinstance(obj, pikepdf.Dictionary)
                    and obj.get('/Subtype') == pikepdf.Name.Type1
                    and '/Widths' in obj
                    and '/FontFile' in obj.get('/FontDescriptor', {})
                    for obj in document.objects
                )
                if has_type1:
                    repaired_widths = _normalize_type1_widths(document, directory, pdfa.check(document, profile))
                report = pdfa.save(document, stream, profile, output_intent=intent)
            data = stream.getvalue()
            # pdfa.save reopens and validates the written bytes before copying
            # them to this stream; revalidating would repeat the same full scan.
            if not report.passed:
                raise OneKitError("The converted PDF did not pass PDF/A validation; no output was produced.")
        except pdfa.PdfaError as error:
            raise OneKitError("The PDF contains content that cannot be validated as PDF/A; no output was produced. " + error.report.summary(limit=3)) from error
        except (pikepdf.PdfError, pikepdf.PasswordError) as error:
            raise OneKitError("Cannot convert this PDF. It is damaged or encrypted.") from error
    warnings = list(conversion.warnings)
    if flattened_forms:
        warnings.append("Form fields were made static to preserve their visible appearance; they are no longer editable.")
    if repaired_widths:
        warnings.append("Inconsistent font widths were corrected to match the embedded fonts. Review text spacing.")
    warnings.append("PDF/A conversion can replace fonts and remove unsupported actions or metadata. Review the result.")
    return Result([output(file, "pdf", data)], warnings, _details(report))
