<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="url-inspector"></a>
# Ispettore URL

Comando: `onekit run url-inspect`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Analisi**. Fedeltà: **con limitazioni**. Ispeziona i componenti URL, lo stato HTTP, URL finale e gli header di risposta disponibili direttamente dal tuo dispositivo. Registra fino a 10 reindirizzamenti HTTP. I guasti di rete lasciano un report parziale. Questo non è un controllo di phishing, malware, DNS o proprietà.

Tipi accettati: `txt`. Tipo di output: `json`. Accetta più input: **no**.

Validazione dell’input: **testo**. Numero di file richiesto: **1–1**. CLI: **16,384 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: nessuna.

Pacchetti Python: libreria standard o motore esterno. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/link_tools.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
