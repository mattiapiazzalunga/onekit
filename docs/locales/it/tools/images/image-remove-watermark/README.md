<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="remove-image-watermark"></a>
# Rimuovi filigrana dall'immagine

Comando: `onekit run image-remove-watermark`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Immagini**. Fedeltà: **con limitazioni**. Ricostruisci manualmente le aree con filigrana dai pixel circostanti usando la diffusione armonica. Stima i contenuti mancanti; marchi grandi, texture e volti potrebbero non ricostruirsi in modo convincente. Nessun rilevamento automatico dei marchi.

Tipi accettati: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo di output: `png`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `regions`, `iterations`.

Pacchetti Python: Pillow, numpy. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/photo_tools.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
