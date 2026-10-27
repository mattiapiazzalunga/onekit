<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="excel-to-xml"></a>
# Da Excel a XML

Comando: `onekit run xlsx-to-xml`. Usa `onekit run --help` per gli argomenti di input e output.

Categoria: **Convertitori**. Fedeltà: **esatta**. Le tabelle XML usano record piatti ripetuti. La conversione da JSON a XML preserva i tipi usando uno schema tipizzato con radice ed elementi; gli attributi XML usano @ e il testo usa #text nel JSON. Le formule dei fogli di calcolo non vengono valutate; per impostazione predefinita viene usato il primo foglio. Controlla lo schema e i valori dopo la conversione.

Tipi accettati: `xlsx`. Tipo di output: `xml`. Accetta più input: **no**.

Validazione dell’input: **per tipo di file**. Numero di file richiesto: **1–1**. CLI: **134,217,728 byte per file**, **134,217,728 byte totali**. Il contenuto viene controllato prima dell’elaborazione. Rinominare un file non ne cambia il formato effettivo.

Opzioni: `sheet`.

Pacchetti Python: openpyxl. Motori esterni: consultare la matrice dei motori per sviluppatori per gli adattatori dei linguaggi di programmazione.

Implementazione dell’elaborazione: [adattatore condiviso della famiglia di strumenti](../../../../../../src/onekit/tools/structured_data.py). Contratti e dati di test per le regressioni: [test](../../../../../../tests/test_core.py). Configurazione dei motori e licenze: [guida ai motori](../../../docs/engines.md).

Questa directory è generata dal catalogo condiviso da `python scripts/tool_docs.py`. Modifica il registro e l'adattatore di famiglia, aggiungi dati di prova per i test di regressione, poi rigenera la directory.
