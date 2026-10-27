<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Remove Image Watermark

Command: `onekit run image-remove-watermark`. Use `onekit run --help` for input and output arguments.

Category: **images**.
Fidelity: **compromise**. Reconstruct manually selected watermark areas from surrounding pixels using harmonic diffusion. Estimates missing content; large marks, textures and faces may not reconstruct convincingly. No automatic mark detection.

Accepted types: `png, jpeg, webp, gif, bmp, tiff, ico`. Output type: `png`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `regions`, `iterations`.

Python packages: Pillow, numpy.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/photo_tools.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
