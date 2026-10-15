<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# LaTeX to PDF

Command: `onekit run latex-to-pdf`. Use `onekit run --help` for input and output arguments.

Category: **converters**. Browser support: **in development**.
Fidelity: **compromise**. Formatting, fonts, layout, formulas or unsupported elements may change. Scanned PDFs require OCR first.

Accepted types: `latex`. Output type: `pdf`.
Accepts multiple inputs: **no**.

Options: none.

Python packages: standard library or external engine.
External engines: pdflatex.

Processing implementation: [shared family adapter](../../../src/onekit/tools/converters/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
