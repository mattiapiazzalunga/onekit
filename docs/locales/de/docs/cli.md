<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-reference"></a>
# CLI-Referenz

Verwenden Sie `onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","opacity":0.25}'`, um ein PDF-Textwasserzeichen hinzuzufügen. Siehe den [-Wasserzeichen-Leitfaden ](watermark.md) für Position, Drehung, Seitenbereiche und wiederholte Layouts.

Dauerhaftes Schwärzen ist mit `onekit run pdf-redact` und `onekit run image-redact` möglich. Die ausgewählten Bereiche werden über `regions` angegeben. Der [Leitfaden zum Schwärzen](redaction.md) erläutert Koordinaten, Rasterung und den Schutz vertraulicher Inhalte in den exportierten Dateien.

Verwenden Sie `onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"[0-9]+","flags":"g"}'`, um JavaScript-Reguläre Ausdrücke zu testen. Erfordert Node.js; siehe den [ Regex-Tester-Leitfaden ](regex.md) für Gruppen, Ersetzungen und Ausführungsgrenzen.

Standard-Barcodes sind über `onekit run text-to-barcode`, `onekit run scan-barcode` und `onekit run barcode-to-text` verfügbar. Installieren Sie die optionale Abhängigkeitsgruppe `barcode` oder `qrcode`. Weitere Informationen finden Sie unter [Barcode-Einstellungen und unterstützte Standards](qrcode.md#standard-linear-barcodes).

`onekit --version` meldet die Kernversion. `python -m onekit` ruft denselben CLI auf.

| Befehl | Verhalten |
| --- | --- |
| `onekit list [--group GROUP] [--json]` | Werkzeuge, Verträge, Verfügbarkeit und Treue entdecken. |
| `onekit doctor [TOOL_ID] [--json]` | Überprüfen Sie Python-Pakete, Engines und Lizenzrichtlinienblöcke. |
| `onekit run TOOL_ID INPUTS -o OUTPUT` | Verarbeitet Dateien; die Verschlüsselung akzeptiert auch Verzeichnisse. |
| `onekit pipeline --steps WORKFLOW INPUTS -o OUTPUT` | Führt 1 bis 16 geordnete Werkzeugschritte aus einer JSON-Datei aus. |
| `onekit engines install [--directory DIRECTORY]` | Installieren Sie die gesperrten Node-Entwickler-Engines; benötigt Node/npm. |
| `onekit download URL -o OUTPUT [--quality best\|720\|1080] [--force]` | Laden Sie ein einzelnes Video über yt-dlp herunter; erfordert Internet und FFmpeg. |

`run` akzeptiert `--options` mit einem JSON-Objekt, `--ask-password` und `--force`. Pipelines unterstützen auch die Passwortabfrage und das Überschreiben-Flag. Verwenden Sie einen Dateinamen für eine Ausgabe oder ein Verzeichnis für mehrere Ausgaben. Ziele ohne Erweiterung sind Verzeichnisse. Konfligierende Ausgabennamen werden abgelehnt.

<a id="local-agents-and-automation"></a>
## Local agents and automation

**Ihre CLI. Ihre CLI für Agenten.** OneKit ist sowohl an Ihrem Terminal als auch als Dateiverarbeitungs-Toolkit für lokale AI-Agenten nützlich, die Shell-Befehle ausführen oder Unterprozesse starten können. Ein Agent kann Tool-Verträge entdecken, Anforderungen prüfen, einen ausgewählten Vorgang ausführen und die Ausgabedateien überprüfen.

```sh
onekit list --json
onekit doctor pdf-merge --json
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit pipeline --steps workflow.1kit input.pdf -o output/
```

`list --json` zeigt Tool-IDs, akzeptierte Eingaben, Ausgabeformate, Optionen, Grenzen und Hinweise zur Genauigkeit an. `doctor TOOL_ID --json` meldet die Einsatzbereitschaft, fehlende Abhängigkeiten und Lizenz- bzw. Richtlinienblockaden. Analysieren Sie diese JSON-Antworten statt der für Menschen lesbaren Auflistungen. `run` und `pipeline` schreiben ihre Ergebnisse an das mit `-o` angegebene Ziel; sie haben keine allgemeine `--json`-Antwortkennzeichnung. Einige Tools erzeugen JSON-Berichtsdateien.

Für einen lokalen Agenten, entdecke zuerst das Tool, überprüfen Sie seine Anforderungen und rufe es dann mit expliziten Pfaden und einem JSON-Objekt in `--options` auf, wo nötig. Übergeben Sie die Unterprozess-Argumente als Liste, um Pfade und JSON ohne Shell-Quoting zu erhalten. Überprüfen Sie den Exit-Status, bevor Sie die Ausgaben verwenden:

| Exit-Code | Bedeutung |
| --- | --- |
| `0` | Befehl erfolgreich abgeschlossen. |
| `1` | `doctor` hat fehlende Anforderungen oder eine Richtlinienblockade gefunden; überprüfen Sie den Bericht. |
| `2` | Ungültige Argumente oder ein Verarbeitungs-/Ein-/Ausgabefehler; siehe stderr. |
| `130` | Befehl durch Tastaturabbruch beendet. |

Wählen Sie für jeden Auftrag einen neuen Ausgabeordner; bestehende Ausgaben bleiben erhalten, es sei denn, `--force` wird angegeben. `--ask-password` erfordert ein interaktives Terminal. Bereite Abhängigkeiten und Modell-Caches vor unbeaufsichtigte Läufe vor: Fehlende Komponenten können eine automatische Einrichtung und Netzwerknutzung auslösen, und einige native Installer erfordern Interaktion oder erhöhte Rechte. Netzwerktwerkzeuge kontaktieren auch die angeforderten Quellen.

Die Datei wird auf Ihrem Rechner verarbeitet. Wenn der Agent ein entferntes Modell verwendet, bestimmt die Handhabung von Dateiinhalt und Befehlergebnissen durch den Agenten, was an diesen Anbieter gesendet wird. Dieselbe [PolyForm Shield-Lizenz ](licenses.md) gilt für die agentengesteuerte Nutzung.

<a id="tool-options"></a>
## Tool options

Die Generierung von QR, die Konfiguration vCard/Wi-Fi, das Scannen von Bildern und das Rückwärtsdekodieren sind im [QR Code-Handbuch](qrcode.md) dokumentiert. Installieren Sie das `qrcode` Extra und benutze dann `onekit run text-to-qrcode input.txt -o code.png` oder `onekit run scan-qrcode photo.jpg -o decoded.json`.

Die Seitennummerierung beginnt bei 1. `pages` akzeptiert Nummern und aufsteigende Bereiche wie `1,3-5`. Beim Ordnen und Extrahieren bleiben die Reihenfolge und absichtliche Wiederholungen erhalten. Die Drehung akzeptiert Vielfache von 90 und gilt standardmäßig für alle Seiten. Die PDF-Bearbeitung fügt `text` auf `page` an den Koordinaten `x`/`y` ein, gemessen in PDF-Punkten vom Ursprung unten links; vorhandene Inhalte werden nicht neu umbrochen. Zum Signieren werden der Pfad zu einem PKCS#12-`certificate` und dessen `password` benötigt.

Bild `format` unterstützt PNG, JPEG, WebP, TIFF, BMP, ICO, GIF und PDF, falls zutreffend. `quality` ist 1–100. `box` ist `[left, top, right, bottom]` in Pixeln. Animationen/Metadaten können entfernt werden; Transparenz wird für JPEG/PDF auf Weiß reduziert. Kompression kann eine bereits optimierte Datei vergrößern.

Das Spreadsheet `sheet` wählt ein Arbeitsblatt aus, standardmäßig das aktive. Excel Lesen verwendet zwischengespeicherte Formelergebnisse. JSON-zu-Excel erwartet ein Array von Objekten. CSV `delimiter` Standardmäßig auf Komma gesetzt. Formelähnliche XLSX Strings bleiben Text; importieren Sie nicht vertrauenswürdige CSV als Text in Tabellenkalkulationsanwendungen.

Die Kodierungsumwandlung akzeptiert `source_encoding` und `encoding`. Andere Textwerkzeuge verwenden UTF-8.. Für PDF, JPEG und PNG akzeptiert `metadata` die beschreibenden Textfelder `Title`, `Author`, `Subject`, `Keywords` und `Comment`. Nicht angegebene Felder bleiben erhalten; ein leerer String löscht den Wert eines Feldes. Der Python-Helfer `onekit.tools.file_metadata.read_metadata(artifact)` liest diese Felder, ohne das Artefakt zu verändern, einschließlich unterstützter EXIF-, PNG-Text- und XMP-Werte. Andere Metadatenformate verwenden optionale ExifTool-Tag/Value-Paare innerhalb ihrer Formatabdeckung. Inspector-Signaturen identifizieren nicht jeden proprietären Dateityp.

Notebook-Vergleich `mode` ist `both`, `markdown` oder `code`. LaTeX-Modus ist `all` oder heuristisch `text`. PDF/Word-Vergleich extrahiert Text. Diff JSON enthält normalisierte Seiten, geänderte Blöcke und einen einheitlichen Patch, einschließlich Unterschiede bei abschließenden Zeilenumbrüchen. OCR `language` verwendet installierte Tesseract-Codes und `dpi` ist 36–300. PDF/A-Konvertierung erfordert eine lizenzierte `icc_profile`; prüfen Sie die Archivausgabe unabhängig.

Medienoptionen umfassen `format`, `codec` und `bitrate`, abhängig vom FFmpeg-Build. Schriftarten unterstützen `ttf`, `otf`, `woff` und `woff2` und bewahren die Outline-Technologie. Archive unterstützen ZIP und TAR/gzip/bzip2/xz-Kombinationen.

<a id="limits-and-errors"></a>
## Limits and errors

Siehe [ Eingabevalidierung ](input-validation.md) für die durchgesetzten pro-Werkzeug-Typen, Byte/Anzahl-Limits, Signatur-/Containerprüfungen und Regeln zur Archivdekompression. Diese gelten sowohl für direkte Python API Aufrufe als auch für jeden Pipeline-Schritt sowie das CLI. Führen Sie `onekit list --json` aus, um genaue maschinenlesbare Verträge zu erhalten.

Eingaben des Kerns: 256 Dateien und 128 MiB. Pipelines: 16 Schritte. Bilder und gerenderte Seiten: 40 Millionen Pixel. Vergleiche: 10.000 Zeilen und 2 Millionen Zeichen. Archiv-Dekomprimierung: 128 MiB, 4096 Einträge und Prüfung des Expansionsverhältnisses. Externe Engines haben Zeitlimits. Große, gültige Eingaben können diese bewusst gesetzten Grenzen überschreiten.

Exit-Codes: 0 Erfolg; 1 unvollständiger Arztbericht; 2 Eingabe-/Verarbeitungsfehler; 130 Abbruch. Validatoren können erfolgreich `valid: false` ausgeben: Überprüfen Sie den Bericht, statt anzunehmen, dass Exit 0 eine gültige Quelle bedeutet. Typ-/Importprüfung kann ein vollständiges Projekt erfordern. Python Syntaxprüfung führt die Eingabe nie aus.

Englisch ist die Standardeinstellung. Zukünftige CLI-Übersetzungen nutzen gettext-Domain `onekit` unter `onekit/locales`; IDs, Befehlsnamen und JSON-Schlüssel bleiben sprachunabhängig.

Notebook-Zusammenführung akzeptiert `merge` mit `from` (`left` oder `right`) und dem nullbasierten geänderten Zelle-`block`-Index zusammen mit `mode`. Es gibt das aktualisierte Ziel-Notebook aus und bewahrt ausgeschlossene Zellen sowie Notebook-Metadaten. Einheitliche Patches beschreiben die verglichene Darstellung und sind im Allgemeinen keine Patches für rohes PDF, Word oder Notebook-Container.

<a id="image-effects"></a>
## Image effects

`onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output` kombiniert Unschärfe, Pixelierung, Box-Blur, feste Abdeckung und Graustufen in einem Tool. Verwenden Sie `scope: "selected"` mit normalisierten rechteckigen `regions`, um bestimmte Bereiche anzusprechen. Siehe den [-Bild-Effekt-Guide](image-effects.md) für alle Optionen und Limits.

<a id="portable-workflows"></a>
## Portable workflows

`onekit workflow export SOURCE -o workflow.1kit` überprüft ein Legacy-Schritte-Array oder ein Workflow-Dokument und speichert ein portables Dokument. `onekit workflow import workflow.1kit -o saved.1kit` überprüft und speichert ein importiertes Dokument. Beide Befehle lassen Passwörter weg und lehnen vorhandene Ausgabepfade ab, es sei denn, `--force` wird bereitgestellt. Keiner der Befehle verarbeitet Dateien.

Führen Sie einen importierten Workflow mit `onekit pipeline --steps saved.1kit INPUTS -o OUTPUT` aus. Die .1kit-Erweiterung erkennt OneKit-Dokumente; alte .json- und .onekit.json-Workflow-Dateien und Schrittabfolgen bleiben unterstützt. Workflow-Dokumente sind UTF-8 JSON, maximal 1 MiB, mit folgender Struktur:

```json
{
  "format": "onekit-workflow",
  "version": 1,
  "steps": [{"tool": "dev-format-json", "options": {}}]
}
```

<a id="automatic-setup"></a>
## Automatic setup

`onekit run`, `onekit download` und `onekit pipeline` installieren fehlende Python-Pakete und native Engines, bevor sie mit der Verarbeitung beginnen. Abhängigkeiten werden im Benutzer-Cache OneKit gespeichert, ohne die Systeminstallation Python zu verändern. Whisper- und U2Net-Modelle werden beim ersten Gebrauch automatisch heruntergeladen und für spätere Ausführungen zwischengespeichert. OCR-Sprachdaten werden für die angeforderten Sprachen abgerufen.

Der erste Durchlauf benötigt eine Internetverbindung und genügend Speicherplatz. Native Engines verwenden conda-forge über eine private Micromamba-Installation oder den System-Paketmanager für Engines, die dort nicht verfügbar sind; die Verfügbarkeit hängt vom Betriebssystem und der Architektur ab. Setup-Fehler stoppen die Verarbeitung mit einer Fehlermeldung und können wiederholt werden. `onekit doctor` überprüft die Bereitschaft, ohne etwas zu installieren. `ONEKIT_CACHE` ändert den Speicherort des Setup-Caches. `ONEKIT_ALLOW_COPYLEFT=0` blockiert weiterhin eingeschränkte Engines.

<a id="local-license-and-copyright-estimates"></a>
## Local license and copyright estimates

Die `licenses`-Gruppe stellt `license-pdf`, `license-word`, `license-powerpoint`, `license-excel`, `license-video`, `license-audio`, `license-image`, `license-font`, `license-epub`, `license-code` und `license-dataset` bereit.

```sh
onekit run license-image photo.jpg -o report.json
onekit run license-pdf --url https://example.org/document.pdf -o report.json
onekit run license-code project.zip -o report.json
onekit run license-code ./project -o report.json
onekit run license-code --url https://github.com/owner/repository --options '{"ref":"main"}' -o report.json
onekit run license-code --url https://gitlab.com/group/project -o report.json
onekit run license-dataset data.csv LICENSE metadata.json -o report.json
```

**Jedes Ergebnis ist eine unbestätigte Schätzung und muss manuell überprüft werden.** Es listet die angegebenen Metadaten, Urheberrechtshinweise, Namen der Ersteller, SPDX-Syntax und vorläufige Lizenz-Textübereinstimmungen mit ihren Positionen auf. Es bestätigt niemals Eigentum oder erteilt die Erlaubnis, ein Werk zu verwenden. Fehlende Angaben bedeuten niemals gemeinfrei oder frei verwendbar. Namen der Ersteller beweisen nicht das Urheberrecht. Prüfen Sie die ursprüngliche Quelle, die vollständigen Bedingungen und die beabsichtigte Nutzung; Projektabhängigkeiten und Assets können separate Lizenzen haben. Offizielle Referenzen erklären Standards, nicht die Authentizität oder Anwendbarkeit der Angaben in einem hochgeladenen Werk.

<a id="downloads-image-transforms-and-url-inspection"></a>
## Downloads, image transforms and URL inspection

```sh
onekit run audio-download --url 'https://example.org/audio.flac' -o downloads/
onekit run audio-download --url 'https://example.org/audio.wav' --options '{"format":"mp3","quality":"320"}' -o downloads/
onekit run image-download --url 'https://example.org/photo.jpg' -o downloads/
onekit run image-rotate-flip photo.png --options '{"angle":"90","flip":"horizontal"}' -o rotated.png
onekit run url-inspect --url 'https://example.org/path?x=1#section' -o report.json
```

Das Herunterladen einer Bild- oder Audiodatei gewährt keine Rechte zur Weiterverbreitung oder Wiederverwendung.

Die Bilddrehung wendet zuerst die EXIF-Ausrichtung an, dreht dann im Uhrzeigersinn um 0/90/180/270 Grad und spiegelt anschließend horizontal, vertikal oder beides im gedrehten Koordinatensystem. Es exportiert ein PNG, wobei die dekodierten RGBA-Pixel und die Transparenz ohne Metadaten erhalten bleiben; animierte und mehrseitige Bilder werden abgelehnt. Das Limit beträgt 40 Millionen Pixel.

<a id="remove-text-formatting"></a>
### Remove text formatting

`onekit run text-strip-formatting document.docx -o plain.txt` exportiert Word-Text als UTF-8 TXT. TXT, HTML und Markdown-Dateien werden ebenfalls unterstützt, bis zu 8 MiB. Verwenden Sie `--options '{"input_format":"html"}'`, um HTML in einer TXT-Datei zu interpretieren. Es wird keine OCR durchgeführt.

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

Hilf, OneKits offene Revolution zu entwickeln: alltägliche Werkzeuge für alle, von praktischen Aufgaben bis hin zu Workflows, die von lokalen AI-Agenten ausgeführt werden. Tragen Sie dazu bei, Werkzeuge effizienter und effektiver zu machen: Geschwindigkeit und Speichernutzung verbessern, fehlerhafte Ergebnisse korrigieren, Regressionsbeispiele hinzufügen oder Dokumentation und Agenten-Workflows klarer gestalten.

Der Kern ist Open Source (PolyForm Shield 1.0.0). Lesen Sie die [-Beitragsanleitung](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) und finden Sie eine Aufgabe in [GitHub-Issues](https://github.com/mattiapiazzalunga/onekit/issues), oder schlage eine Verbesserung im [-Anfrageboard](https://onekit.org/requests/) vor.

Fragen zum Open Source (PolyForm Shield 1.0.0) Kern und zu Beiträgen: [developers@onekit.org](mailto:developers@onekit.org). Allgemeiner Support: [support@onekit.org](mailto:support@onekit.org).
