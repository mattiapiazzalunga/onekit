<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="qr-codes"></a>
# QR कोड

<a id="standard-linear-barcodes"></a>
## मानक रेखीय बारकोड

```sh
onekit run text-to-barcode identifier.txt -o barcode.png --options '{"barcode_type":"ean13"}'
onekit run text-to-barcode identifier.txt -o barcode.svg --options '{"barcode_type":"code128","format":"svg"}'
onekit run scan-barcode photo.jpg -o decoded.json
onekit run barcode-to-text photo.jpg -o identifier.txt
```

मानक: `code128` (डिफ़ॉल्ट, 60 प्रिंट करने योग्य ASCII वर्ण तक), `code39` (48 अपरकेस अक्षर / अंक और समर्थित प्रतीकों तक, वैकल्पिक Mod-43 चेकसम नहीं), `ean13` (12 अंक या 13 सहित चेकसूम) , `ean8` (7/8), `upca` (11/12), `itf` (अंकों की सम संख्या, 80 तक) `isbn13` (EAN-13 978/979 शुरू). आपूर्ति खुदरा चेक अंक सही होना चाहिए; वे चुपचाप बदल नहीं रहे हैं। Omitted अंकों की गणना की जाती है। पहचानकर्ता को OneKit द्वारा सौंपा या पंजीकृत नहीं किया गया है।

`python -m pip install "onekit-tools[qrcode]"` स्थापित करें। सभी QR प्रसंस्करण स्थानीय है और निर्भरता के बाद ऑफ़लाइन काम करता है। QR पीढ़ी Segno का उपयोग करती है; CLI स्कैनिंग ZXing-C++ और Pillow का उपयोग करता है।

| उपकरण | इनपुट | उत्पादन |
| --- | --- | --- |
| `text-to-qrcode` | UTF-8 TXT | PNG या SVG |
| `url-to-qrcode` | TXT एक HTTP (S) युक्त URL | PNG या SVG |
| `wifi-to-qrcode` | Wi-Fi JSON | PNG या SVG |
| `vcard-to-qrcode` | संपर्क JSON या मौजूदा VCF | PNG या SVG |
| `scan-qrcode` | PNG,JPEG, WebP, BMP या GIF | JSON रिपोर्ट |
| `reverse-qrcode` | QR छवि | JSON में कच्ची और व्याख्या की गई सामग्री |
| `qrcode-to-text` | QR छवि | सटीक संग्रहित पाठ |
| `qrcode-to-json` | QR छवि | मूल JSON मान, या अन्य पेलोड के लिए एक रिपोर्ट |

```sh
onekit run text-to-qrcode message.txt -o code.png
onekit run url-to-qrcode link.txt -o code.svg --options '{"format":"svg","error_correction":"Q"}'
onekit run wifi-to-qrcode network.json -o wifi.png
onekit run vcard-to-qrcode contact.json -o output/ --options '{"include_payload":true}'
onekit run scan-qrcode photo.jpg -o decoded.json
onekit run qrcode-to-json code.png -o recovered.json
```

जनरेशन विकल्प: `format` (`png`/`svg`), `error_correction` (`L`/`M`/`Q`/`H`), `scale` (2-16 पिक्सेल प्रति मॉड्यूल), `border` (4-16 मॉड्यूल), `dark` और `light` (छह अंक हेक्स, विपरीत ≥4.5:1), और `include_payload` (भी निर्यात कोडित TXT/JSON/VCF)। डिफ़ॉल्ट: PNG, M, स्केल 8, सीमा 4, सफेद पर काला। प्रिंट के लिए SVG स्केल। इनपुट 16 KiB तक सीमित है, लेकिन QR क्षमता छोटी है और सुधार पर निर्भर करती है; oversized संपर्कों या कम सुधार को छोटा करें। फोटो यूआरएल को छवि प्राप्त किए बिना संग्रहीत किया जाता है।

Wi-Fi उदाहरण:

```json
{"ssid":"Guest Wi-Fi","security":"WPA","password":"example-password","hidden":false}
```

