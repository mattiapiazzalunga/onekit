# PDF/A conversion and validation

The CLI and Python API call `onekit.tools.pdfa`. This module invokes no
executable and opens no network connection. Conversion uses pdftopdfa 0.9.24 for fonts, colour
and normalization, followed by pikepdf 10.17.0 PDF/A preparation and validation of
the exact final bytes. There is no Ghostscript dependency.

Conversion supports PDF/A-2b (default) and 3b. Validation supports 1b, 2b and 3b.
A/U conformance, PDF/A-4 and OCR are outside this adapter. Unsupported constructs
are `not_checked`, not compliant. A `pass` from this conservative allowlist is not
an archival certification; independent veraPDF validation remains recommended for
institutional submissions.

```
onekit run pdf-to-pdfa input.pdf --options '{"profile":"2b"}' -o output
onekit run pdf-validate-pdfa output/input.pdf -o report
onekit doctor pdf-to-pdfa --json
```

The CLI automatically installs a pinned, reviewed **non-OCR level-B subset** of
the upstream packages. It deliberately does not install PaddleOCR, OCRmyPDF or
the cryptography backend for pdfminer's unused PDF parser: no options are forwarded to upstream OCR or A/U tagging APIs. The
upstream `pdftopdfa` wheel is unmodified. Its package metadata includes broader
requirements for APIs OneKit does not invoke. The optional `[pdfa]` extra installs the reviewed prerequisites. For direct
Python API use, install that extra and then `pip install --no-deps pdfminer.six==20260107 pdftopdfa==0.9.24`.
Do not install upstream's OCR extras for this adapter. Upstream's mandatory OCR
requirements currently pin an older PyYAML incompatible with OneKit.
Conversion requires Python 3.12+; standalone validation works on Python 3.11+.
Run `python scripts/check_licenses.py --include-pdfa` to audit the selected runtime.

The former `icc_profile` option remains accepted as an optional local ICC file;
the default preserves the converter's bundled, licensed RGB/CMYK profiles. Encrypted PDFs and digital
signatures are rejected by conversion. Conversion can replace fonts and remove
non-archival actions or metadata; warnings accompany successful output. Failed
or incompletely checked candidates are never returned as converted PDF/A files.
Inputs are not overwritten. The JSON validation report preserves the `compliant`
and `reports` fields and adds the checked profile, verdict and engine.
