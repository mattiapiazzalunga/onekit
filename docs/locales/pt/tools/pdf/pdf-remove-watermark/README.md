<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-pdf-watermark"></a>
# Remover marca de água de PDF

Comando: `onekit run pdf-remove-watermark`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **pdf**. Fidelidade: ** compromisso**. Inspecione e remova textos, imagens e invocações de formulários selecionados, incluindo formulários aninhados e texto codificado por fonte. Remove automaticamente artefatos marcados de marca d'água e anotações de marca d¿água. Objetos não marcados requerem seleção ou texto exato; as marcas achatadas não podem ser separadas da sua imagem. Revise todas as páginas.

Tipos aceites: `pdf`. Tipo de saída: `pdf`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `text`, `mode`, `objects`.

Python pacotes: pypdf. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/pdf_design.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
