<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="color-picker"></a>
# Seletor de cores

Comando: `onekit run color-picker`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **design**. Fidelidade: **Exacto**. Leia uma cor HEX de seis dígitos de TXT ou prove um pixel de imagem EXIF orientado. Relatórios visíveis sRGB, original RGBA, OKLCH e contraste de texto. Os pixels transparentes são compostos em branco.

Tipos aceites: `png, jpeg, webp, gif, bmp, tiff, ico, txt`. Tipo de saída: `json`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `x`, `y`.

Python pacotes: Pillow. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/photo_tools.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
