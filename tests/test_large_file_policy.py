# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
from dataclasses import replace
from types import SimpleNamespace

import pytest

from onekit import Artifact, OneKitError, Result, execute, pipeline
from onekit.catalog import LARGE_BROWSER_PDF_TOOLS, TOOLS
from onekit.validation import BROWSER_BYTES, check_batch


def test_large_browser_policy_is_explicit():
    assert BROWSER_BYTES == 100 * 1024 * 1024
    assert len(LARGE_BROWSER_PDF_TOOLS) == 8
    for tool in TOOLS.values():
        if tool.id in LARGE_BROWSER_PDF_TOOLS:
            assert tool.browser
            assert tool.browser_max_file_bytes == BROWSER_BYTES
            assert tool.browser_max_total_bytes == BROWSER_BYTES
        else:
            assert tool.browser_max_file_bytes <= 32 * 1024 * 1024
            assert tool.browser_max_total_bytes == 32 * 1024 * 1024


def test_output_keeps_the_tool_limit(monkeypatch):
    # Small test limits exercise the real API without allocating huge buffers.
    tool = replace(TOOLS['file-inspect'], browser_max_total_bytes=4)
    monkeypatch.setitem(TOOLS, tool.id, tool)
    monkeypatch.setattr('onekit.api.importlib.import_module', lambda _: SimpleNamespace(
        run=lambda *_: Result([Artifact('result.bin', b'12345')])
    ))
    with pytest.raises(OneKitError, match='Output exceeds'):
        execute(tool.id, [Artifact('input.bin', b'x')], browser=True)


def test_workflow_fanout_cannot_bypass_aggregate_tool_limit(monkeypatch):
    tool = replace(TOOLS['file-inspect'], browser_max_total_bytes=4)
    monkeypatch.setitem(TOOLS, tool.id, tool)
    with pytest.raises(OneKitError, match='Input exceeds'):
        pipeline([{'tool': tool.id}], [Artifact('a.bin', b'123'), Artifact('b.bin', b'456')], browser=True)


def test_workflow_fanout_output_cannot_bypass_aggregate_tool_limit(monkeypatch):
    tool = replace(TOOLS['file-inspect'], browser_max_total_bytes=4)
    monkeypatch.setitem(TOOLS, tool.id, tool)
    monkeypatch.setattr('onekit.api.importlib.import_module', lambda _: SimpleNamespace(
        run=lambda *_: Result([Artifact('result.bin', b'123')])
    ))
    with pytest.raises(OneKitError, match='Output exceeds'):
        pipeline([{'tool': tool.id}], [Artifact('a.bin', b'x'), Artifact('b.bin', b'y')], browser=True)


def test_batch_override_cannot_raise_global_limit():
    with pytest.raises(OneKitError):
        check_batch([Artifact('x', b'12345')], browser=True, max_bytes=4)
