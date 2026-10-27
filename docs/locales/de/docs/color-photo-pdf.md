<a id="color-photo-restoration-and-pdf-forms"></a>
# Farbe, Fotorestaurierung und PDF-Formulare

Diese Werkzeuge werden über den Standardbefehl `onekit run TOOL ... --options JSON` und die Python `execute` API bereitgestellt. Siehe `onekit run --help` für Ein-/Ausgabe-Argumente. Alle unten genannten Koordinaten beziehen sich auf das Bild nach der EXIF-Ausrichtung oder die angezeigte PDF-Seite nach der Drehung.

- `color-picker`: Untersuchen Sie eine UTF-8-Datei, die `#RRGGBB` enthält, oder beprobe ein Bild mit ganzzahligen Pixeloptionen `x` und `y` (standardmäßig zentriert). Meldet HEX, RGB, OKLCH, Schwarz/Weiß-Textkontrast und das originale RGBA für Bilder. Sichtbare Farben werden auf Weiß zusammengesetzt.
- `image-extract-colors`: `colors` (2–32, Standard 6). Median-Cut-Quantisierung eines Thumbnails, begrenzt auf 256 × 256. Vollständig transparente Pixel werden ausgeschlossen; teilweise Alpha wird auf Weiß zusammengesetzt. Brüche beschreiben dieses Sample.
- `jpg-to-svg`: `colors` (2–32, Standard 16), `resolution` (32–512, Standard 256). Quantisiert ein begrenztes Bild, fasst horizontale Abschnitte gleicher Farbe vertikal zusammen und schreibt ausgefüllte SVG-Pfade. Es wird keine Bitmap eingebettet. Dies erzeugt Vektorkacheln mit einem posterisierten Erscheinungsbild, nicht glatte Kurvenerfassung.
- `image-repair`: Ohne `regions` wendet es einen Medianfilter von `size` 3 oder 5 auf isolierte Flecken an. Mit Regionen rekonstruiert es ausgewählte Pixel mit festen umgebenden Pixeln und diskreter harmonischer Diffusion (`iterations` 10–500, Standard 200).
- `image-remove-watermark`: erfordert `regions`; verwendet die gleiche lokale Rekonstruktion. Es schätzt fehlende Pixel und kann versteckten Originalinhalt nicht wiederherstellen. Texturen, große Markierungen und komplexe Hintergründe können schlechte Ergebnisse liefern.
- `image-sharpen`: `method` ist `unsharp` (Standard) oder `deconvolution`. `radius` zwischen 0.3 und 5 legt den Radius der Unscharfmaskierung oder die geschätzte Gaußsche Punktspreizung fest. Bei der Unscharfmaskierung liegt `amount` zwischen 0 und 300 Prozent (Standard 150). Richardson–Lucy verwendet 1 bis 30 `iterations` (Standard 10), gespiegelte Randauffüllung und FFT-Faltung für höchstens eine Million Quellpixel. Es setzt Gaußsche Unschärfe voraus und korrigiert keine beliebigen Bewegungen. Beide Methoden können Rauschen und Halos verstärken.
- `pdf-remove-watermark`: standardmäßig entfernt `mode: "remove"` `/Artifact`-Gruppen, die mit `/Subtype /Watermark` markiert sind (einschließlich benannter Ressourcen für Eigenschaften) und `/Watermark`-Anmerkungen. Der optionale Parameter `text` sucht nach vollständigen Textobjekten, wobei Leerzeichen normalisiert und Glyphen über ihre Schriftkodierung/ToUnicode-Tabelle decodiert werden. Verschachtelte Form XObjects werden rekursiv verarbeitet. Verwenden Sie `mode: "inspect"`, um einen JSON-Bericht über Text-, Bild- und Form-XObject-Aufruf-IDs zu erhalten; übergeben Sie ausgewählte IDs im Entfernen-Modus als `objects`. Wenn ein Form XObject ausgewählt wird, wird die gesamte Grafikgruppe entfernt. Geänderte Form XObjects werden pro Aufruf kopiert, sodass nicht ausgewählte Verwendungen einer gemeinsamen Ressource unverändert bleiben. IDs beziehen sich auf dasselbe Original-PDF und müssen nach Änderungen erneut überprüft werden. Dies ist das Entfernen von Zeichenobjekten, keine sichere Schwärzung: Unbenutzte Ressourcenobjekte können im Ergebnis bleiben. Es erkennt nicht automatisch beliebige nicht markierte Inhalte als Wasserzeichen, und ein in ein gescanntes Bild eingebettetes Wasserzeichen kann nicht von diesem Bild getrennt werden. Ein Bericht enthält bis zu 2.000 Kandidaten, die Rekursion ist auf 12 Ebenen begrenzt und die Verarbeitung auf 300.000 Grafikoperationen. Null Treffer erzeugen einen expliziten Fehler.
- `pdf-make-fillable`: `fields` ist ein JSON-Array standardmäßiger AcroForm-Felder. Jedes Feld hat einen eindeutigen ASCII-`name`, einen `type` (`text`, `checkbox`, `choice`), eine ab 1 nummerierte `page` und normalisierte Koordinaten `x`, `y`, `width`, `height`. Unterstützt werden das optionale `required`, `multiline` für Text und `choices` für Auswahlmöglichkeiten. Vorhandene Felder und Seiteninhalte bleiben erhalten. Doppelte Namen, verschlüsselte PDFs und XFA werden abgelehnt. Keine automatische Erkennung leerer Bereiche.

Bildbereiche sind Arrays von Objekten wie `{"page":1,"x":0.2,"y":0.3,"width":0.1,"height":0.05}`. Koordinaten sind normalisiert zu 0–1 von der oberen linken Ecke. Die Rekonstruktion unterstützt bis zu 100 Rechtecke, höchstens 35 % des Bildes und eine Begrenzungsbox (einschließlich Polsterung) von einer Million Pixeln. Nur RGB innerhalb der Maske ändern sich; der ursprüngliche Alphawert bleibt erhalten. Ausgaben sind PNG ohne Quell-Metadaten. Animierte/mehrbildrige Bilder werden abgelehnt. Allgemeine Bilddekodierung ist auf 40 Millionen Pixel begrenzt. PDFs sind auf 256 Seiten und Formulare auf 200 neue Felder begrenzt.

Beispiel für Python-Nutzung:

```python
from onekit import Artifact, execute

result = execute("pdf-make-fillable", [Artifact("source.pdf", pdf_bytes)], {
    "fields": [{"name": "Name", "type": "text", "page": 1,
                "x": 0.1, "y": 0.2, "width": 0.4, "height": 0.05}]
})
```

Überprüfen Sie die resultierenden Dateien und behalten Sie die Originale. Ein kompatibler PDF-Leser wird benötigt, um Formulare auszufüllen und zu speichern.
