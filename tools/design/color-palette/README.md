<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Color Palette Generator

Command: `onekit run color-palette`. Use `onekit run --help` for input and output arguments.

Category: **design**.
Fidelity: **exact**. Five-color OKLCH palettes with sRGB chroma reduction and WCAG text contrast. Harmony rules are design heuristics, not accessibility guarantees.

Accepted types: `txt`. Output type: `json`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **128 bytes per file**, **1,048,576 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `harmony`, `lightness`, `chroma`, `hue`, `format`.

Python packages: standard library or external engine.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/design.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
