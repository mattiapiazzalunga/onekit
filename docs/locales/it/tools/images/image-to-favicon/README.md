<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="image-to-favicon"></a>
# Immagine per favicon

Comando: `onekit run image-to-favicon`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Immagini**. Fedeltà: **con limitazioni**. Ridimensiona il primo fotogramma dell'immagine in icone quadrate. Fit mantiene l'intera immagine con padding trasparente; fill ritaglia i bordi. I file originali rimangono invariati.

Tipi accettati: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo di output: `*`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **67,108,864 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `format`, `fit`.

Pacchetti Python: Pillow. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/favicon.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
