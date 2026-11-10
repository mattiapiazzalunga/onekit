<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="release-operations"></a>
# Operações de lançamento

Proteger `main` e estável `v*` etiquetas. Registar o PyPI Editor confiável para repositório `onekit`, fluxo de trabalho `release.yml` e ambiente `pypi`. Atualize a versão do pacote, lockfile, catálogo e documentação, em seguida, publique uma tag SemVer estável correspondente de um commit revisado.

O fluxo de trabalho de lançamento verifica a tag, executa verificações necessárias CLI e publica distribuições universais wheel/fonte, a imagem GHCR e os ativos de liberação GitHub. `onekit-release.json` contém versão, commit fonte, checksums de ativos e URLs de download. As repetições de publicação devem preservar os ativos imutáveis existentes; as alterações de código requerem uma nova versão.

<a id="pypi-license-metadata"></a>
## Metadados de licença no PyPI

A PyPI pacote é código aberto (PolyForm Shield 1.0.0), com a restrição de não concorrência explicada no README exibido em sua página de projeto. `project.license` usos `LicenseRef-PolyForm-Shield-1.0.0`; wheel e arquivo de origem incluem a LICENÇA completa e NOTICE. Os metadados do projeto ligam-se à licença e documentação. Não adicione um classificador de licença aprovado pela OSI: esta licença restringe os produtos concorrentes.

Antes da publicação, construa a partir do commit de liberação pretendido e valide os artefatos reais:

```sh
uv build
python scripts/check_distribution_licenses.py
```

O IC e a compilação de lançamento executam esta verificação antes que os artefatos possam ser publicados. PyPI renderiza o pacote README, então a reconstrução é necessária após alterar a documentação ou metadados de licença. Publicar uma versão nova e não utilizada ao substituir uma versão já publicada; as distribuições PyPI existentes não podem ser sobrescritas. Versões distribuídas anteriormente mantêm seus termos de licenciamento originais. A versão atual do checkout não é automaticamente avançada por uma mudança de licença.

O proprietário do projeto configura a conta PyPI, o Editor Trusted e a publicação separadamente; a preparação local não envia pacotes ou altera a página ao vivo PyPI.

<a id="weekly-dependency-maintenance"></a>
## Manutenção semanal das dependências

Dependebot monitora o lockfile uv, CLI dependências do motor Node, Docker e GitHub Ações. O fluxo de trabalho agendado verifica retestes dependências bloqueadas e motores nativos. Atualizações elegíveis Python somente de bloqueio permanecem sujeitas a verificações bem-sucedidas e proteção de filiais.
