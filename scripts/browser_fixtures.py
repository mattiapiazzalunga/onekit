# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
"""Generate the same real fixtures for CPython and browser regression tests."""
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]
from onekit import execute
from onekit.catalog import TOOLS
from test_core import browser_case

fixtures = []
for tool in TOOLS.values():
    if not tool.browser:
        continue
    files, options = browser_case(tool)
    result = execute(tool.id, files, options, browser=True)
    text_extensions = (".json", ".md", ".html", ".csv", ".base64", ".txt")
    fixtures.append({"tool": tool.id, "files": [{"name": f.name, "data": base64.b64encode(f.data).decode()} for f in files], "options": options, "expectedNames": [f.name for f in result.files], "expectedText": [{"name": f.name, "data": base64.b64encode(f.data).decode()} for f in result.files if f.name.endswith(text_extensions)]})
Path(sys.argv[1]).write_text(json.dumps(fixtures), encoding="utf-8")
