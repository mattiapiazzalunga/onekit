<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-audio-from-video"></a>
# Audio aus Video entfernen

Befehl: `onekit run video-mute`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Video**. Wiedergabetreue: **mit Einschränkungen**. Exportiert MP4 ohne Audiospuren mit FFmpeg. Das Video wird neu codiert und kann an Qualität verlieren.

Akzeptierte Typen: `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Ausgabetyp: `mp4`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: keine.

Python-Pakete: Standardbibliothek oder externe Engine. Externe Engines: ffmpeg, ffprobe.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/video_edit.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
