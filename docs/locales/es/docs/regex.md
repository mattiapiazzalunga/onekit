<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# Probador de Regex

```sh
onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"(?<word>\\w+)","flags":"g","enable_replacement":true,"replacement":"[$<word>]"}'
onekit doctor dev-regex-test
```

El reporte del JSON incluye el patrón, las banderas, el conteo de coincidencias, el estado de truncamiento, el texto exactamente coincidido, las posiciones de inicio/fin, los grupos capturados numerados y los grupos con nombre. Los grupos que no coinciden son nulos. Las posiciones usan unidades de código UTF-16, como hace JavaScript, así que los caracteres astrales de Unicode ocupan dos unidades. Las coincidencias globales vacías avanzan correctamente, incluso con la bandera Unicode activada.

Establece `enable_replacement` en true y proporciona `replacement` para previsualizar las sustituciones. Los tokens de sustitución compatibles corresponden a los de las cadenas JavaScript: `$$`, `$&`, `$1`–`$99`, `$<name>`, `$'` y el token de prefijo formado por un dólar y una comilla invertida. Las sustituciones nunca modifican la entrada de prueba. Cuando se truncan los resultados de las coincidencias, no se muestra el resultado de la sustitución, para evitar presentar un resultado incompleto.
