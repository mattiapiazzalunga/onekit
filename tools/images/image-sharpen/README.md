<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Sharpen and Deblur Image

Command: `onekit run image-sharpen`. Use `onekit run --help` for input and output arguments.

Category: **images**.
Fidelity: **compromise**. Unsharp masking or bounded Gaussian Richardson-Lucy deconvolution. Deblurring assumes a blur model and may amplify noise or halos; missing detail cannot be guaranteed. Deconvolution is limited to one million pixels.

Accepted types: `png, jpeg, webp, gif, bmp, tiff, ico`. Output type: `png`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `method`, `radius`, `amount`, `iterations`.

Python packages: Pillow, numpy.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/photo_tools.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
