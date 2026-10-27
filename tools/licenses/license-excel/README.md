<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Excel license checker

Command: `onekit run license-excel`. Use `onekit run --help` for input and output arguments.

Category: **licenses**.
Fidelity: **compromise**. An estimate based on declarations and metadata, not a rights certificate or legal clearance. Verify every finding with the original source and rights holder. Missing information never means free to use. Authors and copyright holders may differ. Files are analyzed locally; links are downloaded directly from their source. Archives are bounded and scans can be incomplete.

Accepted types: `xlsx, xlsm, xls`. Output type: `json`.
Accepts multiple inputs: **no**.

Input validation: **any**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `ref`.

Python packages: license-expression, defusedxml, olefile.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/license_check.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
