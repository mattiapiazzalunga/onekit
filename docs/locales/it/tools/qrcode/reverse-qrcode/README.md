<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="reverse-qr-code"></a>
# Inverti il codice QR

Comando: `onekit run reverse-qrcode`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Codici QR**. Fedeltà: **esatta**. Legge i payload QR localmente da un'immagine; La decodifica inversa rivela il contenuto memorizzato, non l'immagine originale o le impostazioni del generatore. Nessun link viene aperto automaticamente.

Tipi accettati: `png, jpeg, webp, bmp, gif`. Tipo di output: `json`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **16,777,216 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: nessuna.

Pacchetti Python: Pillow, zxing-cpp. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/qrcode.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
