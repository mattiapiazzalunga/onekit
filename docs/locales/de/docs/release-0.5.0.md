<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="onekit-050"></a>
# OneKit 0.5.0

Erste Version der Offline-CLI und der Python-Verarbeitungs-API mit 230 Tools für Dokumente, PDFs, Bilder, Medien, Archive, Schriftarten, Entwicklerwerkzeuge, QR-Codes, Lizenzangaben und Dateiüberprüfung. Die Basisinstallation hat keine Laufzeitabhängigkeiten; optionale Extras und externe Engines ermöglichen die Nutzung der ausgewählten Tools.

Beinhaltet begrenzte Eingabevalidierung, wiederverwendbare Workflows, lokale Abhängigkeitsinstallationen, formatspezifische Verarbeitungskontrakte und quellenbasierte Lizenzprüfung. Lizenzberichte bleiben ungeprüfte Schätzungen, die manuell überprüft werden müssen.

Leistungsupdates beschleunigen die Vorbereitung von undurchsichtigen Bildern sowie die Textüberprüfung. Unbenutzte Importe und überflüssige Entwickler-Engine-Zuweisungen wurden entfernt.

Modell-Engines sind optional: installieren Sie bei Bedarf das `background`- oder `transcription`-Extra. U2Net läuft direkt mit ONNX Runtime und einem prüfsummen-verifizierten zwischengespeicherten Modell. Whisper verwendet faster-whisper. Dateien bleiben lokal; beim ersten Lauf werden Modellgewichte heruntergeladen. Die Videobearbeitung erfordert FFmpeg und ffprobe. Das Herunterladen von Videos verwendet das separate `video`-Extra.

Aktualisiert Pillow auf Version 13 und die festgeschriebene Version von certifi, um die in veröffentlichten Sicherheitshinweisen gemeldeten Probleme zu beheben. Die plattformübergreifende Gruppe optionaler Abhängigkeiten `all` bleibt von Modell-Engines und Signaturfunktionen getrennt.
