<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Download image

Command: `onekit run image-download`. Use `onekit run --help` for input and output arguments.

Category: **images**.
Fidelity: **exact**. Download original PNG, JPEG, WebP, GIF, TIFF, BMP, ICO or AVIF bytes from a direct URL or the first accessible image exposed by a page. Up to 128 MiB. Sites may block access. Downloading does not grant usage rights.

Accepted types: `txt`. Output type: `*`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **16,384 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: none.

Python packages: standard library or external engine.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/link_tools.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
