# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import hashlib
import io
import json

import pytest
from pypdf import PdfReader

from onekit import Artifact, execute
from onekit.execution import ExecutionContext
from onekit.models import OneKitError


def test_tagged_text_preserves_content_and_structure_across_page_splits():
    text = '\n\n'.join('Paragraph %d: caf\u00e8, reading order and embedded fonts. ' % i + 'Long text. ' * 110 for i in range(15))
    result = execute('txt-to-pdfua', [Artifact('source.txt', text.encode())], {'title': 'Accessible document', 'language': 'it'})
    reader = PdfReader(io.BytesIO(result.files[0].data))
    assert len(reader.pages) > 2
    assert reader.trailer['/Root']['/Lang'] == 'it'
    assert reader.trailer['/Root']['/MarkInfo']['/Marked']
    assert reader.metadata.title == 'Accessible document'
    extracted = '\n'.join(page.extract_text() for page in reader.pages)
    assert all('Paragraph %d:' % i in extracted for i in range(15))
    tree = reader.trailer['/Root']['/StructTreeRoot']
    nums = tree['/ParentTree']['/Nums']
    for i, page in enumerate(reader.pages):
        assert page['/Tabs'] == '/S'
        assert page['/StructParents'] == i
        assert nums[2*i] == i
        for mcid, ref in enumerate(nums[2*i+1]):
            assert ref.get_object()['/K'] == mcid
            assert ref.get_object().raw_get('/Pg') == page.indirect_reference
    assert result.details['compliant'] is None


@pytest.mark.parametrize('text,options', [(b'', {}), ('\u6f22'.encode(), {}), (b'valid', {'title': '\x00'}), (b'valid', {'language': 'invalid language'})])
def test_unsupported_text_is_rejected_without_an_accessibility_claim(text, options):
    with pytest.raises(OneKitError):
        execute('txt-to-pdfua', [Artifact('text.txt', text)], options)


def test_machine_pass_does_not_claim_full_pdfua_conformance_and_report_binds_bytes():
    file = execute('txt-to-pdfua', [Artifact('source.txt', b'Example.')]).files[0]
    envelope = {'sha256': hashlib.sha256(file.data).hexdigest(), 'engine_version': '0.12.1',
                'report': {'profile': 'ua1', 'is_compliant': True, 'rules': {'total': 104, 'passed': 104, 'failed': 0}, 'failures': []}}
    context = ExecutionContext(pdf_validator=lambda f, p: envelope)
    report = execute('pdf-validate-pdfua', [file], context=context).details
    assert report['machine_compliant'] and report['compliant'] is None
    assert report['verdict'] == 'manual_review'
    assert report['requires_manual_review'] and report['sha256'] == envelope['sha256']
    assert json.loads(execute('pdf-validate-pdfua', [file], context=context).files[0].data)['raw_report'] == envelope['report']
    envelope['sha256'] = '0' * 64
    with pytest.raises(OneKitError, match='integrity'):
        execute('pdf-validate-pdfua', [file], context=context)


def test_no_engine_or_unsupported_profile_never_passes():
    file = execute('txt-to-pdfua', [Artifact('source.txt', b'Example.')]).files[0]
    assert execute('pdf-validate-pdfua', [file]).details['verdict'] == 'not_checked'
    context = ExecutionContext(pdf_validator=lambda f, p: {'sha256': hashlib.sha256(f.data).hexdigest(), 'engine_version': '0.12.1', 'error_kind': 'safety_limit'})
    assert execute('pdf-validate-pdfua', [file], context=context).details['verdict'] == 'not_checked'
