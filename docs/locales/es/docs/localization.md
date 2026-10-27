<a id="cli-localization"></a>
# Localización de la CLI

Idiomas: `en`, `it`, `fr`, `es`, `de`, `ru`, `zh` (chino simplificado). Selecciona uno con `onekit --language it ...`, o `ONEKIT_LANGUAGE=it`. Se utiliza la configuración regional del sistema operativo cuando no se establece ningún otro. Las configuraciones regionales no compatibles usan inglés. Los nombres de comandos, claves de opciones, rutas, identificadores de formato y contratos JSON legibles por máquina permanecen estables. La ayuda humana, estado, advertencias y errores conocidos están localizados. Los diagnósticos del motor externo mantienen su texto original.

Toda persona o IA que añada o modifique una herramienta DEBE actualizar los siete catálogos de textos en el mismo cambio. Los nombres, la ayuda, las descripciones, los mensajes de error, los avisos, el README y la documentación de las herramientas deben mantener una correspondencia uno a uno. No sustituyas traducciones pendientes por texto en inglés. Conserva intactos los marcadores, los ejemplos de código, las URL y los avisos que deban reproducirse literalmente por ley. Revisa el significado y la terminología en su contexto.

Catálogos: `src/onekit/locales/{language}.json`. Código de presentación: `i18n.py`. Los mensajes en inglés son claves normalizadas; los algoritmos de procesamiento permanecen independientes. El registro de idioma independiente es `src/onekit/locales/languages.json`, incluyendo alias del sistema operativo. Agrega una entrada en el registro y un catálogo completo juntos. La terminología revisada se registra en `scripts/localization-reviewed.json`; aplícala con `python scripts/apply_localization_review.py src/onekit/locales` antes de auditar.

1. Edita el mensaje o la documentación en inglés en su archivo original.
2. Ejecuta `python scripts/localization_inventory.py`.
3. Actualiza los demás catálogos de idiomas y elimina las entradas obsoletas. Los scripts de preparación pueden generar borradores de traducción; los textos generados deben revisarse.
4. Ejecuta `python scripts/audit_localization.py` y `pytest tests/test_i18n.py`.
5. Ejecuta `python scripts/localize_docs.py` para regenerar los documentos Markdown traducidos en `docs/locales/{language}/`, conservando la estructura relativa de los documentos originales.

El comando de autoría fuera de línea necesita un directorio de modelo Argos local seguido de directorios de catálogo. CTranslate2 y SentencePiece son dependencias de autoría, no requisitos de ejecución de CLI. Ningún servicio de traducción es contactado por el CLI.

Las traducciones y la documentación del CLI se mantienen de forma independiente de cualquier sitio web que incluya la librería de procesamiento. Solo los enlaces de uso público pertenecen aquí.
