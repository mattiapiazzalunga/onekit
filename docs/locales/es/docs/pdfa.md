<a id="pdfa-conversion-and-validation"></a>
# Conversión y validación PDF/A

El CLI y Python API llaman a `onekit.tools.pdfa`. Este módulo no ejecuta ningún archivo ni abre ninguna conexión de red. La conversión usa pdftopdfa 0.9.24 para fuentes, color y normalización, seguida de pikepdf 10.17.0 PDF/A preparación y validación de los bytes finales exactos. No hay dependencia Ghostscript.

La conversión admite PDF/A-2b (predeterminado) y 3b. La validación admite 1b, 2b y 3b. La conformidad A/U, PDF/A-4 y OCR están fuera de este adaptador. Los constructos no compatibles se marcan como `not_checked`, no como conformes. Un `pass` de esta lista permisiva conservadora no es una certificación de archivo; se sigue recomendando la validación independiente veraPDF para presentaciones institucionales.

```
onekit run pdf-to-pdfa input.pdf --options '{"profile":"2b"}' -o output
onekit run pdf-validate-pdfa output/input.pdf -o report
onekit doctor pdf-to-pdfa --json
```

El CLI instala automáticamente un **subconjunto de nivel B no-OCR** de los paquetes upstream que está fijado y revisado. Deliberadamente no instala PaddleOCR, OCRmyPDF ni el backend de criptografía para el parser PDF no usado de pdfminer: no se envían opciones a las APIs de etiquetado OCR o A/U del upstream. El `pdftopdfa` wheel del upstream no se modifica. Sus metadatos de paquete incluyen requisitos más amplios para APIs que OneKit no invoca. El extra opcional `[pdfa]` instala los requisitos previos revisados. Para uso directo de Python API, instala ese extra y luego `pip install --no-deps pdfminer.six==20260107 pdftopdfa==0.9.24`. No instales los extras del upstream OCR para este adaptador. Los requisitos obligatorios OCR de Upstream actualmente fijan una versión anterior de PyYAML que es incompatible con OneKit. La conversión requiere Python 3.12+; la validación independiente funciona en Python 3.11+. Ejecuta `python scripts/check_licenses.py --include-pdfa` para auditar el runtime seleccionado.

La antigua opción `icc_profile` sigue siendo aceptada como un archivo local opcional ICC; por defecto se preservan los perfiles RGB/CMYK incluidos y con licencia del convertidor. Los PDFs cifrados y las firmas digitales son rechazados durante la conversión. La conversión puede reemplazar fuentes y eliminar acciones o metadatos no archivables; las advertencias acompañan al resultado exitoso. Los candidatos que fallan o que no son revisados completamente nunca se devuelven como archivos convertidos PDF/A. Las entradas no se sobrescriben. El informe de validación JSON preserva los campos `compliant` y `reports` y añade el perfil revisado, el veredicto y el motor.
