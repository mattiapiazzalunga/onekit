<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Markdown to LaTeX

Command: `onekit run md-to-latex`. Use `onekit run --help` for input and output arguments.

Category: **converters**. Browser support: **in development**.
Fidelity: **compromise**. Formatting, fonts, layout, formulas or unsupported elements may change. Scanned PDFs require OCR first.

Accepted types: `md`. Output type: `latex`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **8,388,608 bytes per file**, **134,217,728 bytes total**.
Browser: **8,388,608 bytes per file**, **33,554,432 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: none.

Python packages: standard library or external engine.
External engines: pandoc.

Processing implementation: [shared family adapter](../../../src/onekit/tools/converters/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
