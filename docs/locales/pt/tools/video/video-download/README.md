<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-video"></a>
# Transferir vídeo

Comando: `onekit run video-download`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **vídeo**. Fidelidade: **Exacto**. Downloads do YouTube e outros sites do yt-dlp, até 128 MiB. O suporte ao site varia; uma conexão à internet é necessária.

Tipos aceites: `txt`. Tipo de saída: `*`. Aceita múltiplas entradas: **no**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **1-1**. CLI: **16.384 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `quality`, `cookies`, `cookies_from_browser`, `format_id`, `referer`, `list_formats`.

Python embalagens: yt-dlp. Motores externos: ffmpeg.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/video_download.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
