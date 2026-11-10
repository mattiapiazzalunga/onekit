<a id="digital-signature-validation"></a>
# Validazione delle firme digitali

CLI e browser eseguono lo stesso motore Python di validazione. Nessun documento viene caricato online. Vengono controllate firme e scadenze delle liste di fiducia UE; i servizi non supportati sono esclusi.

Integrità crittografica e validazione AdES sono risultati distinti. La validazione usa prove locali e liste di fiducia UE autenticate. Se mancano prove, l’esito è indeterminato. L’equivalenza con DSS non è certificata.

Verifica localmente le firme PDF e CMS con validazione AdES. Le firme separate richiedono il file originale. Puoi aggiungere un archivio ZIP di prove della firma. Se mancano prove di fiducia o revoca, l’esito è indeterminato.

Aggiorna le liste di fiducia pubbliche con questo comando. Non invia documenti o dati dei firmatari.

```sh
python -m pip install "onekit-tools[verification,trustlists]"
python -m onekit.signature_evidence eu-trust-lists.zip
onekit run signature-verify signed.pdf eu-trust-lists.zip -o report
```

Il manifest dello ZIP di prove usa la struttura seguente. I certificati aggiuntivi non diventano mai arbitrariamente radici di fiducia.

```json
{"schema":"onekit-signature-evidence-v1","lotl":"lotl.xml","trusted_lists":[{"url":"https://official.example/list.xml","path":"tl/list.xml"}],"certificates":[],"crls":[],"ocsps":[]}
```

Python nativo Windows ARM64 può richiedere strumenti di compilazione per cryptography. Usa Python x64 quando non è disponibile una wheel binaria.

Lo snapshot attuale contiene 30 territori. Le estensioni TakenOverBy supportate preservano la cronologia del servizio e non trasferiscono la fiducia a un altro prestatore.

L’accettazione degli algoritmi usa le soglie della versione fissata di DSS 6.5.1; l’integrità matematica viene riportata separatamente.

Su Windows, l’extra trustlists abilita TLS con verifica tramite l’archivio dei certificati del sistema operativo.

L’istantanea delle liste di fiducia ha copertura parziale. Le prove mancanti lasciano l’esito indeterminato. I test selezionati con DSS non dimostrano un’equivalenza completa eIDAS o PAdES.
