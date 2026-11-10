<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="verify-digital-signature"></a>
# Verificar assinatura digital

Comando: `onekit run signature-verify`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: ** segurança**. Fidelidade: **Exacto**. Verifica as assinaturas PDF e CMS localmente com validação AdES. As assinaturas destacadas requerem o arquivo original. Opcionalmente, adicione uma prova de assinatura ZIP. A falta de confiança ou revogação de provas dá um resultado indeterminado.

Tipos aceites: `*`. Tipo de saída: `json`. Aceita múltiplas entradas: **yes**.

Validação de entrada: **any**. Contagem de ficheiros necessária: **1–3**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: nenhuma.

Python pacotes: pypdf, asn1crypto, pycryptodome, pyhanko, pyhanko-certvalidator, cryptography, signxml, xsdata. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/signatures.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
