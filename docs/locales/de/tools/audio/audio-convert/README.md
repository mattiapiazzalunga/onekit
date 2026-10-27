<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="convert-audio"></a>
# Audio umwandeln

Befehl: `onekit run audio-convert`. Informationen zu Eingabe- und Ausgabeargumenten erhalten Sie mit `onekit run --help`.

Kategorie: **Audio**. Wiedergabetreue: **mit Einschränkungen**. Verfügbare Codecs hängen von Ihrem FFmpeg-Build ab; erneutes Kodieren kann Qualität verlieren.

Akzeptierte Typen: `mp3, wav, flac, ogg, aac, m4a, mp4, aif, aiff, opus, wma`. Ausgabetyp: `*`. Mehrere Eingaben möglich: **nein**.

Eingabevalidierung: **nach Dateityp**. Erforderliche Dateianzahl: **1–1**. CLI: **134.217.728 Byte pro Datei**, **134.217.728 Byte insgesamt**. Der Inhalt wird vor der Verarbeitung geprüft. Das Umbenennen einer Datei ändert nicht ihr tatsächliches Format.

Optionen: `format`, `codec`, `bitrate`.

Python-Pakete: Standardbibliothek oder externe Engine. Externe Engines: ffmpeg, ffprobe.

Verarbeitungsimplementierung: [gemeinsamer Adapter der Werkzeugfamilie](../../../../../../src/onekit/tools/media/__init__.py). Verträge und Testdaten für Regressionstests: [Tests](../../../../../../tests/test_core.py). Einrichtung der Engines und Lizenzen: [Engine-Leitfaden](../../../docs/engines.md).

Dieses Verzeichnis wird vom gemeinsamen Katalog durch `python scripts/tool_docs.py` erstellt. Bearbeiten Sie das Register und den Familienadapter, fügen Sie Regressionsvorrichtungen hinzu und generiere dann das Verzeichnis erneut.
