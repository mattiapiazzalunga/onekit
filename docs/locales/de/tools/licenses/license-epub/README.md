<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="epub-license-checker"></a>
# EPUB Lizenzprüfer

Befehl: `onekit run license-epub`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Lizenzen**. Wiedergabetreue: **mit Einschränkungen**. Eine Schätzung basierend auf Angaben und Metadaten, kein Rechtezertifikat oder rechtliche Freigabe. Überprüfen Sie jedes Ergebnis mit der Originalquelle und dem Rechteinhaber. Fehlende Informationen bedeuten niemals, dass es frei nutzbar ist. Autoren und Rechteinhaber können abweichen. Dateien werden lokal analysiert; Links werden direkt von ihrer Quelle heruntergeladen. Archive sind begrenzt und Scans können unvollständig sein.

Akzeptierte Typen: `epub`. Ausgabetyp: `json`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **beliebiger Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `ref`.

Python-Pakete: license-expression, defusedxml. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/license_check.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
