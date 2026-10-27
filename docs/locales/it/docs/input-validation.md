<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="input-validation"></a>
# Validazione input

Ogni voce di catalogo dichiara formati accettati, conteggi dei file e limiti di byte. `onekit list --json` espone i valori. Sia l’esecuzione diretta che le pipeline rispettano i contratti.

<a id="limits"></a>
## Limits

I limiti complessivi per ciascun lotto sono 128 MiB e 256 file. Gli input di testo sono limitati a 8 MiB per file, le immagini raster a 64 MiB e i font a 16 MiB. Un confronto richiede esattamente due input. Le immagini raster decodificate sono limitate a 40 milioni di pixel complessivi fra tutti i fotogrammi. Il contenuto decompresso di archivi e file Office è limitato a 128 MiB e 4096 voci.

Gli strumenti a input singolo rifiutano file extra. La mappatura della pipeline applica deliberatamente un passaggio a input singolo a ciascun output precedente. Le collezioni di output vengono controllate gradualmente in modo che un passaggio mappato non possa accumulare dati restituiti illimitati. Conteggi dei file CLI, estensioni e dimensioni vengono controllati prima della lettura dei contenuti dei file, e i byte effettivamente letti sono limitati anche se un file cresce durante la lettura.

<a id="content-rules"></a>
## Content rules

- Gli strumenti PDF richiedono intestazioni PDF e una posizione coerente per il riferimento incrociato finale. `pdf-repair` permette deliberatamente riferimenti incrociati danneggiati dopo aver controllato l'intestazione PDF; il suo parser deve comunque recuperare un vero PDF. Le immagini rinominate in `.pdf` vengono rifiutate.
- Gli input raster vengono verificati con Pillow per formato reale, struttura e dimensioni decodificate. Un PNG rinominato in JPEG viene rifiutato. L'export Base64 decodifica anche l'immagine prima di accettarla.
- Word, Excel e PowerPoint richiedono parti di contenitore ZIP distinte e radici XML con namespace. Rinominare Excel in `.docx` non lo trasforma in Word. I conteggi delle directory e i budget di espansione vengono controllati prima di allocare la tabella voci ZIP o leggere le parti del documento.
- I font richiedono intestazioni SFNT/WOFF corrispondenti, intervalli di tabelle validi e limitati e dimensioni coerenti dei font compressi. L’espansione dichiarata WOFF non può superare il budget in byte del font.
- Gli input multimediali hanno estensioni audio/video esplicite e firme di contenitore. FFprobe verifica i tipi di stream prima della conversione FFmpeg; la conversione video richiede video, e la conversione audio richiede audio senza stream video ordinari. La cover art allegata è consentita. Entrambi gli eseguibili sono segnalati da `doctor`.
- Gli archivi rifiutano percorsi non sicuri/duplicati, symlink, voci crittografate ZIP, directory non valide, directory multi-volume/ZIP64 e flussi compressi concatenati non supportati. I rapporti di espansione ZIP sono limitati. La decompressione TAR è limitata prima dell’analisi dei membri/PAX, con un’ulteriore concessione fissa 4 MiB per intestazioni/padding TAR; anche la memoria del decoder XZ è limitata.
- La decrittazione accetta solo il formato criptato OneKit e autentica i suoi contenuti prima del ripristino dell'archivio limitato. Le opzioni dell'utente non possono aumentare il budget di espansione imposto.
- Gli strumenti di testo richiedono testo decodificabile senza byte di controllo binario. Gli strumenti per sviluppatori accettano le loro estensioni di linguaggio e input neutro `.txt`; gli adattatori shell/Dockerfile permettono anche sorgenti senza estensione. Gli strumenti di validazione accettano intenzionalmente sorgenti sintatticamente non validi e restituiscono `valid: false`. La conversione della codifica usa la codifica sorgente selezionata; altri strumenti di testo richiedono UTF-8..
- Ispezione, adattatori dei metadata e crittografia accettano intenzionalmente tipi di file arbitrari. I loro limiti di conteggio/byte si applicano ancora. Ispezionare un file danneggiato o sconosciuto è un'operazione supportata, piuttosto che un motivo per rifiutarlo solo per il suo contenuto.
