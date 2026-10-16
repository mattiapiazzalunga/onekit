<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
<p align="center"><img src="images/logo.svg" alt="OneKit" width="120"></p>
<h1 align="center">OneKit</h1>
<p align="center">One simple toolkit. Your files stay yours.</p>
<p align="center"><a href="https://github.com/mattiapiazzalunga/onekit/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/mattiapiazzalunga/onekit"></a> <a href="https://pypi.org/project/onekit-tools/"><img alt="PyPI" src="https://img.shields.io/pypi/v/onekit-tools"></a> <img alt="Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-blue"> <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue"></p>

An offline Python toolkit for conversions, PDFs, images, archives, fonts, file inspection, encryption, developer utilities, OCR and comparisons. Use this CLI or the graphical interface at **[onekit.org](https://onekit.org)**. Both use the same processing core and catalog.

**Status:** release candidate `0.2.0`. Stable downloads exist only after the release workflow completes. The distribution is `onekit-tools`; the separately owned PyPI project called `onekit` is unrelated.

## Install

Python 3.11+ is required. The universal wheel supports Windows, macOS and Linux on x64/ARM64. Optional native libraries and external engines have additional platform requirements.

After publication:

```sh
python -m pip install onekit-tools
python -m pip install "onekit-tools[pdf,images,documents]"
onekit list
onekit doctor
```

From a source checkout:

```sh
python -m pip install -e ".[all,test]"
python -m onekit --help
python -m pytest -q
```

The base CLI has **no runtime dependencies**. Install only the extras you need. `all` includes the standard Python families; cryptographic signing uses the separate `signing` extra. Install native engines separately. For Node-based developer tools, install Node.js 24+ and run `onekit engines install`. Processing never silently downloads compiler/converter programs.

## Use

```sh
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit run pdf-extract-pages document.pdf --options '{"pages":"1,3-5"}' -o selected.pdf
onekit run image-convert image.png --options '{"format":"webp"}' -o image.webp
onekit run diff-notebook before.ipynb after.ipynb --options '{"mode":"code"}' -o changes.json
onekit run security-encrypt private-folder --ask-password -o private.onekit
onekit run security-decrypt private.onekit --ask-password -o restored
```

Options are JSON objects; pass them as one quoted shell argument. Use `--ask-password` for secrets. Existing outputs are preserved unless you pass `--force`.

`onekit list --group pdf`, `onekit list --json` and `onekit doctor TOOL_ID` expose contracts and requirements. Every tool has a directory under [tools](tools), containing metadata and a pointer to its shared implementation. See the [CLI guide](docs/cli.md) for options and limits.

## Toolkit

| Family | Capabilities |
| --- | --- |
| Converters | Markdown, HTML, LaTeX, PDF, Word, PowerPoint, images, Base64, Excel, CSV and JSON |
| PDF | Merge/split, page selection/order/removal, compression, repair, text overlays, rotation, digital signatures, encryption/unlock, external PDF/A conversion/validation |
| Images | Extract embedded PDF images, compress, crop and change format |
| Media | Audio/video conversion through separately installed FFmpeg |
| Archives / fonts | ZIP/TAR variants; TTF/OTF containers and WOFF/WOFF2 |
| Inspector / security | Type signatures, structure, metadata, encoding, hashes, text counts; authenticated encrypted file/folder archives |
| Developer | Language-specific formatting, parser/compiler validation and selected minification |
| OCR | Scanned images/PDF to searchable PDF, Word, Markdown, LaTeX, HTML and JSON |
| Diff | Text, code, normalized JSON, notebooks, LaTeX, PDF and Word text |

Content-preserving operations and conversions with compromises are distinguished explicitly. PDF-to-Word reconstructs extracted text, not original layout. OCR is not guaranteed exact. Fonts retain their outline technology. The browser exposes only tools verified in its worker; native-only features remain in development there.

## Pipelines and development

`onekit pipeline --steps workflow.json INPUTS -o OUTPUT` accepts a portable `onekit-workflow` JSON document exported by the web app, or a legacy ordered JSON array of `{ "tool": "...", "options": {} }` steps. Each receives prior outputs. Single-input steps map over multiple outputs; merge steps receive the collection. Incompatible types stop processing.

Read [architecture](docs/architecture.md), [engine setup and licenses](docs/engines.md), [release operations](docs/releases.md), [contribution requirements](CONTRIBUTING.md) and [security](SECURITY.md). New features and fixes require regression tests. GitHub Actions checks platform compatibility, browser contracts, native integrations, security, licenses and packaging before publication. Dependabot monitors locks, browser requirements, Node engines, Actions and Docker. Conservative compatible lock-only updates can auto-merge after all checks.

Report bugs and suggestions through [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues) or the [website request board](https://onekit.org/requests/). Contributors can find work in either place.

## License and creator

Created by **[Mattia Piazzalunga](https://www.mattiapiazzalunga.com)**. Copyright © 2026 Mattia Piazzalunga. Licensed under [Apache-2.0](LICENSE); see [NOTICE](NOTICE), [AUTHORS.txt](AUTHORS.txt) and [CONTRIBUTORS.txt](CONTRIBUTORS.txt). Third-party components retain their licenses. External engines are separate programs with their own redistribution obligations.

Export and reimport workflows without processing input files:

```sh
onekit workflow export steps.json -o workflow.onekit.json
onekit workflow import workflow.onekit.json -o saved-workflow.json
onekit pipeline --steps saved-workflow.json input.json -o output.json
```

The web app imports and exports the same versioned JSON, including block positions and expansion state. Workflow files contain tool settings; input files and passwords are excluded from exports. Reenter passwords before running. Browser imports report unsupported tools or option values without replacing the current workflow. CLI-only workflows can still be imported, exported and run with the CLI.
