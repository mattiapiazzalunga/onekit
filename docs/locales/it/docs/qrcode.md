<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="qr-codes"></a>
# Codici QR

<a id="standard-linear-barcodes"></a>
## Standard linear barcodes

```sh
onekit run text-to-barcode identifier.txt -o barcode.png --options '{"barcode_type":"ean13"}'
onekit run text-to-barcode identifier.txt -o barcode.svg --options '{"barcode_type":"code128","format":"svg"}'
onekit run scan-barcode photo.jpg -o decoded.json
onekit run barcode-to-text photo.jpg -o identifier.txt
```

Standard: `code128` (predefinito, fino a 60 caratteri stampabili ASCII), `code39` (fino a 48 lettere maiuscole/cifre e simboli supportati, senza checksum facoltativo Mod-43), `ean13` (12 cifre o 13 incluso checksum), `ean8` (7/8), `upca` (11/12), `itf` (un numero pari di cifre, fino a 80), `isbn13` (EAN-13 iniziando 978/979). Le cifre di controllo retail fornite devono essere corrette; non vengono mai sostituite silenziosamente. Le cifre omesse vengono calcolate. Gli identificatori non sono assegnati o registrati da OneKit.

Installa `python -m pip install "onekit-tools[qrcode]"`. Tutto il processamento QR è locale e funziona offline dopo l'installazione delle dipendenze. La generazione QR usa Segno; la scansione CLI usa ZXing-C++ e Pillow.

| Strumento | Input | Output |
| --- | --- | --- |
| `text-to-qrcode` | UTF-8 TXT | PNG o SVG |
| `url-to-qrcode` | TXT contenente un HTTP(S) URL | PNG o SVG |
| `wifi-to-qrcode` | Wi-Fi JSON | PNG o SVG |
| `vcard-to-qrcode` | Contatta JSON o VCF esistente | PNG o SVG |
| `scan-qrcode` | PNG, JPEG, WebP, BMP o GIF | JSON rapporto |
| `reverse-qrcode` | Immagine QR | Contenuti grezzi e interpretati in JSON |
| `qrcode-to-text` | Immagine QR | Testo esattamente salvato |
| `qrcode-to-json` | Immagine QR | Valore originale JSON, o un report per altri payload |

```sh
onekit run text-to-qrcode message.txt -o code.png
onekit run url-to-qrcode link.txt -o code.svg --options '{"format":"svg","error_correction":"Q"}'
onekit run wifi-to-qrcode network.json -o wifi.png
onekit run vcard-to-qrcode contact.json -o output/ --options '{"include_payload":true}'
onekit run scan-qrcode photo.jpg -o decoded.json
onekit run qrcode-to-json code.png -o recovered.json
```

Opzioni di generazione: `format` (`png`/`svg`), `error_correction` (`L`/`M`/`Q`/`H`), `scale` (2–16 pixel per modulo), `border` (4–16 moduli), `dark` e `light` (esadecimale a sei cifre, contrasto ≥4.5:1), e `include_payload` (esporta anche TXT/JSON/VCF codificati). Predefiniti: PNG, M, scala 8, bordo 4, nero su bianco. SVG scala per la stampa. L'input è limitato a 16 KiB, ma la capacità di QR è minore e dipende dalla correzione; ridurre i contatti troppo grandi o abbassare la correzione. Gli URL delle foto sono memorizzati senza recuperare l'immagine.

Esempio Wi-Fi:

```json
{"ssid":"Guest Wi-Fi","security":"WPA","password":"example-password","hidden":false}
```

Sicurezza: `WPA` (WPA/WPA2 personale), `WEP`, `nopass` (aperto), `SAE` (WPA3), `WPA2-EAP` (azienda). L'azienda aggiunge `identity`, `anonymous_identity`, `eap`, `phase2`. Il supporto per WPA3 e aziendale varia a seconda del telefono. Le password rimangono leggibili nel payload QR. I caratteri speciali usano la convenzione di escape [ZXing Wi-Fi](https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11).

Esempio di contatto:

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

Campi aggiuntivi: `prefix`, `middle_name`, `suffix`, `nickname`, `department`, `title`, `role`, `anniversary`, `gender` (M/F/O/N/U), `language`, `timezone`, `uid`, `photo_url`, `latitude`, `longitude`. Le date usano il formato YYYY-MM-DD. Gli indirizzi supportano anche `po_box`, `extended`, `region`, `label`, `preferred`. Le voci ripetute di telefono/email/URL/social accettano `value`, `type`, `label`, `preferred`, con un massimo di 20 voci per lista. Sono accettate anche voci semplici di testo. vCard 3.0 è il formato predefinito; 4.0 usa le preferenze moderne e i parametri di valore di testo. Il ripiegamento delle righe UTF-8 e l’escape del testo seguono [vCard](https://www.rfc-editor.org/rfc/rfc6350). Le etichette personalizzate usano le proprietà X-ABLabel raggruppate; il supporto dei campi facoltativi dipende dal programma che legge i contatti.

La decodifica rivela il testo memorizzato e classifica i collegamenti, Wi-Fi, vCard e JSON. Non può recuperare il generatore, le impostazioni originali, la foto originale o il contenuto dietro un URL. `qrcode-to-json` restituisce il JSON originale quando viene trovato un simbolo JSON; altrimenti restituisce `{ "count": ..., "codes": [...] }` con testo grezzo e campi interpretati.

Forme dei moduli: `shape=square` (predefinita), `shape=rounded` o `shape=dots`. La forma selezionata si applica ai moduli di dati e di correzione degli errori nelle esportazioni PNG e SVG. I marker del finder rimangono quadrati per impostazione predefinita e possono avere angoli arrotondati con `corner_style=rounded`. I pattern di allineamento, temporizzazione e altre funzioni rimangono quadrati. Le dimensioni PNG seguono ancora `scale` e `border`.

L’esportazione JPEG (`format=jpeg`) è disponibile con tutte le forme del modulo e uno sfondo solido. Usa PNG o SVG quando è necessaria la trasparenza.

Scegli `corner_style=square` (predefinito) o `rounded` per i tre marcatori di rilevamento, indipendentemente dalla forma dei moduli. Aggiungi un elemento centrale con `overlay_type=text` e `overlay_text` (1–16 caratteri), oppure `overlay_type=image` e `overlay_image_base64` (PNG/JPEG in base64, fino a 2 MiB e 4 milioni di pixel). `overlay_size` è il 10–20 percento del simbolo QR, con valore predefinito 16. Gli elementi centrali impongono la correzione degli errori H. Il renderer individua un’area centrale contenente solo dati e può ridurre o spostare leggermente l’elemento per preservare i pattern funzionali. L’elemento ha uno sfondo chiaro anche nelle esportazioni trasparenti. Tutte queste opzioni funzionano con PNG, JPEG e SVG.
