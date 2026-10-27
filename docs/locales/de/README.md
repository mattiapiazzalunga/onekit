<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->

Sprachen: [English](../../../README.md) · [Italiano](../it/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Deutsch](README.md) · [Русский](../ru/README.md) · [中文](../zh/README.md).

<p align="center">
  <a href="https://onekit.org"><img src="https://raw.githubusercontent.com/mattiapiazzalunga/onekit/main/images/logo.png" alt="OneKit logo" width="112" height="112"></a>
</p>
<h1 align="center">OneKit</h1>
<p align="center">Ein Werkzeugkasten. Ihre Dateien bleiben Ihre Dateien.</p>
<p align="center"><a href="https://github.com/mattiapiazzalunga/onekit/stargazers"><img alt="GitHub-Sterne" src="https://img.shields.io/github/stars/mattiapiazzalunga/onekit"></a> <a href="https://pypi.org/project/onekit-tools/"><img alt="PyPI" src="https://img.shields.io/pypi/v/onekit-tools"></a> <img alt="PolyForm-Shield-1.0.0" src="https://img.shields.io/badge/license-PolyForm_Shield_1.0.0-blue"> <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue"></p>

Ein offline nutzbares Python-Toolkit mit 230 Werkzeugen für Konvertierungen, PDF-Dateien, Bilder, Archive, Schriftarten, Dateiprüfung, Verschlüsselung, Entwickleraufgaben, OCR und Vergleichen Sie. Verwenden Sie diese CLI oder die grafische Oberfläche unter **[onekit.org](https://onekit.org)**.

**Quellversion:** `0.6.3`. Stabile Downloads gibt es nur, nachdem der Release-Workflow abgeschlossen ist. Die Distribution ist `onekit-tools`; das separat gehörende PyPI-Projekt namens `onekit` ist nicht damit verwandt.

Der [Leitfaden zu Kontakten und Medien](docs/contact-media.md) behandelt die Erstellung eigenständiger vCards, das Auslesen von vCards aus QR-Codes, die Bildvergrößerung, das Entfernen von Hintergründen, die Komprimierung und Geschwindigkeitsanpassung von Videos und GIFs sowie die lokale Audiotranskription.

Lizenzprüfungen: Überprüfen Sie PDF, Word, PowerPoint, Excel, Video, Audio, Bilder, Schriftarten, EPUB, Code/Projekte und Datensätze aus Dateien oder öffentlichen URLs. Die Analyse bleibt lokal; Berichte sind **unverifizierte Schätzungen, keine Eigentumsnachweise oder Nutzungserlaubnis**. Siehe [Lizenzprüfungsnutzung und -grenzen](docs/cli.md#local-license-and-copyright-estimates).

**Ihre CLI. Ihre CLI für Agenten.** Nutzen Sie OneKit selbst oder lassen Sie einen lokalen AI-Agenten es über ein Terminal oder Unterprozess aufrufen. Entdecken Sie Tools und Anforderungen als JSON, geben Sie explizite Ein-/Ausgabepfade an und verwenden Sie gespeicherte `.1kit`-Workflows für wiederholbare Dateiaufgaben. Siehe [lokale Agenten und Automatisierung](docs/cli.md#local-agents-and-automation).

<a id="install"></a>
## Install

Python 3.11 oder neuer ist erforderlich. Das universelle Wheel-Paket unterstützt Windows, macOS und Linux auf x64/ARM64. Für optionale native Bibliotheken und externe Engines gelten zusätzliche Plattformanforderungen.

Nach der Veröffentlichung:

```sh
python -m pip install onekit-tools
python -m pip install "onekit-tools[pdf,images,documents]"
onekit list
onekit doctor
```

Aus einer lokalen Kopie des Quellcode-Repositorys:

```sh
python -m pip install -e ".[all,test]"
python -m onekit --help
python -m pytest -q
```

Die Basis CLI hat **keine Laufzeitabhängigkeiten**. Installieren Sie nur die Extras, die Sie benötigen. `all` beinhaltet die Standard-Python-Familien; Video-Downloads, Hintergrundentfernung, Transkription und kryptografische Signaturen verwenden die separaten Extras `video`, `background`, `transcription` und `signing`. Installieren Sie Native Engines separat. Für Node-basierte Entwickler-Tools installieren Sie Node.js, 24+ und führen Sie `onekit engines install` aus. Die CLI bereitet fehlende Abhängigkeiten und externe Engines bei der ersten Nutzung vor. Hintergrundentfernung und Transkription laden die Modellgewichte bei der ersten Nutzung herunter und verwenden danach den lokalen Cache erneut.

<a id="use"></a>
## Use

```sh
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit run pdf-extract-pages document.pdf --options '{"pages":"1,3-5"}' -o selected.pdf
onekit run image-convert image.png --options '{"format":"webp"}' -o image.webp
onekit run diff-notebook before.ipynb after.ipynb --options '{"mode":"code"}' -o changes.json
onekit run security-encrypt private-folder --ask-password -o private.zip
onekit run security-decrypt private.zip --ask-password -o restored
```

Optionen sind JSON-Objekte; übergeben Sie sie als ein einzelnes in Anführungszeichen gesetztes Shell-Argument. Verwenden Sie `--ask-password` für sensible Daten. Bestehende Ausgaben bleiben erhalten, außer Sie übergibst `--force`.

`onekit list --group pdf`, `onekit list --json` und `onekit doctor TOOL_ID` zeigen Verträge und Anforderungen an. Jedes Tool hat ein Verzeichnis unter [tools](../../../tools), das Metadaten und einen Verweis auf die gemeinsame Implementierung enthält. Siehe den [CLI-Guide](docs/cli.md) für Optionen und Grenzen.

<a id="toolkit"></a>
## Toolkit

| Familie | Funktionen |
| --- | --- |
| Konverter | Markdown, HTML, LaTeX, PDF, Word, PowerPoint, Bilder, Base64, Excel, CSV und JSON |
| PDF | Zusammenführen/teilen, Seitenauswahl/Reihenfolge/Entfernen, Kompression, Reparatur, [direkte Textbearbeitung](docs/pdf-editing.md), Textüberlagerungen, Rotation, digitale Signaturen, Verschlüsselung/Entsperren, [lokale PDF/A-Konvertierung und -Validierung](docs/pdfa.md) |
| Bilder | Extrahieren Sie eingebettete PDF Bilder, komprimieren Sie, schneiden Sie und ändern Sie das Format |
| Medien | Audio-/Video-Konvertierung über separat installierte FFmpeg |
| Archive / Schriften | ZIP/TAR Varianten; TTF/OTF Container und WOFF/WOFF2 |
| Inspektor / Sicherheit | Tippen von Signaturen, Struktur, Metadaten, Kodierung, Hashes, Textanzahlen; authentifizierte verschlüsselte Datei-/Ordnerarchive |
| Entwickler | Sprachspezifische Formatierung, Parser/Compiler-Validierung und ausgewählte Minifizierung |
| OCR | Gescannte Bilder/PDF in durchsuchbare PDF, Word, Markdown, LaTeX, HTML und JSON umwandeln |
| Diff | Text, Code, normalisiertes JSON, Notizbücher, LaTeX, PDF und Word-Text |

<a id="pipelines-and-development"></a>
## Pipelines and development

`onekit pipeline --steps workflow.1kit INPUTS -o OUTPUT` akzeptiert ein versioniertes `.1kit`-Workflow-Dokument. Jeder Schritt erhält die vorherigen Ausgaben. Schritte mit einem Eingang werden auf mehrere Ausgaben angewendet; Merge-Schritte erhalten die gesamte Sammlung. Nicht kompatible Typen stoppen die Verarbeitung.

Melden Sie Bugs und Vorschläge über [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues) oder das [ Website-Anfrageboard ](https://onekit.org/requests/). Mitwirkende können an beiden Orten Arbeiten finden.

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

Hilf, OneKits offene Revolution zu entwickeln: alltägliche Werkzeuge für alle, von praktischen Aufgaben bis hin zu Workflows, die von lokalen AI-Agenten ausgeführt werden. Tragen Sie dazu bei, Werkzeuge effizienter und effektiver zu machen: Geschwindigkeit und Speichernutzung verbessern, fehlerhafte Ergebnisse korrigieren, Regressionsbeispiele hinzufügen oder Dokumentation und Agenten-Workflows klarer gestalten.

Der Kern ist Open Source (PolyForm Shield 1.0.0). Lesen Sie die [-Beitragsanleitung](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) und finden Sie eine Aufgabe in [GitHub-Issues](https://github.com/mattiapiazzalunga/onekit/issues), oder schlage eine Verbesserung im [-Anfrageboard](https://onekit.org/requests/) vor.

<a id="license-and-creator"></a>
## License and creator

Erstellt von **[Mattia Piazzalunga](mailto:hello@mattiapiazzalunga.com)**. Copyright © 2026 Mattia Piazzalunga. Open Source (PolyForm Shield 1.0.0), lizenziert unter [PolyForm Shield 1.0.0](../../../LICENSE); siehe [NOTICE](../../../NOTICE), [AUTHORS.txt](../../../AUTHORS.txt) und [CONTRIBUTORS.txt](../../../CONTRIBUTORS.txt). Drittanbieter-Komponenten behalten ihre Lizenzen. Externe Engines sind separate Programme mit eigenen Verteilungspflichten.

Sie dürfen den Kern für zulässige Zwecke verwenden, ändern und weitergeben, einschließlich kommerzieller und interner Nutzung. Sie dürfen ihn jedoch nicht nutzen, um ein Produkt oder einen Service anzubieten, der mit der Software oder mit einem Produkt, das der Lizenzgeber oder seine Partner unter Verwendung der Software bereitstellen, konkurriert; auch kostenlose Angebote und verschiedene Plattformen oder Schnittstellen können konkurrieren. Beim Teilen von Kopien die Lizenztexte oder deren URL und alle erforderlichen Hinweiszeilen, die mit der Software geliefert werden, beifügen. Die vollständige Lizenz gilt, einschließlich ihrer Ausnahmen für neue und eingestellte Produkte, Patentbedingungen und Haftungsausschluss. Hier beschreibt „Open Source (PolyForm Shield 1.0.0)“ den veröffentlichten Quellcode unter diesen Bedingungen; die Wettbewerbseinschränkung bedeutet, dass dies Quellcode-verfügbare Software ist und kein uneingeschränktes Open Source gemäß der Open Source Definition. Siehe [den Lizenzleitfaden](docs/licenses.md).

Workflows exportieren und wieder importieren, ohne Eingabedateien zu verarbeiten:

```sh
onekit workflow export workflow.1kit -o exported-workflow.1kit
onekit workflow import workflow.1kit -o saved-workflow.1kit
onekit pipeline --steps saved-workflow.1kit input.json -o output.json
```

Standard-Barcodes sind in der Kategorie QR Codes & Barcodes und CLI verfügbar: `text-to-barcode`, `scan-barcode`, `barcode-to-text`. Code 128, Code 39, EAN-13, EAN-8, UPC-A, ITF und ISBN-13 unterstützen PNG/SVG, konfigurierbare Abmessungen und Prüfziffernprüfung. Installieren Sie `onekit-tools[barcode]` oder `onekit-tools[qrcode]`.

Das [dauerhafte Schwärzen von PDF-Dateien und Bildern](docs/redaction.md) ist mit `pdf-redact` und `image-redact` möglich. Ausgewählte Bereiche werden in neu kodierten Dateien durch undurchsichtige schwarze Pixel ersetzt. PDF-Dateien werden als reine Bilddokumente ohne ursprünglichen Text, Formulare, Kommentare, Anhänge oder Metadaten neu aufgebaut. Bilder werden zu undurchsichtigen PNG-Dateien ohne ursprüngliche Metadaten oder durch Transparenz verborgene Pixel. Die Originaldateien bleiben unverändert.

Fügen Sie konfigurierbare PDF-Textwasserzeichen mit `pdf-watermark` hinzu: Deckkraft, Farbe, Schriftarten, Seitenbereiche, visuelle Positionen, Drehung und wiederholte Raster. Text und Grafiken bleiben in der PDF. Siehe den [Wasserzeichenleitfaden](docs/watermark.md).

<a id="contacts"></a>
## Contacts

- Allgemeine Fragen und Support: [support@onekit.org](mailto:support@onekit.org).
- Fragen zum Open-Source-Kern (PolyForm Shield 1.0.0) und zu Beiträgen: [developers@onekit.org](mailto:developers@onekit.org).
- Datenschutz, DSGVO und Anfragen zu persönlichen Daten: [privacy@onekit.org](mailto:privacy@onekit.org).
- Rechtliche Fragen, Lizenzen und Genehmigungsanfragen: [legal@onekit.org](mailto:legal@onekit.org).
- Sicherheitslücken und Missbrauchsmeldungen: [security@onekit.org](mailto:security@onekit.org).
