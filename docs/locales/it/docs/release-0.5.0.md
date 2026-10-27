<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="onekit-050"></a>
# OneKit 0.5.0

Prima versione del processore offline CLI e Python con API usando 230 strumenti per documenti, PDF, immagini, media, archivi, font, utility per sviluppatori, codici QR, dichiarazioni di licenza e ispezione dei file. L’installazione base non ha dipendenze runtime; componenti opzionali ed engine esterni abilitano gli strumenti selezionati.

Include la convalida degli input limitati, flussi di lavoro riutilizzabili, configurazione delle dipendenze locali, contratti di elaborazione specifici per il formato e ispezione delle licenze basata sulle fonti. I rapporti sulle licenze rimangono stime non verificate che richiedono revisione manuale.

Aggiornamenti delle prestazioni accelerano la preparazione delle immagini opache e l'ispezione del testo. Importazioni non utilizzate e assegnazioni ridondanti del motore di sviluppo sono state rimosse.

I motori modello sono opzionali: installa l'extra `background` o `transcription` quando necessario. U2Net funziona direttamente con il Runtime ONNX e un modello in cache verificato tramite checksum. Whisper utilizza faster-whisper. I file rimangono locali; alla prima esecuzione vengono scaricati i pesi del modello. Il processamento video richiede FFmpeg e ffprobe. Il download dei video utilizza l'extra separato `video`.

Aggiorna Pillow alla versione 13 e la versione fissata di certifi per risolvere i problemi segnalati negli avvisi pubblicati. Il gruppo portabile di dipendenze opzionali `all` rimane separato dai motori dei modelli e dalle funzionalità di firma.
