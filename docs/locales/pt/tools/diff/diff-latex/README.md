<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="compare-latex-files"></a>
# Comparar ficheiros LaTeX

Comando: `onekit run diff-latex`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: ** diff**. Fidelidade: ** compromisso**. A comparação do Notebook pode incluir Markdown, código ou ambos. O modo texto LaTeX omite comandos.

Tipos aceites: `latex, txt`. Tipo de saída: `json`. Aceita múltiplas entradas: **yes**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **2–2**. CLI: **8.388.608 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `mode`.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/diff/__init__.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
