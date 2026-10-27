<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="external-engines-and-licenses"></a>
# Motori esterni e licenze

Il proprietario ha approvato motori open-source installati separatamente. Non sono inclusi nel wheel Python, nel download del codice sorgente o nell'immagine Docker iniziale. `onekit doctor` riporta i requisiti. `ONEKIT_ALLOW_COPYLEFT=0` disabilita esplicitamente gli adattatori copyleft elencati. Mantieni aggiornati gli strumenti upstream; i processi locali non sono una sandbox completa per documenti ostili.

| Motore | Comando | Usa / considerazioni sulla licenza |
| --- | --- | --- |
| LibreOffice | `soffice` / `libreoffice` | Office → PDF/immagini; MPL e avvisi di terze parti. |
| Pandoc | `pandoc` | Conversione avanzata del markup; GPL. |
| TeX Live/pdfTeX | `pdflatex` | LaTeX/Pandoc PDF; motore, macro e font hanno licenze separate. |
| FFmpeg | `ffmpeg` | Media; LGPL o GPL a seconda della build e dei codec. |
| veraPDF | `verapdf` | Verifica indipendente opzionale dei risultati archiviati; requisiti a monte GPL/MPL e Java. |
| ExifTool | `exiftool` | Metadati nei tipi di file supportati; licenza Perl upstream. |
| Tesseract | `tesseract` | OCR; motore Apache e dati linguistici con licenza separata. |

Se distribuisci questi programmi, anche dentro Docker, conserva le loro licenze/avvisi e fornisci i materiali corrispondenti richiesti per il codice sorgente/la compilazione. Valuta separatamente le integrazioni di rete AGPL. L’uso commerciale e gli obblighi di sorgente/ridistribuzione sono questioni diverse. Processi separati non eliminano universalmente gli obblighi. Leggi il materiale autorevole [FFmpeg](https://ffmpeg.org/legal.html), [LibreOffice](https://www.libreoffice.org/licenses/), [Ghostscript](https://www.ghostscript.com/licensing/) e [MPL](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) prima di creare una distribuzione pacchettizzata.

La fedeltà dei documenti Office dipende da font e risorse. PDF→Word esporta il testo estratto; PDF→PowerPoint crea diapositive contenenti immagini. La riparazione dei PDF non è garantita; la compressione è senza perdita. La [conversione e convalida PDF/A](pdfa.md) usa librerie MPL separate tramite l’adattatore Python condiviso, con profili ICC inclusi e muniti di licenza. Ghostscript non è necessario. Resta consigliata una convalida indipendente degli standard. L’accuratezza OCR dipende dalla qualità delle scansioni e dai pacchetti linguistici.

<a id="developer-tools"></a>
## Developer tools

Installa Node.js 24+ e esegui `onekit engines install` per Prettier/plugin con versioni fissate, esbuild, HTML minifier, SVGO e GraphQL.js. Si installano nella cache dell'utente OneKit, non globalmente. `ONEKIT_NODE_ENGINE_PATH` seleziona un'alternativa. Riesegui l'installer dopo un aggiornamento del motore approvato. Il gruppo di parser copre JS/TS/JSX/TSX, markup, fogli di stile, Markdown/MDX, GraphQL, Vue, Svelte, Astro, Solidity e PHP.

Installa compilatori/lanciatori upstream per il tuo OS e aggiungi i comandi documentati al PATH. Alcuni file isolati necessitano delle loro dipendenze di progetto o del nome di file esatto della classe Java. La validazione del formato/parser non garantisce la correttezza dei tipi a livello di progetto.

Su Windows, gli adattatori Bash/Shell preferiscono un interprete reale presente nel PATH e poi rilevano Git per Windows nelle directory di installazione standard di sistema/utente. Il launcher WSL di System32 non è considerato un parser locale compatibile. La validazione della sintassi PowerShell richiede `pwsh`; la formattazione richiede inoltre PSScriptAnalyzer (`Install-Module PSScriptAnalyzer -Scope CurrentUser`). `onekit doctor dev-format-powershell` controlla quel modulo separatamente e segnala il comando di configurazione. Questi programmi/moduli non vengono scaricati durante l'elaborazione dei file.

<a id="platform-qualifications"></a>
## Platform qualifications

I controlli delle licenze nella CI installano ed esaminano anche l’extra separato per la firma (`scripts/check_licenses.py --include-signing`). MIT-0 è riconosciuta come licenza permissiva ([testo SPDX](https://spdx.org/licenses/MIT-0.html)). I dati dell’archivio Mozilla delle autorità attendibili inclusi nella versione fissata di `certifi`, 2026.7.22, costituiscono un’eccezione esplicita per quella specifica versione alla regola su MPL-2.0; quando li ridistribuisci, conserva senza modifiche la licenza e le informative originali ([informativa originale](https://github.com/certifi/python-certifi/blob/master/LICENSE)). Le nuove versioni richiedono un’altra revisione. Questa eccezione non ammette in generale altri pacchetti MPL e non modifica la licenza PolyForm-Shield-1.0.0 di OneKit.

Il core universale Python supporta Linux, Windows e macOS incluso ARM64. Extra nativi e motori esterni determinano requisiti aggiuntivi. CI dichiara i runner x64/ARM su tutte e tre le famiglie di OS. Su Windows ARM, Brotli/WOFF2 e lo stack separato di crittografia per la firma potrebbero richiedere strumenti di build nativi o x64 Python in emulazione. WOFF/TTF/OTF non richiedono il codificatore WOFF2. L'extra `all` esclude la firma separata. Riporta questi vincoli opzionali invece di affermare che esiste un wheel nativo quando non è così.
