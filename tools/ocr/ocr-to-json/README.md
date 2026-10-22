<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# OCR to JSON

Command: `onekit run ocr-to-json`. Use `onekit run --help` for input and output arguments.

Category: **ocr**.
Fidelity: **compromise**. Recognition depends on scan quality and installed language packs. Equations and layout may need manual correction.

Accepted types: `pdf, png, jpeg, webp, gif, bmp, tiff, ico`. Output type: `json`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `language`, `dpi`.

Python packages: pytesseract, Pillow, pypdfium2, python-docx.
External engines: tesseract.

Processing implementation: [shared family adapter](../../../src/onekit/tools/ocr/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
