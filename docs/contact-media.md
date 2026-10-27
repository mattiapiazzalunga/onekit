<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Contacts, image enlargement and local media tools

| Tool | Input | Options | Output |
| --- | --- | --- | --- |
| `vcard-generate` | Contact JSON, as for `vcard-to-qrcode` | Contact fields belong in the input JSON | VCF 3.0 / 4.0 |
| `qrcode-to-vcard` | QR image containing a complete vCard | None | One VCF per detected contact |
| `image-upscale` | Single-frame image | `scale`: 2 (default), 3 or 4 | PNG |
| `image-remove-background` | Single-frame image | None | Transparent PNG |
| `video-compress` | Video | `compression_level`: light, balanced (default), maximum | MP4, or original if smaller |
| `video-speed` | Video | `speed`: 0.25–4, default 2 | MP4 with synchronized, pitch-preserving audio |
| `video-to-gif` | Video | `start`: seconds, `duration`: 0.1–30, `fps`: 1–30, `width`: 64–1280 | Looping GIF without audio |
| `audio-to-text` | Audio | `language`: auto (default), it, en or another Whisper language code | TXT and timestamp JSON |

Install only the Python extras needed:

```sh
python -m pip install 'onekit-tools[qrcode,images,background,transcription]'
```

Video operations also need `ffmpeg` and `ffprobe` on PATH. The CLI uses the installed
FFmpeg build; supported codecs depend on that build. `onekit doctor TOOL` checks
the required engines and packages.

```sh
onekit run vcard-generate contact.json -o contact.vcf
onekit run qrcode-to-vcard contact-qr.png -o contacts/
onekit run image-upscale photo.png --options '{"scale":2}' -o larger.png
onekit run image-remove-background portrait.jpg -o transparent.png
onekit run video-compress clip.mov --options '{"compression_level":"balanced"}' -o compressed/
onekit run video-speed clip.mp4 --options '{"speed":0.5}' -o slower.mp4
onekit run video-to-gif clip.mp4 --options '{"start":1,"duration":3,"fps":12,"width":480}' -o clip.gif
onekit run audio-to-text voice.wav --options '{"language":"it"}' -o transcript/
```

Contact JSON example:

```json
{"first_name":"Ada","last_name":"Lovelace","version":"3.0","emails":["ada@example.org"]}
```

QR extraction accepts complete vCard 3.0/4.0 payloads with a display name. It does
not follow contact download URLs or convert arbitrary QR text into contact data.
Upscaling uses Lanczos resampling, not an AI model. Output is limited to 40 million
pixels. Animated images are rejected by the Python image adapters.

The CLI background adapter loads U2Net directly with ONNX Runtime, avoiding
rembg's Pillow <13 dependency constraint. Model downloads are checksum-verified
and cached under the local OneKit model cache. Optional model engines remain
separate from the portable `all` extra.
