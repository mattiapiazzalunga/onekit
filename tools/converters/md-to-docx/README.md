<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Markdown to Word

Command: `onekit run md-to-docx`. Use `onekit run --help` for input and output arguments.

Category: **converters**. Browser support: **available**.
Fidelity: **compromise**. CommonMark headings, lists, emphasis and code are exported. Images, advanced layouts and Markdown extensions may need adjustment.

Accepted types: `md`. Output type: `docx`.
Accepts multiple inputs: **no**.

Options: none.

Python packages: markdown-it-py, python-docx.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/converters/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
