<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="encrypt-files-or-folders"></a>
# Cifrar archivos o carpetas

Comando: `onekit run security-encrypt`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Seguridad**. Fidelidad: **exacta**. AES-256 cifrado ZIP, compatible con 7-Zip. Los nombres de archivo permanecen visibles. Perder la contraseña hace que la recuperación sea imposible.

Tipos admitidos: `*`. Tipo de salida: `zip`. Admite varias entradas: **sí**.

Validación de entrada: **cualquier tipo de archivo**. Número de archivos requerido: **1–256**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: `password`.

Paquetes Python: pycryptodome, stream-zip, stream-unzip. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/security/__init__.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
