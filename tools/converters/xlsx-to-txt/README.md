<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Excel to TXT

Command: `onekit run xlsx-to-txt`. Use `onekit run --help` for input and output arguments.

Category: **converters**.
Fidelity: **compromise**. Exports one Excel worksheet as tab-separated UTF-8 text. Uses stored formula results without recalculation; formatting and other sheets are omitted.

Accepted types: `xlsx`. Output type: `txt`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `sheet`.

Python packages: openpyxl.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/text_converters.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
