# Processing services

`ExecutionContext` can supply trusted local engine primitives independently of
tool options. The processing API continues to validate input artifacts, apply
budgets and check output artifacts. An engine service returns readings or pixels;
the public processing handler interprets those readings and builds the result.
Services are scoped to one execution and do not change the default CLI engines.

The optional services are documented on `ExecutionContext`: symbol reading, OCR,
speech recognition, foreground masks and PDF rasterization. PDF page records carry
encoded raster data and physical dimensions in points. Raster encoding, slide
assembly and destructive redaction remain in the public handlers. Speech records
use a language and a list of start/end/text segments. OCR records contain text or
searchable PDF bytes per page, with optional physical dimensions for rescaling.

The JavaScript processing modules are usable independently of the Python driver:

- `tools/developer/source_engine.mjs` exports source transformation and result
  handling, a native formatter host interface, syntax-tree checks, local JSON
  Pointer validation, API specification selection and container recipe processing.
  Engine loading, process isolation and parser lifetime belong to the caller.
- `tools/document_engine.mjs` exports basic semantic document conversion using a
  subset of Pandoc document nodes. It accepts Markdown and HTML parser services,
  omits active content and external image loading, and writes standalone LaTeX.
  A PDF writer service receives the semantic document; layout, font resources and
  rendering belong to that writer. Parser complexity limits are caller parameters.

The document subset covers paragraphs, headings, emphasis, code, links, lists,
quotes and horizontal rules. Tables are represented by text rows. It does not
claim the full functionality of a document typesetting engine. Existing native
CLI document conversion remains available with its original engine contracts.

For installations without native document executables, the Python processing API
also accepts `ExecutionContext(portable_documents=True)`. Markdown/HTML to PDF or
LaTeX then uses `tools/portable_documents.py`: bounded local HTML parsing,
MarkdownIt, escaped LaTeX, and ReportLab layout with its bundled Vera fonts.
It never fetches resources or executes source markup. This deliberately basic
mode omits CSS and active content, represents tables as text rows, rejects
unsupported PDF glyphs. `DocumentLimits` controls node, nesting, block and PDF
page budgets independently of input and output byte limits. Install the
`documents` and `pdf` extras. Native Pandoc/TeX conversion stays the default;
changes exclusive to those native paths do not affect portable mode.

`tools/symbols.py` exposes the ZXing reader settings used by native scanning.
Supplied readers can consume the same formats, rotation and inversion settings.
The barcode handler normalizes format aliases before assembling the public result.
`input_image` and `pixel_input` share image orientation and white alpha compositing
between native reading and supplied pixel-based readers. Callers can narrow the
pixel budget independently of the detection settings.

`tools/background.py` exposes the U2Net model checksum, `foreground_input` and
`foreground_output`. The input is a contiguous little-endian float32 tensor with
shape `[1,3,320,320]`; the supplied prediction is the first float32 output with
shape `[1,1,320,320]`. Both native inference and supplied predictions use the
same tensor preparation, mask normalization and image resizing. Inference runtime
differences can still affect floating-point results.

`tools/transcription.py` exposes `recognition_parameters`, including model,
language, sample rate, beam width and previous-text conditioning. A different
inference host must explicitly support those settings; shared settings do not
establish equivalence of decoding implementations or quantized model conversions.

The developer handler uses sqlparse and SQLFluff directly when installed in its
Python environment. The original standalone `sqlformat` and `sqlfluff` commands
remain supported when those imports are unavailable. SQL validation uses the
requested SQLFluff dialect, with ANSI as the default; it does not execute queries.
