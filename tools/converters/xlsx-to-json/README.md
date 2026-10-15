<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Excel to JSON

Command: `onekit run xlsx-to-json`. Use `onekit run --help` for input and output arguments.

Category: **converters**. Browser support: **available**.
Fidelity: **compromise**. Formatting, fonts, layout, formulas or unsupported elements may change. Scanned PDFs require OCR first.

Accepted types: `xlsx`. Output type: `json`.
Accepts multiple inputs: **no**.

Options: `sheet`.

Python packages: openpyxl.
External engines: soffice.

Processing implementation: [shared family adapter](../../../src/onekit/tools/converters/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
