<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="json-to-xml"></a>
# JSON para XML

Comando: `onekit run json-to-xml`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **conversores**. Fidelidade: **Exacto**. XML tabelas usam registros planos repetidos. JSON a XML preserva tipos usando um esquema root/item tipado; XML atributos usam @ e texto usa #text em JSON. As fórmulas da folha de cálculo não são avaliadas; a primeira folha é usada por padrão. Reveja o esquema e valores após a conversão.

Tipos aceites: `json`. Tipo de saída: `xml`. Aceita múltiplas entradas: **no**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **1-1**. CLI: **8.388.608 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/structured_data.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
