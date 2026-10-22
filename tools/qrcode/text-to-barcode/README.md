<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Generate barcode

Command: `onekit run text-to-barcode`. Use `onekit run --help` for input and output arguments.

Category: **qrcode**.
Fidelity: **exact**. Generates Code 128, Code 39, EAN-13, EAN-8, UPC-A, ITF and ISBN-13 locally. Retail check digits are validated or calculated; identifiers are not registered or assigned by OneKit.

Accepted types: `txt`. Output type: `png`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **1,024 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `barcode_type`, `format`, `module_width`, `height`, `quiet_zone`, `show_text`, `font_size`, `dpi`.

Python packages: python-barcode, Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/barcode/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
