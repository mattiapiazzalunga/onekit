<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="release-operations"></a>
# Operazioni di rilascio

Proteggi il branch `main` e i tag stabili `v*`. Registra il PyPI Trusted Publisher per il repository `onekit`, il workflow `release.yml` e l'ambiente `pypi`. Aggiorna la versione del pacchetto, il lockfile, il catalogo e la documentazione, poi pubblica un tag SemVer stabile corrispondente da un commit revisionato.

Il flusso di lavoro di rilascio verifica il tag, esegue i controlli CLI richiesti e pubblica le distribuzioni universali wheel/source, l'immagine GHCR e gli asset di rilascio GitHub. `onekit-release.json` contiene versione, commit del sorgente, checksum degli asset e URL di download. I tentativi di pubblicazione devono preservare gli asset immutabili esistenti; le modifiche al codice richiedono una nuova versione.

<a id="pypi-license-metadata"></a>
## PyPI license metadata

Il pacchetto PyPI è Open Source (PolyForm Shield 1.0.0), con la restrizione di non concorrenza spiegata nel README mostrato nella pagina del progetto. `project.license` utilizza `LicenseRef-PolyForm-Shield-1.0.0`; wheel e l’archivio sorgente includono la LICENSE e NOTICE complete. I metadati del progetto collegano alla licenza e alla documentazione. Non aggiungere un classificatore di licenza approvato da OSI: questa licenza limita i prodotti concorrenti.

Prima della pubblicazione, costruisci dal commit di rilascio previsto e verifica gli artefatti effettivi:

```sh
uv build
python scripts/check_distribution_licenses.py
```

La CI e la build di rilascio eseguono questo controllo prima della pubblicazione degli artefatti. PyPI visualizza il README incluso nel pacchetto: dopo una modifica alla documentazione o ai metadati della licenza è quindi necessario ricostruire il pacchetto. Per sostituire un rilascio già pubblicato, pubblica una versione nuova e mai utilizzata: le distribuzioni PyPI esistenti non possono essere sovrascritte. Le versioni già distribuite conservano le condizioni di licenza originali. Una modifica della licenza non incrementa automaticamente la versione della copia di lavoro corrente.

Il proprietario del progetto configura separatamente l’account PyPI, il Publisher affidabile e la pubblicazione; la preparazione locale non carica pacchetti né cambia la pagina live PyPI.

<a id="weekly-dependency-maintenance"></a>
## Weekly dependency maintenance

Dependabot monitora il file di blocco uv, le dipendenze del motore CLI Node, Docker e GitHub Actions. Il workflow di controlli programmati ritesta le dipendenze bloccate e i motori nativi. Gli aggiornamenti Python solo di blocco rimangono soggetti a controlli riusciti e protezione del ramo.
