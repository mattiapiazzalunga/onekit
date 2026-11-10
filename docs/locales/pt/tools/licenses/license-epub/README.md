<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="epub-license-checker"></a>
# Verificador de licenças de EPUB

Comando: `onekit run license-epub`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **licenças**. Fidelidade: ** compromisso**. Uma estimativa baseada em declarações e metadados, não um certificado de direitos ou autorização legal. Verifique todos os achados com a fonte original e titular de direitos. A falta de informação nunca significa livre de usar. Autores e titulares de direitos autorais podem diferir. Os arquivos são analisados localmente; os links são baixados diretamente a partir de sua fonte. Os arquivos estão limitados e os exames podem ser incompletos.

Tipos aceites: `epub`. Tipo de saída: `json`. Aceita múltiplas entradas: **no**.

Validação de entrada: **any**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `ref`.

Python pacotes: license-expression, defusedxml. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/license_check.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
