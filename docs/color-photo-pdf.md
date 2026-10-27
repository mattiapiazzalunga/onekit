# Color, photo restoration and PDF forms

These tools are exposed through the standard `onekit run TOOL ... --options JSON` command and the Python `execute` API. See `onekit run --help` for input/output arguments. All coordinates below refer to the image after EXIF orientation or the displayed PDF page after rotation.

- `color-picker`: inspect a UTF-8 file containing `#RRGGBB`, or sample an image with integer pixel options `x` and `y` (center by default). Reports HEX, RGB, OKLCH, black/white text contrast and original RGBA for images. Visible colors are composited on white.
- `image-extract-colors`: `colors` (2–32, default 6). Median-cut quantization of a thumbnail bounded to 256 × 256. Fully transparent pixels are excluded; partial alpha is composited on white. Fractions describe this sample.
- `jpg-to-svg`: `colors` (2–32, default 16), `resolution` (32–512, default 256). Quantizes a bounded image, merges horizontal equal-color runs vertically, and writes filled SVG paths. No bitmap is embedded. This produces vector tiles with a posterized appearance, not smooth curve tracing.
- `image-repair`: without `regions`, applies a median filter of `size` 3 or 5 to isolated speckles. With regions, reconstructs selected pixels using fixed surrounding pixels and discrete harmonic diffusion (`iterations` 10–500, default 200).
- `image-remove-watermark`: requires `regions`; uses the same local reconstruction. It estimates missing pixels and cannot recover hidden original content. Texture, large marks and intricate backgrounds may give poor results.
- `image-sharpen`: `method` is `unsharp` (default) or `deconvolution`. `radius` 0.3–5 sets the unsharp radius or estimated Gaussian point spread. Unsharp `amount` 0–300 percent (default 150). Richardson–Lucy uses 1–30 `iterations` (default 10), reflect padding and FFT convolution, up to one million source pixels. It assumes Gaussian blur and does not correct arbitrary motion. Both may amplify noise and halos.
- `pdf-remove-watermark`: default `mode: "remove"` removes `/Artifact` groups tagged `/Subtype /Watermark` (including named property resources) and `/Watermark` annotations. Optional `text` matches full text objects with whitespace normalized, decoding glyphs through their font encoding/ToUnicode map. Nested Form XObjects are processed recursively. Use `mode: "inspect"` to get a JSON report of text, image and form invocation IDs; pass selected IDs as `objects` in remove mode. Selecting a form removes its entire graphic group. Modified forms are copied per invocation so unselected uses of a shared resource remain unchanged. IDs refer to the same original PDF and must be reinspected after changes. This is drawing-object removal, not secure redaction: unused resource objects may remain in the output. It does not identify arbitrary untagged content as a watermark automatically, and a mark merged into a scanned image cannot be separated from that image. A report contains up to 2,000 candidates, recursion is limited to 12 levels and processing to 300,000 drawing operations. Zero matches produces an explicit error.
- `pdf-make-fillable`: `fields` is a JSON array of standard AcroForm widgets with unique ASCII `name`, `type` (`text`, `checkbox`, `choice`), 1-based `page`, normalized `x`, `y`, `width`, `height`. Optional `required`, text `multiline`, and choice `choices` are supported. Existing fields and page content are preserved. Duplicate names, encrypted PDFs and XFA are rejected. No automatic blank recognition.

Image regions are arrays of objects such as `{"page":1,"x":0.2,"y":0.3,"width":0.1,"height":0.05}`. Coordinates are normalized to 0–1 from the top left. Reconstruction supports up to 100 rectangles, at most 35% of the image and a bounding box (including padding) of one million pixels. Only RGB inside the mask changes; original alpha is retained. Outputs are PNG with no source metadata. Animated/multiframe images are rejected. General image decoding is limited to 40 million pixels. PDFs are limited to 256 pages and forms to 200 new fields.

Example Python usage:

```python
from onekit import Artifact, execute

result = execute("pdf-make-fillable", [Artifact("source.pdf", pdf_bytes)], {
    "fields": [{"name": "Name", "type": "text", "page": 1,
                "x": 0.1, "y": 0.2, "width": 0.4, "height": 0.05}]
})
```

Review the resulting files and keep the originals. A compatible PDF reader is needed to fill and save forms.
