<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Compare Jupyter notebook files

Command: `onekit run diff-notebook`. Use `onekit run --help` for input and output arguments.

Category: **diff**. Browser support: **available**.
Fidelity: **exact**. Notebook comparison can include Markdown, code or both. LaTeX text mode omits commands.

Accepted types: `*`. Output type: `json`.
Accepts multiple inputs: **yes**.

Options: `mode`.

Python packages: standard library or external engine.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/diff/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
