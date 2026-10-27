<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Color Picker

Command: `onekit run color-picker`. Use `onekit run --help` for input and output arguments.

Category: **design**.
Fidelity: **exact**. Read a six-digit HEX color from TXT or sample an EXIF-oriented image pixel. Reports visible sRGB, original RGBA, OKLCH and text contrast. Transparent pixels are composited on white.

Accepted types: `png, jpeg, webp, gif, bmp, tiff, ico, txt`. Output type: `json`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `x`, `y`.

Python packages: Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/photo_tools.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
