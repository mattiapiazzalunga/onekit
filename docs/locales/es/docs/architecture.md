<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="architecture-and-extension-guide"></a>
# Guía de arquitectura y extensiones

`Artifact(name, data)` es una carga útil de bytes con nombre e inmutable. `Result(files, warnings, details)` transporta salidas y avisos de fidelidad. `execute(tool_id, files, options)` valida contratos e importa de manera diferida un adaptador de procesamiento. `pipeline(steps, files)` compone operaciones y mapea múltiples salidas a través de pasos de entrada única.

El catálogo define ID estables, familias, tipos aceptados y de salida, multiplicidad, opciones, fidelidad, límites y dependencias. Los adaptadores de procesamiento son independientes del acceso al sistema de archivos CLI. Los nombres portátiles rechazan la traversa y los nombres de dispositivos reservados. Las salidas de CLI escriben preservando los archivos existentes por defecto. Las llamadas del motor nativo usan arrays de argumentos, directorios temporales y límites de tiempo controlados.

Para agregar una herramienta, implementa su adaptador de familia, declara la entrada del catálogo, añade pruebas semánticas y de regresión con entradas inválidas, declara dependencias opcionales y revisa las licencias. Regenera los directorios de herramientas con `python scripts/tool_docs.py`. Documenta la fidelidad y los requerimientos de la plataforma.


La API de procesamiento v1 se describe en `contracts/processing-v1.json`. Ejecuta `python scripts/check_contracts.py` antes de enviar cambios. Agregar herramientas, formatos y opciones es compatible; eliminar IDs/opciones existentes, cambiar tipos de salida o restringir contratos de entrada requiere una migración versionada explícita. Los algoritmos internos y la organización de los manejadores pueden cambiar sin modificar el contrato público.

`ExecutionContext` permite que los llamantes Python reduzcan los presupuestos por lote y por herramienta y proporcionen un lector de metadatos de medios locales confiable. No acepta servicios de motor a través de opciones de herramienta proporcionadas por el usuario. Los contextos son inmutables, están limitados a una ejecución y se comparten entre los pasos del flujo de trabajo. CLI utiliza los servicios de motor local predeterminados.

El adaptador de fuente Node delega las reglas de formato y minificación a `tools/developer/source_engine.mjs`. Su cargador de motor es una dependencia a nivel de proceso; el texto fuente no puede elegir paquetes o comandos ejecutables de manera arbitraria.
