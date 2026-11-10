<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="epub-to-pdf"></a>
# EPUB para PDF

Comando: `onekit run epub-to-pdf`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **conversores**. Fidelidade: ** compromisso**. Exporta texto básico em EPUB ordem de leitura. CSS, imagens, layouts fixos e conteúdo interativo são omitidos; livros criptografados ou protegidos por DRM são rejeitados.

Tipos aceites: `epub`. Tipo de saída: `pdf`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: reportlab, Pillow, defusedxml. Motores externos: veja a matriz do motor de desenvolvimento para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/epub_pdf.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
