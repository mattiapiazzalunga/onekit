<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="convert-audio"></a>
# Converter áudio

Comando: `onekit run audio-convert`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **áudio**. Fidelidade: ** compromisso**. Os codecs disponíveis dependem da sua compilação FFmpeg; a recodificação pode perder qualidade.

Tipos aceites: `mp3, wav, flac, ogg, aac, m4a, mp4, aif, aiff, opus, wma`. Tipo de saída: `*`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `format`, `codec`, `bitrate`.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: ffmpeg, ffprobe.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/media/__init__.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
