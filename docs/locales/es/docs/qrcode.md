<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="qr-codes"></a>
# Códigos QR

<a id="standard-linear-barcodes"></a>
## Standard linear barcodes

```sh
onekit run text-to-barcode identifier.txt -o barcode.png --options '{"barcode_type":"ean13"}'
onekit run text-to-barcode identifier.txt -o barcode.svg --options '{"barcode_type":"code128","format":"svg"}'
onekit run scan-barcode photo.jpg -o decoded.json
onekit run barcode-to-text photo.jpg -o identifier.txt
```

Estándares: `code128` (predeterminado, hasta 60 caracteres imprimibles ASCII), `code39` (hasta 48 letras mayúsculas/dígitos y símbolos compatibles, sin Mod-43 suma de verificación opcional), `ean13` (12 dígitos o 13 incluyendo suma de verificación), `ean8` (7/8), `upca` (11/12), `itf` (un número par de dígitos, hasta 80), `isbn13` (EAN-13 comenzando 978/979). Los dígitos de verificación proporcionados en el comercio minorista deben ser correctos; nunca se reemplazan silenciosamente. Los dígitos omitidos se calculan. Los identificadores no son asignados ni registrados por OneKit.

Instala `python -m pip install "onekit-tools[qrcode]"`. Todo el procesamiento QR es local y funciona sin conexión después de instalar las dependencias. La generación QR usa Segno; el escaneo CLI usa ZXing-C++ y Pillow.

| Herramienta | Entrada | Salida |
| --- | --- | --- |
| `text-to-qrcode` | UTF-8 TXT | PNG o SVG |
| `url-to-qrcode` | TXT que contiene un HTTP(S) URL | PNG o SVG |
| `wifi-to-qrcode` | Wi-Fi JSON | PNG o SVG |
| `vcard-to-qrcode` | Contacta a JSON o a VCF existente | PNG o SVG |
| `scan-qrcode` | PNG, JPEG, WebP, BMP o GIF | JSON informe |
| `reverse-qrcode` | Imagen QR | Contenido en bruto e interpretado en JSON |
| `qrcode-to-text` | Imagen QR | Texto exacto almacenado |
| `qrcode-to-json` | Imagen QR | Valor original JSON, o un informe para otras cargas útiles |

```sh
onekit run text-to-qrcode message.txt -o code.png
onekit run url-to-qrcode link.txt -o code.svg --options '{"format":"svg","error_correction":"Q"}'
onekit run wifi-to-qrcode network.json -o wifi.png
onekit run vcard-to-qrcode contact.json -o output/ --options '{"include_payload":true}'
onekit run scan-qrcode photo.jpg -o decoded.json
onekit run qrcode-to-json code.png -o recovered.json
```

Opciones de generación: `format` (`png`/`svg`), `error_correction` (`L`/`M`/`Q`/`H`), `scale` (2–16 píxeles por módulo), `border` (4–16 módulos), `dark` y `light` (hexadecimal de seis dígitos, contraste ≥4.5:1), y `include_payload` (también exporta codificado TXT/JSON/VCF). Valores predeterminados: PNG, M, escala 8, borde 4, negro sobre blanco. SVG escala para impresión. La entrada está limitada a 16 KiB, pero la capacidad de QR es menor y depende de la corrección; acorta contactos sobredimensionados o reduce la corrección. Las URL de fotos se almacenan sin obtener la imagen.

Ejemplo Wi-Fi:

```json
{"ssid":"Guest Wi-Fi","security":"WPA","password":"example-password","hidden":false}
```

Seguridad: `WPA` (WPA/WPA2 personal), `WEP`, `nopass` (abierto), `SAE` (WPA3), `WPA2-EAP` (empresa). La versión Enterprise añade `identity`, `anonymous_identity`, `eap`, `phase2`. WPA3 y el soporte Enterprise varían según el teléfono. Las contraseñas siguen siendo legibles en la carga útil QR. Los caracteres especiales usan la convención de escape [ZXing Wi-Fi](https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11).

Ejemplo de contacto:

```json
{
  "version":"4.0", "formatted_name":"Ada Lovelace",
  "first_name":"Ada", "last_name":"Lovelace", "organization":"Example",
  "phones":[{"value":"+390123456789","type":"work,voice","preferred":true,"label":"Office"}],
  "emails":[{"value":"ada@example.org","type":"work"}],
  "urls":["https://example.org"],
  "addresses":[{"street":"Example Street 1","city":"Milano","postal_code":"20100","country":"Italy","type":"work"}],
  "social_profiles":[{"value":"https://www.linkedin.com/in/example","type":"linkedin"}],
  "birthday":"1815-12-10", "categories":["Work","Research"], "note":"Example contact"
}
```

Campos adicionales: `prefix`, `middle_name`, `suffix`, `nickname`, `department`, `title`, `role`, `anniversary`, `gender` (M/F/O/N/U), `language`, `timezone`, `uid`, `photo_url`, `latitude`, `longitude`. Las fechas usan YYYY-MM-DD. Las direcciones también admiten `po_box`, `extended`, `region`, `label`, `preferred`. Las entradas repetidas de teléfono/correo/URL/redes sociales admiten `value`, `type`, `label`, `preferred`, con hasta 20 entradas por lista. También se aceptan entradas de cadenas simples. vCard 3.0 es el predeterminado; 4.0 usa parámetros de preferencia moderna y valor de texto. El plegado de líneas UTF-8 y el escape del texto siguen [vCard](https://www.rfc-editor.org/rfc/rfc6350). Las etiquetas personalizadas usan propiedades X-ABLabel agrupadas; la compatibilidad con los campos opcionales depende del programa lector.

La decodificación revela el texto almacenado y clasifica los enlaces, Wi-Fi, vCard y JSON. No puede recuperar el generador, la configuración original, la foto de origen ni el contenido detrás de un URL. `qrcode-to-json` devuelve el JSON original cuando se encuentra un símbolo JSON; de lo contrario, devuelve `{ "count": ..., "codes": [...] }` con texto sin procesar y campos interpretados.

Formas de módulo: `shape=square` (predeterminada), `shape=rounded` o `shape=dots`. La forma seleccionada se aplica a los módulos de datos y de corrección de errores en las exportaciones PNG y SVG. Los marcadores de búsqueda se mantienen cuadrados por defecto y pueden usar esquinas redondeadas con `corner_style=rounded`. Los patrones de alineación, temporización y otras funciones se mantienen cuadrados. Las dimensiones de PNG aún siguen a `scale` y `border`.

La exportación JPEG (`format=jpeg`) está disponible con todas las formas del módulo y un fondo sólido. Usa PNG o SVG cuando se necesite transparencia.

Elige `corner_style=square` (predeterminado) o `rounded` para los tres patrones de posición, independientemente de la forma de los módulos. Añade un elemento central con `overlay_type=text` y `overlay_text` (1–16 caracteres), o con `overlay_type=image` y `overlay_image_base64` (PNG/JPEG en base64, hasta 2 MiB y 4 millones de píxeles). `overlay_size` representa el 10–20 por ciento del símbolo QR, con 16 como valor predeterminado. Los elementos centrales fuerzan la corrección de errores H. El renderizador encuentra un área central que contiene solo datos y puede reducir o desplazar ligeramente el elemento para conservar los patrones funcionales. El elemento tiene un fondo claro incluso en las exportaciones transparentes. Todas estas opciones funcionan con PNG, JPEG y SVG.
