<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# HTML to JSON

Command: `onekit run html-to-json`. Use `onekit run --help` for input and output arguments.

Category: **converters**. Browser support: **available**.
Fidelity: **compromise**. Structured conversion; the output represents the source data.

Accepted types: `html`. Output type: `json`.
Accepts multiple inputs: **no**.

Options: none.

Python packages: standard library or external engine.
External engines: pandoc.

Processing implementation: [shared family adapter](../../../src/onekit/tools/converters/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
