<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# OneKit 0.5.0

Initial release of the offline CLI and Python processing API with 230 tools for
documents, PDFs, images, media, archives, fonts, developer utilities, QR codes,
license declarations and file inspection. The base installation has no runtime
dependencies; optional extras and external engines enable the selected tools.

Includes bounded input validation, reusable workflows, local dependency setup,
format-specific processing contracts and source-based license inspection.
License reports remain unverified estimates that require manual review.

Performance updates accelerate opaque-image preparation and text inspection.
Unused imports and redundant developer-engine assignments have been removed.

Model engines are optional: install the `background` or `transcription` extra
when needed. U2Net runs directly with ONNX Runtime and a checksum-verified cached
model. Whisper uses faster-whisper. Files remain local; the first run downloads
model weights. Video processing requires FFmpeg and ffprobe. Video downloading
uses the separate `video` extra.

Updates Pillow to 13 and the certifi lock to address published advisories.
The portable `all` extra remains separate from model engines and signing.
