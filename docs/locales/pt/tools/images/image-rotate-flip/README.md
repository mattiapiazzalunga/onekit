<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="rotate-and-flip-image"></a>
# Rodar e inverter imagem

Comando: `onekit run image-rotate-flip`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **imagens**. Fidelidade: **Exacto**. Aplicar a orientação EXIF, rodar no sentido horário em 0, 90, 180 ou 270 graus, então refletir horizontalmente, verticalmente ou ambos. Exporta um PNG sem metadados, preservando pixels decodificados e transparência. Apenas imagens de um quadro; até 40 milhões de pixels.

Tipos aceites: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo de saída: `png`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `angle`, `flip`.

Python pacotes: Pillow. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/image_transform.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
