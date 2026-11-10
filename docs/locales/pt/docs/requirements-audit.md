<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-requirements-verification"></a>
# CLI verificação de requisitos

`tests/test_requirements.py` verifica a cobertura do catálogo, CLI invocações e pipelines mal formados. `tests/test_core.py` verifica contratos de processamento e semântica de saída. Validação de entrada, expansão de arquivos, criptografia e proteções do sistema de arquivos têm testes de regressão dedicados.

Executar `python -m pytest -q` para a suite padrão. Os motores instalados separadamente são testados com `python -m pytest -q -m native`; desde que as dependências descritas em `docs/engines.md` antes de executar essas verificações. Passar no pacote padrão não verifica todos os motores externos ou todas as plataformas suportadas.
