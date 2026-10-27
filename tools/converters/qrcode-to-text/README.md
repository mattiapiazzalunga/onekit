<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# QR code to text

Command: `onekit run qrcode-to-text`. Use `onekit run --help` for input and output arguments.

Category: **converters**.
Fidelity: **exact**. Reads QR payloads locally from an image; Reverse reveals the stored content, not the original image or generator settings. No links are opened automatically.

Accepted types: `png, jpeg, webp, bmp, gif`. Output type: `txt`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **16,777,216 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: none.

Python packages: Pillow, zxing-cpp.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/qrcode.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
