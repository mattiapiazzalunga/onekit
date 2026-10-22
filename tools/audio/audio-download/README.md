<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Download audio

Command: `onekit run audio-download`. Use `onekit run --help` for input and output arguments.

Category: **audio**.
Fidelity: **compromise**. Download a direct audio file or an audio source exposed by an accessible page. Original mode preserves downloaded bytes; MP3 conversion is lossy. Up to 128 MiB. Login and protected streams may prevent downloads. Use only with permission.

Accepted types: `txt`. Output type: `*`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **16,384 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `format`, `quality`.

Python packages: standard library or external engine.
External engines: ffmpeg, ffprobe.

Processing implementation: [shared family adapter](../../../src/onekit/tools/link_tools/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
