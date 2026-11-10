# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
from test_integrity_tools import signed_cms

from onekit import Artifact, execute
from onekit.execution import ExecutionContext
from onekit.tools import signature_dss


def test_certificate_mode_never_calls_an_installed_dss_runtime(monkeypatch):
    def unexpected():
        raise AssertionError('DSS must not be selected by certificate-only processing')

    monkeypatch.setattr(signature_dss, 'configured_runtime', unexpected)
    context = ExecutionContext(signature_certificate_only=True)
    result = execute('signature-verify', [Artifact('signed.p7m', signed_cms(b'original'))], context=context)
    assert result.details['verdict'] == 'cryptographic_match'
    assert result.details['signatures'][0]['certificateSubject']
    assert 'validation' not in result.details
