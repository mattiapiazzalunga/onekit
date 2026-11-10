<a id="digital-signature-validation"></a>
# Validação de assinatura digital

O CLI e o navegador executam o mesmo motor de validação Python. Nenhum documento é enviado. As assinaturas da lista de confiança da UE e a caducidade são verificadas; os serviços não suportados estão excluídos.

Integridade criptográfica e validação do AdES são resultados separados. A validação utiliza provas locais e listas de confiança autenticadas da UE. As provas desaparecidas são indeterminadas. Equivalência com DSS não é certificada.

Verifica as assinaturas PDF e CMS localmente com validação AdES. As assinaturas destacadas requerem o arquivo original. Opcionalmente, adicione uma prova de assinatura ZIP. A falta de confiança ou revogação de provas dá um resultado indeterminado.

Atualizar listas de confiança públicas com este comando. Ele não envia nenhum documento ou dados de assinatura.

```sh
python -m pip install "onekit-tools[verification,trustlists]"
python -m onekit.signature_evidence eu-trust-lists.zip
onekit run signature-verify signed.pdf eu-trust-lists.zip -o report
```

O manifesto de provas ZIP utiliza a seguinte estrutura. Certificados suplementares nunca se tornam âncoras arbitrárias de confiança.

```json
{"schema":"onekit-signature-evidence-v1","lotl":"lotl.xml","trusted_lists":[{"url":"https://official.example/list.xml","path":"tl/list.xml"}],"certificates":[],"crls":[],"ocsps":[]}
```

Nativo Windows ARM64 Python pode exigir ferramentas de construção para criptografia. Use x64 Python quando um binário wheel não estiver disponível.

O instantâneo atual contém 30 territórios. Suportado TakenOverPor extensões preservar histórico de serviço e não transferir confiança para outro provedor.

A aceitação do algoritmo utiliza os limiares fixados DSS 6.5.1; a integridade matemática é reportada separadamente.

Em Windows, a lista de confiança extra permite verificar TLS através da loja de certificados do sistema operacional.

O snapshot de confiança tem cobertura parcial. A falta de provas permanece indeterminada. Os testes de referência DSS selecionados não estabelecem equivalência exaustiva do eIDAS ou do PAdES.
