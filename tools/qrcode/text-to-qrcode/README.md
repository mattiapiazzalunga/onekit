<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Text to QR code

Command: `onekit run text-to-qrcode`. Use `onekit run --help` for input and output arguments.

Category: **qrcode**.
Fidelity: **exact**. Creates a standard QR code locally. Capacity depends on the content and error correction. Keep the quiet zone and test the code before printing.

Accepted types: `txt`. Output type: `png`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **16,384 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `format`, `shape`, `corner_style`, `overlay_type`, `overlay_text`, `overlay_image_base64`, `overlay_size`, `error_correction`, `scale`, `border`, `dark`, `light`, `transparent_background`, `include_payload`.

Python packages: segno, Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/qrcode/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
