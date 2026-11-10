<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-requirements-verification"></a>
# CLI आवश्यकता सत्यापन

`tests/test_requirements.py` चेक कैटलॉग कवरेज, CLI इनवोकेशन और विकृत पाइप लाइन। `tests/test_core.py` प्रसंस्करण अनुबंधों और आउटपुट semantics को सत्यापित करता है। इनपुट सत्यापन, संग्रह विस्तार, एन्क्रिप्शन और फ़ाइल सिस्टम सुरक्षा में समर्पित प्रतिगमन परीक्षण हैं।

डिफ़ॉल्ट सूट के लिए `python -m pytest -q` रन। अलग-अलग स्थापित इंजनों का परीक्षण `python -m pytest -q -m native` के साथ किया जाता है; इन चेकों को चलाने से पहले `docs/engines.md` में वर्णित निर्भरता का प्रावधान। डिफ़ॉल्ट सूट पास करना सभी बाहरी इंजनों या हर समर्थित प्लेटफॉर्म को सत्यापित नहीं करता है।
