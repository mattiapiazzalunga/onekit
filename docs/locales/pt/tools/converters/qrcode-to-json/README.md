<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="qr-code-to-json"></a>
# Código QR para JSON

Comando: `onekit run qrcode-to-json`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **conversores**. Fidelidade: **Exacto**. Lê QR cargas úteis localmente a partir de uma imagem; Reverse revela o conteúdo armazenado, não as configurações originais da imagem ou gerador. Nenhuma ligação é aberta automaticamente.

Tipos aceites: `png, jpeg, webp, bmp, gif`. Tipo de saída: `json`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **16.777.216 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: Pillow, zxing-cpp. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/qrcode.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
