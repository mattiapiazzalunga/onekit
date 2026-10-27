<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# Tester regex

```sh
onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"(?<word>\\w+)","flags":"g","enable_replacement":true,"replacement":"[$<word>]"}'
onekit doctor dev-regex-test
```

Il rapporto JSON include il pattern, i flag, il numero di corrispondenze, lo stato di troncamento, il testo esatto di ogni corrispondenza, le posizioni iniziali e finali, i gruppi di cattura numerati e quelli con nome. I gruppi senza corrispondenza hanno valore null. Le posizioni sono espresse in unità di codice UTF-16, come in JavaScript: i caratteri Unicode al di fuori del piano multilingue di base occupano quindi due unità. Le corrispondenze vuote nelle ricerche globali fanno avanzare correttamente la posizione, anche quando è attivo il flag Unicode.

Imposta `enable_replacement` su true e fornisci `replacement` per visualizzare un’anteprima delle sostituzioni. I token di sostituzione supportati corrispondono a quelli delle stringhe JavaScript: `$$`, `$&`, `$1`–`$99`, `$<name>`, `$'` e il token di prefisso formato da dollaro e backtick. Le sostituzioni non modificano mai l’input del test. Quando i risultati delle corrispondenze vengono troncati, il risultato della sostituzione non viene mostrato, per evitare di presentare un risultato incompleto.
