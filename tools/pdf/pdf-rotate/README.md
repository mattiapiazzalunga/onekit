<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Rotate PDF

Command: `onekit run pdf-rotate`. Use `onekit run --help` for input and output arguments.

Category: **pdf**. Browser support: **available**.
Fidelity: **exact**. Page operations preserve content. Encryption permissions are advisory.

Accepted types: `pdf`. Output type: `pdf`.
Accepts multiple inputs: **no**.

Options: `angle`, `pages`.

Python packages: pycryptodome, pypdf.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdf/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
