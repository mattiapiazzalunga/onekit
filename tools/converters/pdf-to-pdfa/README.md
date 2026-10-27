<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# PDF to PDF/A

Command: `onekit run pdf-to-pdfa`. Use `onekit run --help` for input and output arguments.

Category: **converters**.
Fidelity: **compromise**. Convert to PDF/A-2b or 3b locally with embedded fonts. The exact output is validated before download. Unsupported content can be removed or rejected; review the result.

Accepted types: `pdf`. Output type: `pdfa`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `icc_profile`, `profile`.

Python packages: pdftopdfa, pikepdf, jsonschema, fonttools, pdfminer.six.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/converters/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
