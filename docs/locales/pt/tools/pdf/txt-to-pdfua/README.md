<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="text-to-pdfua"></a>
# Texto para PDF/UA

Comando: `onekit run txt-to-pdfua`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **pdf**. Fidelidade: **Exacto**. Crie uma etiqueta PDF/UA-1 a partir de texto simples com um título e idioma. Linhas em branco, parágrafos separados. Somente fontes latinas; reveja ordem de leitura e significado. As verificações automáticas não substituem a revisão manual de acessibilidade.

Tipos aceites: `txt`. Tipo de saída: `pdf`. Aceita múltiplas entradas: **no**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **1-1**. CLI: **262.144 bytes por arquivo**, **8.388.608 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `title`, `language`.

Python pacotes: reportlab, pypdf, Travesseiro. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/pdfua.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
