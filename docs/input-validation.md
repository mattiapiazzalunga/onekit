<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Input validation

Every catalog entry declares accepted formats, file counts and byte limits. `onekit list --json` exposes the values. Both direct execution and pipelines enforce the contracts.

## Limits

The global batch ceiling is 128 MiB and 256 files. Text inputs are limited to 8 MiB per file, raster images to 64 MiB and fonts to 16 MiB. A diff requires exactly two inputs. Decoded raster images are limited to 40 million pixels across frames. Archive and Office expansion is limited to 128 MiB and 4096 entries.

Single-input tools reject extra files. Pipeline mapping deliberately applies a single-input step to each preceding output. Output collections are checked incrementally so a mapped step cannot accumulate unlimited returned data. CLI file counts, extensions and sizes are checked before reading file contents, and the actual bytes read are bounded even if a file grows during reading.

## Content rules

- PDF tools require PDF headers and a coherent final cross-reference location. `pdf-repair` deliberately permits damaged cross-references after checking the PDF header; its parser still has to recover an actual PDF. Images renamed to `.pdf` are rejected.
- Raster inputs are checked with Pillow for actual format, structure and decoded dimensions. A PNG renamed to JPEG is rejected. Base64 export also decodes the image before accepting it.
- Word, Excel and PowerPoint require distinct ZIP container parts and namespaced XML roots. Renaming Excel to `.docx` does not turn it into Word. Directory counts and expansion budgets are inspected before allocating the ZIP entry table or reading document parts.
- Fonts require matching SFNT/WOFF headers, valid bounded table ranges and coherent compressed-font sizes. Declared WOFF expansion cannot exceed the font byte budget.
- Media inputs have explicit audio/video extensions and container signatures. FFprobe verifies stream kinds before FFmpeg conversion; video conversion requires video, and audio conversion requires audio without ordinary video streams. Attached cover art is allowed. Both executables are reported by `doctor`.
- Archives reject unsafe/duplicate paths, symlinks, encrypted ZIP entries, invalid directories, multi-volume/ZIP64 directories and unsupported concatenated compressed streams. ZIP expansion ratios are bounded. TAR decompression is bounded before member/PAX parsing, with an additional fixed 4 MiB allowance for TAR headers/padding; XZ decoder memory is limited too.
- Decryption accepts only the OneKit encrypted format and authenticates its contents before bounded archive restoration. User options cannot increase the enforced expansion budget.
- Text tools require decodable text without binary control bytes. Developer tools accept their language extensions and neutral `.txt` input; shell/Dockerfile adapters also allow extensionless source. Validation tools intentionally accept syntactically invalid source and return `valid: false`. Encoding conversion uses the selected source encoding; other text tools require UTF-8.
- Inspection, metadata adapters and encryption intentionally accept arbitrary file types. Their count/byte limits still apply. Inspecting a damaged or unknown file is a supported operation, rather than a reason to reject it solely for its content.
