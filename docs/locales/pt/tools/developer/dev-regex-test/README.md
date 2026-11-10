<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# Testar expressões regulares

Comando: `onekit run dev-regex-test`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **Developer**. Fidelidade: **Exacto**. Ensaios JavaScript expressões regulares localmente com capturas, grupos nomeados, UTF-16 posições e substituição. Até 128 KiB do texto, 1000 correspondências e 1 MiB de produção. A execução é limitada em tempo; o CLI exige Node.js.

Tipos aceites: `txt`. Tipo de saída: `json`. Aceita múltiplas entradas: **no**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **1-1**. CLI: **131.072 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `pattern`, `flags`, `max_matches`, `enable_replacement`, `replacement`.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: node.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/regex_tester.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
