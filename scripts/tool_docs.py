# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Generate each tool's own directory without duplicating processing logic."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from onekit.catalog import manifest

for tool in manifest():
    if sys.argv[1:] and tool['id'] not in sys.argv[1:]:
        continue
    directory = ROOT / "tools" / tool["group"] / tool["id"]
    directory.mkdir(parents=True, exist_ok=True)
    metadata = {"copyright": "Copyright 2026 Mattia Piazzalunga", "spdx": "LicenseRef-PolyForm-Shield-1.0.0", **tool}
    (directory / "tool.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    implementation = tool["handler"] + (".py" if (ROOT / "src" / "onekit" / "tools" / (tool["handler"] + ".py")).is_file() else "/__init__.py")
    text = f"""<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# {tool['name']}

Command: `onekit run {tool['id']}`. Use `onekit run --help` for input and output arguments.

Category: **{tool['group']}**.
Fidelity: **{tool['fidelity']}**. {tool['note']}

Accepted types: `{', '.join(tool['accepts'])}`. Output type: `{tool['produces']}`.
Accepts multiple inputs: **{'yes' if tool['multiple'] else 'no'}**.

Input validation: **{tool['input_mode']}**. Required file count: **{tool['min_files']}–{tool['max_files']}**.
CLI: **{tool['max_file_bytes']:,} bytes per file**, **{tool['max_total_bytes']:,} bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: {', '.join('`'+name+'`' for name in tool['options']) or 'none'}.

Python packages: {', '.join(tool['packages']) or 'standard library or external engine'}.
External engines: {', '.join(tool['engines']) or 'see the developer engine matrix for language adapters'}.

Processing implementation: [shared family adapter](../../../src/onekit/tools/{implementation}).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
"""
    (directory / "README.md").write_text(text, encoding="utf-8")
