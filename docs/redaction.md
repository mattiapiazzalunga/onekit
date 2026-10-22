<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Permanent redaction

## PDF

Every page is rendered, the selected pixels are replaced with opaque black, and a fresh PDF is built from the already-redacted images. No original PDF objects are copied. This removes original selectable text, OCR layers, hidden layers, form fields, annotation/comment objects, links, scripts, attachments, metadata, thumbnails and incremental save history from the output. Visible annotation appearances are flattened into pixels so an existing opaque annotation does not unexpectedly reveal the content it covered. Review the preview for field/annotation appearance differences; no interactive objects are retained. Unselected visible page content remains as pixels.

## Images

Pixels are replaced with solid black before encoding a new opaque RGB PNG. There is no removable overlay, original layer or original unmasked pixel data in the encoded regions. Source EXIF, GPS, XMP, comments, profiles, thumbnails and other original metadata are not copied. Transparency is composited onto white, discarding hidden RGB values under transparent pixels. EXIF orientation is applied before interpreting the areas. Animated and multi-frame inputs are rejected so extra frames cannot remain unredacted; export one frame first.

## CLI and workflows

Install `onekit-tools[pdf]` for PDF redaction or `onekit-tools[images]` for images. Both tools accept `regions`, an array of rectangles, optionally serialized as a JSON string. Each rectangle has `page` (one based, default 1), `x`, `y`, `width`, `height`. Coordinates are fractions of the visually oriented page/image with origin at the top left: `0.1` means 10%. For images, `page` must be 1. Up to 500 rectangles can be selected. Bounds must fit inside the page; masks round outward and expand one output pixel to cover fractional edges.

```sh
onekit run pdf-redact private.pdf -o redacted.pdf --options '{"regions":[{"page":1,"x":0.1,"y":0.2,"width":0.5,"height":0.1}],"dpi":200}'
onekit run image-redact private.jpg -o redacted.png --options '{"regions":[{"x":0.2,"y":0.2,"width":0.3,"height":0.2}]}'
```
