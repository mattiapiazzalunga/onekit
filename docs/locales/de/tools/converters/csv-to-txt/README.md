<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="csv-to-txt"></a>
# CSV in TXT

Befehl: `onekit run csv-to-txt`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Konverter**. Wiedergabetreue: **exakt**. Wandelt CSV-Zeilen in in Anführungszeichen gesetzte, tabulatorgetrennte UTF-8 TXT um. Wählen Sie das Eingabetrennzeichen. Eingebettete Tabs und Zeilenumbrüche bleiben in Anführungszeichen.

Akzeptierte Typen: `csv`. Ausgabetyp: `txt`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **Text**. Erforderliche Dateianzahl: **1–1**. CLI: **8.388.608 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `delimiter`.

Python-Pakete: Standardbibliothek oder externe Engine. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/text_converters.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
