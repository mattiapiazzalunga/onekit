<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-text-editing"></a>
# Edición de texto PDF

Inspecciona el archivo fuente para obtener IDs de cuadro de texto estables y texto original:

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

El CLI acepta el mismo objeto de opciones a través de `--options`. `edits` puede ser un array JSON o un string que contenga ese array. El modo de inspección produce `*.text-boxes.json`; el modo de edición produce `*.edited.pdf`. Mantén el PDF original sin cambios entre inspección y edición. Se rechazan IDs obsoletos, ediciones duplicadas y textos originales que no coinciden.

Los documentos escaneados requieren primero OCR. No se ofrece edición directa del texto de objetos Form XObject reutilizables, de los operadores de texto con comillas simples o dobles, de la escritura vertical ni del texto usado como máscara de recorte. Las fuentes con tablas de correspondencia incompletas también pueden no estar disponibles. El carácter que se va a insertar debe existir en la tabla de correspondencia de la fuente original; el motor indica los caracteres no compatibles en lugar de cambiar la fuente sin avisar. La edición afecta a una sola línea y no redistribuye los párrafos. Usa una herramienta específica de censura permanente para eliminar información confidencial, incluidas sus copias en anotaciones, historial del documento, metadatos u otros objetos PDF.

Las opciones anteriores `text`, `x`, `y`, `page` siguen disponibles para scripts que agregan superposiciones de texto. Suministra `edits` para reemplazar el texto existente.
