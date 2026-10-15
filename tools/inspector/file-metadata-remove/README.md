<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Remove metadata

Command: `onekit run file-metadata-remove`. Use `onekit run --help` for input and output arguments.

Category: **inspector**. Browser support: **in development**.
Fidelity: **exact**. Preserves the selected content; validate important outputs.

Accepted types: `*`. Output type: `*`.
Accepts multiple inputs: **no**.

Options: none.

Python packages: standard library or external engine.
External engines: exiftool.

Processing implementation: [shared family adapter](../../../src/onekit/tools/inspector/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
