<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="automatically-blur-faces"></a>
# Desfocar rostos automaticamente

Comando: `onekit run image-blur-faces`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **imagens**. Fidelidade: ** compromisso**. Detecta rostos localmente com a YuNet e borra-os num novo PNG. Revise cada face antes de compartilhar: detecção automática pode perder rostos e borrar não garante o anonimato. Imagens de quadro único, até 16 milhões de pixels.

Tipos aceites: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo de saída: `png`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: onnxruntime, numpy, Pillow. Motores externos: veja a matriz do motor de desenvolvimento para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/face_blur.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
