<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="verify-digital-signature"></a>
# Verificar firma digital

Comando: `onekit run signature-verify`. Utiliza `onekit run --help` para consultar los argumentos de entrada y salida.

Categoría: **Seguridad**. Fidelidad: **exacta**. Verificación criptográfica sin conexión de las firmas PDF y CMS/P7M/P7S usando certificados incorporados. Las firmas separadas requieren el archivo original. No se verifican cadenas de confianza, revocación, estado de firma calificada ni marcas de tiempo confiables.

Tipos admitidos: `*`. Tipo de salida: `json`. Admite varias entradas: **sí**.

Validación de entrada: **cualquier tipo de archivo**. Número de archivos requerido: **1–2**. CLI: **134 217 728 bytes por archivo**, **134 217 728 bytes en total**. El contenido se comprueba antes del procesamiento. Cambiar el nombre de un archivo no modifica su formato real.

Opciones: ninguna.

Paquetes Python: pypdf, asn1crypto, pycryptodome. Motores externos: consulte la matriz de motores de las herramientas de desarrollo para conocer los adaptadores de los lenguajes de programación.

Implementación del procesamiento: [adaptador compartido de la familia de herramientas](../../../../../../src/onekit/tools/signatures.py). Contratos y datos para pruebas de regresión: [pruebas](../../../../../../tests/test_core.py). Configuración de motores y licencias: [guía de motores](../../../docs/engines.md).

Este directorio se genera a partir del catálogo compartido por `python scripts/tool_docs.py`. Edita el registro y el adaptador de familia, agrega datos de prueba para las pruebas de regresión, y luego regenera el directorio.
