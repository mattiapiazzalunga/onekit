<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-image-watermark"></a>
# Remover marca de água da imagem

Comando: `onekit run image-remove-watermark`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **imagens**. Fidelidade: ** compromisso**. Reconstruir áreas de marca d'água manualmente selecionadas a partir de pixels circundantes usando difusão harmônica. Estima-se que o conteúdo em falta; grandes marcas, texturas e faces podem não reconstruir de forma convincente. Sem detecção automática de marcas.

Tipos aceites: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo de saída: `png`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `regions`, `iterations`.

Python pacotes: Pillow, numpy. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/photo_tools.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
