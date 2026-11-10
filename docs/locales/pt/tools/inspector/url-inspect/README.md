<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="url-inspector"></a>
# Inspecionar URL

Comando: `onekit run url-inspect`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **inspector**. Fidelidade: ** compromisso**. Inspecione URL componentes, status HTTP, final URL e cabeçalhos de resposta disponíveis diretamente do seu dispositivo. Registros até 10 HTTP redirecionamentos. Falhas de rede deixam um relatório parcial. Este não é um phishing, malware, DNS ou verificação de propriedade.

Tipos aceites: `txt`. Tipo de saída: `json`. Aceita múltiplas entradas: **no**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **1-1**. CLI: **16.384 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/link_tools.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
