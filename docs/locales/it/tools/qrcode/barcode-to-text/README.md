<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="barcode-to-text"></a>
# Da codice a barre a testo

Comando: `onekit run barcode-to-text`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Codici QR**. Fedeltà: **esatta**. Legge localmente codici a barre lineari standard da un'immagine; Usa un'immagine nitida con barre complete e margini laterali chiari.

Tipi accettati: `png, jpeg, webp, bmp, gif`. Tipo di output: `txt`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **16,777,216 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: nessuna.

Pacchetti Python: Pillow, zxing-cpp. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/barcode.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
