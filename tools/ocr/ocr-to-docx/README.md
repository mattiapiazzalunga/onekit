<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# OCR to Word

Command: `onekit run ocr-to-docx`. Use `onekit run --help` for input and output arguments.

Category: **ocr**. Browser support: **in development**.
Fidelity: **compromise**. Recognition depends on scan quality and installed language packs. Equations and layout may need manual correction.

Accepted types: `pdf, png, jpeg, webp, gif, bmp, tiff, ico`. Output type: `docx`.
Accepts multiple inputs: **no**.

Options: `language`, `dpi`.

Python packages: pytesseract, Pillow, pypdfium2, python-docx.
External engines: tesseract.

Processing implementation: [shared family adapter](../../../src/onekit/tools/ocr/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
