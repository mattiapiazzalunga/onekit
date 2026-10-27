<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# Testeur de regex

```sh
onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"(?<word>\\w+)","flags":"g","enable_replacement":true,"replacement":"[$<word>]"}'
onekit doctor dev-regex-test
```

Le rapport JSON inclut le motif, les flags, le nombre de correspondances, l'état de troncature, le texte exactement trouvé, les positions de début/fin, les groupes capturés numérotés et les groupes nommés. Les groupes non appariés sont nuls. Les positions utilisent des unités de code UTF-16, comme le fait JavaScript, donc les caractères Unicode astraux occupent deux unités. Les correspondances globales vides avancent correctement, même sous le flag Unicode.

Définissez `enable_replacement` sur true et fournissez `replacement` pour prévisualiser les remplacements. Les jetons de substitution pris en charge correspondent à ceux du remplacement de chaînes JavaScript : `$$`, `$&`, `$1`–`$99`, `$<name>`, `$'` et le jeton de préfixe composé d’un dollar et d’un accent grave. Les remplacements ne modifient jamais l’entrée de test. Lorsque les résultats des correspondances sont tronqués, le résultat du remplacement n’est pas fourni, afin de ne pas présenter un résultat incomplet.
