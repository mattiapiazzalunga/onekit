<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Remove PDF Watermark

Command: `onekit run pdf-remove-watermark`. Use `onekit run --help` for input and output arguments.

Category: **pdf**.
Fidelity: **compromise**. Inspect and remove selected text, images and form invocations, including nested forms and font-encoded text. Removes tagged watermark artifacts and watermark annotations automatically. Untagged objects require selection or exact text; flattened marks cannot be separated from their image. Review every page.

Accepted types: `pdf`. Output type: `pdf`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `text`, `mode`, `objects`.

Python packages: pypdf.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdf_design.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
