<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Verify digital signature

Command: `onekit run signature-verify`. Use `onekit run --help` for input and output arguments.

Category: **security**.
Fidelity: **exact**. Offline cryptographic verification of PDF and CMS/P7M/P7S signatures using embedded certificates. Detached signatures require the original file. Trust chains, revocation, qualified-signature status and trusted timestamps are not checked.

Accepted types: `*`. Output type: `json`.
Accepts multiple inputs: **yes**.

Input validation: **any**. Required file count: **1–2**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: none.

Python packages: pypdf, asn1crypto, pycryptodome.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/signatures.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
