<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="minify-tsx"></a>
# TSX minifizieren

Befehl: `onekit run dev-minify-tsx`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Entwicklung**. Wiedergabetreue: **mit Einschränkungen**. Erzeugt minifizierte JavaScript (.js). TypeScript-Typen werden entfernt; JSX und TSX werden kompiliert. Behalten Sie die Originalquelle.

Akzeptierte Typen: `tsx, txt`. Ausgabetyp: `js`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **Text**. Erforderliche Dateianzahl: **1–1**. CLI: **8.388.608 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: keine.

Python-Pakete: Standardbibliothek oder externe Engine. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/developer/__init__.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
