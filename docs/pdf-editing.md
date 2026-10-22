<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# PDF text editing

Inspect the source file to obtain stable text-box IDs and original text:

```python
from onekit.api import execute
from onekit.models import Artifact

source = Artifact("document.pdf", open("document.pdf", "rb").read())
inspection = execute("pdf-edit", [source], {"mode": "inspect"})
box = inspection.details["pages"][0]["runs"][0]
result = execute("pdf-edit", [source], {
    "edits": [{"page": 1, "id": box["id"], "original": box["text"], "text": "Updated text"}]
})
open("edited.pdf", "wb").write(result.files[0].data)
```

The CLI accepts the same options object through `--options`. `edits` can be a JSON
array or a string containing that array. Inspect mode outputs `*.text-boxes.json`;
edit mode outputs `*.edited.pdf`. Keep the original PDF unchanged between inspection
and editing. Stale IDs, duplicate edits and mismatching original text are rejected.

Scans need OCR first. Text inside reusable Form XObjects, quote text operators,
vertical writing and clipping text are not offered for direct editing. Fonts with
incomplete mappings may also be unavailable. A replacement character must exist in
the original font mapping; the engine reports unsupported characters instead of
silently changing the font. Editing is single-line and does not reflow paragraphs.
Use a dedicated redaction tool to remove confidential information, including copies
in annotations, document history, metadata or other PDF objects.

The previous `text`, `x`, `y`, `page` options remain available for scripts that add
text overlays. Supply `edits` to replace existing text.
