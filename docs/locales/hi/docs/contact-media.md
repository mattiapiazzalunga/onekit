<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="contacts-image-enlargement-and-local-media-tools"></a>
# संपर्क, छवि विस्तार और स्थानीय मीडिया उपकरण

| उपकरण | इनपुट | विकल्प | उत्पादन |
| --- | --- | --- | --- |
| `vcard-generate` | संपर्क करें JSON, जैसा कि `vcard-to-qrcode` के लिए है | संपर्क क्षेत्र इनपुट JSON से संबंधित हैं | VCF 3.0 / 4.0 |
| `qrcode-to-vcard` | QR छवि एक पूर्ण vCard युक्त | कोई नहीं | एक VCF प्रति पता लगाया संपर्क |
| `image-upscale` | एकल फ्रेम छवि | `scale`: 2 (डिफ़ॉल्ट), 3 या 4 | PNG |
| `image-remove-background` | एकल फ्रेम छवि | कोई नहीं | पारदर्शक PNG |
| `video-compress` | वीडियो | `compression_level`: प्रकाश, संतुलित (डिफ़ॉल्ट), अधिकतम | MP4, या मूल यदि छोटा |
| `video-speed` | वीडियो | `speed`: 0.25-4, डिफ़ॉल्ट 2 | सिंक्रनाइज़, पिच संरक्षित ऑडियो के साथ MP4 |
| `video-to-gif` | वीडियो | `start`: सेकंड, `duration`: 0.1-30, `fps`: 1-30, `width`: 64-1280 | बिना ऑडियो के लूपिंग GIF |
| `audio-to-text` | ऑडियो | `language`: ऑटो (डिफ़ॉल्ट), यह एन या किसी अन्य व्हिस्पर भाषा कोड | TXT और टाइमस्टैम्प JSON |

केवल Python अतिरिक्त की जरूरत स्थापित करें:

```sh
python -m pip install 'onekit-tools[qrcode,images,background,transcription]'
```

वीडियो संचालन के लिए PATH पर `ffmpeg` और `ffprobe` की भी आवश्यकता है। CLI स्थापित FFmpeg निर्माण का उपयोग करता है; समर्थित कोडेक उस बिल्ड पर निर्भर करते हैं। `onekit doctor TOOL` आवश्यक इंजन और पैकेज की जांच करता है।

```sh
onekit run vcard-generate contact.json -o contact.vcf
onekit run qrcode-to-vcard contact-qr.png -o contacts/
onekit run image-upscale photo.png --options '{"scale":2}' -o larger.png
onekit run image-remove-background portrait.jpg -o transparent.png
onekit run video-compress clip.mov --options '{"compression_level":"balanced"}' -o compressed/
onekit run video-speed clip.mp4 --options '{"speed":0.5}' -o slower.mp4
onekit run video-to-gif clip.mp4 --options '{"start":1,"duration":3,"fps":12,"width":480}' -o clip.gif
onekit run audio-to-text voice.wav --options '{"language":"it"}' -o transcript/
```

JSON उदाहरण से संपर्क करें:

```json
{"first_name":"Ada","last_name":"Lovelace","version":"3.0","emails":["ada@example.org"]}
```

QR निष्कर्षण एक प्रदर्शन नाम के साथ पूरा vCard 3.0 / 4.0 पेलोड स्वीकार करता है। यह कॉन्टैक्ट डाउनलोड URL का पालन नहीं करता है और न ही मनमाने QR टेक्स्ट को संपर्क डेटा में परिवर्तित करता है। Upscaling Lanczos resampling, एक AI मॉडल नहीं का उपयोग करता है। आउटपुट 40 मिलियन पिक्सेल तक सीमित है। एनिमेटेड छवियों को Python छवि एडाप्टर द्वारा अस्वीकार कर दिया गया है।

CLI पृष्ठभूमि एडाप्टर सीधे ONNX रनटाइम के साथ U2Net लोड करता है, जो रीम्बग की Pillow <13 निर्भरता बाधा से बचने में मदद करता है। मॉडल डाउनलोड स्थानीय OneKit मॉडल कैश के तहत चेकसम सत्यापित और कैश किए गए हैं। वैकल्पिक मॉडल इंजन पोर्टेबल `all` अतिरिक्त से अलग रहते हैं।
