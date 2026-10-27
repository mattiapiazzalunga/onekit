<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# Regex-Tester

```sh
onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"(?<word>\\w+)","flags":"g","enable_replacement":true,"replacement":"[$<word>]"}'
onekit doctor dev-regex-test
```

Der JSON-Bericht enthält das Muster, Flags, Trefferanzahl, Trunkierungsstatus, exakt übereinstimmenden Text, Start-/Endpositionen, nummerierte Capture-Gruppen und benannte Gruppen. Nicht übereinstimmende Gruppen sind null. Die Positionen verwenden UTF-16-Codeeinheiten, wie es JavaScript tut, sodass astrale Unicode-Zeichen zwei Einheiten einnehmen. Leere globale Treffer werden korrekt weitergeschaltet, auch unter dem Unicode-Flag.

Setzen Sie `enable_replacement` auf true und geben Sie `replacement` an, um Ersetzungen in der Vorschau zu sehen. Die unterstützten Ersetzungs-Token entsprechen der JavaScript-Zeichenkettenersetzung: `$$`, `$&`, `$1`–`$99`, `$<name>`, `$'` und das Präfix-Token aus Dollarzeichen und Backtick. Ersetzungen ändern niemals die Testeingabe. Wenn die Trefferliste gekürzt wird, wird das Ersetzungsergebnis nicht angezeigt, damit kein unvollständiges Ergebnis dargestellt wird.
