<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="ocr-to-word"></a>
# OCR in Word

Befehl: `onekit run ocr-to-docx`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **OCR**. Wiedergabetreue: **mit Einschränkungen**. Die Erkennung hängt von der Scanqualität und den installierten Sprachpaketen ab. Gleichungen und Layout müssen möglicherweise manuell korrigiert werden.

Akzeptierte Typen: `pdf, png, jpeg, webp, gif, bmp, tiff, ico`. Ausgabetyp: `docx`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `language`, `dpi`.

Python-Pakete: pytesseract, Pillow, pypdfium2, python-docx. Externe Engines: tesseract.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/ocr/__init__.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
