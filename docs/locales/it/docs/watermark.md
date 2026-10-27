<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-watermark"></a>
# Filigrana PDF

Nella categoria PDF, carica un PDF, inserisci testo e regola opacità, colore, font, rotazione e posizione. L'anteprima mostra la posizione del watermark sulla pagina scelta. Esporta per controllare il rendering finale del font PDF. Scegli un singolo watermark o una griglia ripetuta 3 × 4. Il testo viene automaticamente ridotto quando necessario per adattarsi alla pagina o alla cella, fino a un limite di leggibilità di sei punti. I PDF crittografati devono essere sbloccati prima. Le firme digitali esistenti non sono più valide dopo la modifica di un documento; lo strumento avvisa quando sono presenti campi firma.

```sh
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","pages":"1,3-5","opacity":0.25,"angle":45}'
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"DRAFT","layout":"repeat","color":"#b00000"}'
```

| Opzione | Valori / predefiniti |
| --- | --- |
| `text` | 1–200 caratteri, fino a cinque righe; predefinito BOZZA |
| `pages` | Intervalli basati su uno solo, ad esempio `1,3-5`; vuoto o omesso significa tutti |
| `font` | Helvetica-Grassetto (predefinito), Helvetica, Times-Roman, Courier |
| `font_size` | 8–160 punti; default 48, adattato automaticamente quando necessario |
| `color` | Esadecimale a sei cifre; predefinito #666666 |
| `opacity` | 0.05–1; predefinito 0.25 |
| `angle` | -180–180 gradi, in senso antiorario; predefinito 45 |
| `position` | centro, in alto a sinistra/centro/destra, a metà a sinistra/destra, in basso a sinistra/centro/destra |
| `layout` | singolo (predefinito) o ripeti (3 × 4 griglia; la posizione viene ignorata) |
| `margin` | 0–144 punti; predefinito 24 |

I font supportano caratteri e punteggiatura dell'Europa occidentale, inclusi gli accenti italiani. I caratteri non supportati generano un errore. È possibile elaborare fino a 512 pagine. Il posizionamento utilizza la crop box orientata visivamente, mantenendo la rotazione originale e le coordinate delle annotazioni. Una filigrana indica il contenuto visibile; non rimuove il contenuto sottostante.
