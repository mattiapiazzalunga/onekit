<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Compress PDF

Command: `onekit run pdf-compress`. Use `onekit run --help` for input and output arguments.

Category: **pdf**.
Fidelity: **compromise**. Light preserves image quality. Balanced and Maximum may reduce image quality and resolution. The original is kept if no smaller output is found.

Accepted types: `pdf`. Output type: `pdf`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `compression_level`.

Python packages: pycryptodome, pypdf, Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdf/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
