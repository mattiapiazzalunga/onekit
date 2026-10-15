<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Validate pdfa PDF

Command: `onekit run pdf-validate-pdfa`. Use `onekit run --help` for input and output arguments.

Category: **pdf**. Browser support: **in development**.
Fidelity: **exact**. Page operations preserve content. Encryption permissions are advisory.

Accepted types: `pdf`. Output type: `json`.
Accepts multiple inputs: **no**.

Options: none.

Python packages: standard library or external engine.
External engines: verapdf.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdf/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
