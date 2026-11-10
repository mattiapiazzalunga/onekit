<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Text to PDF/UA

Command: `onekit run txt-to-pdfua`. Use `onekit run --help` for input and output arguments.

Category: **pdf**.
Fidelity: **exact**. Create a tagged PDF/UA-1 from plain text with a title and language. Blank lines separate paragraphs. Latin fonts only; review reading order and meaning. Automatic checks do not replace manual accessibility review.

Accepted types: `txt`. Output type: `pdf`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **262,144 bytes per file**, **8,388,608 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `title`, `language`.

Python packages: reportlab, pypdf, Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdfua.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
