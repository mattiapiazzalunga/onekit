<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="add-text-to-image"></a>
# Adicionar texto à imagem

Comando: `onekit run image-add-text`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **imagens**. Fidelidade: ** compromisso**. Adiciona texto da Europa Ocidental a um novo PNG com tamanho ajustável, cor e posição. Animação e metadados não são retidos.

Tipos aceites: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo de saída: `png`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `text`, `font_size`, `color`, `position`, `margin`, `x`, `y`, `text_boxes`.

Python pacotes: Pillow. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/image_text.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
