<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="release-operations"></a>
# Operaciones de lanzamiento

Protege la rama `main` y las etiquetas estables `v*`. Registra al Publicador Confiable PyPI para el repositorio `onekit`, flujo de trabajo `release.yml` y entorno `pypi`. Actualiza la versión del paquete, el archivo de bloqueo, el catálogo y la documentación, luego publica una etiqueta SemVer estable correspondiente desde un commit revisado.

El flujo de trabajo de lanzamiento verifica la etiqueta, ejecuta las comprobaciones requeridas CLI y publica las distribuciones universales wheel/source, la imagen de GHCR y los recursos de lanzamiento GitHub. `onekit-release.json` contiene la versión, el commit de origen, las sumas de verificación de los recursos y las URLs de descarga. Los reintentos de publicación deben preservar los recursos inmutables existentes; los cambios de código requieren una nueva versión.

<a id="pypi-license-metadata"></a>
## PyPI license metadata

El paquete PyPI es de código abierto (PolyForm Shield 1.0.0), con la restricción de no competencia explicada en README que se muestra en la página del proyecto. `project.license` usa `LicenseRef-PolyForm-Shield-1.0.0`; el wheel y el archivo fuente incluyen los archivos LICENSE y NOTICE completos. Los metadatos del proyecto enlazan con la licencia y la documentación. No agregues un clasificador de licencia aprobado por la OSI: esta licencia restringe productos competidores.

Antes de la publicación, construye desde el commit de la versión prevista y valida los artefactos reales:

```sh
uv build
python scripts/check_distribution_licenses.py
```

CI y la versión de lanzamiento ejecutan esta verificación antes de que los artefactos puedan ser publicados. PyPI muestra el README incluido en el paquete, así que es necesario reconstruir después de cambiar la documentación o los metadatos de la licencia. Publica una nueva versión, sin usar, al reemplazar un lanzamiento ya publicado; las distribuciones PyPI existentes no se pueden sobrescribir. Las versiones distribuidas anteriormente mantienen sus términos de licencia originales. La versión actual en el checkout no se actualiza automáticamente con un cambio de licencia.

El propietario del proyecto configura la cuenta PyPI, el Editor de confianza y la publicación por separado; la preparación local no sube paquetes ni cambia la página en vivo PyPI.

<a id="weekly-dependency-maintenance"></a>
## Weekly dependency maintenance

Dependabot supervisa el archivo de bloqueo uv, las dependencias del motor CLI Node, Docker y GitHub Actions. El flujo de trabajo Checks programado vuelve a probar dependencias y motores nativos bloqueados. Las actualizaciones Python solo de bloqueo elegibles siguen sujetas a revisiones exitosas y protección de ramas.
