<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Add page numbers to PDF

Command: `onekit run pdf-page-numbers`. Use `onekit run --help` for input and output arguments.

Category: **pdf**.
Fidelity: **exact**. Adds sequential numbers to all or selected pages, retaining source text and graphics. Existing digital signatures are invalidated.

Accepted types: `pdf`. Output type: `pdf`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `pages`, `start_number`, `number_style`, `font_size`, `position`, `margin`, `color`.

Python packages: pypdf, reportlab.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdf.page_numbers/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
