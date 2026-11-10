<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="add-page-numbers-to-pdf"></a>
# Adicionar números de página a PDF

Comando: `onekit run pdf-page-numbers`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **pdf**. Fidelidade: **Exacto**. Adiciona números sequenciais a todas ou páginas selecionadas, retendo texto de origem e gráficos. As assinaturas digitais existentes são inválidas.

Tipos aceites: `pdf`. Tipo de saída: `pdf`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `pages`, `start_number`, `number_style`, `font_size`, `position`, `margin`, `color`.

Python pacotes: pypdf, reportlab. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/pdf.page_numbers/__init__.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
