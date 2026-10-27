<a id="color-photo-restoration-and-pdf-forms"></a>
# Colore, restauro foto e moduli PDF

Questi strumenti sono accessibili tramite il comando standard `onekit run TOOL ... --options JSON` e i Python `execute` API. Vedi `onekit run --help` per gli argomenti di input/output. Tutte le coordinate qui sotto si riferiscono all'immagine dopo l'orientamento EXIF o alla pagina PDF visualizzata dopo la rotazione.

- `color-picker`: ispeziona un file UTF-8 contenente `#RRGGBB`, oppure campiona un'immagine con coordinate intere dei pixel `x` e `y` (al centro per impostazione predefinita). Riporta HEX, RGB, OKLCH, contrasto testo bianco/nero e RGBA originale per le immagini. I colori visibili sono compositati su bianco.
- `image-extract-colors`: `colors` (2–32, default 6). Quantizzazione median-cut di una miniatura limitata a 256 × 256. I pixel completamente trasparenti sono esclusi; il canale alfa parziale è compositato su bianco. Le frazioni descrivono questo campione.
- `jpg-to-svg`: `colors` (2–32, predefinito 16), `resolution` (32–512, predefinito 256). Quantizza un'immagine limitata, unisce verticalmente le sequenze orizzontali di colore uguale e scrive percorsi SVG riempiti. Nessuna bitmap viene incorporata. Questo produce tile vettoriali con un aspetto posterizzato, non con un tracciamento di curve fluide.
- `image-repair`: senza `regions`, applica un filtro mediano di `size` 3 o 5 a macchie isolate. Con le regioni, ricostruisce i pixel selezionati usando i pixel circostanti fissi e la diffusione armonica discreta (`iterations` 10–500, predefinito 200).
- `image-remove-watermark`: richiede `regions`; utilizza la stessa ricostruzione locale. Stima i pixel mancanti e non può recuperare contenuti originali nascosti. Texture, grandi segni e sfondi intricati possono dare risultati scadenti.
- `image-sharpen`: `method` può essere `unsharp` (predefinito) o `deconvolution`. `radius`, tra 0.3 e 5, imposta il raggio della maschera di contrasto o la diffusione gaussiana stimata di un punto. Per la maschera di contrasto, `amount` varia da 0 a 300 percento (predefinito 150). Richardson–Lucy usa da 1 a 30 `iterations` (predefinito 10), estensione dei bordi per riflessione e convoluzione FFT, fino a un milione di pixel sorgente. Presuppone una sfocatura gaussiana e non corregge movimenti arbitrari. Entrambi i metodi possono amplificare rumore e aloni.
- `pdf-remove-watermark`: di default `mode: "remove"` rimuove i gruppi `/Artifact` contrassegnati `/Subtype /Watermark` (incluse le risorse di proprietà denominate) e le annotazioni `/Watermark`. Il parametro facoltativo `text` cerca corrispondenze con oggetti di testo completi, normalizzando gli spazi e decodificando i glifi tramite la codifica del font o la mappa ToUnicode. Gli XObject Form nidificati vengono elaborati ricorsivamente. Usa `mode: "inspect"` per ottenere un report JSON di ID di testo, immagini e invocazioni di Form XObject; passa gli ID selezionati come `objects` in modalità rimozione. Selezionando un Form XObject si rimuove l'intero gruppo grafico. I Form XObject modificati vengono copiati per ogni invocazione così gli usi non selezionati di una risorsa condivisa restano invariati. Gli ID si riferiscono allo stesso PDF originale e devono essere reinspezionati dopo le modifiche. Si tratta di rimozione di oggetti grafici, non di oscuramento sicuro dei dati: oggetti di risorsa non utilizzati possono rimanere nell'output. Non identifica automaticamente contenuti arbitrari senza tag come filigrane, e una filigrana incorporata in un’immagine scansionata non può essere separata da quell’immagine. Un report contiene fino a 2.000 elementi candidati, la ricorsione è limitata a 12 livelli e l'elaborazione a 300.000 operazioni grafiche. Se non vengono trovate corrispondenze, viene restituito un errore esplicito.
- `pdf-make-fillable`: `fields` è un array JSON di widget AcroForm standard. Ogni widget ha un `name` ASCII univoco, un `type` (`text`, `checkbox`, `choice`), una `page` numerata da 1 e coordinate normalizzate `x`, `y`, `width`, `height`. Sono supportati `required` facoltativo, `multiline` per il testo e `choices` per le opzioni di scelta. I campi esistenti e il contenuto delle pagine vengono preservati. Sono rifiutati nomi duplicati, PDF cifrati e XFA. Nessun riconoscimento automatico degli spazi vuoti.

Le regioni delle immagini sono array di oggetti come `{"page":1,"x":0.2,"y":0.3,"width":0.1,"height":0.05}`. Le coordinate sono normalizzate a 0–1 dall'angolo in alto a sinistra. La ricostruzione supporta fino a 100 rettangoli, al massimo 35% dell'immagine e una bounding box (incluso il padding) di un milione di pixel. Solo RGB all'interno della maschera cambia; l'alpha originale viene mantenuto. Gli output sono PNG senza metadata sorgente. Le immagini animate/multiframe vengono rifiutate. La decodifica generale delle immagini è limitata a 40 milioni di pixel. I PDF sono limitati a 256 pagine e i form a 200 nuovi campi.

Esempio di utilizzo Python:

```python
from onekit import Artifact, execute

result = execute("pdf-make-fillable", [Artifact("source.pdf", pdf_bytes)], {
    "fields": [{"name": "Name", "type": "text", "page": 1,
                "x": 0.1, "y": 0.2, "width": 0.4, "height": 0.05}]
})
```

Esamina i file risultanti e conserva gli originali. Per compilare e salvare i moduli è necessario un lettore PDF compatibile.
