<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# CLI reference

`onekit --version` reports the core version. `python -m onekit` invokes the same CLI.

| Command | Behavior |
| --- | --- |
| `onekit list [--group GROUP] [--json]` | Discover tools, contracts, availability and fidelity. |
| `onekit doctor [TOOL_ID] [--json]` | Check Python packages, engines and license-policy blocks. |
| `onekit run TOOL_ID INPUTS -o OUTPUT` | Process files; encryption also accepts directories. |
| `onekit pipeline --steps WORKFLOW INPUTS -o OUTPUT` | Execute 1–16 ordered tool steps from a JSON file. |
| `onekit engines install [--directory DIRECTORY]` | Install locked Node developer engines; requires Node/npm. |

`run` accepts `--options` with a JSON object, `--ask-password` and `--force`. Pipelines support the password prompt and overwrite flag too. Use a filename for one output or a directory for multiple outputs. Extensionless destinations are directories. Conflicting output names are rejected.

## Tool options

Pages are one based. `pages` accepts numbers and ascending ranges, such as `1,3-5`. Ordering and intentional duplicates are preserved for organize/extract. Rotation accepts multiples of 90 and defaults to all pages. PDF editing adds `text` to `page` at `x`/`y` PDF points from the lower-left origin; it does not reflow existing content. Signing requires a PKCS#12 `certificate` path and its `password`.

Image `format` supports PNG, JPEG, WebP, TIFF, BMP, ICO, GIF and PDF as applicable. `quality` is 1–100. `box` is `[left, top, right, bottom]` in pixels. Animation/metadata may be removed; transparency is flattened to white for JPEG/PDF. Compression can increase an already optimized file.

Spreadsheet `sheet` selects a worksheet, defaulting to the active one. Excel reading uses cached formula values. JSON-to-Excel expects an array of objects. CSV `delimiter` defaults to comma. Formula-like XLSX strings remain text; import untrusted CSV as text in spreadsheet applications.

Encoding conversion accepts `source_encoding` and `encoding`. Other text tools use UTF-8. Metadata `metadata` is a JSON object of ExifTool tag/value pairs; coverage is limited to its supported formats. Inspector signatures do not identify every proprietary file type.

Decryption defaults to restoring individual files. Set `restore` to `zip` to emit one `restored.zip` retaining nested folder paths; the browser provides the same option. Folder encryption in the browser uses the folder picker and processes its contents locally.

Notebook comparison `mode` is `both`, `markdown` or `code`. LaTeX mode is `all` or heuristic `text`. PDF/Word comparison extracts text. Diff JSON contains normalized sides, changed blocks and a unified patch, including trailing-newline differences. OCR `language` uses installed Tesseract codes and `dpi` is 36–300. PDF/A conversion requires a licensed `icc_profile`; validate archival output independently.

Media options include `format`, `codec` and `bitrate`, depending on the FFmpeg build. Fonts support `ttf`, `otf`, `woff` and `woff2`, preserving outline technology. Archives support ZIP and TAR/gzip/bzip2/xz combinations.

## Limits and errors

See [input validation](input-validation.md) for the enforced per-tool types, byte/count limits, signature/container checks and archive expansion rules. These apply to direct Python API calls and every pipeline step as well as the CLI. Run `onekit list --json` for exact machine-readable contracts.

Core inputs: 256 files and 128 MiB. Pipelines: 16 steps. Images/rendered pages: 40 million pixels. Comparisons: 10,000 lines and 2 million characters. Archive expansion: 128 MiB, 4096 entries and ratio checks. External engines have timeouts. Large valid inputs can exceed these deliberate limits.

Exit codes: 0 success; 1 incomplete doctor report; 2 input/processing error; 130 cancellation. Validators can successfully emit `valid: false`: inspect the report rather than assuming exit 0 means valid source. Type/import checking can require a complete project. Python syntax validation never executes the input.

English is the default. Future CLI translations use gettext domain `onekit` under `onekit/locales`; IDs, command names and JSON keys remain language-independent.

Notebook merge accepts `merge` with `from` (`left` or `right`) and the zero-based changed-cell `block` index, together with `mode`. It emits the updated target notebook and preserves excluded cells and notebook metadata. Unified patches describe the compared representation and are not generally patches for raw PDF, Word or notebook containers.

## Portable workflows

`onekit workflow export SOURCE -o workflow.onekit.json` validates a legacy steps array or a workflow document and saves a portable document. `onekit workflow import workflow.onekit.json -o saved.json` validates and saves an imported document. Both commands preserve the editor layout, omit passwords and refuse existing output paths unless `--force` is supplied. Neither command processes files.

Run an imported workflow with `onekit pipeline --steps saved.json INPUTS -o OUTPUT`. Legacy steps arrays remain supported. Workflow documents are UTF-8 JSON, at most 1 MiB, with the following structure:

```json
{
  "format": "onekit-workflow",
  "version": 1,
  "steps": [{"tool": "dev-format-json", "options": {}}],
  "layout": {
    "nodes": [
      {"x": 0, "y": 0, "expanded": false},
      {"x": 20, "y": 10, "expanded": true},
      {"x": 0, "y": 0, "expanded": false}
    ]
  }
}
```

`layout` is optional and ignored during execution. Nodes are ordered as input, steps, actions. Coordinates are finite pixel offsets from the default layout, bounded to ±10000. Version 1 supports 1–16 steps. Input files are selected separately. Passwords can be supplied with `--ask-password`. Exported browser-compatible workflows can be reopened using **Import workflow** in the web app; tools unavailable in the browser require the CLI.
