<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Extract images from PDF

Command: `onekit run image-extract-pdf`. Use `onekit run --help` for input and output arguments.

Category: **images**.
Fidelity: **exact**. Preserves the selected content; validate important outputs.

Accepted types: `pdf`. Output type: `image`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **67,108,864 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: none.

Python packages: pycryptodome, pypdf, Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/images/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
