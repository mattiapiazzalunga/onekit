<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Decrypt files or folders

Command: `onekit run security-decrypt`. Use `onekit run --help` for input and output arguments.

Category: **security**. Browser support: **available**.
Fidelity: **exact**. Authenticated AES-256-GCM with scrypt. Losing the password makes recovery impossible.

Accepted types: `onekit`. Output type: `*`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Browser: **33,554,432 bytes per file**, **33,554,432 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `password`, `restore`.

Python packages: pycryptodome.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/security/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
