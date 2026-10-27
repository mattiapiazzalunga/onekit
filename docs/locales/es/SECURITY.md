<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="security-policy"></a>
# Política de seguridad

Reporta vulnerabilidades de forma privada a `security@onekit.org` con versión, plataforma, herramienta, versiones de dependencias, impacto y reproducción sintética. No publiques archivos sensibles, credenciales o reportes privados con exploits listos en rastreadores públicos. Las correcciones apuntan a la última versión estable; no se garantiza tiempo de respuesta.

El núcleo impone límites a las rutas, los tamaños de entrada, la descompresión de archivos, los píxeles de las imágenes, las comparaciones y los flujos de procesamiento. El cifrado usa AES-256-GCM autenticado con una sal y un nonce nuevos, junto con scrypt; no se pueden recuperar las contraseñas perdidas. Las salidas existentes se conservan de forma predeterminada. La validación de Python analiza el código fuente sin ejecutarlo.

Los conversores/compiladores externos son programas nativos separados, no un sandbox completo. Manténlos actualizados y aísla documentos hostiles usando los controles del SO. El CLI no es un servicio de conversión remota no autenticado. Editar un PDF firmado puede invalidar firmas; los permisos de PDF no son equivalentes a la integridad del cifrado.

Los controles ordinarios nunca deben recibir secretos de publicación. Las etiquetas estables identifican commits principales protegidos y revisados. Fallos de dependencia, licencia y seguridad bloquean la publicación. Ninguna suite de pruebas garantiza inmunidad frente a todos los inputs o ataques malformados.
