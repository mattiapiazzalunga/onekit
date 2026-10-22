<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Convert audio

Command: `onekit run audio-convert`. Use `onekit run --help` for input and output arguments.

Category: **audio**.
Fidelity: **compromise**. Available codecs depend on your FFmpeg build; re-encoding can lose quality.

Accepted types: `mp3, wav, flac, ogg, aac, m4a, mp4, aif, aiff, opus, wma`. Output type: `*`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `format`, `codec`, `bitrate`.

Python packages: standard library or external engine.
External engines: ffmpeg, ffprobe.

Processing implementation: [shared family adapter](../../../src/onekit/tools/media/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
