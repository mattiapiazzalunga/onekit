<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# TXT to Excel

Command: `onekit run txt-to-xlsx`. Use `onekit run --help` for input and output arguments.

Category: **converters**.
Fidelity: **exact**. Parses delimited TXT into an Excel worksheet. Cells are stored as text, preserving leading zeros and preventing formula execution. Requires consistent column counts.

Accepted types: `txt`. Output type: `xlsx`.
Accepts multiple inputs: **no**.

Input validation: **encoded-text**. Required file count: **1–1**.
CLI: **8,388,608 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `delimiter`, `source_encoding`.

Python packages: openpyxl.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/text_converters.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
