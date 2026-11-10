<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="txt-to-html"></a>
# TXT para HTML

Comando: `onekit run txt-to-html`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **conversores**. Fidelidade: **Exacto**. Cria um documento seguro HTML com texto simples escapado e espaço em branco preservado. A marcação do código-fonte é mostrada literalmente, nunca executada.

Tipos aceites: `txt`. Tipo de saída: `html`. Aceita múltiplas entradas: **no**.

Validação de entrada: **encoded-text**. Contagem de ficheiros necessária: **1-1**. CLI: **8.388.608 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `source_encoding`.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/text_converters.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
