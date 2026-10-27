<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Video to text

Command: `onekit run video-to-text`. Use `onekit run --help` for input and output arguments.

Category: **video**.
Fidelity: **compromise**. Transcribes the audio of a video locally with multilingual Whisper tiny. Exports UTF-8 text and timestamped segments. Recognition can make mistakes; this does not read subtitles or text visible in frames.

Accepted types: `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Output type: `txt`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `language`.

Python packages: faster-whisper.
External engines: see the developer engine matrix for language adapters.

Processing implementation: [shared family adapter](../../../src/onekit/tools/transcription.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
