<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="mp4-to-mp3"></a>
# MP4 para MP3

Comando: `onekit run mp4-to-mp3`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **vídeo**. Fidelidade: ** compromisso**. Extrai a primeira faixa de áudio de um MP4 como MP3 em 192 kbps. Requer uma faixa de áudio; a recodificação pode perder qualidade.

Tipos aceites: `mp4`. Tipo de saída: `mp3`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: ffmpeg, ffprobe.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/video_edit.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
