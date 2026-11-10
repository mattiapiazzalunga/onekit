<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# रेगुलर एक्सप्रेशन जाँचें

```sh
onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"(?<word>\\w+)","flags":"g","enable_replacement":true,"replacement":"[$<word>]"}'
onekit doctor dev-regex-test
```

JSON रिपोर्ट में पैटर्न, झंडे, मैच गिनती, ट्रंचशन स्टेटस, सटीक मिलान किए गए टेक्स्ट, स्टार्ट / एंड पोजीशन, क्रमांकित कैप्चर ग्रुप और नामित समूह शामिल हैं। Unmatched समूह null हैं। स्थितियां UTF-16 कोड इकाइयों का उपयोग करती हैं, जैसा कि JavaScript करता है, इसलिए astral Unicode वर्ण दो यूनिटों पर कब्जा करते हैं। खाली वैश्विक मैच सही ढंग से आगे बढ़ते हैं, जिनमें यूनिकोड ध्वज के तहत शामिल है।

`enable_replacement` को सही करने और प्रतिस्थापन पूर्वावलोकन के लिए `replacement` की आपूर्ति करने के लिए सेट करें। समर्थित प्रतिस्थापन टोकन JavaScript स्ट्रिंग प्रतिस्थापन से मेल खाते हैं: `$$`, `$&`, `$1`-`$99`, `$<name>`, `$'` और डॉलर-plus-backtick prefix टोकन। प्रतिस्थापन कभी परीक्षण इनपुट परिवर्तित नहीं होता है। जब मैच के परिणाम truncated होते हैं, तो एक अधूरा परिणाम प्रस्तुत करने के बजाय प्रतिस्थापन को रोक दिया जाता है।
