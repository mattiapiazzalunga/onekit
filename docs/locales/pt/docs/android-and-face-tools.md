<a id="android-packages-and-automatic-face-blur"></a>
# Pacotes Android e desfoque facial automático

Pacotes um APK autônomo e seus metadados em um arquivo XAPK sem reescrever bytes APK. Os APKs divididos são rejeitados. Requer um instalador compatível com XAPK; as assinaturas não são verificadas.

Extrai dados originais APKs e OBB sem reescrever bytes APK. Os APKs divididos devem ser instalados em conjunto; eles não são fundidos em um APK universal. As assinaturas não são verificadas.

Detecta rostos localmente com a YuNet e borra-os num novo PNG. Revise cada face antes de compartilhar: detecção automática pode perder rostos e borrar não garante o anonimato. Imagens de quadro único, até 16 milhões de pixels.

A saída PNG omite metadados de origem. Nenhuma imagem é exportada quando nenhuma face é detectada.

```sh
onekit run apk-to-xapk app.apk -o app.xapk
onekit run xapk-to-apk app.xapk -o extracted/
onekit run image-blur-faces photo.jpg -o blurred.png
```

Instale o opcional `faces` extra para detecção de face local.
