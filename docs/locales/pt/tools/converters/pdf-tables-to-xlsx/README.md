<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-tables-to-excel"></a>
# Tabelas de PDF para Excel

Comando: `onekit run pdf-tables-to-xlsx`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **conversores**. Fidelidade: ** compromisso**. Detecta tabelas de texto selecionável alinhado. As varreduras requerem OCR; layouts complexos, células mescladas e alinhamento de colunas exigem revisão. Excel usa uma folha por tabela; CSV exporta um arquivo por tabela.

Tipos aceites: `pdf`. Tipo de saída: `xlsx`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `pages`.

Python pacotes: pycryptodome, pypdf, openpyxl. Motores externos: veja a matriz do motor de desenvolvimento para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/pdf_tables.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
