<a id="android-packages-and-automatic-face-blur"></a>
# Paquetes Android y desenfoque automático de rostros

Empaqueta un APK independiente y sus metadatos en un archivo XAPK sin modificar los bytes del APK. Se rechazan los APK divididos. Requiere un instalador compatible con XAPK; no se verifican las firmas.

Extrae los APK originales y los datos OBB sin modificar los bytes de los APK. Los APK divididos deben instalarse juntos; no se fusionan en un APK universal. No se verifican las firmas.

Detecta rostros localmente con YuNet y los desenfoca en un nuevo PNG. Revisa cada rostro antes de compartir: la detección automática puede omitir algunos y el desenfoque no garantiza el anonimato. Imágenes de un solo fotograma, hasta 16 millones de píxeles.

El PNG exportado omite los metadatos originales. No se exporta ninguna imagen si no se detectan rostros.

```sh
onekit run apk-to-xapk app.apk -o app.xapk
onekit run xapk-to-apk app.xapk -o extracted/
onekit run image-blur-faces photo.jpg -o blurred.png
```

Instala el extra opcional `faces` para detectar rostros localmente.
