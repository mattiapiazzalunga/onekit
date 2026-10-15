# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
"""A retry may reuse existing identical PyPI files, never different files."""
import json
import urllib.error
import urllib.request
from pathlib import Path

manifest = json.loads(Path("release/onekit-release.json").read_text())
try:
    with urllib.request.urlopen(f"https://pypi.org/pypi/onekit-tools/{manifest['version']}/json", timeout=30) as response:
        remote = json.load(response)
except urllib.error.HTTPError as exc:
    if exc.code != 404:
        raise
else:
    expected = {file["name"]: file["sha256"] for file in manifest["assets"]}
    for file in remote.get("urls", []):
        if expected.get(file["filename"]) != file["digests"]["sha256"]:
            raise SystemExit("Existing PyPI distribution differs. Refusing to continue publication.")
