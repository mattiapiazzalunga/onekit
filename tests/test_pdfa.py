# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json

import pytest

from onekit.api import execute
from onekit.models import Artifact, OneKitError

pikepdf = pytest.importorskip('pikepdf')
pytest.importorskip('pdftopdfa')


def document():
    from reportlab.pdfgen.canvas import Canvas
    stream = io.BytesIO()
    canvas = Canvas(stream)
    canvas.drawString(50, 700, 'OneKit: real PDF/A font embedding')
    canvas.save()
    return Artifact('source.pdf', stream.getvalue())


@pytest.mark.parametrize('profile', ['2b', '3b'])
def test_pdfa_flattens_form_values_without_losing_their_appearance(profile):
    from pypdf import PdfReader
    from reportlab.pdfgen.canvas import Canvas
    stream = io.BytesIO()
    canvas = Canvas(stream)
    canvas.drawString(50,700,'Form document')
    canvas.acroForm.textfield(name='name', value='Ada Lovelace', x=50,y=600,width=200,height=30)
    canvas.showPage(); canvas.save()
    result = execute('pdf-to-pdfa',[Artifact('form.pdf',stream.getvalue())],{'profile':profile})
    assert result.details['compliant']
    assert 'Ada Lovelace' in PdfReader(io.BytesIO(result.files[0].data)).pages[0].extract_text()
    with pikepdf.open(io.BytesIO(result.files[0].data)) as pdf:
        assert '/AcroForm' not in pdf.Root
    assert any('no longer editable' in warning for warning in result.warnings)


def test_pdfa_normalizes_embedded_type1_widths_and_tex_provenance(tmp_path):
    from pathlib import Path

    import reportlab
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfgen.canvas import Canvas
    fonts = Path(reportlab.__file__).parent/'fonts'
    face = pdfmetrics.EmbeddedType1Face(str(fonts/'callig15.afm'),str(fonts/'callig15.pfb'))
    pdfmetrics.registerTypeFace(face)
    pdfmetrics.registerFont(pdfmetrics.Font('RegressionType1',face.name,'WinAnsiEncoding'))
    stream = io.BytesIO(); canvas = Canvas(stream)
    canvas.beginForm('TeXForm');canvas.setFont('RegressionType1',16);canvas.drawString(20,20,'Hello');canvas.endForm()
    canvas.doForm('TeXForm');canvas.showPage();canvas.save()
    with pikepdf.open(io.BytesIO(stream.getvalue())) as pdf:
        for obj in pdf.objects:
            if isinstance(obj,pikepdf.Dictionary) and obj.get('/Subtype') == pikepdf.Name.Type1 and '/Widths' in obj:
                offset = ord('H')-int(obj.FirstChar)
                obj.Widths[offset] = float(obj.Widths[offset])+20
                obj.Encoding = pikepdf.Dictionary(BaseEncoding=pikepdf.Name.StandardEncoding)
        for page in pdf.pages:
            if '/Trans' in page.obj:
                del page.obj['/Trans']
        from onekit.tools.pdfa import _normalize_type1_widths
        assert _normalize_type1_widths(pdf,tmp_path,pikepdf.pdfa.check(pdf,'2b'))
        for obj in pdf.objects:
            if isinstance(obj,pikepdf.Stream) and obj.get('/Subtype') == pikepdf.Name.Form:
                obj['/PTEX.FileName'] = pikepdf.String('source.pdf')
                obj['/PTEX.PageNumber'] = 1
        stream = io.BytesIO();pdf.save(stream)
    result = execute('pdf-to-pdfa',[Artifact('tex.pdf',stream.getvalue())])
    assert result.details['compliant']


@pytest.mark.parametrize('profile', ['2b', '3b'])
def test_pdfa_converts_and_validates_exact_bytes(profile):
    source = document()
    result = execute('pdf-to-pdfa', [source], {'profile': profile})
    assert result.details['compliant'] is True
    assert result.details['profile'] == profile
    validation = execute('pdf-validate-pdfa', result.files)
    assert validation.details['verdict'] == 'pass'
    assert json.loads(validation.files[0].text())['compliant'] is True
    from pypdf import PdfReader
    assert 'OneKit' in PdfReader(io.BytesIO(result.files[0].data)).pages[0].extract_text()
    assert result.files[0].data != source.data


def test_pdfa_validator_does_not_trust_declaration_or_rewrite_input():
    source = document()
    result = execute('pdf-validate-pdfa', [source])
    assert result.details['verdict'] == 'not_checked'
    with pikepdf.open(io.BytesIO(source.data)) as pdf:
        for page in pdf.pages:
            if '/Trans' in page.obj:
                del page.obj['/Trans']
        with pdf.open_metadata() as metadata:
            metadata['pdfaid:part'] = '2'
            metadata['pdfaid:conformance'] = 'B'
        output = io.BytesIO()
        pdf.save(output)
    claimed = Artifact('claimed.pdf', output.getvalue())
    result = execute('pdf-validate-pdfa', [claimed])
    assert result.details['compliant'] is False
    assert result.details['reports']
    assert any('font' in finding['message'].lower() for finding in result.details['reports'])


