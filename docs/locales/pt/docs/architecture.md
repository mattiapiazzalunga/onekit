<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="architecture-and-extension-guide"></a>
# Guia de arquitetura e extensão

`Artifact(name, data)` é uma carga imutável chamada bytes. `Result(files, warnings, details)` carrega saídas e avisos de fidelidade. `execute(tool_id, files, options)` valida os contratos e importa um adaptador de processamento apenas quando necessário. `pipeline(steps, files)` compõe operações e mapeia múltiplas saídas através de etapas de entrada única.

O catálogo define IDs estáveis, famílias, tipos aceitos e de saída, multiplicidade, opções, fidelidade, limites e dependências. Os adaptadores de processamento são independentes do acesso ao sistema de arquivos CLI. Nomes portáteis rejeitam nomes de dispositivos de travessia e reservados. CLI saída escreve preservar arquivos existentes por padrão. Chamadas de motores nativos usam arrays de argumentos, diretórios temporários e tempo limite.

Para adicionar uma ferramenta, implemente seu adaptador de família, declare a entrada do catálogo, adicione testes de regressão semânticos e inválidos, declare dependências opcionais e reveja licenças. Regenerar diretórios de ferramentas com `python scripts/tool_docs.py`. Fidelidade do documento e requisitos da plataforma.


O processamento API v1 está descrito em `contracts/processing-v1.json`. Executar `python scripts/check_contracts.py` antes de enviar alterações. Adicionar ferramentas, formatos e opções é compatível; remover IDs/opções existentes, mudar tipos de saída ou restringir contratos de entrada requer uma migração versionada explícita. Algoritmos internos e organização do manipulador podem mudar sem alterar o contrato público.

`ExecutionContext` permite Python chamadores menor lote e orçamentos por ferramenta e fornecer um leitor de metadados de mídia local confiável. Não aceita serviços de motor através de opções de ferramentas fornecidas pelo usuário. Contextos são imutáveis, escopo para uma execução e compartilhado por etapas de pipeline. O CLI usa os serviços de motor local padrão.

O adaptador de fonte Node delega as regras de formatação e minificação para `tools/developer/source_engine.mjs`. Seu carregador de motor é uma dependência de nível de processo; texto fonte não pode escolher pacotes arbitrários ou comandos executáveis.
