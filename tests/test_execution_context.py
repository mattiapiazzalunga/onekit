# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
from dataclasses import FrozenInstanceError
from types import SimpleNamespace

import pytest

from onekit import Artifact, ExecutionContext, OneKitError, Result, ToolLimits, execute, pipeline
from onekit.execution import DEFAULT_CONTEXT, current_context


def test_context_limits_apply_to_direct_and_mapped_outputs(monkeypatch):
    context = ExecutionContext(max_batch_bytes=8, tool_limits={"file-inspect": ToolLimits(4, 4)})
    monkeypatch.setattr("onekit.api.importlib.import_module", lambda _: SimpleNamespace(
        run=lambda *_: Result([Artifact("out", b"123")])
    ))
    assert execute("file-inspect", [Artifact("in", b"x")], context=context).files
    with pytest.raises(OneKitError, match="Output exceeds"):
        pipeline([{"tool": "file-inspect"}], [Artifact("a", b"x"), Artifact("b", b"y")], context=context)
    with pytest.raises(OneKitError, match="[Ii]nput.*exceed"):
        execute("file-inspect", [Artifact("in", b"12345")], context=context)


def test_context_is_immutable_and_services_do_not_escape_failed_calls(monkeypatch):
    limits = {"file-inspect": ToolLimits(4, 4)}
    context = ExecutionContext(tool_limits=limits, media_probe=lambda _: {"streams": []})
    limits.clear()
    assert "file-inspect" in context.tool_limits
    with pytest.raises(TypeError):
        context.tool_limits["other"] = ToolLimits()
    with pytest.raises(FrozenInstanceError):
        context.max_batch_bytes = 1
    def fail(*_):
        assert current_context() is context
        raise OneKitError("Engine stopped")
    monkeypatch.setattr("onekit.api.importlib.import_module", lambda _: SimpleNamespace(run=fail))
    with pytest.raises(OneKitError, match="Engine stopped"):
        execute("file-inspect", [Artifact("in", b"x")], context=context)
    assert current_context() is DEFAULT_CONTEXT


@pytest.mark.parametrize("budget", [True, 0, -1, 128 * 1024 * 1024 + 1, "4"])
def test_callers_cannot_raise_global_budgets(budget):
    with pytest.raises(OneKitError):
        ExecutionContext(max_batch_bytes=budget)


def test_user_options_cannot_supply_trusted_metadata(monkeypatch):
    from onekit.execution import use_context
    from onekit.tools.native import inspect_media
    file = Artifact("in.mp3", b"data")
    with use_context(ExecutionContext(media_probe=lambda _: {"streams": [], "format": {}})):
        assert inspect_media(file) == {"streams": [], "format": {}}
    with use_context(ExecutionContext(media_probe=lambda _: {"streams": "invalid"})):
        with pytest.raises(OneKitError, match="invalid report"):
            inspect_media(file)


def test_json_metadata_cannot_override_the_local_reader(monkeypatch):
    import json
    actual = {"streams": [{"codec_type": "audio", "tags": {"artist": "Engine reader"}}], "format": {}}
    forged = {"streams": [{"codec_type": "audio", "tags": {"artist": "User option"}}], "format": {}}
    calls = []
    monkeypatch.setattr("onekit.tools.native.command", lambda *args, **kwargs: calls.append(args) or json.dumps(actual).encode())
    result = execute("license-audio", [Artifact("a.mp3", b"test media")], {"_media_metadata": forged})
    assert calls
    assert result.details["declared_creators"][0]["value"] == "Engine reader"
