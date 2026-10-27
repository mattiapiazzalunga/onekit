<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="security-policy"></a>
# Politica di sicurezza

Segnala le vulnerabilità privatamente a `security@onekit.org` con versione, piattaforma, strumenti, versioni delle dipendenze, impatto e riproduzione sintetica. Non pubblicare file sensibili, credenziali o report privati pronti per exploit su tracker pubblici. Le correzioni mirano all’ultima release stabile; non è garantito un tempo di risposta.

Il core impone limiti ai percorsi, alle dimensioni degli input, alla decompressione degli archivi, ai pixel delle immagini, ai confronti e alle pipeline. La cifratura usa AES-256-GCM autenticato con salt e nonce nuovi e scrypt; le password perse non possono essere recuperate. Gli output esistenti vengono preservati per impostazione predefinita. La convalida Python analizza il codice sorgente senza eseguirlo.

I convertitori/compilatori esterni sono programmi nativi separati, non una sandbox completa. Tienili aggiornati e isola i documenti ostili usando i controlli del sistema operativo. La CLI non è un servizio di conversione remota senza autenticazione. Modificare un PDF firmato può invalidare le firme; i permessi PDF non equivalgono all'integrità della crittografia.

I controlli ordinari non devono mai ricevere segreti di pubblicazione. I tag stabili identificano i commit principali protetti e revisionati. Fallimenti di dipendenze, licenze e sicurezza bloccano la pubblicazione. Nessuna suite di test garantisce immunità da tutti gli input malformati o attacchi.
