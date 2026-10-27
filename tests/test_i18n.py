import json
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


def test_language_option_works_before_or_after_command(capsys):
    for arguments in (["--language", "it", "--help"], ["run", "--language", "it", "--help"]):
        with pytest.raises(SystemExit) as error:
            cli.main(arguments)
        assert error.value.code == 0
        output = capsys.readouterr().out
        assert "OneKit" in output
        assert "--language" in output or "--output" in output
        assert "https://onekit.org" in output
        assert "show this help message and exit" not in output


def test_language_never_changes_machine_readable_tool_contracts(capsys):
    reports = []
    for language in ("en", "it", "fr", "es", "de", "ru", "zh"):
        assert cli.main(["--language", language, "list", "--json"]) == 0
        reports.append(json.loads(capsys.readouterr().out))
    assert all(report == reports[0] for report in reports)


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
            relative = re.sub(r"^docs/locales/(?:it|fr|es|de|ru|zh)/", "", relative)
            result.append(relative + (separator + fragment if separator else ""))
        return Counter(result)

    failures = []
    for name in sources:
        original_path = root / name
        original = original_path.read_text(encoding="utf-8")
        original_code = [block for kind, block in blocks(original) if kind == "code"]
        original_links = destinations(original_path, original)
        for language in i18n.LANGUAGES:
            if language == "en":
                continue
            target = root / "docs/locales" / language / name
            translated = target.read_text(encoding="utf-8")
            assert [block for kind, block in blocks(translated) if kind == "code"] == original_code, (language, name)
            actual_links = destinations(target, translated)
            if actual_links != original_links:
                failures.append((language, name, dict(original_links - actual_links), dict(actual_links - original_links)))
    assert not failures, failures[:12]
