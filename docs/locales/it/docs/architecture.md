<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="architecture-and-extension-guide"></a>
# Guida all'architettura e alle estensioni

`Artifact(name, data)` è un payload di byte nominato immutabile. `Result(files, warnings, details)` trasporta output e avvisi di fedeltà. `execute(tool_id, files, options)` valida contratti e importa pigramente un adattatore di elaborazione. `pipeline(steps, files)` compone operazioni e mappa più output attraverso passaggi a input singolo.

Il catalogo definisce ID stabili, famiglie, tipi accettati e di output, molteplicità, opzioni, fedeltà, limiti e dipendenze. Gli adapter di elaborazione sono indipendenti dall'accesso al filesystem CLI. I nomi portabili rifiutano la traversata e i nomi di dispositivi riservati. Le scritture di output CLI preservano i file esistenti per impostazione predefinita. Le chiamate del motore nativo usano array di argomenti, directory temporanee e timeout limitati.

Per aggiungere uno strumento, implementa il suo adattatore di famiglia, dichiara la voce nel catalogo, aggiungi test di regressione semantici e per input non valido, dichiara le dipendenze opzionali e rivedi le licenze. Rigenera le directory degli strumenti con `python scripts/tool_docs.py`. Documenta la fedeltà e i requisiti della piattaforma.


L’API di elaborazione v1 è descritta in `contracts/processing-v1.json`. Esegui `python scripts/check_contracts.py` prima di inviare le modifiche. Aggiungere strumenti, formati e opzioni è compatibile; rimuovere ID/opzioni esistenti, cambiare tipi di output o restringere i contratti di input richiede una migrazione con versione esplicita. Gli algoritmi interni e l'organizzazione dei gestori possono cambiare senza modificare il contratto pubblico.

`ExecutionContext` permette ai chiamanti di Python di abbassare i budget di batch e per strumento e fornire un lettore di metadati dei media locali affidabile. Non accetta servizi del motore tramite opzioni degli strumenti fornite dall'utente. I contesti sono immutabili, limitati a una singola esecuzione e condivisi tra i passaggi della pipeline. CLI usa i servizi motore locali predefiniti.

L'adattatore sorgente Node delega le regole di formattazione e minificazione a `tools/developer/source_engine.mjs`. Il suo loader del motore è una dipendenza a livello di processo; il testo sorgente non può scegliere pacchetti o comandi eseguibili a piacimento.
