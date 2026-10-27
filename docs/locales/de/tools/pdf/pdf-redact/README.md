<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanently-redact-pdf"></a>
# PDF dauerhaft schwärzen

Befehl: `onekit run pdf-redact`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **PDF**. Wiedergabetreue: **mit Einschränkungen**. Schwärzt ausgewählte Bereiche dauerhaft und baut jede Seite aus Rasterpixeln neu auf. Ursprüngliche Texte, Anhänge, Kommentare, Formulare und Metadaten werden nicht übernommen; auswählbarer Text und Vektorqualität gehen verloren. Die Originaldatei bleibt unverändert.

Akzeptierte Typen: `pdf`. Ausgabetyp: `pdf`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `regions`, `dpi`.

Python-Pakete: pypdfium2, Pillow, reportlab, pypdf. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/redaction.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
