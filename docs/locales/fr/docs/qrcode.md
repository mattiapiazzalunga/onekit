<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="qr-codes"></a>
# Codes QR

<a id="standard-linear-barcodes"></a>
## Standard linear barcodes

```sh
onekit run text-to-barcode identifier.txt -o barcode.png --options '{"barcode_type":"ean13"}'
onekit run text-to-barcode identifier.txt -o barcode.svg --options '{"barcode_type":"code128","format":"svg"}'
onekit run scan-barcode photo.jpg -o decoded.json
onekit run barcode-to-text photo.jpg -o identifier.txt
```

Normes : `code128` (par défaut, jusqu'à 60 caractères imprimables ASCII), `code39` (jusqu'à 48 lettres majuscules/chiffres et symboles pris en charge, pas de Mod-43 facultatif de contrôle), `ean13` (12 chiffres ou 13 y compris le contrôle), `ean8` (7/8), `upca` (11/12), `itf` (un nombre pair de chiffres, jusqu'à 80), `isbn13` (EAN-13 commençant 978/979). Les chiffres de contrôle fournis par le commerce doivent être corrects ; ils ne sont jamais remplacés silencieusement. Les chiffres omis sont calculés. Les identifiants ne sont pas attribués ni enregistrés par OneKit.

Installez `python -m pip install "onekit-tools[qrcode]"`. Tout le traitement QR est local et fonctionne hors ligne après l'installation des dépendances. La génération QR utilise Segno ; le scan CLI utilise ZXing-C++ et Pillow.

| Outil | Entrée | Sortie |
| --- | --- | --- |
| `text-to-qrcode` | UTF-8 TXT | PNG ou SVG |
| `url-to-qrcode` | TXT contenant un HTTP(S) URL | PNG ou SVG |
| `wifi-to-qrcode` | Wi-Fi JSON | PNG ou SVG |
| `vcard-to-qrcode` | Contacter JSON ou VCF existant | PNG ou SVG |
| `scan-qrcode` | PNG, JPEG, WebP, BMP ou GIF | JSON rapport |
| `reverse-qrcode` | Image QR | Contenu brut et interprété dans JSON |
| `qrcode-to-text` | Image QR | Texte exact stocké |
| `qrcode-to-json` | Image QR | Valeur originale JSON, ou un rapport pour d'autres charges. |

```sh
onekit run text-to-qrcode message.txt -o code.png
onekit run url-to-qrcode link.txt -o code.svg --options '{"format":"svg","error_correction":"Q"}'
onekit run wifi-to-qrcode network.json -o wifi.png
onekit run vcard-to-qrcode contact.json -o output/ --options '{"include_payload":true}'
onekit run scan-qrcode photo.jpg -o decoded.json
onekit run qrcode-to-json code.png -o recovered.json
```

Options de génération : `format` (`png`/`svg`), `error_correction` (`L`/`M`/`Q`/`H`), `scale` (2–16 pixels par module), `border` (4–16 modules), `dark` et `light` (hexadécimal à six chiffres, contraste ≥4.5:1), et `include_payload` (exporte aussi les TXT/JSON/VCF encodés). Par défaut : PNG, M, échelle 8, bordure 4, noir sur blanc. SVG s'adapte pour l'impression. L'entrée est limitée à 16 KiB, mais la capacité QR est plus petite et dépend de la correction ; raccourcissez les contacts trop grands ou réduisez la correction. Les URLs des photos sont stockées sans récupérer l'image.

Exemple Wi-Fi :

```json
{"ssid":"Guest Wi-Fi","security":"WPA","password":"example-password","hidden":false}
```

Sécurité : `WPA` (WPA/WPA2 personnel), `WEP`, `nopass` (ouvert), `SAE` (WPA3), `WPA2-EAP` (entreprise). L’entreprise ajoute `identity`, `anonymous_identity`, `eap`, `phase2`. WPA3 et le support entreprise varient selon le téléphone. Les mots de passe restent lisibles dans la charge utile QR. Les caractères spéciaux utilisent la convention d’échappement [ZXing Wi-Fi](https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11).

Exemple de contact :

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

Champs supplémentaires : `prefix`, `middle_name`, `suffix`, `nickname`, `department`, `title`, `role`, `anniversary`, `gender` (M/F/O/N/U), `language`, `timezone`, `uid`, `photo_url`, `latitude`, `longitude`. Les dates utilisent le format YYYY-MM-DD. Les adresses prennent également en charge `po_box`, `extended`, `region`, `label`, `preferred`. Les entrées répétées de téléphone/e-mail/URL/réseaux sociaux acceptent `value`, `type`, `label`, `preferred`, avec jusqu'à 20 entrées par liste. Les entrées simples de chaînes de caractères sont également acceptées. vCard 3.0 est la valeur par défaut ; 4.0 utilise les préférences modernes et les paramètres de valeur de texte. Le repliement des lignes UTF-8 et l’échappement du texte suivent [vCard](https://www.rfc-editor.org/rfc/rfc6350). Les étiquettes personnalisées utilisent les propriétés X-ABLabel groupées ; la prise en charge des champs facultatifs dépend du logiciel de lecture.

L'inversion révèle le texte stocké et classe les liens, Wi-Fi, vCard et JSON. Elle ne peut pas récupérer le générateur, les paramètres d'origine, la photo source ou le contenu derrière un URL. `qrcode-to-json` renvoie le JSON d'origine lorsqu'un symbole JSON est trouvé ; sinon, il renvoie `{ "count": ..., "codes": [...] }` avec le texte brut et les champs interprétés.

Formes de module : `shape=square` (par défaut), `shape=rounded` ou `shape=dots`. La forme sélectionnée s'applique aux modules de données et de correction d'erreurs dans les exports PNG et SVG. Les marqueurs de repérage restent carrés par défaut et peuvent utiliser des coins arrondis avec `corner_style=rounded`. Les motifs d'alignement, de synchronisation et autres fonctions restent carrés. Les dimensions PNG suivent toujours `scale` et `border`.

L'exportation JPEG (`format=jpeg`) est disponible avec toutes les formes du module et un arrière-plan uni. Utilisez PNG ou SVG lorsque la transparence est nécessaire.

Choisissez `corner_style=square` (par défaut) ou `rounded` pour les trois repères de positionnement, indépendamment de la forme des modules. Ajoutez un élément central avec `overlay_type=text` et `overlay_text` (1–16 caractères), ou `overlay_type=image` et `overlay_image_base64` (PNG/JPEG en base64, jusqu’à 2 MiB et 4 millions de pixels). `overlay_size` représente 10–20 pour cent du symbole QR, avec 16 par défaut. Les éléments centraux imposent la correction d’erreurs H. Le moteur trouve une zone centrale contenant uniquement des données et peut réduire ou décaler légèrement l’élément pour préserver les motifs fonctionnels. L’élément conserve un fond clair même dans les exports transparents. Toutes ces options fonctionnent avec PNG, JPEG et SVG.
