<a id="android-packages-and-automatic-face-blur"></a>
# Paquets Android et floutage automatique des visages

Regroupe un APK autonome et ses métadonnées dans une archive XAPK sans modifier les octets de l’APK. Les APK fractionnés sont refusés. Un installateur compatible XAPK est nécessaire ; les signatures ne sont pas vérifiées.

Extrait les APK d’origine et les données OBB sans modifier les octets des APK. Les APK fractionnés doivent être installés ensemble ; ils ne sont pas fusionnés en un APK universel. Les signatures ne sont pas vérifiées.

Détecte les visages localement avec YuNet et les floute dans un nouveau PNG. Vérifiez chaque visage avant de partager : la détection automatique peut en manquer et le floutage ne garantit pas l’anonymat. Images non animées, jusqu’à 16 millions de pixels.

Le PNG exporté omet les métadonnées d’origine. Aucune image n’est exportée si aucun visage n’est détecté.

```sh
onekit run apk-to-xapk app.apk -o app.xapk
onekit run xapk-to-apk app.xapk -o extracted/
onekit run image-blur-faces photo.jpg -o blurred.png
```

Installez le groupe optionnel `faces` pour la détection locale des visages.
