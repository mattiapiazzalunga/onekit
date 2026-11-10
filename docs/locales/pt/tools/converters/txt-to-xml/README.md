<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="txt-to-xml"></a>
# TXT para XML

Comando: `onekit run txt-to-xml`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **conversores**. Fidelidade: **Exacto**. Requer validade XML já contida na TXT Arquivo. Valida sua marcação e escreve UTF-8 XML; DTDs e entidades são rejeitadas.

Tipos aceites: `txt`. Tipo de saída: `xml`. Aceita múltiplas entradas: **no**.

Validação de entrada: **encoded-text**. Contagem de ficheiros necessária: **1-1**. CLI: **8.388.608 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `source_encoding`.

Python embalagens: defusedxml. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/text_converters.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
