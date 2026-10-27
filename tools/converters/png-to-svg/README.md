<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# PNG to SVG

Command: `onekit run png-to-svg`. Use `onekit run --help` for input and output arguments.

Category: **converters**.
Fidelity: **compromise**. Vectorizes a PNG as palette-based vector tiles, without embedding a bitmap. Gradients and fine detail are approximated; transparent pixels are composited on white.

Accepted types: `png`. Output type: `svg`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `colors`, `resolution`.

Python packages: Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/vector_images.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
