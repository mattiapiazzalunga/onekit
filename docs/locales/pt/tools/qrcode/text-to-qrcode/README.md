<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="text-to-qr-code"></a>
# Texto para Código QR

Comando: `onekit run text-to-qrcode`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **qrcode**. Fidelidade: **Exacto**. Cria um código QR padrão localmente. A capacidade depende do conteúdo e da correção de erros. Mantenha a zona silenciosa e teste o código antes de imprimir.

Tipos aceites: `txt`. Tipo de saída: `png`. Aceita múltiplas entradas: **no**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **1-1**. CLI: **16.384 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `format`, `shape`, `corner_style`, `overlay_type`, `overlay_text`, `overlay_image_base64`, `overlay_size`, `error_correction`, `scale`, `border`, `dark`, `light`, `transparent_background`, `include_payload`.

Python pacotes: segno, Pillow. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/qrcode.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
