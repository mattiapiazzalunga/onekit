<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Image to PowerPoint

Command: `onekit run image-to-pptx`. Use `onekit run --help` for input and output arguments.

Category: **converters**.
Fidelity: **compromise**. Formatting, fonts, layout, formulas or unsupported elements may change. Scanned PDFs require OCR first.

Accepted types: `png, jpeg, webp, gif, bmp, tiff, ico`. Output type: `pptx`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **67,108,864 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: none.

Python packages: python-pptx, Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/converters/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
