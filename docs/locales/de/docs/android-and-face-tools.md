<a id="android-packages-and-automatic-face-blur"></a>
# Android-Pakete und automatisches Weichzeichnen von Gesichtern

Verpackt ein eigenständiges APK mit seinen Metadaten in ein XAPK-Archiv, ohne APK-Bytes zu verändern. Split-APKs werden abgelehnt. Ein XAPK-kompatibles Installationsprogramm ist erforderlich; Signaturen werden nicht überprüft.

Extrahiert die ursprünglichen APKs und OBB-Daten, ohne APK-Bytes zu verändern. Split-APKs müssen gemeinsam installiert werden; sie werden nicht zu einem universellen APK zusammengeführt. Signaturen werden nicht überprüft.

Erkennt Gesichter lokal mit YuNet und zeichnet sie in einem neuen PNG weich. Prüfen Sie vor dem Teilen jedes Gesicht: Die automatische Erkennung kann Gesichter übersehen, und Weichzeichnen garantiert keine Anonymität. Einzelbilder mit bis zu 16 Millionen Pixeln.

Das ausgegebene PNG enthält keine ursprünglichen Metadaten. Wenn kein Gesicht erkannt wird, wird kein Bild exportiert.

```sh
onekit run apk-to-xapk app.apk -o app.xapk
onekit run xapk-to-apk app.xapk -o extracted/
onekit run image-blur-faces photo.jpg -o blurred.png
```

Installieren Sie das optionale Extra `faces` für die lokale Gesichtserkennung.
