<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="input-validation"></a>
# Eingabevalidierung

Jeder Katalogeintrag gibt akzeptierte Formate, Dateianzahlen und Byte-Grenzen an. `onekit list --json` legt die Werte offen. Sowohl direkte Ausführung als auch Pipelines setzen die Vorgaben durch.

<a id="limits"></a>
## Limits

Die Gesamtgrenzen pro Stapel betragen 128 MiB und 256 Dateien. Texteingaben sind auf 8 MiB pro Datei begrenzt, Rasterbilder auf 64 MiB und Schriftdateien auf 16 MiB. Ein Vergleich benötigt genau zwei Eingaben. Dekodierte Rasterbilder sind über alle Einzelbilder hinweg auf insgesamt 40 Millionen Pixel begrenzt. Der entpackte Inhalt von Archiven und Office-Dateien ist auf 128 MiB und 4096 Einträge begrenzt.

Werkzeuge für eine einzelne Eingabedatei lehnen zusätzliche Dateien ab. Die Pipeline-Zuordnung wendet absichtlich einen Schritt mit einer Eingabe auf jede vorherige Ausgabe an. Ausgabesammlungen werden schrittweise überprüft, sodass ein zugeordneter Schritt nicht unbegrenzt zurückgegebene Daten ansammeln kann. CLI Dateianzahl, Erweiterungen und Größen werden vor dem Lesen der Dateiinhalte überprüft, und die tatsächlich gelesenen Bytes sind begrenzt, selbst wenn eine Datei während des Lesens wächst.

<a id="content-rules"></a>
## Content rules

- PDF-Werkzeuge erfordern PDF-Header und einen kohärenten finalen Querverweisort. `pdf-repair` erlaubt absichtlich beschädigte Querverweise nach der Überprüfung des PDF-Headers; sein Parser muss dennoch ein tatsächliches PDF wiederherstellen. In `.pdf` umbenannte Bilder werden abgelehnt.
- Rastereingaben werden mit Pillow auf tatsächliches Format, Struktur und dekodierte Abmessungen überprüft. Ein in JPEG umbenanntes PNG wird abgelehnt. Base64-Export dekodiert das Bild ebenfalls vor der Annahme.
- Word, Excel und PowerPoint erfordern unterschiedliche ZIP-Containerteile und Namespaced-XML-Wurzeln. Das Umbenennen von Excel zu `.docx` macht es nicht zu Word. Verzeichnisanzahlen und Erweiterungsbudgets werden überprüft, bevor die ZIP-Eintragstabelle zugewiesen oder Dokumentteile gelesen werden.
- Schriftdateien benötigen passende SFNT/WOFF-Header, gültige Tabellenbereiche innerhalb der zulässigen Grenzen und konsistente Größenangaben für komprimierte Schriften. Die angegebene Größe nach dem Entpacken einer WOFF-Datei darf das Byte-Limit für Schriften nicht überschreiten.
- Medieneingaben haben explizite Audio-/Video-Erweiterungen und Container-Signaturen. FFprobe überprüft die Stream-Arten vor der FFmpeg-Konvertierung; Videokonvertierung erfordert Video, und Audiokonvertierung erfordert Audio ohne gewöhnliche Videostreams. Angehängte Cover-Art ist erlaubt. Beide ausführbaren Dateien werden von `doctor` gemeldet.
- Archive lehnen unsichere/duplizierte Pfade, Symlinks, verschlüsselte ZIP-Einträge, ungültige Verzeichnisse, Multi-Volume-/ZIP64-Verzeichnisse und nicht unterstützte zusammengeführte komprimierte Streams ab. ZIP-Expansionsverhältnisse sind begrenzt. TAR-Dekompression ist vor dem Member-/PAX-Parsen begrenzt, mit einem zusätzlichen festen 4 MiB-Zuschlag für TAR-Header/Padding; XZ-Dekoder-Speicher ist ebenfalls begrenzt.
- Die Entschlüsselung akzeptiert nur das OneKit-verschlüsselte Format und überprüft dessen Inhalte, bevor das gebundene Archiv wiederhergestellt wird. Benutzeroptionen können das festgelegte Dekompressionsbudget nicht erhöhen.
- Textwerkzeuge benötigen lesbaren Text ohne binäre Steuerbytes. Entwicklerwerkzeuge akzeptieren ihre Sprach-Erweiterungen und neutrale `.txt`-Eingaben; Shell-/Dockerfile-Adapter erlauben ebenfalls Quelltextdateien ohne Dateiendung. Validierungswerkzeuge akzeptieren absichtlich syntaktisch ungültigen Quellcode und geben `valid: false` zurück. Die Kodierungsumwandlung verwendet die ausgewählte Quellkodierung; andere Textwerkzeuge benötigen UTF-8..
- Inspektion, Metadaten-Adapter und Verschlüsselung akzeptieren absichtlich beliebige Dateitypen. Ihre Anzahl-/Byte-Grenzen gelten weiterhin. Das Untersuchen einer beschädigten oder unbekannten Datei ist eine unterstützte Operation, und kein Grund, sie ausschließlich wegen ihres Inhalts abzulehnen.
