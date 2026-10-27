<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="decrypt-files-or-folders"></a>
# Decripta file o cartelle

Comando: `onekit run security-decrypt`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Sicurezza**. Fedeltà: **esatta**. AES-256 crittografato ZIP, compatibile con 7-Zip. I nomi dei file restano visibili. Perdere la password rende il recupero impossibile.

Tipi accettati: `zip`. Tipo di output: `*`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `password`, `restore`.

Pacchetti Python: pycryptodome, stream-zip, stream-unzip. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/security/__init__.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
