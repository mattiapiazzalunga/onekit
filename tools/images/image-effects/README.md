<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Blur, pixelate & image effects

Command: `onekit run image-effects`. Use `onekit run --help` for input and output arguments.

Category: **images**.
Fidelity: **compromise**. Blur, pixelate, box blur, solid cover or grayscale in one tool. Apply to the whole image or selected areas, with adjustable intensity and a fresh PNG export. Blur and pixelation do not guarantee permanent removal of sensitive details. Single-frame images only.

Accepted types: `png, jpeg, webp, gif, bmp, tiff, ico`. Output type: `png`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `effect`, `scope`, `strength`, `color`, `regions`.

Python packages: Pillow.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/image_effects.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
