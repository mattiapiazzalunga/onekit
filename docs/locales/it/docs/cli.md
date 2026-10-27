<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-reference"></a>
# Riferimento della CLI

Usa `onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","opacity":0.25}'` per aggiungere un watermark testuale PDF. Vedi la [guida alle filigrane](watermark.md) per posizione, rotazione, intervalli di pagine e layout ripetuti.

L’oscuramento permanente è disponibile tramite `onekit run pdf-redact` e `onekit run image-redact`, specificando le aree da oscurare in `regions`. La [guida all’oscuramento](redaction.md) descrive coordinate, rasterizzazione e garanzie di riservatezza dei file esportati.

Usa `onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"[0-9]+","flags":"g"}'` per testare espressioni regolari JavaScript. Richiede Node.js; vedi la [guida al tester di espressioni regolari](regex.md) per catture, sostituzioni e limiti di esecuzione.

I codici a barre standard sono disponibili tramite `onekit run text-to-barcode`, `onekit run scan-barcode` e `onekit run barcode-to-text`. Installa l'extra `barcode` o `qrcode`. Vedi [le impostazioni dei codici a barre e gli standard supportati](qrcode.md#standard-linear-barcodes).

`onekit --version` riporta la versione core. `python -m onekit` invoca lo stesso CLI.

| Comando | Comportamento |
| --- | --- |
| `onekit list [--group GROUP] [--json]` | Scopri strumenti, contratti, disponibilità e fedeltà. |
| `onekit doctor [TOOL_ID] [--json]` | Controlla i pacchetti, i motori e i blocchi di policy di licenza Python. |
| `onekit run TOOL_ID INPUTS -o OUTPUT` | Elabora file; la crittografia accetta anche cartelle. |
| `onekit pipeline --steps WORKFLOW INPUTS -o OUTPUT` | Esegue da 1 a 16 passaggi ordinati, definiti in un file JSON. |
| `onekit engines install [--directory DIRECTORY]` | Installa i motori per sviluppatori Node bloccati; richiede Node/npm. |
| `onekit download URL -o OUTPUT [--quality best\|720\|1080] [--force]` | Scarica un singolo video tramite yt-dlp; richiede internet e FFmpeg. |

`run` accetta `--options` con un oggetto JSON, `--ask-password` e `--force`. Le pipeline supportano anche il prompt della password e il flag di sovrascrittura. Usa un nome file per un'uscita singola o una directory per più uscite. Le destinazioni senza estensione sono directory. I nomi di uscita in conflitto vengono rifiutati.

<a id="local-agents-and-automation"></a>
## Local agents and automation

**La tua CLI. La tua CLI per gli agenti.** OneKit è utile sia al tuo terminale sia come toolkit per l'elaborazione di file per agenti locali AI che possono eseguire comandi shell o avviare sottoprocessi. Un agente può scoprire i contratti degli strumenti, controllare i requisiti, eseguire un'operazione selezionata e ispezionare i file di output.

```sh
onekit list --json
onekit doctor pdf-merge --json
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit pipeline --steps workflow.1kit input.pdf -o output/
```

`list --json` espone gli ID degli strumenti, gli input accettati, i formati di output, le opzioni, i limiti e le note sulla fedeltà. `doctor TOOL_ID --json` segnala lo stato di prontezza, le dipendenze mancanti e i blocchi della politica di licenza. Analizza queste risposte JSON piuttosto che gli elenchi leggibili dall’uomo. `run` e `pipeline` scrivono i loro risultati nella destinazione fornita con `-o`; non hanno un flag di risposta generale `--json`. Alcuni strumenti producono file di rapporti JSON.

Per un agente locale, scopri prima lo strumento, controlla i suoi requisiti, poi chiamalo con percorsi espliciti e un oggetto JSON in `--options` dove necessario. Passa gli argomenti di subprocess come lista per preservare percorsi e JSON senza dover gestire le virgolette della shell. Controlla lo stato di uscita prima di consumare gli output:

