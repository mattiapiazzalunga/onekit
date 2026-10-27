<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Calculate checksum

Command: `onekit run file-checksum`. Use `onekit run --help` for input and output arguments.

Category: **inspector**.
Fidelity: **exact**. Calculates SHA-256, SHA-512, SHA-1 or MD5 locally. An optional expected checksum can be compared against one file. A checksum does not verify a digital signature or establish file safety.

Accepted types: `*`. Output type: `json`.
Accepts multiple inputs: **yes**.

Input validation: **any**. Required file count: **1–20**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `algorithm`, `expected`.

Python packages: standard library or external engine.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/file_checksum.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
