<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Video to frames

Command: `onekit run video-to-frames`. Use `onekit run --help` for input and output arguments.

Category: **video**.
Fidelity: **compromise**. Extracts PNG frames from a video using FFmpeg. Choose start, duration and width. Up to 120 frames: original-frame mode preserves each frame in the interval; otherwise timestamps are sampled at the requested frame rate.

Accepted types: `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Output type: `png`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `start`, `duration`, `fps`, `width`, `all_frames`.

Python packages: Pillow.
External engines: ffmpeg, ffprobe.

Processing implementation: [shared family adapter](../../../src/onekit/tools/video_edit.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
