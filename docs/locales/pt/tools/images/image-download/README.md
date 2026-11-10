<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-image"></a>
# Transferir imagem

Comando: `onekit run image-download`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **imagens**. Fidelidade: **Exacto**. Baixar original PNG, JPEG, WebP, GIF, TIFF, BMP, ICO ou AVIF bytes de um direto URL ou a primeira imagem acessível exposta por uma página. Até 128 MiB. Os sites podem bloquear o acesso. O download não concede direitos de uso.

Tipos aceites: `txt`. Tipo de saída: `*`. Aceita múltiplas entradas: **no**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **1-1**. CLI: **16.384 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/link_tools.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
