<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Trim video

Command: `onekit run video-trim`. Use `onekit run --help` for input and output arguments.

Category: **video**.
Fidelity: **compromise**. Keeps the selected start-to-end range in seconds and exports MP4 with audio when present. Re-encoding may lose quality.

Accepted types: `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Output type: `mp4`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `start`, `end`.

Python packages: standard library or external engine.
External engines: ffmpeg, ffprobe.

Processing implementation: [shared family adapter](../../../src/onekit/tools/video_edit.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
