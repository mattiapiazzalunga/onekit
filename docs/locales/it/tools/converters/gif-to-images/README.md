<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="gif-to-images"></a>
# Da GIF a immagini

Comando: `onekit run gif-to-images`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Convertitori**. Fedeltà: **con limitazioni**. Esporta ogni fotogramma GIF come immagine PNG ricomposta, rispettando le regole di cancellazione dei fotogrammi e la trasparenza. Fino a 120 fotogrammi e 40 milioni di pixel complessivi. Le durate dei fotogrammi sono incluse nei dettagli del risultato.

Tipi accettati: `gif`. Tipo di output: `png`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: nessuna.

Pacchetti Python: Pillow. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/image_frames.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
