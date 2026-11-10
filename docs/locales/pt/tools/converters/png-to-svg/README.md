<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="png-to-svg"></a>
# PNG para SVG

Comando: `onekit run png-to-svg`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **conversores**. Fidelidade: ** compromisso**. Vectoriza um PNG como telhas vetoriais baseadas em paletas, sem incorporar um bitmap. Gradientes e detalhes finos são aproximados; pixels transparentes são compostos em branco.

Tipos aceites: `png`. Tipo de saída: `svg`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `colors`, `resolution`.

Python pacotes: Pillow. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/vector_images.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
