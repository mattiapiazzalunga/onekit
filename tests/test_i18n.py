import json
import argparse
import ast
import inspect
import subprocess
import sys
import re
from collections import Counter
from pathlib import Path

import pytest

from onekit import cli, i18n


@pytest.fixture(autouse=True)
def restore_language():
    yield
    i18n.configure("en")


@pytest.mark.parametrize("language", ["it", "pt", "hi"])
def test_language_option_works_before_or_after_command(capsys, language):
    for arguments in (["--language", language, "--help"], ["run", "--language", language, "--help"]):
        with pytest.raises(SystemExit) as error:
            cli.main(arguments)
        assert error.value.code == 0
        output = capsys.readouterr().out
        assert "OneKit" in output
        assert "--language" in output or "--output" in output
        assert "onekit.org" not in output
        assert "CONTRIBUTING.md" in output
        assert "show this help message and exit" not in output


def test_language_never_changes_machine_readable_tool_contracts(capsys):
    reports = []
    for language in i18n.LANGUAGES:
        assert cli.main(["--language", language, "list", "--json"]) == 0
        reports.append(json.loads(capsys.readouterr().out))
    assert all(report == reports[0] for report in reports)


@pytest.mark.parametrize("locale_name, expected", [
    ("pt-PT", "pt"), ("pt_BR.UTF-8", "pt"), ("Portuguese_Brazil", "pt"),
    ("Português", "pt"), ("hi_IN.UTF-8", "hi"), ("Hindi_India", "hi"), ("हिंदी", "hi"),
])
def test_new_languages_accept_regional_and_native_locale_names(monkeypatch, locale_name, expected):
    monkeypatch.setenv("ONEKIT_LANGUAGE", locale_name)
    assert i18n.configure() == expected
    assert i18n.gettext("Interface language") != "Interface language"


@pytest.mark.parametrize("language", ["pt", "hi"])
def test_new_languages_localize_cli_errors_without_changing_option_keys(capsys, language):
    assert cli.main(["--language", language, "run", "dev-format-json", "--options", "[]", "-o", "output"]) == 2
    error = capsys.readouterr().err
    assert "OneKit" in error and "--options" in error and "JSON" in error
    assert "must contain a JSON object" not in error


@pytest.mark.parametrize("language", ["pt", "hi"])
def test_language_option_overrides_environment(monkeypatch, capsys, language):
    monkeypatch.setenv("ONEKIT_LANGUAGE", "en")
    assert cli.main(["--language", language]) == 0
    output = capsys.readouterr().out
    assert "Your files stay yours" not in output
    assert "--language" in output


@pytest.mark.parametrize("language, expected", [("pt", "Formatar JSON"), ("hi", "JSON फ़ॉर्मैट करें")])
def test_new_languages_translate_generated_tool_names_in_human_list(capsys, language, expected):
    assert cli.main(["--language", language, "list", "--group", "developer"]) == 0
    output = capsys.readouterr().out
    assert "dev-format-json" in output
    assert expected in output
    assert "Format JSON" not in output


@pytest.mark.parametrize("language", ["pt", "hi"])
def test_every_tool_has_a_translated_presentation_name(language):
    i18n.configure(language)
    for tool in cli.TOOLS.values():
        assert i18n.gettext(tool.name) != tool.name, (language, tool.id, tool.name)


def test_localized_error_preserves_interpolated_file_names(monkeypatch):
    monkeypatch.setattr(i18n, "_catalog", {"Cannot read '{0}'.": "Impossibile leggere '{0}'."})
    monkeypatch.setattr(i18n, "_patterns", [(i18n.re.compile(r"^Cannot read '(.*?)'\.$"), ["{0}"], "Impossibile leggere '{0}'.")])
    assert i18n.gettext("Cannot read '日本語 {1}.txt'.") == "Impossibile leggere '日本語 {1}.txt'."


def test_catalogs_remain_aligned():
    root_directory = Path(__file__).resolve().parents[1]
    source_check = subprocess.run([sys.executable, str(root_directory / "scripts/localization_inventory.py"), "--check"], capture_output=True, text=True, encoding="utf-8")
    assert source_check.returncode == 0, source_check.stdout + source_check.stderr
    root = Path(i18n.__file__).parent / "locales"
    source = json.loads((root / "en.json").read_text(encoding="utf-8"))
    for language in i18n.LANGUAGES:
        catalog = json.loads((root / f"{language}.json").read_text(encoding="utf-8"))
        assert catalog.keys() == source.keys(), language
        for key, value in catalog.items():
            assert sorted(i18n.re.findall(r"\{\d+\}", key)) == sorted(i18n.re.findall(r"\{\d+\}", value)), (language, key)


def test_registered_argparse_messages_cover_current_python():
    root = Path(__file__).resolve().parents[1]
    registered = json.loads((root / 'scripts/argparse-messages.json').read_text(encoding='utf-8'))['messages']
    current = set()
    source = re.sub(r'(?m)^(\s*)lazy import ', r'\1import ', inspect.getsource(argparse))
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('_', 'ngettext'):
            for argument in node.args[:2 if node.func.id == 'ngettext' else 1]:
                if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                    current.add(argument.value)
    assert current <= set(registered), current - set(registered)


def test_translated_documentation_preserves_code_and_link_destinations(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root / "scripts"))
    from localization_markdown import blocks

    sources = json.loads((root / "docs/localization-sources.json").read_text(encoding="utf-8"))
    def destinations(path, content):
        prose = "".join(block for kind, block in blocks(content) if kind != "code")
        links = re.findall(r"\]\(([^)]*)\)", prose)
        links += [match[1] for match in re.findall(r"\b(?:src|href)=([\"'])([^\"']+)\1", prose)]
        result = []
        for link in links:
            if re.match(r"[a-z]+:", link) or link.startswith("/"):
                result.append(link)
                continue
            destination, separator, fragment = link.partition("#")
            resolved = (path.parent / destination).resolve() if destination else path.resolve()
            relative = resolved.relative_to(root).as_posix()
            codes = "|".join(re.escape(code) for code in i18n.LANGUAGES if code != "en")
            relative = re.sub(rf"^docs/locales/(?:{codes})/", "", relative)
            result.append(relative + (separator + fragment if separator else ""))
        return Counter(result)

    failures = []
    for name in sources:
        original_path = root / name
        original = original_path.read_text(encoding="utf-8")
        original_code = [block for kind, block in blocks(original) if kind == "code"]
        original_inline = Counter(match[0] for kind, block in blocks(original) if kind != "code"
                                  for match in re.finditer(r"(?P<tick>`+).*?(?P=tick)", block))
        original_links = destinations(original_path, original)
        for language in i18n.LANGUAGES:
            if language == "en":
                continue
            target = root / "docs/locales" / language / name
            translated = target.read_text(encoding="utf-8")
            assert [block for kind, block in blocks(translated) if kind == "code"] == original_code, (language, name)
            translated_inline = Counter(match[0] for kind, block in blocks(translated) if kind != "code"
                                        for match in re.finditer(r"(?P<tick>`+).*?(?P=tick)", block))
            assert translated_inline == original_inline, (language, name, original_inline - translated_inline,
                                                          translated_inline - original_inline)
            actual_links = destinations(target, translated)
            if actual_links != original_links:
                failures.append((language, name, dict(original_links - actual_links), dict(actual_links - original_links)))
    assert not failures, failures[:12]
