<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Validate PDF/A

Command: `onekit run pdf-validate-pdfa`. Use `onekit run --help` for input and output arguments.

Category: **pdf**.
Fidelity: **exact**. Validate PDF/A-1b, 2b or 3b with pikepdf. Unsupported constructs are reported as not checked, never as compliant. Other conformance levels are not supported.

Accepted types: `pdf`. Output type: `json`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `profile`.

Python packages: pikepdf, jsonschema, fonttools.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/pdf/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
