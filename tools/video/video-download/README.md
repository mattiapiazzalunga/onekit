<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Download video

Command: `onekit run video-download`. Use `onekit run --help` for input and output arguments.

Category: **video**.
Fidelity: **exact**. Downloads from YouTube and other yt-dlp sites, up to 128 MiB. Site support varies; an internet connection is required.

Accepted types: `txt`. Output type: `*`.
Accepts multiple inputs: **no**.

Input validation: **text**. Required file count: **1–1**.
CLI: **16,384 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `quality`, `cookies`, `cookies_from_browser`, `format_id`, `referer`, `list_formats`.

Python packages: yt-dlp.
External engines: ffmpeg.

Processing implementation: [shared family adapter](../../../src/onekit/tools/video_download.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
