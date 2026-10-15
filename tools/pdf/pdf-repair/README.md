<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Repair PDF

Command: `onekit run pdf-repair`. Use `onekit run --help` for input and output arguments.

Category: **pdf**. Browser support: **available**.
Fidelity: **compromise**. Repair is best effort. Editing adds text overlays. Signing requires a PKCS#12 certificate.

Accepted types: `pdf`. Output type: `pdf`.
Accepts multiple inputs: **no**.

Options: none.

Python packages: pycryptodome, pypdf.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdf/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
