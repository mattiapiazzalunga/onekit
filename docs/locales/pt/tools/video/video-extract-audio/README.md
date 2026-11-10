<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="extract-audio-from-video"></a>
# Extrair áudio de vídeo

Comando: `onekit run video-extract-audio`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **vídeo**. Fidelidade: ** compromisso**. Extrai a primeira faixa de áudio como MP3 em 192 kbps usando FFmpeg. Requer um vídeo contendo áudio; a recodificação pode perder qualidade.

Tipos aceites: `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Tipo de saída: `mp3`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: ffmpeg, ffprobe.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/video_edit.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
