<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="verify-digital-signature"></a>
# Verifica firma digitale

Comando: `onekit run signature-verify`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Sicurezza**. Fedeltà: **esatta**. Verifica crittografica offline delle firme PDF e CMS/P7M/P7S usando certificati incorporati. Le firme separate richiedono il file originale. Catene di fiducia, revoche, stato della firma qualificata e timestamp fidati non vengono controllati.

Tipi accettati: `*`. Tipo di output: `json`. Accetta più input: **sì**.

Validazione dell’input: **qualsiasi tipo di file**. Numero di file richiesto: **1–2**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: nessuna.

Pacchetti Python: pypdf, asn1crypto, pycryptodome. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/signatures.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
