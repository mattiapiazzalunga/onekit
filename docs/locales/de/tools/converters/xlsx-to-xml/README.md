<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="excel-to-xml"></a>
# Excel in XML

Befehl: `onekit run xlsx-to-xml`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Konverter**. Wiedergabetreue: **exakt**. XML-Tabellen verwenden wiederholte flache Datensätze. JSON bis XML bewahren die Typen unter Verwendung eines typisierten Root-/Item-Schemas; XML-Attribute verwenden @ und Text verwendet #text in JSON. Tabellenkalkulationsformeln werden nicht ausgewertet; standardmäßig wird das erste Blatt verwendet. Überprüfen Sie Schema und Werte nach der Konvertierung.

Akzeptierte Typen: `xlsx`. Ausgabetyp: `xml`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `sheet`.

Python-Pakete: openpyxl. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/structured_data.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
