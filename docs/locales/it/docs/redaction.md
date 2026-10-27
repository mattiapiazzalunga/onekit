<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanent-redaction"></a>
# Oscuramento permanente

<a id="pdf"></a>
## PDF

Ogni pagina viene renderizzata, i pixel selezionati vengono sostituiti con nero opaco e viene costruito un nuovo PDF dalle immagini con i contenuti sensibili già oscurati. Nessun oggetto originale PDF viene copiato. Questo rimuove il testo selezionabile originale, i livelli OCR, i livelli nascosti, i campi modulo, gli oggetti di annotazione/commento, i link, gli script, gli allegati, i metadati, le miniature e la cronologia dei salvataggi incrementali dall'output. Gli aspetti visivi delle annotazioni vengono appiattite in pixel così che un'annotazione opaca esistente non riveli inaspettatamente il contenuto che copriva. Controlla l'anteprima per le differenze nell'aspetto dei campi/annotazioni; nessun oggetto interattivo viene mantenuto. Il contenuto della pagina visibile non selezionato rimane come pixel.

<a id="images"></a>
## Images

I pixel vengono sostituiti con nero pieno prima di codificare un nuovo PNG RGB opaco. Nelle aree codificate non rimangono sovrapposizioni rimovibili, livelli originali o dati dei pixel originali non oscurati. I metadati originali EXIF, GPS, XMP, i commenti, i profili, le miniature e gli altri metadati originali non vengono copiati. La trasparenza viene composta su uno sfondo bianco, eliminando i valori RGB nascosti sotto i pixel trasparenti. L’orientamento EXIF viene applicato prima di interpretare le aree. Le immagini animate e con più fotogrammi vengono rifiutate per impedire che rimangano altri fotogrammi non oscurati; esporta prima un singolo fotogramma.

<a id="cli-and-workflows"></a>
## CLI and workflows

Installa `onekit-tools[pdf]` per l’oscuramento permanente dei PDF o `onekit-tools[images]` per le immagini. Entrambi gli strumenti accettano `regions`, un array di rettangoli, opzionalmente serializzato come stringa JSON. Ogni rettangolo specifica `page` (numerazione a partire da 1, valore predefinito 1), `x`, `y`, `width`, `height`. Le coordinate sono frazioni della pagina/immagine orientata visivamente con origine in alto a sinistra: `0.1` significa 10%. Per le immagini, `page` deve essere 1. Possono essere selezionati fino a 500 rettangoli. Le aree devono rientrare nella pagina; i bordi delle maschere vengono arrotondati verso l’esterno e ampliati di un pixel di output per coprire anche le porzioni frazionarie dei bordi.

```sh
onekit run pdf-redact private.pdf -o redacted.pdf --options '{"regions":[{"page":1,"x":0.1,"y":0.2,"width":0.5,"height":0.1}],"dpi":200}'
onekit run image-redact private.jpg -o redacted.png --options '{"regions":[{"x":0.2,"y":0.2,"width":0.3,"height":0.2}]}'
```
