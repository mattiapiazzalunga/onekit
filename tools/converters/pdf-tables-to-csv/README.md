<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# PDF tables to CSV

Command: `onekit run pdf-tables-to-csv`. Use `onekit run --help` for input and output arguments.

Category: **converters**.
Fidelity: **compromise**. Detects tables from aligned selectable text. Scans require OCR; complex layouts, merged cells and column alignment require review. Excel uses one sheet per table; CSV exports one file per table.

Accepted types: `pdf`. Output type: `csv`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `pages`.

Python packages: pycryptodome, pypdf.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdf_tables.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
