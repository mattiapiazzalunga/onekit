<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Convert text encoding

Command: `onekit run file-encoding-convert`. Use `onekit run --help` for input and output arguments.

Category: **inspector**.
Fidelity: **exact**. Preserves the selected content; validate important outputs.

Accepted types: `*`. Output type: `*`.
Accepts multiple inputs: **no**.

Input validation: **encoded-text**. Required file count: **1–1**.
CLI: **8,388,608 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `source_encoding`, `encoding`.

Python packages: standard library or external engine.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/inspector/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
