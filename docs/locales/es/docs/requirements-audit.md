<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-requirements-verification"></a>
# Verificación de requisitos CLI

`tests/test_requirements.py` verifica la cobertura del catálogo, las invocaciones CLI y las canalizaciones mal formadas. `tests/test_core.py` comprueba los contratos de procesamiento y la semántica de la salida. La validación de entrada, la expansión de archivos, la encriptación y las protecciones del sistema de archivos tienen pruebas de regresión dedicadas.

Ejecuta `python -m pytest -q` para la suite predeterminada. Los motores instalados por separado se prueban con `python -m pytest -q -m native`; proporciona las dependencias descritas en `docs/engines.md` antes de ejecutar estas comprobaciones. Pasar la suite predeterminada no verifica todos los motores externos ni todas las plataformas compatibles.
