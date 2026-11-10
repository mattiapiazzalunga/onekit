<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->

भाषाएँ: [English](../../../README.md) · [Italiano](../it/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Deutsch](../de/README.md) · [Русский](../ru/README.md) · [中文](../zh/README.md) · [Português](../pt/README.md) · [हिन्दी](README.md).

<p align="center">
  <a href="https://onekit.org"><img src="https://raw.githubusercontent.com/mattiapiazzalunga/onekit/main/images/logo.png" alt="OneKit logo" width="112" height="112"></a>
</p>
<h1 align="center">OneKit</h1>
<p align="center">एक आसान टूलकिट। आपकी फ़ाइलें आपकी ही रहती हैं।</p>
<p align="center"><a href="https://github.com/mattiapiazzalunga/onekit/stargazers"><img alt="GitHub सितारों" src="https://img.shields.io/github/stars/mattiapiazzalunga/onekit"></a> <a href="https://pypi.org/project/onekit-tools/"><img alt="PyPI" src="https://img.shields.io/pypi/v/onekit-tools"></a> <img alt="PolyForm-Shield-1.0.0" src="https://img.shields.io/badge/license-PolyForm_Shield_1.0.0-blue"> <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue"></p>

एक ऑफलाइन Python उपकरण किट के साथ 230 उपकरणों के लिए रूपांतरण, पीडीएफ, छवियों, अभिलेखागार, फ़ॉन्ट्स, फ़ाइल निरीक्षण, एन्क्रिप्शन, डेवलपर उपयोगिताएँ, OCR और तुलना इसका प्रयोग करें CLI या ***** पर चित्रमय इंटरफ़ेस[onekit.org](https://onekit.org)**.

** स्रोत संस्करण:* `0.6.3` रिलीज वर्कफ़्लो पूरा होने के बाद ही स्थिर डाउनलोड मौजूद हैं। वितरण `onekit-tools` है; अलग से स्वामित्व वाली PyPI परियोजना जिसे `onekit` कहा जाता है, असंबंधित है।

[ संपर्क और मीडिया गाइड](docs/contact-media.md) स्टैंडअलोन vCard पीढ़ी, QR-to-vCard निष्कर्षण, छवि upscaling, पृष्ठभूमि हटाने, वीडियो संपीड़न/गति/GIF और स्थानीय ऑडियो transcription शामिल हैं।

[एंड्रॉयड पैकेज और स्वचालित चेहरा धुंधला](docs/android-and-face-tools.md) देखें।

लाइसेंस जांच: निरीक्षण PDF, Word, PowerPoint, Excel, वीडियो, ऑडियो, चित्र, फ़ॉन्ट्स, EPUBफाइलों या सार्वजनिक यूआरएल से कोड/प्रोजेक्ट्स और डेटासेट। विश्लेषण स्थानीय रहता है; रिपोर्ट्स ** अनधिकृत अनुमान हैं, स्वामित्व प्रमाण पत्र या उपयोग करने की अनुमति नहीं*। देखें [लाइसेंस चेक उपयोग और सीमा](docs/cli.md#local-license-and-copyright-estimates).

**आपका CLI आपका एजेंटिक CLI.* अपने आप में OneKit का उपयोग करें या स्थानीय AI एजेंट को टर्मिनल या सबप्रोसेस के माध्यम से कॉल करें। JSON के रूप में उपकरण और आवश्यकताओं की खोज करें, एक्सप्लिकिट इनपुट / आउटपुट पथ पास करें और दोहराए जाने योग्य फ़ाइल कार्यों के लिए `.1kit` वर्कफ़्लोज़ को पुनः उपयोग करें। [local एजेंट और स्वचालन](docs/cli.md#local-agents-and-automation) देखें।

<a id="install"></a>
## इंस्टॉल करें

Python 3.11+ की आवश्यकता है। यूनिवर्सल wheel x64/ARM64 पर Windows, macOS और Linux का समर्थन करता है। वैकल्पिक मूल पुस्तकालयों और बाहरी इंजनों में अतिरिक्त प्लेटफ़ॉर्म आवश्यकताएं होती हैं।

प्रकाशन के बाद:

```sh
python -m pip install onekit-tools
python -m pip install "onekit-tools[pdf,images,documents]"
onekit list
onekit doctor
```

एक स्रोत चेकआउट से:

```sh
python -m pip install -e ".[all,test]"
python -m onekit --help
python -m pytest -q
```

आधार CLI में ** कोई रनटाइम निर्भरता* नहीं है। केवल वही अतिरिक्त आप की जरूरत है। `all` में मानक Python परिवार शामिल हैं; वीडियो डाउनलोडिंग, पृष्ठभूमि हटाने, ट्रांसक्रिप्शन और क्रिप्टोग्राफिक हस्ताक्षर अलग `video`, `background`, `transcription` और `signing` एक्स्ट्रा का उपयोग करते हैं। अलग से मूल इंजन स्थापित करें। नोड-आधारित डेवलपर टूल के लिए, Node.js 24+ स्थापित करें और `onekit engines install` चलाएं। CLI पहली बार उपयोग पर लापता निर्भरता और बाहरी इंजन तैयार करता है। पहले उपयोग पर पृष्ठभूमि हटाने और ट्रांसक्रिप्शन डाउनलोड मॉडल भार, फिर स्थानीय कैश का पुन: उपयोग करें।

<a id="use"></a>
## उपयोग

```sh
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit run pdf-extract-pages document.pdf --options '{"pages":"1,3-5"}' -o selected.pdf
onekit run image-convert image.png --options '{"format":"webp"}' -o image.webp
onekit run diff-notebook before.ipynb after.ipynb --options '{"mode":"code"}' -o changes.json
onekit run security-encrypt private-folder --ask-password -o private.zip
onekit run security-decrypt private.zip --ask-password -o restored
```

विकल्प JSON ऑब्जेक्ट हैं; उन्हें एक उद्धृत शेल तर्क के रूप में पास करें। रहस्यों के लिए `--ask-password` का उपयोग करें। मौजूदा आउटपुट को तब तक संरक्षित किया जाता है जब तक कि आप `--force` पास नहीं करते।

`onekit list --group pdf`, `onekit list --json` और `onekit doctor TOOL_ID` अनुबंध और आवश्यकताओं को उजागर करना। प्रत्येक उपकरण में एक निर्देशिका है [उपकरण](../../../tools)मेटाडाटा और इसके साझा कार्यान्वयन के लिए एक सूचक युक्त,। देखें [CLI गाइड](docs/cli.md) विकल्प और सीमा के लिए।

<a id="toolkit"></a>
## टूलकिट

| परिवार | क्षमता |
| --- | --- |
| कन्वर्टर्स | Markdown, HTML, LaTeX, PDF, Word, PowerPoint, छवियों, Base64, Excel, CSV और JSON |
| PDF | Merge/split, पृष्ठ चयन/order/removal, संपीड़न, मरम्मत, [direct text edit](docs/pdf-editing.md), टेक्स्ट ओवरले, रोटेशन, डिजिटल हस्ताक्षर, एन्क्रिप्शन/unlock, [local PDF/A रूपांतरण/validation](docs/pdfa.md) |
| चित्र | एम्बेडेड PDF छवियों, संपीड़न, क्रॉप और परिवर्तन प्रारूप निकालें |
| मीडिया | अलग से स्थापित FFmpeg के माध्यम से ऑडियो/वीडियो रूपांतरण |
| अभिलेखागार / फ़ॉन्ट्स | ZIP/TAR वेरिएंट; TTF/OTF कंटेनर और WOFF/WOFF2 |
| निरीक्षक / सुरक्षा | प्रकार हस्ताक्षर, संरचना, मेटाडाटा, एन्कोडिंग, हैश, पाठ गिनती; प्रमाणित एन्क्रिप्टेड फ़ाइल / फ़ोल्डर अभिलेखागार |
| डेवलपर | भाषा-विशिष्ट स्वरूपण, पार्सर / कंप्यूटर सत्यापन और चयनित minification |
| OCR | स्कैन किए गए चित्र/PDF to searchable PDF, Word, Markdown, LaTeX, HTML और JSON |
| डिफ | पाठ, कोड, सामान्यीकृत JSON, नोटबुक, LaTeX, PDF और Word टेक्स्ट |

<a id="pipelines-and-development"></a>
## वर्कफ़्लो और विकास

`onekit pipeline --steps workflow.1kit INPUTS -o OUTPUT` एक संस्करण `.1kit` वर्कफ़्लो दस्तावेज़ स्वीकार करता है। प्रत्येक चरण को पूर्व आउटपुट प्राप्त होता है। एकाधिक आउटपुट पर सिंगल-इनपुट चरण मानचित्र; विलय कदम संग्रह प्राप्त करते हैं। Incompatible प्रकार रोक प्रसंस्करण।

बग और सुझाव के माध्यम से रिपोर्ट करें [GitHub मुद्दे](https://github.com/mattiapiazzalunga/onekit/issues) या [वेबसाइट अनुरोध बोर्ड](https://onekit.org/requests/). योगदानकर्ता किसी भी स्थान पर काम कर सकते हैं।

<a id="contribute-to-onekit"></a>
## OneKit में योगदान दें

OneKit के खुले क्रांति का निर्माण करने में मदद करें: हर किसी के लिए रोज़मर्रा के उपकरण, हाथों पर काम करने वाले कार्यों से स्थानीय AI एजेंटों द्वारा चलाए जाने वाले वर्कफ़्लोज़ तक। उपकरण को अधिक कुशल और प्रभावी बनाने में योगदान: गति और मेमोरी उपयोग में सुधार, गलत परिणाम ठीक करें, प्रतिगमन उदाहरण जोड़ें, या दस्तावेज़ीकरण और एजेंट वर्कफ़्लो को स्पष्ट करें।

कोर ओपन सोर्स है ()PolyForm Shield 1.0.0). पढ़िए [योगदान गाइड](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) और में एक कार्य खोजने [GitHub मुद्दे](https://github.com/mattiapiazzalunga/onekit/issues), या सुझाव दें कि सुधार पर [अनुरोध बोर्ड](https://onekit.org/requests/).

<a id="license-and-creator"></a>
## लाइसेंस और निर्माता

** द्वारा बनाया गया[Mattia Piazzalunga](mailto:hello@mattiapiazzalunga.com)**. कॉपीराइट © 2026 Mattia Piazzalunga. ओपन सोर्स (Open Source)PolyForm Shield 1.0.0), नीचे लाइसेंस प्राप्त [PolyForm Shield 1.0.0](../../../LICENSE); देखें [सूचना](../../../NOTICE), [AUTHORS.txt](../../../AUTHORS.txt) और [Contributors.txt](../../../CONTRIBUTORS.txt). तृतीय-पक्ष घटक अपने लाइसेंस को बनाए रखते हैं। बाह्य इंजन अपने स्वयं के पुनर्वितरण दायित्वों के साथ अलग-अलग कार्यक्रम हैं।

आप वाणिज्यिक और आंतरिक उपयोग सहित अनुमत उद्देश्यों के लिए कोर का उपयोग, संशोधित और पुनर्वितरण कर सकते हैं। आप सॉफ्टवेयर के साथ प्रतिस्पर्धा करने वाले एक उत्पाद या सेवा प्रदान करने के लिए इसका उपयोग नहीं कर सकते हैं या किसी उत्पाद के साथ लाइसेंसर या इसके सहयोगी सॉफ्टवेयर का उपयोग करके प्रदान करते हैं; मुफ्त पेशकश और विभिन्न प्लेटफार्मों या इंटरफेस भी प्रतिस्पर्धा कर सकते हैं। जब प्रतियां साझा करते हैं, तो लाइसेंस टेक्स्ट या इसके URL और सॉफ़्टवेयर के साथ आपूर्ति की गई किसी भी आवश्यक सूचना लाइन शामिल है। पूर्ण लाइसेंस नए और बंद उत्पादों, पेटेंट शर्तों और वारंटी अस्वीकरण के लिए अपने अपवाद सहित नियंत्रित करता है। यहां, "ओपन सोर्स (PolyForm Shield 1.0.0)" इन शर्तों के तहत प्रकाशित स्रोत का वर्णन करता है; गैर-प्रतियोगिता प्रतिबंध का मतलब है कि यह ओपन सोर्स डेफिनिशन के तहत अप्रतिबंधित ओपन सोर्स के बजाय स्रोत-उपलब्ध सॉफ़्टवेयर है। देखें [the लाइसेंसिंग गाइड](docs/licenses.md).

इनपुट फ़ाइलों को संसाधित किए बिना वर्कफ़्लो निर्यात और आयात करें:

```sh
onekit workflow export workflow.1kit -o exported-workflow.1kit
onekit workflow import workflow.1kit -o saved-workflow.1kit
onekit pipeline --steps saved-workflow.1kit input.json -o output.json
```

मानक बारकोड QR कोड और बारकोड श्रेणी और CLI: `text-to-barcode`, `scan-barcode`, `barcode-to-text` में उपलब्ध हैं। कोड 128, कोड 39, EAN-13, EAN-8, UPC-A, ITF और ISBN-13 समर्थन PNG/SVG, विन्यास आयाम और चेक-अंक सत्यापन। `onekit-tools[barcode]` या `onekit-tools[qrcode]` स्थापित करें।

स्थायी [PDF छवि रिडैक्शन](docs/redaction.md) माध्यम से उपलब्ध है `pdf-redact` और `image-redact`. चयनित क्षेत्र नए एन्कोडेड फ़ाइलों में ठोस ब्लैक पिक्सेल बन जाते हैं। PDF को मूल टेक्स्ट, फ़ॉर्म, टिप्पणियों, अटैचमेंट या मेटाडाटा के बिना इमेज-केवल दस्तावेज़ों के रूप में फिर से बनाया जाता है; चित्र मूल मेटाडाटा या छिपे हुए अल्फा पिक्सेल के बिना अपारदर्शी पीएनजी बन जाते हैं। मूल फ़ाइलों को अपरिवर्तित छोड़ दिया जाता है।

`pdf-watermark` के साथ विन्यास योग्य PDF टेक्स्ट वॉटरमार्क जोड़ें: अपारदर्शिता, रंग, फ़ॉन्ट्स, पृष्ठ रेंज, दृश्य स्थिति, रोटेशन और दोहराया ग्रिड। पाठ और ग्राफिक्स PDF में रहते हैं। [वाटरमार्क गाइड](docs/watermark.md) देखें।

<a id="contacts"></a>
## संपर्क

- सामान्य प्रश्न और समर्थन: [support@onekit.org](mailto:support@onekit.org).
- ओपन सोर्स (Open Source) के बारे में प्रश्नPolyForm Shield 1.0.0) कोर और योगदान: [developers@onekit.org](mailto:developers@onekit.org).
- गोपनीयता, GDPR और व्यक्तिगत डेटा अनुरोध: [privacy@onekit.org](mailto:privacy@onekit.org).
- कानूनी प्रश्न, लाइसेंसिंग और अनुमति अनुरोध: [legal@onekit.org](mailto:legal@onekit.org).
- सुरक्षा भेद्यता और दुरुपयोग रिपोर्ट: [security@onekit.org](mailto:security@onekit.org).
