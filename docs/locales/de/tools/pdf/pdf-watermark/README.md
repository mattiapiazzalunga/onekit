<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="add-watermark-to-pdf"></a>
# Wasserzeichen zu PDF hinzufügen

Befehl: `onekit run pdf-watermark`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **PDF**. Wiedergabetreue: **exakt**. Fügt allen oder ausgewählten Seiten ein Text- oder PNG/JPEG-Bildwasserzeichen hinzu, wobei der Originaltext und die Grafiken erhalten bleiben. Unterstützt westliche europäische Texte, Einzel- oder wiederholtes Layout, Drehung und Deckkraft. Die Originaldatei bleibt unverändert.

Akzeptierte Typen: `pdf`. Ausgabetyp: `pdf`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `text`, `pages`, `font`, `font_size`, `color`, `opacity`, `angle`, `position`, `layout`, `margin`, `watermark_type`, `image_base64`, `image_width`.

Python-Pakete: pypdf, reportlab, Pillow. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/pdf.watermark/__init__.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
