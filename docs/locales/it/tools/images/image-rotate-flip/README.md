<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="rotate-and-flip-image"></a>
# Ruota e capovolgi immagine

Comando: `onekit run image-rotate-flip`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Immagini**. Fedeltà: **esatta**. Applica l'orientamento EXIF, ruota in senso orario di 0, 90, 180 o 270 gradi, poi rifletti orizzontalmente, verticalmente o entrambi. Esporta un PNG senza metadata, preservando pixel decodificati e trasparenza. Solo immagini a frame singolo; fino a 40 milioni di pixel.

Tipi accettati: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo di output: `png`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `angle`, `flip`.

Pacchetti Python: Pillow. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/image_transform.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
