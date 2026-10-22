<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# YouTube audio downloader

Command: `onekit run audio-youtube-download`. Use `onekit run --help` for input and output arguments.

Category: **audio**.
Fidelity: **compromise**. CLI only: extract one completed YouTube video's audio as original audio or MP3 at 64–320 kbps, up to 128 MiB. Use only when the service and applicable rights permit downloading. YouTube's terms restrict downloads; ownership alone is not a blanket authorization. No DRM bypass. Site availability can change. A higher MP3 bitrate cannot improve the source quality.

Accepted types: `txt`. Output type: `*`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **16,384 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `format`, `quality`.

Python packages: yt-dlp, yt-dlp-ejs.
External engines: ffmpeg, ffprobe, node.

Processing implementation: [shared family adapter](../../../src/onekit/tools/audio_youtube/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
