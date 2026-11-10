<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="make-pdf-fillable"></a>
# Criar PDF preenchível

Comando: `onekit run pdf-make-fillable`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **pdf**. Fidelidade: **Exacto**. Adicione campos de texto AcroForm, caixas de seleção e opções suspensas usando retângulos de topo-esquerda normalizados. Mantém os campos existentes e o conteúdo da página. Sem detecção automática em branco ou conversão XFA; verifique a compatibilidade do leitor.

Tipos aceites: `pdf`. Tipo de saída: `pdf`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `fields`.

Python pacotes: pypdf. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/pdf_design.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
