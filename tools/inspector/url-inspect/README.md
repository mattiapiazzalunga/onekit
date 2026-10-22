<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# URL inspector

Command: `onekit run url-inspect`. Use `onekit run --help` for input and output arguments.

Category: **inspector**.
Fidelity: **compromise**. Inspect URL components, HTTP status, final URL and available response headers directly from your device. Records up to 10 HTTP redirects. Network failures leave a partial report. This is not a phishing, malware, DNS or ownership check.

Accepted types: `txt`. Output type: `json`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **16,384 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: none.

Python packages: standard library or external engine.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/link_tools/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
