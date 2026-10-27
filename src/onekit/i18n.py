"""CLI presentation catalogs. Processing values and document formats stay stable."""
from __future__ import annotations

import json
import locale
import os
import re
from pathlib import Path

_language_config = json.loads((Path(__file__).parent / "locales/languages.json").read_text(encoding="utf-8"))
LANGUAGES = tuple(_language_config)
_catalog = {}
_patterns = []
_language = "en"


def configure(language=None):
    global _catalog, _patterns, _language
    try:
        system_language = locale.getlocale()[0]
    except ValueError:
        system_language = None
    preferred = language or os.environ.get("ONEKIT_LANGUAGE") or os.environ.get("LANGUAGE") or os.environ.get("LC_ALL") or os.environ.get("LC_MESSAGES") or os.environ.get("LANG") or system_language or "en"
    aliases = {alias: code for code, settings in _language_config.items() for alias in settings.get("aliases", [])}
    _language = "en"
    for candidate in preferred.split(":"):
        candidate = candidate.split(".")[0].replace("_", "-").lower()
        while candidate:
            canonical = aliases.get(candidate, candidate)
            if canonical in LANGUAGES:
                _language = canonical
                break
            candidate = candidate.rsplit("-", 1)[0] if "-" in candidate else ""
        if candidate:
            break
    path = Path(__file__).parent / "locales" / f"{_language}.json"
    _catalog = json.loads(path.read_text(encoding="utf-8")) if path.exists() and _language != "en" else {}
    _patterns = []
    for key, value in sorted(_catalog.items(), key=lambda item: len(re.sub(r"\{\d+\}", "", item[0])), reverse=True):
        if not re.search(r"\{\d+\}", key):
            continue
        tokens = re.findall(r"\{\d+\}", key)
        pattern = "".join("([\\s\\S]*?)" if re.fullmatch(r"\{\d+\}", part) else re.escape(part) for part in re.split(r"(\{\d+\})", key))
        _patterns.append((re.compile("^" + pattern + "$"), tokens, value))
    return _language


def gettext(value):
    if not isinstance(value, str) or not _catalog:
        return value
    key = re.sub(r"\s+", " ", value).strip()
    translated = _catalog.get(key)
    if translated is None:
        for pattern, tokens, template in _patterns:
            match = pattern.fullmatch(key)
            if match:
                translated = re.sub(r"\{\d+\}", lambda token: match[tokens.index(token[0]) + 1] if token[0] in tokens else token[0], template)
                break
    if translated is None:
        return value
    start = len(value) - len(value.lstrip())
    end = len(value.rstrip())
    return value[:start] + translated + value[end:]


configure()
