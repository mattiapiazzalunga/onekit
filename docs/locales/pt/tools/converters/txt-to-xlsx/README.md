<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="txt-to-excel"></a>
# TXT para Excel

Comando: `onekit run txt-to-xlsx`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **conversores**. Fidelidade: **Exacto**. Parses delimitou TXT em uma planilha Excel. Células são armazenadas como texto, preservando zeros principais e impedindo a execução de fórmulas. Requer contagens consistentes de colunas.

Tipos aceites: `txt`. Tipo de saída: `xlsx`. Aceita múltiplas entradas: **no**.

Validação de entrada: **encoded-text**. Contagem de ficheiros necessária: **1-1**. CLI: **8.388.608 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `delimiter`, `source_encoding`.

Python pacotes: openpyxl. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/text_converters.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
