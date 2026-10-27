<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="sharpen-and-deblur-image"></a>
# Bild schärfen und Unschärfe reduzieren

Befehl: `onekit run image-sharpen`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Bilder**. Wiedergabetreue: **mit Einschränkungen**. Unscharfmaskierung oder Gaußsche Richardson-Lucy-Dekonvolution mit Verarbeitungsgrenzen. Die Reduzierung der Unschärfe beruht auf einem Unschärfemodell und kann Rauschen oder Halos verstärken; die Wiederherstellung fehlender Details ist nicht garantiert. Die Dekonvolution ist auf eine Million Pixel begrenzt.

Akzeptierte Typen: `png, jpeg, webp, gif, bmp, tiff, ico`. Ausgabetyp: `png`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `method`, `radius`, `amount`, `iterations`.

Python-Pakete: Pillow, numpy. Externe Engines: die Adapter für Programmiersprachen finden Sie in der Engine-Matrix für Entwicklerwerkzeuge.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/photo_tools.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
