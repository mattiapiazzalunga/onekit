<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="video-to-frames"></a>
# Da video a fotogrammi

Comando: `onekit run video-to-frames`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Video**. Fedeltà: **con limitazioni**. Estrae fotogrammi PNG da un video usando FFmpeg. Scegli inizio, durata e larghezza. Fino a 120 fotogrammi: la modalità fotogramma originale preserva ogni fotogramma nell'intervallo; altrimenti i timestamp vengono campionati alla frequenza richiesta.

Tipi accettati: `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Tipo di output: `png`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `start`, `duration`, `fps`, `width`, `all_frames`.

Pacchetti Python: Pillow. Motori esterni: ffmpeg, ffprobe.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/video_edit.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
