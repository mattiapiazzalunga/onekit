<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanent-redaction"></a>
# Dauerhaftes Schwärzen

<a id="pdf"></a>
## PDF

Jede Seite wird gerendert, die ausgewählten Pixel werden durch undurchsichtiges Schwarz ersetzt, und ein neuer PDF wird aus den bereits geschwärzten Bildern erstellt. Keine ursprünglichen PDF-Objekte werden kopiert. Dadurch werden Originaltext, OCR-Ebenen, versteckte Ebenen, Formularfelder, Anmerkungs-/Kommentarobjekte, Links, Skripte, Anhänge, Metadaten, Thumbnails und die inkrementelle Verlaufsspeicherung aus der Ausgabe entfernt. Sichtbare Anmerkungen werden in Pixel umgewandelt, sodass eine bestehende undurchsichtige Anmerkung den darüberliegenden Inhalt nicht unerwartet zeigt. Überprüfen Sie die Vorschau auf Unterschiede bei Feld-/Anmerkungsdarstellungen; interaktive Objekte werden nicht beibehalten. Nicht ausgewählter sichtbarer Seiteninhalt bleibt als Pixel erhalten.

<a id="images"></a>
## Images

Die Pixel werden durch deckendes Schwarz ersetzt, bevor eine neue undurchsichtige RGB-PNG-Datei erzeugt wird. Die bearbeiteten Bereiche enthalten keine entfernbare Überlagerung, keine Originalebene und keine ursprünglichen ungeschwärzten Pixeldaten. EXIF-, GPS- und XMP-Daten, Kommentare, Profile, Vorschaubilder und andere Metadaten der Quelldatei werden nicht übernommen. Transparenz wird auf weißem Hintergrund zusammengeführt; verborgene RGB-Werte unter transparenten Pixeln werden verworfen. Die EXIF-Ausrichtung wird vor der Auswertung der Bereiche angewendet. Animierte Eingaben und Eingaben mit mehreren Einzelbildern werden abgelehnt, damit keine zusätzlichen Bilder ungeschwärzt bleiben; exportieren Sie zuerst ein einzelnes Bild.

<a id="cli-and-workflows"></a>
## CLI and workflows

Installiere `onekit-tools[pdf]` zum dauerhaften Schwärzen von PDFs oder `onekit-tools[images]` für Bilder. Beide Tools akzeptieren `regions`, ein Array von Rechtecken, optional als JSON-String serialisiert. Jedes Rechteck hat `page` (einsbasiert, Standard 1), `x`, `y`, `width`, `height`. Die Koordinaten sind Bruchteile der Abmessungen der sichtbar ausgerichteten Seite oder des Bildes mit Ursprung oben links: `0.1` bedeutet 10%. Bei Bildern muss `page` 1 sein. Es können bis zu 500 Rechtecke ausgewählt werden. Die Grenzen müssen innerhalb der Seite liegen; Die Maskengrenzen werden nach außen gerundet und um einen Ausgabepixel erweitert, damit auch anteilige Randpixel abgedeckt sind.

```sh
onekit run pdf-redact private.pdf -o redacted.pdf --options '{"regions":[{"page":1,"x":0.1,"y":0.2,"width":0.5,"height":0.1}],"dpi":200}'
onekit run image-redact private.jpg -o redacted.png --options '{"regions":[{"x":0.2,"y":0.2,"width":0.3,"height":0.2}]}'
```
