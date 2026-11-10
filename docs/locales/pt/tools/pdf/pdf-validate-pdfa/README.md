<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="validate-pdfa"></a>
# Validar PDF/A

Comando: `onekit run pdf-validate-pdfa`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **pdf**. Fidelidade: **Exacto**. Validar PDF/A-1b, 2b ou 3b com pikepdf. Os construtos não suportados são relatados como não verificados, nunca como compatíveis. Outros níveis de conformidade não são suportados.

Tipos aceites: `pdf`. Tipo de saída: `json`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `profile`.

Python pacotes: pikepdf, jsonschema, fonttools. Motores externos: veja a matriz do motor de desenvolvimento para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/pdf/__init__.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
