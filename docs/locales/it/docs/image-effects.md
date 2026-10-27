<a id="image-effects"></a>
# Effetti immagine

```sh
onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output
onekit run image-effects photo.jpg --options '{"effect":"blur","strength":12,"scope":"selected","regions":[{"x":0.1,"y":0.2,"width":0.3,"height":0.25}]}' -o output
```

`strength` è un numero intero da 1 a 100 pixel (almeno 2 per la pixelizzazione). `scope` è `all` (predefinito) o `selected`; la modalità selezionata richiede 1–500 rettangoli con coordinate normalizzate 0–1 e opzionale `page: 1`. `color` usa `#RRGGBB` per copertura solida. L'intensità non ha effetto sulla scala di grigi o sulla copertura solida. Le aree sovrapposte vengono elaborate dai pixel originali, senza sfocatura cumulativa. Al massimo vengono elaborati 80 milioni di pixel selezionati, contando le sovrapposizioni.

Sfocatura ed effetto pixel sono effetti visivi e non garantiscono la rimozione dei dettagli sensibili. Usa l’oscuramento permanente delle immagini quando i contenuti devono essere coperti in modo irreversibile.