| Codice di uscita | Significato |
| --- | --- |
| `0` | Comando completato con successo. |
| `1` | `doctor` ha trovato requisiti mancanti o un blocco di politica; controlla il rapporto. |
| `2` | Argomenti non validi o errore di elaborazione/input/output; leggere stderr. |
| `130` | Comando annullato con un’interruzione da tastiera. |

Scegli un percorso di output nuovo per ogni lavoro; gli output esistenti vengono preservati a meno che non venga fornito `--force`. `--ask-password` richiede un terminale interattivo. Prepara le dipendenze e le cache dei modelli prima delle esecuzioni non assistite: componenti mancanti possono attivare configurazioni automatiche e download di rete, e alcuni installatori nativi richiedono interazione o privilegi elevati. Gli strumenti di rete contattano anche le fonti richieste.

L'elaborazione dei file avviene sul tuo computer. Se l'agente utilizza un modello remoto, la gestione dei contenuti del file e dei risultati dei comandi da parte dell'agente determina cosa viene inviato a quel provider. La stessa licenza [PolyForm Shield](licenses.md) si applica all'uso guidato dall'agente.

<a id="tool-options"></a>
## Tool options

Generazione QR, configurazione vCard/Wi-Fi, scansione delle immagini e decodifica inversa sono documentati nella guida al codice [QR](qrcode.md). Installa il componente aggiuntivo `qrcode`, quindi utilizza `onekit run text-to-qrcode input.txt -o code.png` o `onekit run scan-qrcode photo.jpg -o decoded.json`.

Le pagine sono numerate a partire da 1. `pages` accetta numeri e intervalli crescenti, come `1,3-5`. Nelle operazioni di riordino ed estrazione vengono conservati l’ordine e le ripetizioni intenzionali. La rotazione accetta multipli di 90 e si applica per impostazione predefinita a tutte le pagine. La modifica dei PDF aggiunge `text` a `page` alle coordinate `x`/`y`, espresse in punti PDF con origine nell’angolo inferiore sinistro; non ridistribuisce il contenuto esistente. Per firmare servono il percorso di un `certificate` PKCS#12 e la relativa `password`.

L'immagine `format` supporta PNG, JPEG, WebP, TIFF, BMP, ICO, GIF e PDF se applicabile. `quality` è 1–100. `box` è `[left, top, right, bottom]` in pixel. Le animazioni/meta-dati possono essere rimossi; la trasparenza viene appiattita a bianco per JPEG/PDF. La compressione può aumentare un file già ottimizzato.

L’opzione `sheet` seleziona un foglio di lavoro; per impostazione predefinita viene usato quello attivo. La lettura Excel utilizza i valori delle formule memorizzate nella cache. JSON-to-Excel si aspetta un array di oggetti. CSV `delimiter` predefinito alla virgola. Le stringhe XLSX simili a formule restano testo; importa CSV non attendibili come testo nelle applicazioni per fogli di calcolo.

La conversione di codifica accetta `source_encoding` e `encoding`. Altri strumenti di testo usano UTF-8.. Per PDF, JPEG e PNG, `metadata` accetta i campi di testo descrittivo `Title`, `Author`, `Subject`, `Keywords` e `Comment`. I campi non specificati vengono mantenuti; una stringa vuota cancella il valore di un campo. L'aiutante Python `onekit.tools.file_metadata.read_metadata(artifact)` legge quei campi senza modificare l'artefatto, inclusi i testi supportati EXIF, PNG e i valori XMP. Altri formati di metadata usano coppie opzionali tag/valore ExifTool, all'interno della loro copertura del formato. Le firme dell'ispettore non identificano tutti i tipi di file proprietari.

Il confronto tra notebook `mode` è `both`, `markdown` o `code`. La modalità LaTeX è `all` o euristica `text`. Il confronto PDF/Word estrae il testo. Il diff JSON contiene lati normalizzati, blocchi modificati e una patch unificata, comprese le differenze di newline finali. OCR `language` utilizza codici Tesseract installati e `dpi` è 36–300. La conversione PDF/A richiede un `icc_profile` con licenza; valida l’output di archiviazione in modo indipendente.

Le opzioni dei media includono `format`, `codec` e `bitrate`, a seconda della build FFmpeg. I font supportano `ttf`, `otf`, `woff` e `woff2`, mantenendo la tecnologia dei contorni. Gli archivi supportano le combinazioni ZIP e TAR/gzip/bzip2/xz.

