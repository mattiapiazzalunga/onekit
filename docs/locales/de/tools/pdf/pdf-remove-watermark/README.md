<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-pdf-watermark"></a>
# PDF-Wasserzeichen entfernen

Befehl: `onekit run pdf-remove-watermark`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **PDF**. Wiedergabetreue: **mit Einschränkungen**. Untersuchen und entfernen Sie ausgewählten Text, Bilder und Aufrufe von Form XObjects, einschließlich verschachtelter Form XObjects und über Schriftarten codierten Texts. Als Wasserzeichen markierte Artefakte und Wasserzeichen-Anmerkungen werden automatisch entfernt. Nicht markierte Objekte erfordern eine Auswahl oder den genauen Text; in die Bildpixel eingebettete Markierungen können nicht vom Bild getrennt werden. Prüfen Sie jede Seite.

Akzeptierte Typen: `pdf`. Ausgabetyp: `pdf`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `text`, `mode`, `objects`.

Python-Pakete: pypdf. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/pdf_design.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
