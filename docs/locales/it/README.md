<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->

Lingue: [English](../../../README.md) · [Italiano](README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Deutsch](../de/README.md) · [Русский](../ru/README.md) · [中文](../zh/README.md).

<p align="center">
  <a href="https://onekit.org"><img src="https://raw.githubusercontent.com/mattiapiazzalunga/onekit/main/images/logo.png" alt="OneKit logo" width="112" height="112"></a>
</p>
<h1 align="center">OneKit</h1>
<p align="center">Un solo toolkit. I tuoi file restano tuoi.</p>
<p align="center"><a href="https://github.com/mattiapiazzalunga/onekit/stargazers"><img alt="Stelle su GitHub" src="https://img.shields.io/github/stars/mattiapiazzalunga/onekit"></a> <a href="https://pypi.org/project/onekit-tools/"><img alt="PyPI" src="https://img.shields.io/pypi/v/onekit-tools"></a> <img alt="PolyForm-Shield-1.0.0" src="https://img.shields.io/badge/license-PolyForm_Shield_1.0.0-blue"> <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue"></p>

Un toolkit Python offline con 230 strumenti per conversioni, PDF, immagini, archivi, font, ispezione dei file, crittografia, utilità per sviluppatori, OCR e confronti. Usa questa CLI o l’interfaccia grafica su **[onekit.org](https://onekit.org)**.

**Versione della fonte:** `0.6.1`. I download stabili esistono solo dopo il completamento del flusso di rilascio. La distribuzione è `onekit-tools`; il progetto di proprietà separata PyPI chiamato `onekit` non è correlato.

La [guida a contatti e contenuti multimediali](docs/contact-media.md) descrive la creazione di vCard autonome, l’estrazione di vCard dai codici QR, l’aumento della risoluzione delle immagini, la rimozione dello sfondo, la compressione e la modifica della velocità di video e GIF, e la trascrizione audio locale.

Controlli della licenza: ispeziona PDF, Word, PowerPoint, Excel, video, audio, immagini, font, EPUB, codice/progetti e dataset da file o URL pubblici. L'analisi rimane locale; i report sono **stime non verificate, non certificati di proprietà o permessi d'uso**. Vedi [uso e limiti dei controlli licenza](docs/cli.md#local-license-and-copyright-estimates).

**La tua CLI. La tua CLI per gli agenti.** Usa OneKit tu stesso o lascia che un agente locale AI lo chiami tramite terminale o sottoprocesso. Scopri strumenti e requisiti come JSON, passa percorsi di input/output espliciti e riutilizza flussi di lavoro `.1kit` salvati per compiti ripetibili sui file. Vedi [agenti locali e automazione](docs/cli.md#local-agents-and-automation).

<a id="install"></a>
## Install

È richiesto Python 3.11 o successivo. Il pacchetto wheel universale supporta Windows, macOS e Linux su x64/ARM64. Le librerie native opzionali e i motori esterni prevedono ulteriori requisiti di piattaforma.

Dopo la pubblicazione:

```sh
python -m pip install onekit-tools
python -m pip install "onekit-tools[pdf,images,documents]"
onekit list
onekit doctor
```

Da una copia del repository sorgente:

```sh
python -m pip install -e ".[all,test]"
python -m onekit --help
python -m pytest -q
```

La base CLI **non ha dipendenze a runtime**. Installa solo gli extra di cui hai bisogno. `all` include le famiglie standard Python; il download dei video, la rimozione dello sfondo, la trascrizione e la firma crittografica utilizzano i separati extra `video`, `background`, `transcription` e `signing`. Installa i motori nativi separatamente. Per gli strumenti di sviluppo basati su Node, installa Node.js 24+ e avvia `onekit engines install`. CLI prepara le dipendenze mancanti e i motori esterni al primo utilizzo. La rimozione dello sfondo e la trascrizione scaricano i pesi dei modelli al primo utilizzo, poi riutilizzano la cache locale.

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

Le opzioni sono oggetti JSON; passali come un argomento della shell tra virgolette. Usa `--ask-password` per i segreti. I risultati esistenti vengono preservati a meno che non passi `--force`.

`onekit list --group pdf`, `onekit list --json` e `onekit doctor TOOL_ID` espongono contratti e requisiti. Ogni strumento ha una directory sotto [tools](../../../tools), contenente i metadati e un puntatore alla sua implementazione condivisa. Vedi la guida [CLIguide](docs/cli.md) per opzioni e limiti.

<a id="toolkit"></a>
## Toolkit

| Famiglia | Capacità |
| --- | --- |
| Convertitori | Markdown, HTML, LaTeX, PDF, Word, PowerPoint, immagini, Base64, Excel, CSV e JSON |
| PDF | Unisci/dividi, selezione/ordine/rimozione delle pagine, compressione, riparazione, [modifica diretta del testo](docs/pdf-editing.md), sovrapposizioni di testo, rotazione, firme digitali, crittografia/sblocco, [conversione e convalida locali PDF/A](docs/pdfa.md) |
| Immagini | Estrai immagini PDF incorporate, comprimi, ritaglia e cambia formato |
| Media | Conversione audio/video tramite FFmpeg installato separatamente |
| Archivi / font | Varianti ZIP/TAR; contenitori TTF/OTF e WOFF/WOFF2 |
| Ispettore / sicurezza | Digita firme, struttura, metadati, codifica, hash, conteggi di testo; archivi di file/cartelle autenticati e crittografati |
| Sviluppatore | Formattazione specifica della lingua, validazione parser/compiler e minificazione selezionata |
| OCR | Immagini scansionate/PDF in PDF, Word, Markdown, LaTeX, HTML e JSON ricercabili |
| Diff | Testo, codice, JSON normalizzato, notebook, LaTeX, PDF e testo Word |

<a id="pipelines-and-development"></a>
## Pipelines and development

`onekit pipeline --steps workflow.1kit INPUTS -o OUTPUT` accetta un documento di flusso di lavoro `.1kit` versionato. Ogni passo riceve gli output precedenti. I passaggi a singolo input si applicano a più output; i passaggi di unione ricevono la collezione. Tipi incompatibili fermano l'elaborazione.

Segnala bug e suggerimenti tramite [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues) o il [bacheca delle richieste del sito](https://onekit.org/requests/). I contributori possono trovare lavoro in entrambi i posti.

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

Aiuta a costruire la rivoluzione aperta di OneKit: strumenti quotidiani per tutti, dai compiti pratici ai flussi di lavoro gestiti dagli agenti locali AI. Contribuisci a rendere gli strumenti più efficienti ed efficaci: migliora velocità e uso della memoria, correggi risultati sbagliati, aggiungi esempi di regressione o chiarisci la documentazione e i flussi di lavoro degli agenti.

Il core è Open Source (PolyForm Shield 1.0.0). Leggi la [guida per contribuire](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) e trova un compito in [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues), o suggerisci un miglioramento sulla [bacheca delle richieste](https://onekit.org/requests/).

<a id="license-and-creator"></a>
## License and creator

Creato da **[Mattia Piazzalunga](mailto:hello@mattiapiazzalunga.com)**. Copyright © 2026 Mattia Piazzalunga. Open Source (PolyForm Shield 1.0.0), con licenza [PolyForm Shield 1.0.0](../../../LICENSE); vedere [NOTICE](../../../NOTICE), [AUTHORS.txt](../../../AUTHORS.txt) e [CONTRIBUTORS.txt](../../../CONTRIBUTORS.txt). I componenti di terze parti mantengono le loro licenze. I motori esterni sono programmi separati con propri obblighi di ridistribuzione.

Puoi usare, modificare e ridistribuire il core per scopi consentiti, inclusi usi commerciali e interni. Non puoi usarlo per fornire un prodotto o servizio che compete con il software o con un prodotto che il licenziante o le sue affiliate forniscono usando il software; offerte gratuite e piattaforme o interfacce diverse possono comunque competere. Quando condividi copie, includi il testo della licenza o il suo URL e qualsiasi linea di Avviso Richiesto fornita con il software. La licenza completa regola tutto, comprese le eccezioni per prodotti nuovi e dismessi, i termini di brevetto e la esclusione di garanzia. Qui, “Open Source (PolyForm Shield 1.0.0)” descrive il codice pubblicato sotto questi termini; la restrizione di non concorrenza significa che questo è software con codice sorgente disponibile piuttosto che open source senza restrizioni secondo la Definizione di Open Source. Vedi [la guida alla licenza](docs/licenses.md).

Esporta e reimporta flussi di lavoro senza elaborare i file di input:

```sh
onekit workflow export workflow.1kit -o exported-workflow.1kit
onekit workflow import workflow.1kit -o saved-workflow.1kit
onekit pipeline --steps saved-workflow.1kit input.json -o output.json
```

I codici a barre standard sono disponibili nella categoria Codici QR e codici a barre e nella CLI: `text-to-barcode`, `scan-barcode`, `barcode-to-text`. Codice 128, Codice 39, Codice EAN-13, Codice EAN-8, UPC-A, ITF e ISBN-13 supportano PNG/SVG, dimensioni configurabili e validazione della cifra di controllo. Installa `onekit-tools[barcode]` o `onekit-tools[qrcode]`.

L’[oscuramento permanente di PDF e immagini](docs/redaction.md) è disponibile tramite `pdf-redact` e `image-redact`. Nei nuovi file le aree selezionate vengono sostituite da pixel neri opachi. I PDF vengono ricostruiti come documenti composti solo da immagini, senza testo, moduli, commenti, allegati o metadati originali; le immagini diventano PNG opachi senza metadati originali o pixel nascosti dalla trasparenza. I file originali restano invariati.

Aggiungi filigrane di testo configurabili PDF con `pdf-watermark`: opacità, colore, font, intervalli di pagine, posizioni visive, rotazione e griglie ripetute. Testo e grafica rimangono in PDF. Consulta la [guida alle filigrane](docs/watermark.md).

<a id="contacts"></a>
## Contacts

- Domande generali e supporto: [support@onekit.org](mailto:support@onekit.org).
- Domande sul core Open Source (PolyForm Shield 1.0.0) e sui contributi: [developers@onekit.org](mailto:developers@onekit.org).
- Privacy, GDPR e richieste di dati personali: [privacy@onekit.org](mailto:privacy@onekit.org).
- Domande legali, licenze e richieste di permesso: [legal@onekit.org](mailto:legal@onekit.org).
- Vulnerabilità di sicurezza e segnalazioni di abusi: [security@onekit.org](mailto:security@onekit.org).
