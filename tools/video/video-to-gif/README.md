<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Video to GIF

Command: `onekit run video-to-gif`. Use `onekit run --help` for input and output arguments.

Category: **video**.
Fidelity: **compromise**. Processes locally with FFmpeg. Re-encoding may lose quality. GIF output has no audio.

Accepted types: `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Output type: `gif`.
Accepts multiple inputs: **no**.

Input validation: **typed**. Required file count: **1–1**.
CLI: **134,217,728 bytes per file**, **134,217,728 bytes total**.
Content checks run before processing. Renaming a file does not change its actual format.

Options: `start`, `duration`, `fps`, `width`.

Python packages: standard library or external engine.
External engines: ffmpeg, ffprobe.

Processing implementation: [shared family adapter](../../../src/onekit/tools/video_edit/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
