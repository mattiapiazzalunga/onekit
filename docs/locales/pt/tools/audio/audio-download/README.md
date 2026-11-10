<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-audio"></a>
# Transferir áudio

Comando: `onekit run audio-download`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **áudio**. Fidelidade: ** compromisso**. Baixe um arquivo de áudio direto ou uma fonte de áudio exposta por uma página acessível. O modo original preserva os bytes baixados; MP3 a conversão é perdida. Até 128 MiB. Login e streams protegidos podem evitar downloads. Use apenas com permissão.

Tipos aceites: `txt`. Tipo de saída: `*`. Aceita múltiplas entradas: **no**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **1-1**. CLI: **16.384 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `format`, `quality`.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: ffmpeg, ffprobe.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/link_tools.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
