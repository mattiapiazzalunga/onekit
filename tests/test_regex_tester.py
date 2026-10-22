# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import json

import pytest

from onekit import Artifact, OneKitError, execute
from onekit.cli import doctor, main


def test_regex_cli_named_groups_utf16_indices_and_replacement(tmp_path):
    source = tmp_path / "input.txt"
    source.write_text("🌍 Ada 42", encoding="utf-8")
    destination = tmp_path / "report.json"
    options = {"pattern": "(?<word>[A-Za-z]+)", "flags": "gd", "enable_replacement": True, "replacement": "[$<word>]"}
    assert main(["run", "dev-regex-test", str(source), "--options", json.dumps(options), "-o", str(destination)]) == 0
    report = json.loads(destination.read_text(encoding="utf-8"))
    assert report["matches"][0]["index"] == 3
    assert report["matches"][0]["namedGroups"] == {"word": "Ada"}
    assert report["replacedText"] == "🌍 [Ada] 42"


def test_regex_doctor_does_not_require_unrelated_node_engine_packages(monkeypatch):
    monkeypatch.setattr("onekit.tools.native.executable", lambda *_: "node")
    assert doctor("dev-regex-test")[0]["ready"]


def test_slow_node_startup_does_not_consume_regex_execution_budget(tmp_path, monkeypatch):
    preload = tmp_path / "slow-start.mjs"
    preload.write_text("await new Promise(resolve=>setTimeout(resolve,3500));", encoding="utf-8")
    monkeypatch.setenv("NODE_OPTIONS", "--import=" + preload.as_uri())
    report = execute("dev-regex-test", [Artifact("input.txt", b"Ada 42")], {"pattern": r"\d+"})
    assert report.details["matches"][0]["text"] == "42"


def test_invalid_regex_and_catastrophic_backtracking_are_bounded():
    with pytest.raises(OneKitError, match="Invalid regular expression"):
        execute("dev-regex-test", [Artifact("input.txt", b"hello")], {"pattern": "["})
    with pytest.raises(OneKitError, match="time limit"):
        execute("dev-regex-test", [Artifact("input.txt", b"a"*10000+b"!")], {"pattern": "(a+)+$"})
    assert execute("dev-regex-test", [Artifact("input.txt", b"123")], {"pattern": r"\d+"}).details["matchCount"] == 1
