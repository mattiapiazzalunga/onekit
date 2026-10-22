<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Permanently redact PDF

Command: `onekit run pdf-redact`. Use `onekit run --help` for input and output arguments.

Category: **pdf**.
Fidelity: **compromise**. Permanently masks selected areas and rebuilds every page from raster pixels. Original text, attachments, comments, forms and metadata are not copied; selectable text and vector quality are lost. The original file is unchanged.

Accepted types: `pdf`. Output type: `pdf`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `regions`, `dpi`.

Python packages: pypdfium2, Pillow, reportlab, pypdf.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/redaction/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
