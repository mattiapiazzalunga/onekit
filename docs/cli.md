<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# CLI reference

Use `onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","opacity":0.25}'` to add a PDF text watermark. See the [watermark guide](watermark.md) for position, rotation, page ranges and repeated layouts.

Permanent redaction is available as `onekit run pdf-redact` and `onekit run image-redact`, with selectable areas supplied through `regions`. See the [redaction guide](redaction.md) for coordinates, rasterization and privacy guarantees of the exported files.

Use `onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"[0-9]+","flags":"g"}'` to test JavaScript regular expressions. Requires Node.js; see the [regex tester guide](regex.md) for captures, replacements and execution limits.

Standard barcodes are available through `onekit run text-to-barcode`, `onekit run scan-barcode` and `onekit run barcode-to-text`. Install the `barcode` or `qrcode` extra. See the [barcode settings and supported standards](qrcode.md#standard-linear-barcodes).

`onekit --version` reports the core version. `python -m onekit` invokes the same CLI.

| Command | Behavior |
| --- | --- |
| `onekit list [--group GROUP] [--json]` | Discover tools, contracts, availability and fidelity. |
| `onekit doctor [TOOL_ID] [--json]` | Check Python packages, engines and license-policy blocks. |
| `onekit run TOOL_ID INPUTS -o OUTPUT` | Process files; encryption also accepts directories. |
| `onekit pipeline --steps WORKFLOW INPUTS -o OUTPUT` | Execute 1–16 ordered tool steps from a JSON file. |
| `onekit engines install [--directory DIRECTORY]` | Install locked Node developer engines; requires Node/npm. |
| `onekit download URL -o OUTPUT [--quality best\|720\|1080] [--force]` | Download a single video through yt-dlp; requires internet and FFmpeg. |

`run` accepts `--options` with a JSON object, `--ask-password` and `--force`. Pipelines support the password prompt and overwrite flag too. Use a filename for one output or a directory for multiple outputs. Extensionless destinations are directories. Conflicting output names are rejected.

## Local agents and automation

**Your CLI. Your agentic CLI.** OneKit is useful both at your terminal and as a file-processing toolkit for local AI agents that can execute shell commands or launch subprocesses. An agent can discover tool contracts, check requirements, run a selected operation and inspect its output files.

```sh
onekit list --json
onekit doctor pdf-merge --json
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit pipeline --steps workflow.1kit input.pdf -o output/
```

`list --json` exposes tool IDs, accepted inputs, output formats, options, limits and fidelity notes. `doctor TOOL_ID --json` reports readiness, missing dependencies and license-policy blocks. Parse these JSON responses rather than the human-readable listings. `run` and `pipeline` write their results to the destination supplied with `-o`; they do not have a general `--json` response flag. Some tools produce JSON report files.

For a local agent, discover the tool first, check its requirements, then call it with explicit paths and a JSON object in `--options` where needed. Pass subprocess arguments as a list to preserve paths and JSON without shell quoting. Check the exit status before consuming outputs:

| Exit code | Meaning |
| --- | --- |
| `0` | Command completed successfully. |
| `1` | `doctor` found missing requirements or a policy block; inspect the report. |
| `2` | Invalid arguments or a processing/input/output error; read stderr. |
| `130` | Command cancelled with a keyboard interrupt. |

Choose a fresh output path for each job; existing outputs are preserved unless `--force` is supplied. `--ask-password` requires an interactive terminal. Prepare dependencies and model caches before unattended runs: missing components may trigger automatic setup and network downloads, and some native installers require interaction or elevated privileges. Network tools also contact their requested sources.

File processing runs on your machine. If the agent uses a remote model, the agent's handling of file content and command results determines what is sent to that provider. The same [PolyForm Shield license](licenses.md) applies to agent-driven use.

## Tool options

QR generation, vCard/Wi-Fi configuration, image scanning and reverse decoding are documented in the [QR code guide](qrcode.md). Install the `qrcode` extra, then use `onekit run text-to-qrcode input.txt -o code.png` or `onekit run scan-qrcode photo.jpg -o decoded.json`.

Pages are one based. `pages` accepts numbers and ascending ranges, such as `1,3-5`. Ordering and intentional duplicates are preserved for organize/extract. Rotation accepts multiples of 90 and defaults to all pages. PDF editing adds `text` to `page` at `x`/`y` PDF points from the lower-left origin; it does not reflow existing content. Signing requires a PKCS#12 `certificate` path and its `password`.

Image `format` supports PNG, JPEG, WebP, TIFF, BMP, ICO, GIF and PDF as applicable. `quality` is 1–100. `box` is `[left, top, right, bottom]` in pixels. Animation/metadata may be removed; transparency is flattened to white for JPEG/PDF. Compression can increase an already optimized file.

Spreadsheet `sheet` selects a worksheet, defaulting to the active one. Excel reading uses cached formula values. JSON-to-Excel expects an array of objects. CSV `delimiter` defaults to comma. Formula-like XLSX strings remain text; import untrusted CSV as text in spreadsheet applications.

Encoding conversion accepts `source_encoding` and `encoding`. Other text tools use UTF-8. Metadata `metadata` is a JSON object of ExifTool tag/value pairs; coverage is limited to its supported formats. Inspector signatures do not identify every proprietary file type.

Notebook comparison `mode` is `both`, `markdown` or `code`. LaTeX mode is `all` or heuristic `text`. PDF/Word comparison extracts text. Diff JSON contains normalized sides, changed blocks and a unified patch, including trailing-newline differences. OCR `language` uses installed Tesseract codes and `dpi` is 36–300. PDF/A conversion requires a licensed `icc_profile`; validate archival output independently.

Media options include `format`, `codec` and `bitrate`, depending on the FFmpeg build. Fonts support `ttf`, `otf`, `woff` and `woff2`, preserving outline technology. Archives support ZIP and TAR/gzip/bzip2/xz combinations.

## Limits and errors

See [input validation](input-validation.md) for the enforced per-tool types, byte/count limits, signature/container checks and archive expansion rules. These apply to direct Python API calls and every pipeline step as well as the CLI. Run `onekit list --json` for exact machine-readable contracts.

Core inputs: 256 files and 128 MiB. Pipelines: 16 steps. Images/rendered pages: 40 million pixels. Comparisons: 10,000 lines and 2 million characters. Archive expansion: 128 MiB, 4096 entries and ratio checks. External engines have timeouts. Large valid inputs can exceed these deliberate limits.

Exit codes: 0 success; 1 incomplete doctor report; 2 input/processing error; 130 cancellation. Validators can successfully emit `valid: false`: inspect the report rather than assuming exit 0 means valid source. Type/import checking can require a complete project. Python syntax validation never executes the input.

English is the default. Future CLI translations use gettext domain `onekit` under `onekit/locales`; IDs, command names and JSON keys remain language-independent.

Notebook merge accepts `merge` with `from` (`left` or `right`) and the zero-based changed-cell `block` index, together with `mode`. It emits the updated target notebook and preserves excluded cells and notebook metadata. Unified patches describe the compared representation and are not generally patches for raw PDF, Word or notebook containers.

## Image effects

`onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output`
combines blur, pixelation, box blur, solid cover and grayscale in one tool.
Use `scope: "selected"` with normalized rectangular `regions` to target specific
areas. See the [image effects guide](image-effects.md) for all options and limits.

## Portable workflows

`onekit workflow export SOURCE -o workflow.1kit` validates a legacy steps array or a workflow document and saves a portable document. `onekit workflow import workflow.1kit -o saved.1kit` validates and saves an imported document. Both commands omit passwords and refuse existing output paths unless `--force` is supplied. Neither command processes files.

Run an imported workflow with `onekit pipeline --steps saved.1kit INPUTS -o OUTPUT`. The .1kit extension identifies OneKit documents; legacy .json and .onekit.json workflow files and steps arrays remain supported. Workflow documents are UTF-8 JSON, at most 1 MiB, with the following structure:

```json
{
  "format": "onekit-workflow",
  "version": 1,
  "steps": [{"tool": "dev-format-json", "options": {}}]
}
```

## Automatic setup

`onekit run`, `onekit download` and `onekit pipeline` install missing Python packages and native engines before processing. Dependencies are kept in the user OneKit cache, without changing the system Python installation. Whisper and U2Net models download automatically on first use and are cached for later runs. OCR language data is fetched for the requested languages.

The first run needs an internet connection and enough disk space. Native engines use conda-forge through a private micromamba installation, or the system package manager for engines unavailable there; availability depends on the operating system and architecture. Setup failures stop processing with an error and can be retried. `onekit doctor` checks readiness without installing anything. `ONEKIT_CACHE` changes the setup cache location. `ONEKIT_ALLOW_COPYLEFT=0` continues to block restricted engines.

## Local license and copyright estimates

The `licenses` group provides `license-pdf`, `license-word`, `license-powerpoint`,
`license-excel`, `license-video`, `license-audio`, `license-image`, `license-font`,
`license-epub`, `license-code` and `license-dataset`.

```sh
onekit run license-image photo.jpg -o report.json
onekit run license-pdf --url https://example.org/document.pdf -o report.json
onekit run license-code project.zip -o report.json
onekit run license-code ./project -o report.json
onekit run license-code --url https://github.com/owner/repository --options '{"ref":"main"}' -o report.json
onekit run license-code --url https://gitlab.com/group/project -o report.json
onekit run license-dataset data.csv LICENSE metadata.json -o report.json
```

**Every result is an unverified estimate requiring manual verification.** It lists
declared metadata, copyright notices, creator names, SPDX syntax and tentative
license-text matches with their locations. It never certifies ownership or grants
permission to use a work. Missing declarations never mean public domain or free
to use. Creator names do not prove copyright ownership. Review the original
source, complete terms and intended use; project dependencies and assets may have
separate licenses. Official references explain standards, not the authenticity
or applicability of the declarations in an uploaded work.

## Downloads, image transforms and URL inspection

```sh
onekit run audio-youtube-download --url 'https://www.youtube.com/watch?v=VIDEO_ID' --options '{"format":"mp3","quality":"192"}' -o downloads/
onekit run audio-youtube-download --url 'https://youtu.be/VIDEO_ID' --options '{"format":"original"}' -o downloads/
onekit run audio-download --url 'https://example.org/audio.flac' -o downloads/
onekit run audio-download --url 'https://example.org/audio.wav' --options '{"format":"mp3","quality":"320"}' -o downloads/
onekit run image-download --url 'https://example.org/photo.jpg' -o downloads/
onekit run image-rotate-flip photo.png --options '{"angle":"90","flip":"horizontal"}' -o rotated.png
onekit run url-inspect --url 'https://example.org/path?x=1#section' -o report.json
```

YouTube audio extraction uses yt-dlp, EJS, Node.js, FFmpeg and FFprobe, all prepared
automatically when missing. It supports one completed video, original audio or MP3
at 64, 128, 192, 256 or 320 kbps, and a 128 MiB download/output limit. Higher MP3
bitrates do not restore quality lost in the source. No DRM bypass is provided.
Site support can change and login/protected/live/playlist content is unsupported.

**Use only where the service terms and applicable rights permit downloading.**
The tool does not establish that a particular download is authorized. Read the
[official YouTube terms](https://www.youtube.com/t/terms), which restrict download
and automated access except in authorized or legally permitted cases. Downloading
an image or audio file also does not grant redistribution or reuse rights.

Image rotation applies EXIF orientation first, rotates clockwise by 0/90/180/270
degrees, then reflects horizontally, vertically or both in the rotated coordinate
system. It exports a PNG preserving decoded RGBA pixels and transparency without
metadata; animated and multipage images are rejected. The limit is 40 million pixels.

### Remove text formatting

`onekit run text-strip-formatting document.docx -o plain.txt` exports Word body text as UTF-8 TXT. TXT, HTML and Markdown files are also supported, up to 8 MiB. Use `--options '{"input_format":"html"}'` to interpret HTML stored in a TXT file. No OCR is performed.

## Contribute to OneKit

Help build OneKit's open revolution: everyday tools for everyone, from hands-on tasks to workflows run by local AI agents. Contribute to make tools more efficient and effective: improve speed and memory use, fix incorrect results, add regression examples, or clarify documentation and agent workflows.

The core is Open Source (PolyForm Shield 1.0.0). Read the [contribution guide](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) and find a task in [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues), or suggest an improvement on the [request board](https://onekit.org/requests/).

Questions about the Open Source (PolyForm Shield 1.0.0) core and contributions: [developers@onekit.org](mailto:developers@onekit.org). General support: [support@onekit.org](mailto:support@onekit.org).
