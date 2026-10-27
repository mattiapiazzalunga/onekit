<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="download-audio"></a>
# Scarica audio

Comando: `onekit run audio-download`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Audio**. Fedeltà: **con limitazioni**. Scarica un file audio diretto o una fonte audio esposta da una pagina accessibile. La modalità originale preserva i byte scaricati; la conversione MP3 è con perdita. Fino a 128 MiB. Login e stream protetti possono impedire il download. Usare solo con permesso.

Tipi accettati: `txt`. Tipo di output: `*`. Accetta più input: **no**.

Validazione dell’input: **testo**. Numero di file richiesto: **1–1**. CLI: **16,384 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `format`, `quality`.

Pacchetti Python: libreria standard o motore esterno. Motori esterni: ffmpeg, ffprobe.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/link_tools.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
