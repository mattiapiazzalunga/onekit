<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="generate-vcard"></a>
# Gerar vCard

Comando: `onekit run vcard-generate`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **qrcode**. Fidelidade: **Exacto**. Cria um arquivo de contato vCard 3.0 ou 4.0 a partir dos campos que você fornece. Campos vazios são omitidos. Não se aplica nenhum limite de capacidade QR.

Tipos aceites: `json`. Tipo de saída: `vcf`. Aceita múltiplas entradas: **no**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **1-1**. CLI: **16.384 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/contacts.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
