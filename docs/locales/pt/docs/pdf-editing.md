<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-text-editing"></a>
# PDF edição de texto

Inspecione o arquivo fonte para obter IDs de caixa de texto estáveis e texto original:

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

A CLI aceita as mesmas opções objeto através de `--options`. `edits` pode ser um JSON array ou uma string contendo esse array. Inspecionar saídas de modo `*.text-boxes.json`; editar saídas de modo `*.edited.pdf`. Manter o original PDF inalterado entre a inspecção e a edição. IDs obsoletos, edições duplicadas e texto original desajustado são rejeitados.

As digitalizações precisam de OCR primeiro. Texto dentro do formulário reutilizável XObjects, operadores de texto de citação, escrita vertical e recorte de texto não são oferecidos para edição direta. Fontes com mapeamentos incompletos também podem não estar disponíveis. Um caractere de substituição deve existir no mapeamento original da fonte; o motor reporta caracteres não suportados em vez de mudar silenciosamente a fonte. A edição é de uma única linha e não reflue parágrafos. Use uma ferramenta de redação dedicada para remover informações confidenciais, incluindo cópias em anotações, histórico de documentos, metadados ou outros objetos PDF.

As anteriores `text`, `x`, `y`, `page` opções permanecem disponíveis para scripts que adicionam sobreposições de texto. Forneça `edits` para substituir o texto existente.
