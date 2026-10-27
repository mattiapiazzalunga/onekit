<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="make-pdf-fillable"></a>
# PDF ausfüllbar machen

Befehl: `onekit run pdf-make-fillable`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **PDF**. Wiedergabetreue: **exakt**. Fügt benannte AcroForm-Textfelder, Kontrollkästchen und Dropdown-Auswahllisten hinzu. Die Rechtecke verwenden normalisierte Koordinaten relativ zur linken oberen Ecke. Bestehende Felder und Seiteninhalte bleiben erhalten. Keine automatische Erkennung leerer Bereiche und keine XFA-Konvertierung; prüfen Sie die Kompatibilität mit Ihrem PDF-Reader.

Akzeptierte Typen: `pdf`. Ausgabetyp: `pdf`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `fields`.

Python-Pakete: pypdf. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/pdf_design.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
