<a id="cli-localization"></a>
# Localização da CLI

Línguas: `en`, `it`, `fr`, `es`, `de`, `ru`, `zh` (chinês simplificado), `pt` (português), `hi` (hindi). Selecione um com `onekit --language it ...`, ou `ONEKIT_LANGUAGE=it`. O local do sistema operacional é usado quando nenhum dos dois está definido. Locais não suportados usam inglês. Nomes de comando, chaves de opção, caminhos, identificadores de formato e contratos legíveis por máquina JSON permanecem estáveis. Ajuda humana, status, avisos e erros conhecidos são localizados. Os diagnósticos externos dos motores mantêm o seu texto a montante.

Cada pessoa ou AI adicionar ou mudar uma ferramenta DEVE atualizar todos os nove catálogos de apresentação na mesma mudança. Nomes, ajuda, descrições, mensagens de erro, avisos, README e documentação da ferramenta devem permanecer em uma correspondência individual. Não preencher as traduções em falta com o inglês como atalho. Mantenha os placeholders, exemplos de código, URLs e avisos verbatim legalmente obrigatórios intactos. Reveja o significado e a terminologia no contexto.

Catálogos: `src/onekit/locales/{language}.json`. Código de apresentação: `i18n.py`. Mensagens em inglês são chaves normalizadas; algoritmos de processamento permanecem independentes. O registo de línguas independente é `src/onekit/locales/languages.json`, incluindo os aliases do sistema operativo. Adicione uma entrada de registro e um catálogo completo juntos. A terminologia revista é registada em `scripts/localization-reviewed.json`; aplica-o com `python scripts/apply_localization_review.py src/onekit/locales` Antes da auditoria.

1. Edite a mensagem ou documentação em inglês em seu arquivo original.
2. Corre `python scripts/localization_inventory.py`.
3. Atualizar todos os outros catálogos de idiomas e remover entradas obsoletas. Os scripts de autoria podem redigir traduções; texto gerado requer revisão.
4. Correr `python scripts/audit_localization.py` e `pytest tests/test_i18n.py`.
5. Executar `python scripts/localize_docs.py` para regenerar localizado Markdown sob `docs/locales/{language}/`, mantendo a estrutura original do documento relativo.

O comando de criação offline toma um diretório local do modelo Argos seguido por diretórios de catálogo. CTranslate2 e SentencePiece são dependências de autoria, não CLI requisitos de tempo de execução. Nenhum serviço de tradução é contactado pelo CLI.

As traduções e documentação dos CLI são mantidas independentemente de qualquer site que incorpore a biblioteca de processamento. Apenas as ligações de uso público pertencem aqui.
