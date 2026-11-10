# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import json
import socket
import sys

import pytest

from onekit.cli import main
from onekit.i18n import LANGUAGES, configure


def test_empty_invocation_welcomes_users_and_explains_commands(capsys):
    assert main([]) == 0
    output = capsys.readouterr()
    assert "Welcome to OneKit" in output.out
    assert "onekit.org" not in output.out
    assert "usage: onekit" in output.out
    assert "everyday and agentic tools" in output.out
    assert "CONTRIBUTING.md" in output.out


def test_terminal_commands_welcome_without_polluting_json(monkeypatch, capsys):
    monkeypatch.setattr(sys.stderr, "isatty", lambda: True)
    assert main(["list", "--group", "audio"]) == 0
    welcome = capsys.readouterr().err
    assert "Welcome to OneKit" in welcome
    assert "onekit.org" not in welcome
    assert main(["list", "--json", "--group", "audio"]) == 0
    output = capsys.readouterr()
    assert isinstance(json.loads(output.out), list)
    assert output.err == ""


@pytest.mark.parametrize("language", LANGUAGES)
@pytest.mark.parametrize("arguments", [[], ["--help"], ["run", "--help"], ["list", "--help"]])
def test_cli_presentation_does_not_advertise_webapp(language, arguments, capsys):
    try:
        if "--help" in arguments:
            with pytest.raises(SystemExit) as result:
                main(["--language", language, *arguments])
            assert result.value.code == 0
        else:
            assert main(["--language", language, *arguments]) == 0
        output = capsys.readouterr()
        assert "onekit.org" not in output.out + output.err
    finally:
        configure("en")


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
