<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Edit PDF

Command: `onekit run pdf-edit`. Use `onekit run --help` for input and output arguments.

Category: **pdf**.
Fidelity: **compromise**. Edit supported text boxes using the original font. Longer text is fitted to its original width. Scans, text inside reusable forms and unavailable font characters cannot be edited. This is not a redaction tool. The legacy text option adds an overlay.

Accepted types: `pdf`. Output type: `pdf`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `mode`, `edits`, `password`, `text`, `x`, `y`, `page`.

Python packages: pycryptodome, pypdf, reportlab.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdf/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
