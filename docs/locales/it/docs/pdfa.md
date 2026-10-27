<a id="pdfa-conversion-and-validation"></a>
# PDF/A conversione e validazione

I CLI e Python API chiamano `onekit.tools.pdfa`. Questo modulo non invoca eseguibili e non apre connessioni di rete. La conversione usa pdftopdfa 0.9.24 per font, colore e normalizzazione, seguita da pikepdf 10.17.0 PDF/A per la preparazione e la validazione dei byte finali esatti. Non c’è alcuna dipendenza Ghostscript.

La conversione supporta PDF/A-2b (predefinito) e 3b. La validazione supporta 1b, 2b e 3b. La conformità A/U, PDF/A-4 e OCR sono al di fuori di questo adattatore. Le strutture non supportate sono indicate come `not_checked`, non come conformi. Un `pass` da questa allowlist conservativa non è una certificazione archivistica; è comunque consigliata una validazione veraPDF indipendente per le sottomissioni istituzionali.

```
onekit run pdf-to-pdfa input.pdf --options '{"profile":"2b"}' -o output
onekit run pdf-validate-pdfa output/input.pdf -o report
onekit doctor pdf-to-pdfa --json
```

La CLI installa automaticamente un sottoinsieme fissato e revisionato **livello-B non-OCR** dei pacchetti upstream. Non installa intenzionalmente PaddleOCR, OCRmyPDF o il backend di crittografia per il parser PDF inutilizzato di pdfminer: nessuna opzione viene inoltrata alle API di tagging OCR o A/U upstream. Lo `pdftopdfa` wheel upstream non è modificato. I metadati del pacchetto includono requisiti più ampi per API che OneKit non invoca. L'extra opzionale `[pdfa]` installa i prerequisiti revisionati. Per un utilizzo diretto Python API, installa quell'extra e poi `pip install --no-deps pdfminer.six==20260107 pdftopdfa==0.9.24`. Non installare gli extra OCR dell'upstream per questo adapter. I requisiti obbligatori OCR di Upstream attualmente impongono una versione precedente di PyYAML incompatibile con OneKit. La conversione richiede Python 3.12+; la convalida autonoma funziona su Python 3.11+. Esegui `python scripts/check_licenses.py --include-pdfa` per controllare il runtime selezionato.

L'ex opzione `icc_profile` rimane accettata come file locale opzionale ICC; per impostazione predefinita vengono preservati i profili RGB/CMYK inclusi e con licenza del convertitore. I PDF crittografati e le firme digitali vengono rifiutati dalla conversione. La conversione può sostituire i font e rimuovere azioni o metadati non archivistici; avvisi accompagnano l'output riuscito. I candidati falliti o controllati in modo incompleto non vengono mai restituiti come file PDF/A convertiti. Gli input non vengono sovrascritti. Il rapporto di convalida JSON preserva i campi `compliant` e `reports` e aggiunge il profilo controllato, il verdetto e il motore.
