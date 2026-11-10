<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="automatically-blur-faces"></a>
# Sfoca automaticamente i volti

Comando: `onekit run image-blur-faces`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **immagini**. Fedeltà: **con compromessi**. Rileva i volti localmente con YuNet e li sfoca in un nuovo PNG. Controlla ogni volto prima di condividere: il rilevamento automatico può perderne alcuni e la sfocatura non garantisce l’anonimato. Immagini a singolo fotogramma, fino a 16 milioni di pixel.

Tipi accettati: `png, jpeg, webp, gif, bmp, tiff, ico`. Tipo di output: `png`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: nessuna.

Pacchetti Python: onnxruntime, numpy, Pillow. Motori esterni: vedi la matrice dei motori per sviluppatori per gli adattatori dei linguaggi.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/face_blur.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
