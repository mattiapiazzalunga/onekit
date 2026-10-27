<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="calculate-checksum"></a>
# Prüfsumme berechnen

Befehl: `onekit run file-checksum`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Analyse**. Wiedergabetreue: **exakt**. Berechnet SHA-256, SHA-512, SHA-1 oder MD5 lokal. Eine optionale erwartete Prüfsumme kann mit einer Datei verglichen werden. Eine Prüfsumme verifiziert keine digitale Signatur und garantiert nicht die Sicherheit der Datei.

Akzeptierte Typen: `*`. Ausgabetyp: `json`. Mehrere Eingaben möglich: **ja**.

Eingabevalidierung: **beliebiger Dateityp**. Erforderliche Dateianzahl: **1–20**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `algorithm`, `expected`.

Python-Pakete: Standardbibliothek oder externe Engine. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/file_checksum.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
