<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="external-engines-and-licenses"></a>
# Externe Engines und Lizenzen

Der Besitzer hat separat installierte Open-Source-Engines genehmigt. Sie sind nicht im Python wheel, im Quell-Download oder im initialen Docker-Image enthalten. `onekit doctor` meldet Anforderungen. `ONEKIT_ALLOW_COPYLEFT=0` deaktiviert ausdrücklich die aufgeführten Copyleft-Adapter. Halten Sie die Upstream-Tools auf dem neuesten Stand; lokale Subprozesse sind kein vollständiger Sandbox-Schutz für feindliche Dokumente.

| Engine | Befehl | Verwenden Sie / Lizenzüberlegungen |
| --- | --- | --- |
| LibreOffice | `soffice` / `libreoffice` | Office → PDF/Bilder; MPL und Hinweise von Drittanbietern. |
| Pandoc | `pandoc` | Erweiterte Markup-Konvertierung; GPL. |
| TeX Live/pdfTeX | `pdflatex` | LaTeX/Pandoc PDF; Engine, Makros und Schriftarten haben separate Lizenzen. |
| FFmpeg | `ffmpeg` | Medien; LGPL oder GPL, je nach Build und Codecs. |
| veraPDF | `verapdf` | Optionale unabhängige Überprüfung von Archivausgaben; Anforderungen GPL/MPL und Java im Vorfeld. |
| ExifTool | `exiftool` | Metadaten in unterstützten Dateitypen; Upstream-Perl-Lizenzierung. |
| Tesseract | `tesseract` | OCR; Apache-Engine und separat lizenzierte Sprachdaten. |

Wenn Sie diese Programme verteilen, auch innerhalb von Docker, bewahren Sie deren Lizenzen/Hinweise auf und stellen Sie die erforderlichen entsprechenden Quell-/Build-Materialien bereit. Bewerten Sie AGPL-Netzwerkintegrationen separat. Kommerzielle Nutzung und Quell-/Weitergabeverpflichtungen sind unterschiedliche Fragen. Getrennte Prozesse heben nicht automatisch alle Verpflichtungen auf. Lesen Sie das autoritative [FFmpeg](https://ffmpeg.org/legal.html), [LibreOffice](https://www.libreoffice.org/licenses/), [Ghostscript](https://www.ghostscript.com/licensing/) und [MPL](https://www.mozilla.org/en-US/MPL/2.0/FAQ/)-Material, bevor Sie eine gebündelte Distribution erstellen.

Die Wiedergabetreue von Office-Dokumenten hängt von Schriftarten und Ressourcen ab. PDF zu Word exportiert extrahierten Text; PDF zu PowerPoint erzeugt Bildfolien. Die PDF-Reparatur ist nicht garantiert; die Komprimierung ist verlustfrei. Die [PDF/A-Konvertierung und -Validierung](pdfa.md) verwendet separate MPL-Bibliotheken über den gemeinsamen Python-Adapter mit mitgelieferten, lizenzierten ICC-Profilen. Ghostscript ist nicht erforderlich. Eine unabhängige Prüfung der Standards bleibt empfohlen. Die OCR-Genauigkeit hängt von der Scanqualität und den Sprachpaketen ab.

<a id="developer-tools"></a>
## Developer tools

Installieren Sie Node.js 24+ und führen Sie `onekit engines install` für gesperrte Prettier/Plugins, esbuild, HTML Minifier, SVGO und GraphQL.js aus. Sie werden im Benutzer-OneKit-Cache installiert, nicht global. `ONEKIT_NODE_ENGINE_PATH` wählt eine Alternative. Führen Sie den Installer nach einem genehmigten Engine-Update erneut aus. Die Parser-Gruppe umfasst JS/TS/JSX/TSX, Markup, Stylesheets, Markdown/MDX, GraphQL, Vue, Svelte, Astro, Solidity und PHP.

Installieren Sie upstream Compiler/Launcher für Ihr Betriebssystem und fügen Sie die dokumentierten Befehle zum PATH hinzu. Einige isolierte Dateien benötigen ihre Projektabhängigkeiten oder den genauen Java Klassennamen. Formatierungs-/Parser-Validierung beweist nicht die projektweite Typkorrektheit.

Auf Windows bevorzugen die Adapter Bash/Shell einen tatsächlichen Interpreter im PATH und erkennen dann Git für Windows in seinen Standard-System-/Benutzer-Installationsverzeichnissen. Der System32 WSL-Launcher wird nicht als kompatibler lokaler Parser behandelt. Die PowerShell-Syntaxprüfung erfordert `pwsh`; das Formatieren erfordert zusätzlich PSScriptAnalyzer (`Install-Module PSScriptAnalyzer -Scope CurrentUser`). `onekit doctor dev-format-powershell` prüft dieses Modul separat und meldet den Einrichtungbefehl. Diese Programme/Module werden beim Verarbeiten von Dateien nicht heruntergeladen.

<a id="platform-qualifications"></a>
## Platform qualifications

Die Lizenzprüfungen in der CI installieren und untersuchen auch das separate Signatur-Extra (`scripts/check_licenses.py --include-signing`). MIT-0 wird als freizügige Lizenz anerkannt ([SPDX-Text](https://spdx.org/licenses/MIT-0.html)). Die Mozilla-Vertrauensspeicherdaten aus der festgeschriebenen `certifi`-Version 2026.7.22 bilden eine ausdrückliche, versionsgebundene MPL-2.0-Ausnahme; bei der Weiterverteilung müssen die ursprüngliche Lizenz und die Hinweise unverändert erhalten bleiben ([ursprünglicher Hinweis](https://github.com/certifi/python-certifi/blob/master/LICENSE)). Neue Versionen erfordern eine erneute Prüfung. Diese Ausnahme lässt nicht allgemein andere MPL-Pakete zu und ändert nicht die PolyForm-Shield-1.0.0-Lizenz von OneKit.

Der universelle Python-Core unterstützt Linux, Windows und macOS einschließlich ARM64. Native Extras und externe Engines bestimmen zusätzliche Anforderungen. CI gibt x64/ARM-Läufer auf alle drei Betriebssystemfamilien an. Auf Windows ARM könnten Brotli/WOFF2 und der separate Signatur-Kryptografie-Stack native Build-Tools oder x64 Python unter Emulation erfordern. WOFF/TTF/OTF benötigen den WOFF2-Encoder nicht. Das `all`-Extra schließt separate Signaturen aus. Melden Sie diese optionalen Einschränkungen, statt zu behaupten, dass ein natives wheel existiert, wenn es das nicht tut.
