<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="txt-to-excel"></a>
# TXT in Excel

Befehl: `onekit run txt-to-xlsx`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Konverter**. Wiedergabetreue: **exakt**. Parst abgegrenzte TXT in ein Excel-Arbeitsblatt. Zellen werden als Text gespeichert, wobei führende Nullen erhalten bleiben und die Ausführung von Formeln verhindert wird. Erfordert konsistente Spaltenanzahl.

Akzeptierte Typen: `txt`. Ausgabetyp: `xlsx`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **Text in der gewählten Kodierung**. Erforderliche Dateianzahl: **1–1**. CLI: **8.388.608 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `delimiter`, `source_encoding`.

Python-Pakete: openpyxl. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/text_converters.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