सुरक्षा: `WPA` (WPA/WPA2 व्यक्तिगत), `WEP`, `nopass` (open), `SAE` (WPA3), `WPA2-EAP` (enterprise). एंटरप्राइज में `identity`, `anonymous_identity`, `eap`, `phase2` शामिल हैं। WPA3 और उद्यम समर्थन फोन द्वारा भिन्न होता है। पासवर्ड QR पेलोड में पठनीय रहते हैं। विशेष वर्ण [ZXing Wi-Fi escaping convention](https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11) का उपयोग करते हैं।

उदाहरण के लिए:

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

अतिरिक्त फ़ील्ड: `prefix`, `middle_name`, `suffix`, `nickname`, `department`, `title`, `role`, `anniversary`, `gender` (M/F/O/N/U) `language`, `timezone`, `uid`, `photo_url`, `latitude`, `longitude`. तिथियों का उपयोग YYYY-MM-DD। पता भी समर्थन `po_box`, `extended`, `region`, `label`, `preferred`. बार-बार फोन/ईमेल/URL/सामाजिक प्रविष्टियां स्वीकार करती हैं `value`, `type`, `label`, `preferred`, प्रति सूची 20 प्रविष्टियों तक। सरल स्ट्रिंग प्रविष्टियों को भी स्वीकार किया जाता है। vCard 3.0 डिफ़ॉल्ट है; 4.0 आधुनिक वरीयता और पाठ-मूल्य मापदंडों का उपयोग करता है। UTF-8 तह और पाठ escaping पालन [vCard](https://www.rfc-editor.org/rfc/rfc6350). कस्टम लेबल समूहीकृत X-ABLabel गुणों का उपयोग करते हैं; वैकल्पिक फ़ील्ड पाठक पर निर्भर करती हैं।

रिवर्स संग्रहीत पाठ को प्रकट करता है और लिंक, Wi-Fi, vCard और JSON को वर्गीकृत करता है। यह एक URL के पीछे जनरेटर, मूल सेटिंग्स, स्रोत फोटो या सामग्री को ठीक नहीं कर सकता है। `qrcode-to-json` मूल JSON लौटता है जब एक JSON प्रतीक पाया जाता है; अन्यथा यह कच्चे पाठ और व्याख्या वाले क्षेत्रों के साथ `{ "count": ..., "codes": [...] }` वापस आता है।

मॉड्यूल आकार: `shape=square` (डिफ़ॉल्ट), `shape=rounded`, या `shape=dots`। चयनित आकार PNG और SVG निर्यात में डेटा और त्रुटि सुधार मॉड्यूल पर लागू होता है। खोजक मार्कर डिफ़ॉल्ट रूप से वर्ग रहते हैं और `corner_style=rounded` के साथ गोल कोनों का उपयोग कर सकते हैं। संरेखण, समय और अन्य कार्य पैटर्न वर्ग रहते हैं। PNG आयाम अभी भी `scale` और `border` का पालन करें।

JPEG निर्यात (`format=jpeg`) सभी मॉड्यूल आकार और एक ठोस पृष्ठभूमि के साथ उपलब्ध है। जब पारदर्शिता की आवश्यकता होती है तो PNG या SVG का उपयोग करें।

मॉड्यूल आकार से स्वतंत्र रूप से तीन खोजक मार्करों के लिए `corner_style=square` (डिफ़ॉल्ट) या `rounded` चुनें। `overlay_type=text` और `overlay_text` (1-16 वर्ण), या `overlay_type=image` और `overlay_image_base64` (a base64 PNG/JPEG, 2 MiB और 4 मिलियन पिक्सेल तक) के साथ एक केंद्र चिन्ह जोड़ें। `overlay_size` QR प्रतीक, डिफ़ॉल्ट 16 का 10-20 प्रतिशत है। केंद्र के निशान एच त्रुटि सुधार को मजबूर करते हैं। रेंडर एक केंद्रीय डेटा-केवल क्षेत्र को पाता है और फ़ंक्शन पैटर्न को संरक्षित करने के लिए चिह्न को सिकुड़ या थोड़ा बदल सकता है। चिह्न में पारदर्शी निर्यात के लिए भी प्रकाश समर्थन है। ये सभी विकल्प PNG, JPEG और SVG के साथ काम करते हैं।