def test_pdfa_rejects_unsupported_profiles_and_encrypted_documents():
    source = document()
    with pytest.raises(OneKitError, match='profiles'):
        execute('pdf-to-pdfa', [source], {'profile': '2a'})
    with pikepdf.open(io.BytesIO(source.data)) as pdf:
        stream = io.BytesIO()
        pdf.save(stream, encryption=pikepdf.Encryption(owner='owner', user=''))
    with pytest.raises(OneKitError, match='Encrypted'):
        execute('pdf-to-pdfa', [Artifact('encrypted.pdf', stream.getvalue())])


def test_pdfa_fixed_b_api_never_imports_ocr_or_layout_dependencies(tmp_path):
    import os
    import subprocess
    import sys
    from pathlib import Path
    source = tmp_path / 'source.pdf'
    source.write_bytes(document().data)
    code = """
import sys
for name in ('cryptography', 'paddleocr', 'paddlex', 'ocrmypdf', 'onnxruntime', 'pdfminer.pdfdocument'):
    sys.modules[name] = None
from pathlib import Path
from onekit.api import execute
from onekit.models import Artifact
assert execute('pdf-to-pdfa', [Artifact('source.pdf', Path(sys.argv[1]).read_bytes())]).details['compliant']
"""
    result = subprocess.run([sys.executable, '-c', code, str(source)], check=False, capture_output=True,
                            text=True, env={**os.environ, 'PYTHONPATH': str(Path(__file__).resolve().parents[1] / 'src')})
    assert result.returncode == 0, result.stderr


def test_pdfa_conversion_rejects_signatures_without_invalidating_them():
    source = document()
    with pikepdf.open(io.BytesIO(source.data)) as pdf:
        signature = pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.Sig,
            ByteRange=pikepdf.Array([0, 10, 20, 30]), Contents=pikepdf.String(b'test')))
        field = pdf.make_indirect(pikepdf.Dictionary(FT=pikepdf.Name.Sig, T='Signature', V=signature))
        pdf.Root.AcroForm = pikepdf.Dictionary(Fields=pikepdf.Array([field]))
        stream = io.BytesIO()
        pdf.save(stream)
    with pytest.raises(OneKitError, match='signatures'):
        execute('pdf-to-pdfa', [Artifact('signed.pdf', stream.getvalue())])


def test_pdfa_preserves_colour_intent_for_mixed_rgb_cmyk_and_alpha():
    from PIL import Image
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen.canvas import Canvas
    stream = io.BytesIO()
    canvas = Canvas(stream)
    for mode, format, colour in [('RGB', 'JPEG', (20, 80, 200)), ('CMYK', 'JPEG', (0, 150, 120, 0)), ('RGBA', 'PNG', (30, 180, 80, 160))]:
        image = Image.new(mode, (60, 40), colour)
        encoded = io.BytesIO()
        image.save(encoded, format=format)
        encoded.seek(0)
        canvas.drawImage(ImageReader(encoded), 50, 500, width=300, height=200, mask='auto')
        canvas.drawString(50, 730, mode + ' image')
        canvas.showPage()
    canvas.save()
    converted = execute('pdf-to-pdfa', [Artifact('mixed.pdf', stream.getvalue())])
    assert converted.details['compliant']
    with pikepdf.open(io.BytesIO(converted.files[0].data)) as pdf:
        assert len(pdf.pages) == 3
        assert pdf.Root.OutputIntents[0].DestOutputProfile.N == 4
    assert execute('pdf-validate-pdfa', converted.files).details['compliant']

def test_pdfa_claims_never_trigger_an_external_validator(monkeypatch):
    import pdftopdfa.converter
    def unexpected(*args, **kwargs):
        pytest.fail('PDF/A processing must not launch an external validator')
    monkeypatch.setattr(pdftopdfa.converter, 'validate_with_verapdf', unexpected)
    converted = execute('pdf-to-pdfa', [document()])
    unchanged = execute('pdf-to-pdfa', converted.files)
    assert unchanged.files[0].data == converted.files[0].data
    with pikepdf.open(io.BytesIO(document().data)) as pdf:
        with pdf.open_metadata() as metadata:
            metadata['pdfaid:part'] = '2'
            metadata['pdfaid:conformance'] = 'B'
        stream = io.BytesIO()
        pdf.save(stream)
    repaired = execute('pdf-to-pdfa', [Artifact('claimed.pdf', stream.getvalue())])
    assert repaired.details['compliant']
