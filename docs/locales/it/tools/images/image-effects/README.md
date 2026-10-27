<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="blur-pixelate--image-effects"></a>
# Sfoca, pixella ed effetti immagine

Comando: `onekit run image-effects`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Immagini**. Fedeltà: **con limitazioni**. Sfocatura, pixelatura, sfocatura a riquadro, copertura uniforme o scala di grigi in un unico strumento. Applica all'intera immagine o ad aree selezionate, con intensità regolabile e una nuova esportazione PNG. Sfocatura e pixelatura non garantiscono la rimozione permanente dei dettagli sensibili. Solo immagini a singolo fotogramma.

Tipi accettati: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo di output: `png`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `effect`, `scope`, `strength`, `color`, `regions`.

Pacchetti Python: Pillow. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/image_effects.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
