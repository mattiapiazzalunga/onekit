<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-text-formatting"></a>
# Remover formatação de texto

Comando: `onekit run text-strip-formatting`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **inspector**. Fidelidade: ** compromisso**. Virar o texto colado, UTF-8/UTF-16 ficheiros de texto, HTML, Markdown ou Word DOCX texto do corpo em uma UTF-8 TXT ficheiro localmente. Remove estilos, links e marcação ao reter texto legível e quebras básicas de parágrafo/tabela. Texto simples preserva pontuação literal. Não OCR; DOCX cabeçalhos, rodapés, imagens e comentários são omitidos. Até 8 MiB por entrada.

Tipos aceites: `txt, html, md, docx`. Tipo de saída: `txt`. Aceita múltiplas entradas: **no**.

Validação de entrada: **any**. Contagem de ficheiros necessária: **1-1**. CLI: **8.388.608 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `input_format`.

Python embalagens: markdown-it-py, defusedxml. Motores externos: veja a matriz do motor de desenvolvimento para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/plain_text.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
