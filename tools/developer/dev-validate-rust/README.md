<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Validate Rust

Command: `onekit run dev-validate-rust`. Use `onekit run --help` for input and output arguments.

Category: **developer**. Browser support: **in development**.
Fidelity: **exact**. Validation checks the configured parser or compiler; project-wide types, imports and dependencies may require a local project.

Accepted types: `*`. Output type: `json`.
Accepts multiple inputs: **no**.

Options: none.

Python packages: standard library or external engine.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/developer/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
