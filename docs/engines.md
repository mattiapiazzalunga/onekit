<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# External engines and licenses

The owner approved separately installed open-source engines. They are not bundled in the Python wheel, source download or initial Docker image. `onekit doctor` reports requirements. `ONEKIT_ALLOW_COPYLEFT=0` explicitly disables listed copyleft adapters. Keep upstream tools updated; local subprocesses are not a complete sandbox for hostile documents.

| Engine | Command | Use / license considerations |
| --- | --- | --- |
| LibreOffice | `soffice` / `libreoffice` | Office → PDF/images; MPL and third-party notices. |
| Pandoc | `pandoc` | Advanced markup conversion; GPL. |
| TeX Live/pdfTeX | `pdflatex` | LaTeX/Pandoc PDF; engine, macros and fonts have separate licenses. |
| FFmpeg | `ffmpeg` | Media; LGPL or GPL depending on build and codecs. |
| veraPDF | `verapdf` | Optional independent verification of archival outputs; upstream GPL/MPL and Java requirements. |
| ExifTool | `exiftool` | Metadata in supported file types; upstream Perl licensing. |
| Tesseract | `tesseract` | OCR; Apache engine and separately licensed language data. |

If distributing these programs, including inside Docker, preserve their licenses/notices and provide the required corresponding-source/build materials. Assess AGPL network integrations separately. Commercial use and source/redistribution obligations are different questions. Separate processes do not universally eliminate obligations. Read authoritative [FFmpeg](https://ffmpeg.org/legal.html), [LibreOffice](https://www.libreoffice.org/licenses/), [Ghostscript](https://www.ghostscript.com/licensing/) and [MPL](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) material before creating a bundled distribution.

Office fidelity depends on fonts and resources. PDF-to-Word exports extracted text; PDF-to-PowerPoint creates image slides. PDF repair is best effort; compression is lossless. [PDF/A conversion and validation](pdfa.md) use separate MPL libraries through the shared Python adapter, with bundled licensed ICC profiles. Ghostscript is not required. Independent standards validation remains recommended. OCR accuracy depends on scan quality and language packs.

## Developer tools

Install Node.js 24+ and run `onekit engines install` for locked Prettier/plugins, esbuild, HTML minifier, SVGO and GraphQL.js. They install in the user's OneKit cache, not globally. `ONEKIT_NODE_ENGINE_PATH` selects an alternative. Rerun the installer after an approved engine update. The parser group covers JS/TS/JSX/TSX, markup, stylesheets, Markdown/MDX, GraphQL, Vue, Svelte, Astro, Solidity and PHP.

Install upstream compilers/launchers for your OS and add the documented commands to PATH. Some isolated files need their project dependencies or exact Java class filename. Formatting/parser validation does not prove project-wide type correctness.

On Windows, Bash/Shell adapters prefer an actual interpreter on PATH and then detect Git for Windows in its standard system/user installation directories. The System32 WSL launcher is not treated as a compatible local parser. PowerShell syntax validation requires `pwsh`; formatting additionally requires PSScriptAnalyzer (`Install-Module PSScriptAnalyzer -Scope CurrentUser`). `onekit doctor dev-format-powershell` checks that module separately and reports its setup command. These programs/modules are not downloaded while processing files.

## Platform qualifications

CI license checks also install and traverse the separate signing extra (`scripts/check_licenses.py --include-signing`). MIT-0 is recognized as a permissive license ([SPDX text](https://spdx.org/licenses/MIT-0.html)). The locked `certifi` 2026.7.22 Mozilla trust-store data is an explicit version-specific MPL-2.0 exception; retain its unmodified upstream license/notices when redistributing it ([upstream notice](https://github.com/certifi/python-certifi/blob/master/LICENSE)). New versions require another review. This exception does not generally admit other MPL packages or change OneKit's PolyForm-Shield-1.0.0 license.

The universal Python core supports Linux, Windows and macOS including ARM64. Native extras and external engines determine additional requirements. CI declares x64/ARM runners on all three OS families. On Windows ARM, Brotli/WOFF2 and the separate signing cryptography stack may require native build tools or x64 Python under emulation. WOFF/TTF/OTF do not require the WOFF2 encoder. The `all` extra excludes separate signing. Report these optional constraints rather than claiming a native wheel exists when it does not.
