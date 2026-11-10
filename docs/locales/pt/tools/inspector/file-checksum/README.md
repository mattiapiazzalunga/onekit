<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="calculate-checksum"></a>
# Calcular soma de verificação

Comando: `onekit run file-checksum`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **inspector**. Fidelidade: **Exacto**. Calcula SHA-256, SHA-512, SHA-1 ou MD5 localmente. Um checksum opcional esperado pode ser comparado com um arquivo. A soma de verificação não verifica uma assinatura digital nem estabelece a segurança dos ficheiros.

Tipos aceites: `*`. Tipo de saída: `json`. Aceita múltiplas entradas: **yes**.

Validação de entrada: **any**. Contagem de ficheiros necessária: **1–20**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `algorithm`, `expected`.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/file_checksum.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
