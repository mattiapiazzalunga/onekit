<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->

Languages: [English](README.md) · [Italiano](docs/locales/it/README.md) · [Français](docs/locales/fr/README.md) · [Español](docs/locales/es/README.md) · [Deutsch](docs/locales/de/README.md) · [Русский](docs/locales/ru/README.md) · [中文](docs/locales/zh/README.md).

<p align="center">
  <a href="https://onekit.org"><img src="https://raw.githubusercontent.com/mattiapiazzalunga/onekit/main/images/logo.png" alt="OneKit logo" width="112" height="112"></a>
</p>
<h1 align="center">OneKit</h1>
<p align="center">One simple toolkit. Your files stay yours.</p>
<p align="center"><a href="https://github.com/mattiapiazzalunga/onekit/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/mattiapiazzalunga/onekit"></a> <a href="https://pypi.org/project/onekit-tools/"><img alt="PyPI" src="https://img.shields.io/pypi/v/onekit-tools"></a> <img alt="PolyForm-Shield-1.0.0" src="https://img.shields.io/badge/license-PolyForm_Shield_1.0.0-blue"> <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue"></p>

An offline Python toolkit with 230 tools for conversions, PDFs, images, archives, fonts, file inspection, encryption, developer utilities, OCR and comparisons. Use this CLI or the graphical interface at **[onekit.org](https://onekit.org)**.

**Source version:** `0.6.3`. Stable downloads exist only after the release workflow completes. The distribution is `onekit-tools`; the separately owned PyPI project called `onekit` is unrelated.

The [contact and media guide](docs/contact-media.md) covers standalone vCard generation, QR-to-vCard extraction, image upscaling, background removal, video compression/speed/GIF and local audio transcription.

License checks: inspect PDF, Word, PowerPoint, Excel, video, audio, images, fonts, EPUB, code/projects and datasets from files or public URLs. Analysis stays local; reports are **unverified estimates, not ownership certificates or permission to use**. See [license check usage and limits](docs/cli.md#local-license-and-copyright-estimates).

**Your CLI. Your agentic CLI.** Use OneKit yourself or let a local AI agent call it through a terminal or subprocess. Discover tools and requirements as JSON, pass explicit input/output paths and reuse saved `.1kit` workflows for repeatable file tasks. See [local agents and automation](docs/cli.md#local-agents-and-automation).

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

The base CLI has **no runtime dependencies**. Install only the extras you need. `all` includes the standard Python families; video downloading, background removal, transcription and cryptographic signing use the separate `video`, `background`, `transcription` and `signing` extras. Install native engines separately. For Node-based developer tools, install Node.js 24+ and run `onekit engines install`. The CLI prepares missing dependencies and external engines on first use. Background removal and transcription download model weights on first use, then reuse the local cache.

## Use

```sh
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit run pdf-extract-pages document.pdf --options '{"pages":"1,3-5"}' -o selected.pdf
onekit run image-convert image.png --options '{"format":"webp"}' -o image.webp
onekit run diff-notebook before.ipynb after.ipynb --options '{"mode":"code"}' -o changes.json
onekit run security-encrypt private-folder --ask-password -o private.zip
onekit run security-decrypt private.zip --ask-password -o restored
```

Options are JSON objects; pass them as one quoted shell argument. Use `--ask-password` for secrets. Existing outputs are preserved unless you pass `--force`.

`onekit list --group pdf`, `onekit list --json` and `onekit doctor TOOL_ID` expose contracts and requirements. Every tool has a directory under [tools](tools), containing metadata and a pointer to its shared implementation. See the [CLI guide](docs/cli.md) for options and limits.

## Toolkit

| Family | Capabilities |
| --- | --- |
| Converters | Markdown, HTML, LaTeX, PDF, Word, PowerPoint, images, Base64, Excel, CSV and JSON |
| PDF | Merge/split, page selection/order/removal, compression, repair, [direct text editing](docs/pdf-editing.md), text overlays, rotation, digital signatures, encryption/unlock, [local PDF/A conversion/validation](docs/pdfa.md) |
| Images | Extract embedded PDF images, compress, crop and change format |
| Media | Audio/video conversion through separately installed FFmpeg |
| Archives / fonts | ZIP/TAR variants; TTF/OTF containers and WOFF/WOFF2 |
| Inspector / security | Type signatures, structure, metadata, encoding, hashes, text counts; authenticated encrypted file/folder archives |
| Developer | Language-specific formatting, parser/compiler validation and selected minification |
| OCR | Scanned images/PDF to searchable PDF, Word, Markdown, LaTeX, HTML and JSON |
| Diff | Text, code, normalized JSON, notebooks, LaTeX, PDF and Word text |

## Pipelines and development

`onekit pipeline --steps workflow.1kit INPUTS -o OUTPUT` accepts a versioned `.1kit` workflow document. Each step receives prior outputs. Single-input steps map over multiple outputs; merge steps receive the collection. Incompatible types stop processing.

Report bugs and suggestions through [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues) or the [website request board](https://onekit.org/requests/). Contributors can find work in either place.

## Contribute to OneKit

Help build OneKit's open revolution: everyday tools for everyone, from hands-on tasks to workflows run by local AI agents. Contribute to make tools more efficient and effective: improve speed and memory use, fix incorrect results, add regression examples, or clarify documentation and agent workflows.

The core is Open Source (PolyForm Shield 1.0.0). Read the [contribution guide](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) and find a task in [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues), or suggest an improvement on the [request board](https://onekit.org/requests/).

## License and creator

Created by **[Mattia Piazzalunga](mailto:hello@mattiapiazzalunga.com)**. Copyright © 2026 Mattia Piazzalunga. Open Source (PolyForm Shield 1.0.0), licensed under [PolyForm Shield 1.0.0](LICENSE); see [NOTICE](NOTICE), [AUTHORS.txt](AUTHORS.txt) and [CONTRIBUTORS.txt](CONTRIBUTORS.txt). Third-party components retain their licenses. External engines are separate programs with their own redistribution obligations.

You may use, modify and redistribute the core for permitted purposes, including commercial and internal use. You may not use it to provide a product or service that competes with the software or with a product the licensor or its affiliates provides using the software; free offerings and different platforms or interfaces can also compete. When sharing copies, include the license text or its URL and any Required Notice lines supplied with the software. The full license governs, including its exceptions for new and discontinued products, patent terms and warranty disclaimer. Here, “Open Source (PolyForm Shield 1.0.0)” describes published source under these terms; the noncompete restriction means this is source-available software rather than unrestricted open source under the Open Source Definition. See [the licensing guide](docs/licenses.md).

Export and reimport workflows without processing input files:

```sh
onekit workflow export workflow.1kit -o exported-workflow.1kit
onekit workflow import workflow.1kit -o saved-workflow.1kit
onekit pipeline --steps saved-workflow.1kit input.json -o output.json
```

Standard barcodes are available in the QR codes & barcodes category and CLI: `text-to-barcode`, `scan-barcode`, `barcode-to-text`. Code 128, Code 39, EAN-13, EAN-8, UPC-A, ITF and ISBN-13 support PNG/SVG, configurable dimensions and check-digit validation. Install `onekit-tools[barcode]` or `onekit-tools[qrcode]`.

Permanent [PDF and image redaction](docs/redaction.md) is available through `pdf-redact` and `image-redact`. Selected regions become solid black pixels in newly encoded files. PDFs are rebuilt as image-only documents without original text, forms, comments, attachments or metadata; images become opaque PNGs without original metadata or hidden alpha pixels. Original files are left unchanged.

Add configurable PDF text watermarks with `pdf-watermark`: opacity, color, fonts, page ranges, visual positions, rotation and repeated grids. Text and graphics remain in the PDF. See the [watermark guide](docs/watermark.md).

## Contacts

- General questions and support: [support@onekit.org](mailto:support@onekit.org).
- Questions about the Open Source (PolyForm Shield 1.0.0) core and contributions: [developers@onekit.org](mailto:developers@onekit.org).
- Privacy, GDPR and personal-data requests: [privacy@onekit.org](mailto:privacy@onekit.org).
- Legal questions, licensing and permission requests: [legal@onekit.org](mailto:legal@onekit.org).
- Security vulnerabilities and abuse reports: [security@onekit.org](mailto:security@onekit.org).
