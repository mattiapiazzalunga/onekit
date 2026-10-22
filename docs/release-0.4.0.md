<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# OneKit 0.4.0

Model engines are optional: install the `background` or `transcription` extra
when needed. U2Net runs directly with ONNX Runtime and a checksum-verified cached
model. Whisper uses faster-whisper. Files remain local; the first run downloads
model weights. Video processing requires FFmpeg and ffprobe. Video downloading
uses the separate `video` extra.

Updates Pillow to 13 and the certifi lock to address published advisories.
The portable `all` extra remains separate from model engines and signing.
