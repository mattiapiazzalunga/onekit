# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Output regressions captured before the algorithm performance refactor."""
import difflib
import hashlib
import json
from pathlib import Path
import random

import pytest

from onekit import Artifact
from onekit.catalog import TOOLS, Tool
from onekit.models import OneKitError
from onekit.tools import design, diff, photo_tools

GOLDEN = json.loads((Path(__file__).parent / 'fixtures/algorithm-golden.json').read_text(encoding='utf-8'))


@pytest.mark.parametrize('case', GOLDEN['palettes'])
def test_palette_float_values_and_serialized_output_are_unchanged(case):
    assert json.dumps(design.palette(case['color'], **case['options'])) == json.dumps(case['expected'])


@pytest.mark.parametrize('case', GOLDEN['restorations'])
def test_restoration_pixels_are_unchanged(case):
    Image = pytest.importorskip('PIL.Image')
    pytest.importorskip('numpy')
    image = Image.frombytes('RGBA', tuple(case['size']), bytes.fromhex(case['rgba']))
    restored, count = photo_tools.restore(image, case['regions'], case['iterations'])
    assert count == case['pixels']
    assert hashlib.sha256(restored.tobytes()).hexdigest() == case['sha256']


@pytest.mark.parametrize('case', GOLDEN['qr_centers'])
def test_qr_center_placement_and_errors_are_unchanged(case):
    segno = pytest.importorskip('segno')
    from onekit.tools.qrcode import center_box
    matrix = list(segno.make_qr('onekit '*case['length'], error='h').matrix_iter(border=0, verbose=True))
    try:
        result = list(center_box(matrix, case['percent']))
    except OneKitError as error:
        result = [type(error).__name__, str(error)]
    assert result == case['expected']


def test_diff_matches_standard_unified_patch_for_line_endings_unicode_and_empty_inputs():
    rng = random.Random(20261026)
    examples = [('', ''), ('', 'last'), ('last', ''), ('a\r\nb\n', 'a\nb\r'), ('same\n'*300, 'same\n'*299)]
    for _ in range(80):
        examples.append(tuple(''.join(rng.choice(['same\n', 'à 🧰\r\n', 'last', '\r', '\n']) for _ in range(rng.randrange(100))) for _ in range(2)))
    for left, right in examples:
        files = [Artifact('original.txt', left.encode()), Artifact('changed.txt', right.encode())]
        a, b = left.splitlines(keepends=True), right.splitlines(keepends=True)
        expected = ''.join(line if line.endswith('\n') else line+'\n\\ No newline at end of file\n'
                           for line in difflib.unified_diff(a, b, fromfile=files[0].name, tofile=files[1].name))
        result = diff.run(TOOLS['diff-text'], files, {})
        assert result.details['patch'] == expected
        assert json.loads(result.files[0].text()) == result.details


def test_doctor_reuses_probes_only_within_one_environment_snapshot(monkeypatch):
    from onekit import cli
    calls = {'packages': [], 'engines': []}
    available = False
    monkeypatch.setattr('onekit.setup.activate', lambda: None)
    monkeypatch.setenv('ONEKIT_ALLOW_COPYLEFT', '1')
    def spec(name):
        calls['packages'].append(name)
        return None if name == 'absent' and not available else object()
    def executable(name):
        calls['engines'].append(name)
        if name == 'not-there' and not available:
            raise OneKitError('Missing engine')
        return '/engines/'+name
    monkeypatch.setattr(cli.importlib.util, 'find_spec', spec)
    monkeypatch.setattr('onekit.tools.native.executable', executable)
    monkeypatch.setattr(cli, 'TOOLS', {name: Tool(name, name, 'test', 'inspector', packages=('present','absent'), engines=('ffmpeg','not-there')) for name in ['a','b','c']})
    assert cli.doctor() == [{'tool':name,'ready':False,'missing':['absent','not-there'],'policyBlocked':[]} for name in ['a','b','c']]
    assert calls == {'packages':['present','absent'],'engines':['ffmpeg','not-there']}
    available = True
    assert all(row['ready'] for row in cli.doctor())
    assert calls == {'packages':['present','absent']*2,'engines':['ffmpeg','not-there']*2}


def test_pdf_text_budget_counts_content_and_preserves_page_separator_rules(monkeypatch):
    pypdf = pytest.importorskip('pypdf')
    from onekit.tools import pdf_text
    class Page:
        def extract_text(self, **options):
            return 'x'*(32*1024)
    class Reader:
        is_encrypted = False
        pages = [Page()]*256
    monkeypatch.setattr(pypdf, 'PdfReader', lambda *args: Reader())
    result = pdf_text.run(TOOLS['pdf-to-text'], [Artifact('pages.pdf', b'')], {})
    assert result.files[0].data == ('\n\n'.join(['x'*(32*1024)]*256)).encode()
    assert result.details['characters'] == 8*1024*1024+2*255
    Reader.pages = [Page()]*257
    with pytest.raises(OneKitError, match='256 pages'):
        pdf_text.run(TOOLS['pdf-to-text'], [Artifact('pages.pdf', b'')], {})
