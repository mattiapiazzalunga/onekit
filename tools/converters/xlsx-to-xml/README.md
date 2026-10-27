<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Excel to XML

Command: `onekit run xlsx-to-xml`. Use `onekit run --help` for input and output arguments.

Category: **converters**.
Fidelity: **exact**. XML tables use repeated flat records. JSON to XML preserves types using a typed root/item schema; XML attributes use @ and text uses #text in JSON. Spreadsheet formulas are not evaluated; the first sheet is used by default. Review schema and values after conversion.

Accepted types: `xlsx`. Output type: `xml`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `sheet`.

Python packages: openpyxl.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/structured_data.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
