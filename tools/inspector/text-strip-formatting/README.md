<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Remove text formatting

Command: `onekit run text-strip-formatting`. Use `onekit run --help` for input and output arguments.

Category: **inspector**.
Fidelity: **compromise**. Turn pasted text, UTF-8/UTF-16 text files, HTML, Markdown or Word DOCX body text into a UTF-8 TXT file locally. Removes styles, links and markup while retaining readable text and basic paragraph/table breaks. Plain text preserves literal punctuation. No OCR; DOCX headers, footers, images and comments are omitted. Up to 8 MiB per input.

Accepted types: `txt, html, md, docx`. Output type: `txt`.
Accepts multiple inputs: **no**.

Input validation: **any**. Required file count: **1–1**.
CLI: **8,388,608 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `input_format`.

Python packages: markdown-it-py, defusedxml.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/plain_text/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
