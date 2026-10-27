<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="set-metadata"></a>
# Metadaten setzen

Befehl: `onekit run file-metadata-set`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Analyse**. Wiedergabetreue: **exakt**. Beibehaltung der ausgewählten Inhalte; wichtige Ergebnisse überprüfen.

Akzeptierte Typen: `*`. Ausgabetyp: `*`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **beliebiger Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `metadata`.

Python-Pakete: Standardbibliothek oder externe Engine. Externe Engines: exiftool.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/inspector/__init__.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
