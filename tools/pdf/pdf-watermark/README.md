<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Add watermark to PDF

Command: `onekit run pdf-watermark`. Use `onekit run --help` for input and output arguments.

Category: **pdf**.
Fidelity: **exact**. Adds a text or PNG/JPEG image watermark to all or selected pages, retaining source text and graphics. Supports Western European text, single or repeated layout, rotation and opacity. The original file is unchanged.

Accepted types: `pdf`. Output type: `pdf`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `text`, `pages`, `font`, `font_size`, `color`, `opacity`, `angle`, `position`, `layout`, `margin`, `watermark_type`, `image_base64`, `image_width`.

Python packages: pypdf, reportlab, Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdf.watermark/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
