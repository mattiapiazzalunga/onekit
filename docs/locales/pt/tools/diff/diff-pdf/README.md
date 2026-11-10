<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="compare-pdf-files"></a>
# Comparar ficheiros PDF

Comando: `onekit run diff-pdf`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: ** diff**. Fidelidade: ** compromisso**. Compara o texto extraído, não a disposição visual.

Tipos aceites: `pdf`. Tipo de saída: `json`. Aceita múltiplas entradas: **yes**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **2–2**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: pycryptodome, pypdf. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/diff/__init__.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
