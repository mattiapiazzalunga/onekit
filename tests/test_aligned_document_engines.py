# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import shutil

import pytest

from onekit.api import execute
from onekit.execution import ExecutionContext
from onekit.models import Artifact, OneKitError
from onekit.tools.pandoc import conversion_request, engine_ready


@pytest.mark.skipif(shutil.which('node') is None, reason='Optional Node runtime')
def test_tex_formatter_preserves_content_and_is_idempotent():
    source = '\\begin{itemize}\n\\item caffè % preserve comment\n\\item $x^2 + y^2$\n\\end{itemize}\n'
    result = execute('dev-format-latex', [Artifact('sample.tex', source.encode())])
    text = result.files[0].data.decode()
    assert '% preserve comment' in text and '$x^2 + y^2$' in text and 'caffè' in text
    assert execute('dev-format-latex', result.files).files[0].data == result.files[0].data
    with pytest.raises(OneKitError, match='Source is too complex'):
        execute('dev-format-latex', [Artifact('large.tex', b'\xef\xbb\xbf' + b'x' * (256 * 1024))])


def test_document_service_is_trusted_separately_and_rejects_partial_outputs():
    file = Artifact('sample.tex', b'Hello')
    assert conversion_request(file, 'md') == {'options': {'from': 'latex', 'to': 'markdown', 'sandbox': True}, 'stdin': 'Hello'}
    for report in [{'stdout': 'partial', 'warnings': ['missing image']}, {'stdout': 'partial', 'stderr': 'parse error'}, {'stdout': 42}]:
        with pytest.raises(OneKitError, match='Document conversion failed'):
            execute('latex-to-html', [file], context=ExecutionContext(document_converter=lambda request, report=report: report))
    with pytest.raises(OneKitError):
        conversion_request(Artifact('large.tex', b'x' * (256 * 1024 + 1)), 'html')
    with pytest.raises(OneKitError):
        ExecutionContext(document_converter='untrusted')


@pytest.mark.skipif(not engine_ready(), reason='Optional pinned Pandoc WASM engine')
@pytest.mark.parametrize('target,expected', [('html', b'<strong>world</strong>'), ('md', b'**world**')])
def test_real_pinned_pandoc_preserves_semantics_and_blocks_external_resources(target, expected):
    source = Artifact('sample.tex', b'\\section{OneKit}\nHello \\textbf{world}.\n')
    result = execute('latex-to-' + target, [source])
    assert expected in result.files[0].data
    assert result.details['wasm_sha256'].startswith('b47c9de5')
    # Missing includes must fail, without reading local host files or returning partial output.
    with pytest.raises(OneKitError):
        execute('latex-to-' + target, [Artifact('unsafe.tex', b'\\input{/etc/passwd}')])
