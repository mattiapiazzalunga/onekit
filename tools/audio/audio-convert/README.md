<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Convert audio

Command: `onekit run audio-convert`. Use `onekit run --help` for input and output arguments.

Category: **audio**. Browser support: **in development**.
Fidelity: **compromise**. Available codecs depend on your FFmpeg build; re-encoding can lose quality.

Accepted types: `*`. Output type: `*`.
Accepts multiple inputs: **no**.

Options: `format`, `codec`, `bitrate`.

Python packages: standard library or external engine.
External engines: ffmpeg.

Processing implementation: [shared family adapter](../../../src/onekit/tools/media/__init__.py).
Contracts and regression fixtures: [tests](../../../tests/test_core.py).
Engine setup and licenses: [engine guide](../../../docs/engines.md).

This directory is generated from the shared catalog by `python scripts/tool_docs.py`.
Edit the registry and family adapter, add regression fixtures, then regenerate the directory.
