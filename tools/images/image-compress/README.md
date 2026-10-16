<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Compress image

Command: `onekit run image-compress`. Use `onekit run --help` for input and output arguments.

Category: **images**. Browser support: **available**.
Fidelity: **compromise**. Lossy formats discard detail. Animation and metadata can be removed; use a lossless format to preserve pixels.

Accepted types: `png, jpeg, webp, gif, bmp, tiff, ico`. Output type: `image`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **67,108,864 bytes per file**, **134,217,728 bytes total**.
Browser: **33,554,432 bytes per file**, **33,554,432 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `format`, `quality`.

Python packages: Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/images/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
