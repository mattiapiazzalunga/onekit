<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-text-formatting"></a>
# Textformatierung entfernen

Befehl: `onekit run text-strip-formatting`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Analyse**. Wiedergabetreue: **mit Einschränkungen**. Wandeln Sie eingefügten Text, UTF-8/UTF-16-Textdateien, HTML, Markdown oder den Haupttext von Word-DOCX-Dateien lokal in eine UTF-8-codierte TXT-Datei um. Entfernt Formatierungen, Links und Markup, erhält aber lesbaren Text sowie grundlegende Absatz- und Tabellenumbrüche. Reiner Text behält Satzzeichen unverändert bei. Keine OCR; DOCX-Kopf- und Fußzeilen, Bilder und Kommentare werden ausgelassen. Bis zu 8 MiB pro Eingabe.

Akzeptierte Typen: `txt, html, md, docx`. Ausgabetyp: `txt`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **beliebiger Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **8.388.608 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `input_format`.

Python-Pakete: markdown-it-py, defusedxml. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/plain_text.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
