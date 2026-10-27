<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-text-editing"></a>
# PDF Textbearbeitung

Überprüfen Sie die Quelldatei, um stabile Textfeld-IDs und den Originaltext zu erhalten:

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

Der CLI akzeptiert dasselbe Optionsobjekt über `--options`. `edits` kann ein JSON-Array oder ein String sein, der dieses Array enthält. Der Inspektionsmodus gibt `*.text-boxes.json` aus; der Bearbeitungsmodus gibt `*.edited.pdf` aus. Behalten Sie das ursprüngliche PDF zwischen Inspektion und Bearbeitung unverändert bei. Veraltete IDs, doppelte Bearbeitungen und nicht übereinstimmender Originaltext werden abgelehnt.

Scans benötigen zunächst OCR. Text in wiederverwendbaren Form-XObjects, Textoperatoren mit einfachen oder doppelten Anführungszeichen, vertikale Schrift und Text als Beschneidungsmaske werden nicht zur direkten Bearbeitung angeboten. Schriftarten mit unvollständigen Zeichenzuordnungen können ebenfalls nicht verfügbar sein. Das einzufügende Zeichen muss in der Zuordnung der ursprünglichen Schrift vorhanden sein; die Engine meldet nicht unterstützte Zeichen, anstatt die Schrift ohne Hinweis zu ändern. Die Bearbeitung betrifft eine einzelne Zeile und bricht Absätze nicht neu um. Verwenden Sie ein spezielles Werkzeug zum dauerhaften Schwärzen, um vertrauliche Informationen zu entfernen, einschließlich Kopien in Anmerkungen, im Dokumentverlauf, in Metadaten oder anderen PDF-Objekten.

Die vorherigen Optionen `text`, `x`, `y`, `page` bleiben verfügbar für Skripte, die Text-Overlays hinzufügen. Übergeben Sie `edits`, um bestehenden Text zu ersetzen.
