<a id="android-packages-and-automatic-face-blur"></a>
# Pacchetti Android e sfocatura automatica dei volti

Inserisce un APK autonomo e i suoi metadati in un archivio XAPK senza modificare i byte dell’APK. Gli APK split vengono rifiutati. Richiede un programma di installazione compatibile con XAPK; le firme non vengono verificate.

Estrae gli APK originali e i dati OBB senza modificare i byte degli APK. Gli APK split devono essere installati insieme: non vengono uniti in un APK universale. Le firme non vengono verificate.

Rileva i volti localmente con YuNet e li sfoca in un nuovo PNG. Controlla ogni volto prima di condividere: il rilevamento automatico può perderne alcuni e la sfocatura non garantisce l’anonimato. Immagini a singolo fotogramma, fino a 16 milioni di pixel.

Il PNG esportato non contiene i metadati originali. Se non viene rilevato alcun volto, non viene esportata nessuna immagine.

```sh
onekit run apk-to-xapk app.apk -o app.xapk
onekit run xapk-to-apk app.xapk -o extracted/
onekit run image-blur-faces photo.jpg -o blurred.png
```

Installa l’extra opzionale `faces` per il rilevamento locale dei volti.
