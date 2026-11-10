<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="crop-image"></a>
# Recortar imagem

Comando: `onekit run image-crop`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **imagens**. Fidelidade: ** compromisso**. Os formatos de perda descartam detalhes. Animação e metadados podem ser removidos; use um formato sem perdas para preservar pixels.

Tipos aceites: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo de saída: `image`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **67.108.864 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `box`, `format`, `quality`.

Python pacotes: Pillow. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/images/__init__.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
