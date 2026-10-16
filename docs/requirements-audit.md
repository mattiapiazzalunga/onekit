<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: Apache-2.0 -->
# Requirements and local execution audit

16 October 2026. All 187 original tool IDs are covered by the independent prompt regression in `tests/test_requirements.py`. The implementation uses the existing shared catalog and family adapters. Later browser runtime/navigation changes were retained.

Real local processing covered 118 distinct tool IDs, using selected fixtures and options. This is not a claim that every format, compiler or operating system was tested. Browser tools were also invoked through the CLI and graphical controls. Native Node tools were exercised through real installed engines and the CLI. Java, PowerShell, Bash/Shell, Python formatting, PDF rasterization/slides and PDF metadata received additional local checks.

The default Python suite and selected native cases are recorded in the webapp verification report and the workspace requirements report. Twelve existing native integration cases require absent document/media/OCR engines and were not rerun here. Other external developer engines, PDF/A validation and PKCS#12 signing remain subject to their installation and dedicated integration verification.

The standard runtime license inventory passed locally. Signing dependency metadata was additionally checked at locked PyPI versions without loading incompatible Windows ARM native extensions; the CI security job now installs and audits the actual signing extra. MIT-0 is recognized, and the exact unmodified certifi 2026.7.22 MPL trust-store data has a documented version-specific exception.

## Per-tool evidence

`Executed` means a real local processor run on at least one fixture. `Adapter inspected` means the implementation/catalog was checked but its native processing was not executed in this audit. Tool requirements are documented in each generated tool directory and `docs/engines.md`.

