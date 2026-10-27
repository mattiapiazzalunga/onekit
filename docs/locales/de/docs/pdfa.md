<a id="pdfa-conversion-and-validation"></a>
# PDF/A Konvertierung und Validierung

Die CLI und Python API rufen `onekit.tools.pdfa` auf. Dieses Modul führt kein ausführbares Programm aus und öffnet keine Netzwerkverbindung. Die Konvertierung verwendet pdftopdfa 0.9.24 für Schriftarten, Farbe und Normalisierung, gefolgt von pikepdf 10.17.0 PDF/A zur Vorbereitung und Validierung der exakten finalen Bytes. Es besteht keine Ghostscript-Abhängigkeit.

Die Konvertierung unterstützt PDF/A-2b (Standard) und 3b. Die Validierung unterstützt 1b, 2b und 3b. A/U-Konformität, PDF/A-4 und OCR liegen außerhalb dieses Adapters. Nicht unterstützte Konstrukte werden als `not_checked` und nicht als konform eingestuft. Ein `pass` aus dieser konservativen Positivliste ist keine Archivbescheinigung; eine unabhängige veraPDF-Validierung wird für institutionelle Übermittlungen weiterhin empfohlen.

```
onekit run pdf-to-pdfa input.pdf --options '{"profile":"2b"}' -o output
onekit run pdf-validate-pdfa output/input.pdf -o report
onekit doctor pdf-to-pdfa --json
```

Der CLI installiert automatisch ein angepinntes, überprüftes **Nicht-OCR Level-B Teilset** der Upstream-Pakete. Er installiert absichtlich weder PaddleOCR, OCRmyPDF noch das Kryptographie-Backend für den ungenutzten PDF-Parser von pdfminer: Es werden keine Optionen an Upstream OCR oder A/U-Tagging-APIs weitergeleitet. Der Upstream `pdftopdfa` wheel ist unverändert. Seine Paketmetadaten enthalten umfangreichere Anforderungen für APIs, die OneKit nicht aufruft. Das optionale `[pdfa]` Extra installiert die überprüften Voraussetzungen. Für die direkte Python API Verwendung, installieren Sie zunächst dieses Extra und dann `pip install --no-deps pdfminer.six==20260107 pdftopdfa==0.9.24`. Installieren Sie nicht die Extras des Upstreams OCR für diesen Adapter. Die obligatorischen OCR-Anforderungen von Upstream blockieren derzeit eine ältere PyYAML, die mit OneKit nicht kompatibel ist. Die Konvertierung erfordert Python 3.12+; die eigenständige Validierung funktioniert mit Python 3.11+. Führen Sie `python scripts/check_licenses.py --include-pdfa` aus, um die ausgewählte Laufzeit zu prüfen.

Die frühere `icc_profile`-Option bleibt als optionale lokale ICC-Datei akzeptiert; standardmäßig werden die im Konverter enthaltenen, lizenzierten RGB/CMYK-Profile beibehalten. Verschlüsselte PDFs und digitale Signaturen werden bei der Konvertierung abgelehnt. Die Konvertierung kann Schriftarten ersetzen und nicht-archivfähige Aktionen oder Metadaten entfernen; erfolgreiche Ausgaben werden mit Warnungen begleitet. Fehlgeschlagene oder unvollständig geprüfte Kandidaten werden niemals als konvertierte PDF/A-Dateien zurückgegeben. Eingaben werden nicht überschrieben. Der JSON-Validierungsbericht behält die `compliant`- und `reports`-Felder bei und fügt das geprüfte Profil, das Urteil und die Engine hinzu.
