<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Compare JSON files

Command: `onekit run diff-json`. Use `onekit run --help` for input and output arguments.

Category: **diff**. Browser support: **available**.
Fidelity: **exact**. Notebook comparison can include Markdown, code or both. LaTeX text mode omits commands.

Accepted types: `json, txt`. Output type: `json`.
Accepts multiple inputs: **yes**.

Input validation: **text**. Required file count: **2–2**.
CLI: **8,388,608 bytes per file**, **134,217,728 bytes total**.
Browser: **2,000,000 bytes per file**, **33,554,432 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: none.

Python packages: standard library or external engine.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/diff/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
