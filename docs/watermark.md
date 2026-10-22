<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# PDF watermark

In the PDF category, upload a PDF, enter text and adjust opacity, color, font, rotation and position. The preview shows the watermark position on a chosen page. Export to inspect the final PDF font rendering. Choose a single watermark or a repeated 3 × 4 grid. Text is automatically reduced when needed to fit the page or cell, down to a six-point legibility limit. Encrypted PDFs must be unlocked first. Existing digital signatures no longer verify after modifying a document; the tool warns when signature fields are present.

```sh
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","pages":"1,3-5","opacity":0.25,"angle":45}'
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"DRAFT","layout":"repeat","color":"#b00000"}'
```

| Option | Values / default |
| --- | --- |
| `text` | 1–200 characters, up to five lines; default DRAFT |
| `pages` | One-based ranges, e.g. `1,3-5`; empty or omitted means all |
| `font` | Helvetica-Bold (default), Helvetica, Times-Roman, Courier |
| `font_size` | 8–160 points; default 48, automatically fitted when needed |
| `color` | Six-digit hex; default #666666 |
| `opacity` | 0.05–1; default 0.25 |
| `angle` | -180–180 degrees, counterclockwise; default 45 |
| `position` | center, top-left/center/right, middle-left/right, bottom-left/center/right |
| `layout` | single (default) or repeat (3 × 4 grid; position is ignored) |
| `margin` | 0–144 points; default 24 |

Fonts support Western European characters and punctuation, including Italian accents. Unsupported characters fail explicitly. Up to 512 pages can be processed. Placement uses the visually oriented crop box, retaining original rotation and annotation coordinates. A watermark labels visible content; it does not remove underlying content.