<a id="limits-and-errors"></a>
## Limits and errors

Vedi [convalida dell’input](input-validation.md) per i tipi imposti per strumento, limiti di byte/conteggio, controlli di firma/contenitore e regole di espansione degli archivi. Questi valgono per le chiamate dirette Python API e ogni passaggio della pipeline così come per CLI. Esegui `onekit list --json` per contratti leggibili dalla macchina esatti.

Input del core: 256 file e 128 MiB. Pipeline: 16 passaggi. Immagini e pagine renderizzate: 40 milioni di pixel. Confronti: 10.000 righe e 2 milioni di caratteri. Decompressione degli archivi: 128 MiB, 4096 elementi e controlli del rapporto di espansione. I motori esterni hanno limiti di tempo. Input validi ma di grandi dimensioni possono superare questi limiti intenzionali.

Codici di uscita: 0 successo; 1 rapporto diagnostico di doctor incompleto; 2 errore di input/elaborazione; 130 annullamento. I validatori possono emettere con successo `valid: false`: ispeziona il rapporto invece di presumere che il codice di uscita 0 significhi che la fonte è valida. Il controllo di tipo/importazione può richiedere un progetto completo. La convalida della sintassi Python non esegue mai l'input.

L'inglese è il default. Le future traduzioni CLI useranno il dominio gettext `onekit` sotto `onekit/locales`; ID, nomi dei comandi e chiavi JSON rimangono indipendenti dalla lingua.

La fusione dei notebook accetta `merge` con `from` (`left` o `right`) e l'indice della cella modificata basato su zero `block`, insieme a `mode`. Emette il notebook di destinazione aggiornato e conserva le celle escluse e i metadati del notebook. Le patch unificate descrivono la rappresentazione confrontata e in generale non sono patch per PDF, Word o contenitori di notebook grezzi.

<a id="image-effects"></a>
## Image effects

`onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output` combina sfocatura, pixelazione, sfocatura a blocchi, copertura solida e scala di grigi in un unico strumento. Usa `scope: "selected"` con rettangoli a coordinate normalizzate in `regions` per elaborare aree specifiche. Vedi la guida [ sugli effetti immagine](image-effects.md) per tutte le opzioni e i limiti.

<a id="portable-workflows"></a>
## Portable workflows

`onekit workflow export SOURCE -o workflow.1kit` convalida un array di passaggi legacy o un documento di workflow e salva un documento portatile. `onekit workflow import workflow.1kit -o saved.1kit` convalida e salva un documento importato. Entrambi i comandi omettono le password e rifiutano percorsi di output esistenti a meno che non venga fornito `--force`. Nessuno dei due comandi elabora file.

Esegui un workflow importato con `onekit pipeline --steps saved.1kit INPUTS -o OUTPUT`. L'estensione .1kit identifica i documenti OneKit; i file e le array di passaggi legacy .json e .onekit.json continuano a essere supportati. I documenti workflow sono UTF-8 JSON, al massimo 1 MiB, con la seguente struttura:

```json
{
  "format": "onekit-workflow",
  "version": 1,
  "steps": [{"tool": "dev-format-json", "options": {}}]
}
```

<a id="automatic-setup"></a>
## Automatic setup

`onekit run`, `onekit download` e `onekit pipeline` installano i pacchetti mancanti Python e i motori nativi prima di procedere. Le dipendenze vengono conservate nella cache utente OneKit, senza modificare l’installazione di sistema Python. I modelli Whisper e U2Net si scaricano automaticamente al primo utilizzo e vengono memorizzati nella cache per usi successivi. I dati linguistici OCR vengono recuperati per le lingue richieste.

La prima esecuzione richiede una connessione a Internet e spazio sufficiente sul disco. I motori nativi usano conda-forge tramite un’installazione privata di micromamba, oppure il gestore di pacchetti del sistema per i motori non disponibili lì; la disponibilità dipende dal sistema operativo e dall’architettura. I fallimenti nella configurazione interrompono l’elaborazione con un errore e possono essere riprovati. `onekit doctor` verifica la prontezza senza installare nulla. `ONEKIT_CACHE` cambia la posizione della cache di configurazione. `ONEKIT_ALLOW_COPYLEFT=0` continua a bloccare i motori con restrizioni.

