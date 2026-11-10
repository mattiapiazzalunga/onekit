<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="decrypt-files-or-folders"></a>
# Desencriptar ficheiros ou pastas

Comando: `onekit run security-decrypt`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: ** segurança**. Fidelidade: **Exacto**. AES-256 codificados ZIP, compatível com 7-Zip. Os nomes dos ficheiros permanecem visíveis. Perder a senha torna a recuperação impossível.

Tipos aceites: `zip`. Tipo de saída: `*`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `password`, `restore`.

Python pacotes: pycryptodome, stream-zip, stream-unzip. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/security/__init__.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
