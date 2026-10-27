<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-text-editing"></a>
# Modifica testo PDF

Controlla il file sorgente per ottenere ID delle caselle di testo stabili e testo originale:

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

La CLI accetta lo stesso oggetto di opzioni tramite `--options`. `edits` può essere un array JSON o una stringa che contiene quell’array. La modalità di ispezione restituisce `*.text-boxes.json`; la modalità di modifica restituisce `*.edited.pdf`. Mantieni l’originale PDF invariato tra ispezione e modifica. Gli ID scaduti, le modifiche duplicate e il testo originale non corrispondente vengono rifiutati.

Le scansioni richiedono prima l’OCR. Non è disponibile la modifica diretta del testo negli oggetti Form XObject riutilizzabili, degli operatori di testo con apici o virgolette, della scrittura verticale e del testo usato come maschera di ritaglio. Anche i font con mappature incomplete possono non essere disponibili. Il carattere da inserire deve esistere nella mappatura del font originale; il motore segnala i caratteri non supportati anziché cambiare font senza avviso. La modifica riguarda una sola riga e non ridistribuisce i paragrafi. Usa uno strumento dedicato all’oscuramento permanente per rimuovere informazioni riservate, comprese le copie nelle annotazioni, nella cronologia del documento, nei metadati o in altri oggetti PDF.

Le precedenti opzioni `text`, `x`, `y`, `page` sono ancora disponibili per script che aggiungono sovrapposizioni di testo. Fornisci `edits` per sostituire il testo esistente.
