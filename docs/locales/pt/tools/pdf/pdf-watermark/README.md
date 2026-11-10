<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="add-watermark-to-pdf"></a>
# Adicionar marca de água a PDF

Comando: `onekit run pdf-watermark`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **pdf**. Fidelidade: **Exacto**. Adiciona um texto ou marca d'água de imagem PNG/JPEG a todas as páginas ou páginas selecionadas, mantendo texto fonte e gráficos. Suporta texto da Europa Ocidental, layout único ou repetido, rotação e opacidade. O arquivo original está inalterado.

Tipos aceites: `pdf`. Tipo de saída: `pdf`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `text`, `pages`, `font`, `font_size`, `color`, `opacity`, `angle`, `position`, `layout`, `margin`, `watermark_type`, `image_base64`, `image_width`.

Python pacotes: pypdf, reportlab, Pillow. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/pdf.watermark/__init__.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
