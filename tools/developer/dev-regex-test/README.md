<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Regex tester

Command: `onekit run dev-regex-test`. Use `onekit run --help` for input and output arguments.

Category: **developer**.
Fidelity: **exact**. Tests JavaScript regular expressions locally with captures, named groups, UTF-16 positions and replacement. Up to 128 KiB of text, 1000 matches and 1 MiB of output. Execution is time limited; the CLI requires Node.js.

Accepted types: `txt`. Output type: `json`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **131,072 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `pattern`, `flags`, `max_matches`, `enable_replacement`, `replacement`.

Python packages: standard library or external engine.
External engines: node.

Processing implementation: [shared family adapter](../../../src/onekit/tools/regex_tester.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
