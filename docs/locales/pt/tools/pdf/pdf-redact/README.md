<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanently-redact-pdf"></a>
# Ocultar permanentemente conteúdo de PDF

Comando: `onekit run pdf-redact`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **pdf**. Fidelidade: ** compromisso**. Mascara permanentemente áreas selecionadas e reconstrói todas as páginas a partir de pixels raster. Texto original, anexos, comentários, formulários e metadados não são copiados; texto selecionável e qualidade do vetor são perdidos. O arquivo original está inalterado.

Tipos aceites: `pdf`. Tipo de saída: `pdf`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `regions`, `dpi`.

Python pacotes: pypdfium2, Pillow, reportlab, pypdf. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/redaction.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
