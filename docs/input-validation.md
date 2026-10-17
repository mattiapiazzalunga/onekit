<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Input validation

Every catalog entry declares allowed input extensions, an input mode, minimum/maximum file counts and CLI/browser byte limits. The same contracts are exported with the browser core. `onekit list --json` and each generated tool directory expose the exact values. `execute` enforces them before invoking a processor; pipelines enforce them again at each step, including mapped outputs.

## Limits

| Scope | CLI | Browser |
| --- | --- | --- |
| Total input/output batch | 128 MiB, at most 256 files | 100 MiB global ceiling; 32 MiB unless the tool explicitly supports large files, at most 256 files |
| Text/developer input, including encoding conversion | 8 MiB per file | 8 MiB per file |
| Diff input | Exactly two files; text up to 8 MiB per file | Exactly two files, up to 2,000,000 bytes each |
| Raster image input | 64 MiB per file | 32 MiB per file |
| Font input | 16 MiB per file | 16 MiB per file |
| Other binary input | 128 MiB per file | 32 MiB per file |
| PDF merge | 2–256 files within the batch limit | 2–256 files within the batch limit |
| PDF merge, split, remove pages, organize, extract pages, repair, rotate, unlock | 128 MiB per file | 100 MiB per file and total input/output batch |
| Decoded raster images | At most 40 million pixels across frames | Same |
| Archive/Office expansion | At most 128 MiB of file data and 4096 entries | At most 32 MiB of file data and 4096 entries |

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

Extensions and browser MIME labels alone are never evidence of valid binary content. Format-specific processors still parse/decode the input after the shared checks. This contract bounds file data and returned results; it is not a process RSS or operating-system sandbox limit.

## Browser enforcement

File pickers advertise supported extensions. Selection and drag/drop use the same checks for count, size, extension and a small content prefix. Rejected selections are cleared and show an actionable error. Paste input and workflow submissions are checked too. The runtime validates generic payload sizes before creating a worker; the worker repeats envelope/tool checks, and the shared Python core performs the final content/structure validation. Direct worker/runtime calls cannot skip the core contracts. No file-processing upload endpoint is introduced.

The tests include negative cases across all 187 tools, renamed/corrupt binaries, Office container mismatches, oversized selections without reads, direct runtime calls, compressed bombs, forged ZIP counts, pipeline accumulation, media stream mismatches and legitimate inputs that must remain accepted.
