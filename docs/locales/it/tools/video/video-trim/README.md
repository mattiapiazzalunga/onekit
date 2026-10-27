<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="trim-video"></a>
# Taglia video

Comando: `onekit run video-trim`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Video**. Fedeltà: **con limitazioni**. Mantiene l'intervallo selezionato dall'inizio alla fine in secondi ed esporta MP4 con l'audio quando presente. La ricodifica potrebbe perdere qualità.

Tipi accettati: `mp4, webm, mkv, mov, avi, gif, mpeg, mpg, m4v, ogv, ts`. Tipo di output: `mp4`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `start`, `end`.

Pacchetti Python: libreria standard o motore esterno. Motori esterni: ffmpeg, ffprobe.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/video_edit.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
