<a id="cli-localization"></a>
# Localización de la CLI

Idiomas: `en`, `it`, `fr`, `es`, `de`, `ru`, `zh` (Simplified Chinese), `pt` (Portuguese), `hi` (Hindi). Seleccione uno con `onekit --language it ...`, o `ONEKIT_LANGUAGE=it`. El sistema operativo locale se utiliza cuando no está establecido. Los locales no compatibles usan inglés. Nombres de comando, teclas de opción, caminos, identificadores de formato y contratos legibles de máquina JSON permanecen estables. Se localiza la ayuda humana, el estado, las advertencias y los errores conocidos. Los diagnósticos del motor externo conservan su texto de arriba.

Cada persona o AI añadiendo o cambiando una herramienta DEBE actualizar los nueve catálogos de presentación en el mismo cambio. Nombres, ayuda, descripciones, mensajes de error, avisos, README y documentación de herramientas deben permanecer en una correspondencia única. No rellenar las traducciones perdidas con inglés como atajo. Mantenga intactos los titulares de puestos, ejemplos de código, URLs y avisos literales legalmente requeridos. Revisar el significado y la terminología en contexto.

Catálogos: `src/onekit/locales/{language}.json`. Código de presentación: `i18n.py`. Los mensajes en inglés son claves normalizadas; los algoritmos de procesamiento permanecen independientes. El registro de idioma independiente es `src/onekit/locales/languages.json`, incluyendo alias del sistema operativo. Agrega una entrada en el registro y un catálogo completo juntos. La terminología revisada se registra en `scripts/localization-reviewed.json`; aplícala con `python scripts/apply_localization_review.py src/onekit/locales` antes de auditar.

1. Edita el mensaje o la documentación en inglés en su archivo original.
2. Ejecuta `python scripts/localization_inventory.py`.
3. Actualiza los demás catálogos de idiomas y elimina las entradas obsoletas. Los scripts de preparación pueden generar borradores de traducción; los textos generados deben revisarse.
4. Ejecuta `python scripts/audit_localization.py` y `pytest tests/test_i18n.py`.
5. Ejecuta `python scripts/localize_docs.py` para regenerar los documentos Markdown traducidos en `docs/locales/{language}/`, conservando la estructura relativa de los documentos originales.

El comando de autoría fuera de línea necesita un directorio de modelo Argos local seguido de directorios de catálogo. CTranslate2 y SentencePiece son dependencias de autoría, no requisitos de ejecución de CLI. Ningún servicio de traducción es contactado por el CLI.

Las traducciones y la documentación del CLI se mantienen de forma independiente de cualquier sitio web que incluya la librería de procesamiento. Solo los enlaces de uso público pertenecen aquí.
