# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Run the shared JavaScript regex engine in a bounded Node process."""
import json
from pathlib import Path

from ..models import Artifact, Result
from .native import command


def run(tool, files, options):
    request = json.dumps({"text": files[0].text(), "options": options}).encode()
    script = Path(__file__).with_name("regex_cli.mjs")
    # Allow cold/emulated Node startup without extending the regex execution budget.
    output = command("node", ["--max-old-space-size=96", script], script.parent, stdin=request, timeout=15)
    report = json.loads(output)
    warnings = ["Match results were truncated by the configured match or output limit."] if report["truncated"] else []
    if report.get("replacementError"):
        warnings.append(report["replacementError"])
    return Result([Artifact("regex-results.json", json.dumps(report, ensure_ascii=False, indent=2).encode())], warnings=warnings, details=report)
