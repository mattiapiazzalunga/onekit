# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io

import pytest
from pypdf import PdfReader

from onekit import Artifact, execute
from onekit.execution import DocumentLimits, ExecutionContext
from onekit.models import OneKitError


@pytest.mark.parametrize('source', ['md', 'html'])
@pytest.mark.parametrize('target', ['latex', 'pdf'])
def test_portable_exports_are_real_and_do_not_resolve_resources(source, target, monkeypatch):
    import socket
    monkeypatch.setattr(socket, 'create_connection', lambda *args, **kwargs: pytest.fail('Unexpected network access'))
    text = '# Città\n\nCaffè **forte**, 50% & €10.\n\n- Uno\n- Due' if source == 'md' else '<h1>Città</h1><p>Caffè <b>forte</b>, 50% &amp; €10.</p><img src="https://example.invalid/leak" alt="foto"><script>secret()</script>'
    result = execute(f'{source}-to-{target}', [Artifact(f'sample.{source}', text.encode())], context=ExecutionContext(portable_documents=True))
    data = result.files[0].data
    if target == 'pdf':
        reader = PdfReader(io.BytesIO(data))
        assert len(reader.pages) == result.details['pages'] == 1
        content = reader.pages[0].extract_text()
        assert 'Città' in content and '€10' in content
        assert not reader.pages[0].get('/Annots')
    else:
        content = data.decode()
        assert r'\section*{Città}' in content
        assert r'50\% \&' in content
    assert 'secret' not in content and 'example.invalid' not in content


def test_literal_tex_code_cannot_escape_its_context():
    result = execute('md-to-latex', [Artifact('code.md', b'```\n\\end{verbatim}\n\\input{secret}\n```')], context=ExecutionContext(portable_documents=True))
    assert r'\textbackslash{}end\{verbatim\}' in result.files[0].text()
    assert r'\input{secret}' not in result.files[0].text()


@pytest.mark.parametrize('source', ['md', 'html'])
def test_math_symbols_are_preserved_in_pdf(source):
    text = '≈ ≠ ≤ ≥ ∞'
    result = execute(f'{source}-to-pdf', [Artifact(f'math.{source}', text.encode())], context=ExecutionContext(portable_documents=True))
    extracted = PdfReader(io.BytesIO(result.files[0].data)).pages[0].extract_text()
    assert text in extracted


@pytest.mark.parametrize('text,pattern', [('<div>'*60+'x'+'</div>'*60, 'nesting'), ('中文', 'font does not support'), ('<h1>x</h1>'*2000, '100 pages')])
def test_document_resource_limits(text, pattern):
    with pytest.raises(OneKitError, match=pattern):
        execute('html-to-pdf', [Artifact('sample.html', text.encode())], context=ExecutionContext(portable_documents=True, document_limits=DocumentLimits(max_depth=48, max_pages=100)))


def test_portable_mode_is_scoped_and_keeps_native_default(monkeypatch):
    from onekit.tools import native
    calls = []
    monkeypatch.setattr(native, 'convert_document', lambda *args: (calls.append(args), execute('md-to-latex', [args[0]], context=ExecutionContext(portable_documents=True)))[1])
    file = Artifact('sample.md', b'# Heading')
    execute('md-to-latex', [file], context=ExecutionContext(portable_documents=True))
    assert not calls
    execute('md-to-latex', [file])
    assert len(calls) == 1
