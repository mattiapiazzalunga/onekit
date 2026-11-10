<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="wi-fi-to-qr-code"></a>
# Wi-Fi से QR कोड

कमान: `onekit run wifi-to-qrcode`। इनपुट और आउटपुट तर्कों के लिए `onekit run --help` का उपयोग करें।

श्रेणी: **qrcode* Fidelity: ** सटीक* स्थानीय रूप से एक मानक QR कोड बनाता है। क्षमता सामग्री और त्रुटि सुधार पर निर्भर करती है। शांत क्षेत्र रखें और मुद्रण से पहले कोड का परीक्षण करें।

स्वीकृत प्रकार: `json`। आउटपुट प्रकार: `png`। एकाधिक इनपुट स्वीकार करता है: ** नहीं*

इनपुट सत्यापन: ** टेक्स्ट* आवश्यक फ़ाइल गणना: * 1-1* CLI: ** 16,384 बाइट्स प्रति फ़ाइल*, **134,217,728 बाइट्स कुल* प्रसंस्करण से पहले सामग्री जांच चली जाती है। एक फ़ाइल का नाम बदलने के लिए अपने वास्तविक प्रारूप को नहीं बदलता है।

विकल्प: `format`, `shape`, `corner_style`, `overlay_type`, `overlay_text`, `overlay_image_base64`, `overlay_size`, `error_correction`, `scale`, `border`, `dark`, `light`, `transparent_background`, `include_payload`.

Python पैकेज: segno, Pillow। बाहरी इंजन: भाषा एडाप्टर के लिए डेवलपर इंजन मैट्रिक्स देखें।

प्रसंस्करण कार्यान्वयन: [ साझा परिवार एडाप्टर](../../../../../../src/onekit/tools/qrcode.py)। अनुबंध और प्रतिगमन जुड़नार: [tests](../../../../../../tests/test_core.py). इंजन सेटअप और लाइसेंस: [engine गाइड](../../../docs/engines.md)।

यह निर्देशिका `python scripts/tool_docs.py` तक साझा सूची से उत्पन्न होती है। रजिस्ट्री और परिवार एडाप्टर को संपादित करें, प्रतिगमन जुड़नार जोड़ें, फिर निर्देशिका को फिर से उत्पन्न करें।
