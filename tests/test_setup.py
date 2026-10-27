# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import subprocess
from dataclasses import replace

import pytest

from onekit import setup
from onekit.catalog import TOOLS
from onekit.models import OneKitError


@pytest.fixture(autouse=True)
def private_cache(monkeypatch, tmp_path):
    monkeypatch.setenv("ONEKIT_CACHE", str(tmp_path))
    monkeypatch.setenv("PATH", setup.os.environ.get("PATH", ""))
    monkeypatch.setenv("PYTHONPATH", setup.os.environ.get("PYTHONPATH", ""))
    monkeypatch.setattr(setup.sys, "path", setup.sys.path.copy())


def test_ready_tool_does_not_install_or_download(monkeypatch):
    monkeypatch.setattr(setup, "run", lambda *args: pytest.fail("Unexpected installation"))
    monkeypatch.setattr(setup.urllib.request, "urlopen", lambda *args, **kwargs: pytest.fail("Unexpected download"))
    setup.ensure_tool(TOOLS["file-count"])


def test_missing_python_dependencies_use_private_cache_and_catalog_constraints(monkeypatch):
    monkeypatch.setattr(setup.importlib.util, "find_spec", lambda name: None)
    calls = []
    monkeypatch.delitem(setup.sys.modules, "PIL", raising=False)
    monkeypatch.setattr(setup, "run", calls.append)
    setup.ensure_tool(replace(TOOLS["file-count"], packages=("Pillow",)))
    assert "--target" in calls[0]
    assert calls[0][-1] == setup.REQUIREMENTS["pillow"]
    assert calls[0][calls[0].index("--target")+1].parent == setup.cache()


def test_blocked_engines_never_install(monkeypatch):
    monkeypatch.setenv("ONEKIT_ALLOW_COPYLEFT", "0")
    monkeypatch.setattr(setup, "run", lambda *args: pytest.fail("Unexpected installation"))
    with pytest.raises(OneKitError, match="disabled"):
        setup.ensure_tool(TOOLS["video-compress"])


def test_native_install_reuses_environment_and_deduplicates_packages(monkeypatch):
    prefix = setup.cache() / "engines"
    (prefix / "conda-meta").mkdir(parents=True)
    installed = False
    def executable(name):
        if not installed:
            raise OneKitError("missing")
        return name
    calls = []
    def run(args):
        nonlocal installed
        calls.append(args)
        installed = True
    monkeypatch.setattr("onekit.tools.native.executable", executable)
    monkeypatch.setattr(setup, "micromamba", lambda: "micromamba")
    monkeypatch.setattr(setup, "run", run)
    setup.native_engines(["ffmpeg", "ffprobe"])
    assert calls[0][1] == "install"
    assert calls[0].count("ffmpeg") == 1
    setup.native_engines(["ffmpeg"])
    assert len(calls) == 1


def test_setup_failure_is_actionable(monkeypatch):
    def fail(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "installer")
    monkeypatch.setattr(setup.subprocess, "run", fail)
    with pytest.raises(OneKitError, match="Automatic setup failed"):
        setup.run(["installer"])




def test_download_format_listing_does_not_install_ffmpeg(monkeypatch):
    calls = []
    monkeypatch.setattr(setup, "python_packages", lambda specs: None)
    monkeypatch.setattr(setup, "native_engines", calls.append)
    setup.ensure_tool(TOOLS["video-download"], {"list_formats": True})
    assert calls == [[]]


def test_activation_is_idempotent():
    setup.activate()
    initial = setup.os.environ["PATH"]
    for _ in range(100):
        setup.activate()
    assert setup.os.environ["PATH"] == initial


def test_font_license_check_prepares_only_node_when_python_brotli_is_unavailable(monkeypatch):
    calls = []
    monkeypatch.setattr(setup, "python_packages", lambda specs: None)
    monkeypatch.setattr(setup, "native_engines", lambda engines: calls.append(list(engines)))
    real_spec = setup.importlib.util.find_spec
    monkeypatch.setattr(setup.importlib.util, "find_spec", lambda name: None if name in ("brotli", "brotlicffi") else real_spec(name))
    monkeypatch.setattr("onekit.cli.install_node_engines", lambda *_: pytest.fail("Font metadata needs no developer npm bundle"))
    setup.ensure_tool(TOOLS["license-font"])
    assert calls == [["node"]]


def test_original_audio_download_needs_no_transcoding_engine(monkeypatch):
    calls = []
    monkeypatch.setattr(setup, "python_packages", lambda specs: None)
    monkeypatch.setattr(setup, "native_engines", lambda engines: calls.append(list(engines)))
    setup.ensure_tool(TOOLS["audio-download"], {"format": "original"})
    setup.ensure_tool(TOOLS["audio-download"], {"format": "mp3"})
    assert calls == [[], ["ffmpeg", "ffprobe"]]



def test_pdfa_setup_installs_only_the_reviewed_level_b_runtime(monkeypatch):
    calls = []
    monkeypatch.setattr(setup, "run", calls.append)
    setup.python_packages(["pdftopdfa==0.9.24"])
    assert len(calls) == 2
    assert "pikepdf[pdfa]==10.17.0" in calls[0]
    assert "--no-deps" in calls[1]
    assert calls[1][-1] == "pdftopdfa==0.9.24"
    assert "pdfminer.six==20260107" in calls[1]
    assert not any("paddle" in str(arg) or "cryptography" in str(arg) for call in calls for arg in call)