| Tool | Browser | Local processing evidence |
| --- | --- | --- |
| `md-to-latex` | In development | Adapter inspected; engine verification required |
| `md-to-json` | Enabled; GUI verified | Executed |
| `md-to-html` | Enabled; GUI verified | Executed |
| `md-to-pdf` | In development | Adapter inspected; engine verification required |
| `md-to-docx` | Enabled; GUI verified | Executed |
| `pdf-to-pdfa` | In development | Adapter inspected; engine verification required |
| `pdf-to-png` | In development | Executed |
| `pdf-to-jpeg` | In development | Executed |
| `pdf-to-webp` | In development | Executed |
| `pdf-to-tiff` | In development | Executed |
| `pdf-to-docx` | Enabled; GUI verified | Executed |
| `pdf-to-html` | Enabled; GUI verified | Executed |
| `pdf-to-pptx` | In development | Executed |
| `pdf-to-md` | Enabled; GUI verified | Executed |
| `image-to-base64` | Enabled; GUI verified | Executed |
| `image-to-pdf` | Enabled; GUI verified | Executed |
| `image-to-pptx` | Enabled; GUI verified | Executed |
| `base64-to-image` | Enabled; GUI verified | Executed |
| `docx-to-pdf` | In development | Adapter inspected; engine verification required |
| `docx-to-png` | In development | Adapter inspected; engine verification required |
| `docx-to-md` | Enabled; GUI verified | Executed |
| `pptx-to-pdf` | In development | Adapter inspected; engine verification required |
| `pptx-to-png` | In development | Adapter inspected; engine verification required |
| `latex-to-html` | In development | Adapter inspected; engine verification required |
| `latex-to-pdf` | In development | Adapter inspected; engine verification required |
| `latex-to-md` | In development | Adapter inspected; engine verification required |
| `html-to-pdf` | In development | Adapter inspected; engine verification required |
| `html-to-latex` | In development | Adapter inspected; engine verification required |
| `html-to-json` | Enabled; GUI verified | Executed |
| `html-to-md` | Enabled; GUI verified | Executed |
| `xlsx-to-pdf` | In development | Adapter inspected; engine verification required |
| `xlsx-to-csv` | Enabled; GUI verified | Executed |
| `xlsx-to-json` | Enabled; GUI verified | Executed |
| `json-to-xlsx` | Enabled; GUI verified | Executed |
| `csv-to-xlsx` | Enabled; GUI verified | Executed |
| `csv-to-json` | Enabled; GUI verified | Executed |
| `pdf-merge` | Enabled; GUI verified | Executed |
| `pdf-split` | Enabled; GUI verified | Executed |
| `pdf-remove-pages` | Enabled; GUI verified | Executed |
| `pdf-organize` | Enabled; GUI verified | Executed |
| `pdf-extract-pages` | Enabled; GUI verified | Executed |
| `pdf-compress` | Enabled; GUI verified | Executed |
| `pdf-repair` | Enabled; GUI verified | Executed |
| `pdf-edit` | Enabled; GUI verified | Executed |
| `pdf-rotate` | Enabled; GUI verified | Executed |
| `pdf-sign` | In development | Adapter inspected; engine verification required |
| `pdf-protect` | Enabled; GUI verified | Executed |
| `pdf-unlock` | Enabled; GUI verified | Executed |
| `pdf-validate-pdfa` | In development | Adapter inspected; engine verification required |
| `image-compress` | Enabled; GUI verified | Executed |
| `image-crop` | Enabled; GUI verified | Executed |
| `image-convert` | Enabled; GUI verified | Executed |
| `image-extract-pdf` | Enabled; GUI verified | Executed |
| `video-convert` | In development | Adapter inspected; engine verification required |
| `audio-convert` | In development | Adapter inspected; engine verification required |
| `archive-convert` | Enabled; GUI verified | Executed |
| `font-convert` | Enabled; GUI verified | Executed |
| `file-inspect` | Enabled; GUI verified | Executed |
| `file-metadata-set` | In development | Executed |
| `file-metadata-remove` | In development | Executed |
| `file-count` | Enabled; GUI verified | Executed |
| `file-encoding-convert` | Enabled; GUI verified | Executed |
| `security-encrypt` | Enabled; GUI verified | Executed |
| `security-decrypt` | Enabled; GUI verified | Executed |
| `dev-format-javascript` | In development | Executed |
| `dev-format-typescript` | In development | Executed |
| `dev-format-jsx` | In development | Executed |
| `dev-format-tsx` | In development | Executed |
| `dev-format-python` | In development | Executed |
| `dev-format-java` | In development | Adapter inspected; engine verification required |
| `dev-format-c` | In development | Adapter inspected; engine verification required |
| `dev-format-cpp` | In development | Adapter inspected; engine verification required |
| `dev-format-csharp` | In development | Adapter inspected; engine verification required |
| `dev-format-go` | In development | Adapter inspected; engine verification required |
| `dev-format-rust` | In development | Adapter inspected; engine verification required |
| `dev-format-php` | In development | Executed |
| `dev-format-ruby` | In development | Adapter inspected; engine verification required |
| `dev-format-kotlin` | In development | Adapter inspected; engine verification required |
| `dev-format-swift` | In development | Adapter inspected; engine verification required |
| `dev-format-dart` | In development | Adapter inspected; engine verification required |
| `dev-format-scala` | In development | Adapter inspected; engine verification required |
| `dev-format-lua` | In development | Adapter inspected; engine verification required |
| `dev-format-bash` | In development | Adapter inspected; engine verification required |
| `dev-format-shell` | In development | Adapter inspected; engine verification required |
| `dev-format-powershell` | In development | Adapter inspected; engine verification required |
| `dev-format-sql` | In development | Adapter inspected; engine verification required |
| `dev-format-html` | In development | Executed |
| `dev-format-css` | In development | Executed |
| `dev-format-scss` | In development | Executed |
| `dev-format-less` | In development | Executed |
| `dev-format-xml` | Enabled; GUI verified | Executed |
| `dev-format-svg` | Enabled; GUI verified | Executed |
| `dev-format-json` | Enabled; GUI verified | Executed |
| `dev-format-json5` | In development | Executed |
| `dev-format-jsonc` | In development | Executed |
| `dev-format-yaml` | In development | Executed |
| `dev-format-toml` | Enabled; GUI verified | Executed |
| `dev-format-markdown` | In development | Executed |
| `dev-format-mdx` | In development | Executed |
| `dev-format-latex` | In development | Adapter inspected; engine verification required |
| `dev-format-graphql` | In development | Executed |
| `dev-format-vue` | In development | Executed |
| `dev-format-svelte` | In development | Executed |
| `dev-format-astro` | In development | Executed |
| `dev-format-solidity` | In development | Executed |
| `dev-format-hcl` | In development | Adapter inspected; engine verification required |
| `dev-format-terraform` | In development | Adapter inspected; engine verification required |
| `dev-format-dockerfile` | In development | Adapter inspected; engine verification required |
| `dev-format-r` | In development | Adapter inspected; engine verification required |
| `dev-format-julia` | In development | Adapter inspected; engine verification required |
| `dev-format-elixir` | In development | Adapter inspected; engine verification required |
| `dev-format-haskell` | In development | Adapter inspected; engine verification required |
| `dev-validate-javascript` | In development | Executed |
| `dev-validate-typescript` | In development | Executed |
| `dev-validate-jsx` | In development | Executed |
| `dev-validate-tsx` | In development | Executed |
| `dev-validate-python` | Enabled; GUI verified | Executed |
| `dev-validate-java` | In development | Executed |
| `dev-validate-c` | In development | Adapter inspected; engine verification required |
| `dev-validate-cpp` | In development | Adapter inspected; engine verification required |
| `dev-validate-csharp` | In development | Adapter inspected; engine verification required |
| `dev-validate-go` | In development | Adapter inspected; engine verification required |
| `dev-validate-rust` | In development | Adapter inspected; engine verification required |
| `dev-validate-php` | In development | Executed |
| `dev-validate-ruby` | In development | Adapter inspected; engine verification required |
| `dev-validate-kotlin` | In development | Adapter inspected; engine verification required |
| `dev-validate-swift` | In development | Adapter inspected; engine verification required |
| `dev-validate-dart` | In development | Adapter inspected; engine verification required |
| `dev-validate-scala` | In development | Adapter inspected; engine verification required |
| `dev-validate-lua` | In development | Adapter inspected; engine verification required |
| `dev-validate-bash` | In development | Executed |
| `dev-validate-shell` | In development | Executed |
| `dev-validate-powershell` | In development | Executed |
| `dev-validate-sql` | In development | Adapter inspected; engine verification required |
| `dev-validate-html` | In development | Executed |
| `dev-validate-css` | In development | Executed |
| `dev-validate-scss` | In development | Executed |
| `dev-validate-less` | In development | Executed |
| `dev-validate-xml` | Enabled; GUI verified | Executed |
| `dev-validate-svg` | Enabled; GUI verified | Executed |
| `dev-validate-json` | Enabled; GUI verified | Executed |
| `dev-validate-json5` | Enabled; GUI verified | Executed |
| `dev-validate-jsonc` | Enabled; GUI verified | Executed |
| `dev-validate-yaml` | Enabled; GUI verified | Executed |
| `dev-validate-toml` | Enabled; GUI verified | Executed |
| `dev-validate-markdown` | In development | Executed |
| `dev-validate-mdx` | In development | Executed |
| `dev-validate-latex` | In development | Adapter inspected; engine verification required |
| `dev-validate-graphql` | In development | Executed |
| `dev-validate-vue` | In development | Executed |
| `dev-validate-svelte` | In development | Executed |
| `dev-validate-astro` | In development | Executed |
| `dev-validate-solidity` | In development | Executed |
| `dev-validate-hcl` | In development | Adapter inspected; engine verification required |
| `dev-validate-terraform` | In development | Adapter inspected; engine verification required |
| `dev-validate-dockerfile` | In development | Adapter inspected; engine verification required |
| `dev-validate-r` | In development | Adapter inspected; engine verification required |
| `dev-validate-julia` | In development | Adapter inspected; engine verification required |
| `dev-validate-elixir` | In development | Adapter inspected; engine verification required |
| `dev-validate-haskell` | In development | Adapter inspected; engine verification required |
| `dev-validate-xsd` | Enabled; GUI verified | Executed |
| `dev-validate-json-schema` | Enabled; GUI verified | Executed |
| `dev-validate-csv` | Enabled; GUI verified | Executed |
| `dev-validate-openapi` | In development | Adapter inspected; engine verification required |
| `dev-validate-asyncapi` | In development | Adapter inspected; engine verification required |
| `dev-minify-javascript` | In development | Executed |
| `dev-minify-typescript` | In development | Executed |
| `dev-minify-jsx` | In development | Executed |
| `dev-minify-tsx` | In development | Executed |
| `dev-minify-html` | In development | Executed |
| `dev-minify-css` | In development | Executed |
| `dev-minify-json` | Enabled; GUI verified | Executed |
| `dev-minify-svg` | In development | Executed |
| `dev-minify-graphql` | In development | Executed |
| `ocr-to-pdf` | In development | Adapter inspected; engine verification required |
| `ocr-to-docx` | In development | Adapter inspected; engine verification required |
| `ocr-to-md` | In development | Adapter inspected; engine verification required |
| `ocr-to-latex` | In development | Adapter inspected; engine verification required |
| `ocr-to-html` | In development | Adapter inspected; engine verification required |
| `ocr-to-json` | In development | Adapter inspected; engine verification required |
| `diff-text` | Enabled; GUI verified | Executed |
| `diff-json` | Enabled; GUI verified | Executed |
| `diff-notebook` | Enabled; GUI verified | Executed |
| `diff-latex` | Enabled; GUI verified | Executed |
| `diff-pdf` | Enabled; GUI verified | Executed |
| `diff-word` | Enabled; GUI verified | Executed |
| `diff-code` | Enabled; GUI verified | Executed |
