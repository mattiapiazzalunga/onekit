<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# TXT to CSV

Command: `onekit run txt-to-csv`. Use `onekit run --help` for input and output arguments.

Category: **converters**.
Fidelity: **exact**. Parses consistently delimited TXT rows and writes comma-separated CSV. Choose tabs, commas, semicolons, pipes or automatic detection. No column structure is guessed from prose.

Accepted types: `txt`. Output type: `csv`.
Accepts multiple inputs: **no**.

Input validation: **encoded-text**. Required file count: **1–1**.
CLI: **8,388,608 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `delimiter`, `source_encoding`.

Python packages: standard library or external engine.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/text_converters.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
