<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# Testar expressões regulares

```sh
onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"(?<word>\\w+)","flags":"g","enable_replacement":true,"replacement":"[$<word>]"}'
onekit doctor dev-regex-test
```

O relatório JSON inclui o padrão, bandeiras, contagem de correspondências, status truncado, texto exato pareado, posições de início/fim, grupos de captura numerados e grupos nomeados. Grupos inigualáveis são nulos. As posições usam UTF-16 unidades de código, como JavaScript, caracteres Unicode tão astral ocupam duas unidades. Avanço global vazio corresponde corretamente, incluindo sob a bandeira Unicode.

Definir `enable_replacement` ao verdadeiro e ao fornecimento `replacement` Previsão de substituições. Os tokens de substituição suportados correspondem JavaScript substituição de texto: `$$`, `$&`, `$1`–`$99`, `$<name>`, `$'` e o símbolo de prefixo do dólar-plus-backtick. As substituições nunca alteram a entrada de teste. Quando os resultados da correspondência são truncados, a substituição é retida em vez de apresentar um resultado incompleto.
