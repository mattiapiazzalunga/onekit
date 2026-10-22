# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import json
import socket
import sys

from onekit.cli import main


def test_empty_invocation_welcomes_users_and_explains_commands(capsys):
    assert main([]) == 0
    output = capsys.readouterr()
    assert "Welcome to OneKit" in output.out
    assert "free OneKit web app" in output.out and "https://onekit.org" in output.out
    assert "usage: onekit" in output.out
    assert "everyday and agentic tools" in output.out
    assert "CONTRIBUTING.md" in output.out


def test_terminal_commands_include_homepage_without_polluting_json(monkeypatch, capsys):
    monkeypatch.setattr(sys.stderr, "isatty", lambda: True)
    assert main(["list", "--group", "audio"]) == 0
    assert "Welcome to OneKit" in capsys.readouterr().err
    assert main(["list", "--json", "--group", "audio"]) == 0
    output = capsys.readouterr()
    assert isinstance(json.loads(output.out), list)
    assert output.err == ""


def test_cli_contact_processing_is_independent_from_any_web_server(monkeypatch, tmp_path, capsys):
    def offline(*args, **kwargs):
        raise AssertionError("CLI processing must not contact a web server")
    monkeypatch.setattr(socket, "create_connection", offline)
    monkeypatch.setattr(socket.socket, "connect", offline)
    source = tmp_path / "contact.json"
    source.write_text('{"formatted_name":"Local Contact"}', encoding="utf-8")
    output = tmp_path / "contact.vcf"
    assert main(["run", "vcard-generate", str(source), "-o", str(output)]) == 0
    assert "FN:Local Contact" in output.read_text()
    assert str(output) in capsys.readouterr().out