<a id="local-license-and-copyright-estimates"></a>
## Local license and copyright estimates

Il gruppo `licenses` fornisce `license-pdf`, `license-word`, `license-powerpoint`, `license-excel`, `license-video`, `license-audio`, `license-image`, `license-font`, `license-epub`, `license-code` e `license-dataset`.

```sh
onekit run license-image photo.jpg -o report.json
onekit run license-pdf --url https://example.org/document.pdf -o report.json
onekit run license-code project.zip -o report.json
onekit run license-code ./project -o report.json
onekit run license-code --url https://github.com/owner/repository --options '{"ref":"main"}' -o report.json
onekit run license-code --url https://gitlab.com/group/project -o report.json
onekit run license-dataset data.csv LICENSE metadata.json -o report.json
```

**Ogni risultato è una stima non verificata che richiede una verifica manuale.** Elenca i metadati dichiarati, gli avvisi di copyright, i nomi dei creatori, la sintassi SPDX e corrispondenze provvisorie di testo di licenza con le loro posizioni. Non certifica mai la proprietà né concede il permesso di usare un’opera. La mancanza di dichiarazioni non significa mai dominio pubblico o uso libero. I nomi dei creatori non dimostrano la proprietà del copyright. Controlla la fonte originale, i termini completi e l’uso previsto; le dipendenze del progetto e le risorse possono avere licenze separate. I riferimenti ufficiali spiegano gli standard, non l’autenticità o l’applicabilità delle dichiarazioni in un’opera caricata.

<a id="downloads-image-transforms-and-url-inspection"></a>
## Downloads, image transforms and URL inspection

```sh
onekit run audio-download --url 'https://example.org/audio.flac' -o downloads/
onekit run audio-download --url 'https://example.org/audio.wav' --options '{"format":"mp3","quality":"320"}' -o downloads/
onekit run image-download --url 'https://example.org/photo.jpg' -o downloads/
onekit run image-rotate-flip photo.png --options '{"angle":"90","flip":"horizontal"}' -o rotated.png
onekit run url-inspect --url 'https://example.org/path?x=1#section' -o report.json
```

Scaricare un file immagine o audio non concede diritti di ridistribuzione o riutilizzo.

La rotazione dell'immagine applica prima l'orientamento EXIF, ruota in senso orario di 0/90/180/270 gradi, poi riflette orizzontalmente, verticalmente o entrambe nel sistema di coordinate ruotato. Esporta un PNG preservando i pixel RGBA decodificati e la trasparenza senza metadata; le immagini animate e multipagina vengono rifiutate. Il limite è di 40 milioni di pixel.

<a id="remove-text-formatting"></a>
### Remove text formatting

`onekit run text-strip-formatting document.docx -o plain.txt` esporta il testo del corpo Word come UTF-8 TXT. Anche i file TXT, HTML e Markdown sono supportati, fino a 8 MiB. Usa `--options '{"input_format":"html"}'` per interpretare HTML memorizzati in un file TXT. Nessuna OCR viene eseguita.

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

Aiuta a costruire la rivoluzione aperta di OneKit: strumenti quotidiani per tutti, dai compiti pratici ai flussi di lavoro gestiti dagli agenti locali AI. Contribuisci a rendere gli strumenti più efficienti ed efficaci: migliora velocità e uso della memoria, correggi risultati sbagliati, aggiungi esempi di regressione o chiarisci la documentazione e i flussi di lavoro degli agenti.

Il core è Open Source (PolyForm Shield 1.0.0). Leggi la [guida per contribuire](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) e trova un compito in [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues), o suggerisci un miglioramento sulla [bacheca delle richieste](https://onekit.org/requests/).

Domande sul core Open Source (PolyForm Shield 1.0.0) e contributi: [developers@onekit.org](mailto:developers@onekit.org). Supporto generale: [support@onekit.org](mailto:support@onekit.org).
