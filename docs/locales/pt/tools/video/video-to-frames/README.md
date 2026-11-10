<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="video-to-frames"></a>
# Vídeo para fotogramas

Comando: `onekit run video-to-frames`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **vídeo**. Fidelidade: ** compromisso**. Extrai PNG quadros de um vídeo usando FFmpeg. Escolha o início, a duração e a largura. Até 120 quadros: o modo quadro original preserva cada quadro no intervalo; caso contrário, as datas são amostradas na taxa de quadros solicitada.

Tipos aceites: `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Tipo de saída: `png`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `start`, `duration`, `fps`, `width`, `all_frames`.

Python pacotes: Pillow. Motores externos: ffmpeg, ffprobe.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/video_edit.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
