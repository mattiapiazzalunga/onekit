<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="release-operations"></a>
# Freigabeoperationen

Schützen Sie `main` und stabile `v*`-Tags. Registriere den PyPI Trusted Publisher für Repository `onekit`, Workflow `release.yml` und Umgebung `pypi`. Aktualisiere die Paketversion, Lockfile, Katalog und Dokumentation, und veröffentlichen Sie dann ein passendes stabiles SemVer-Tag von einem überprüften Commit.

Der Release-Workflow überprüft das Tag, führt die erforderlichen CLI-Prüfungen durch und veröffentlicht universelle wheel/Quell-Distributionen, das GHCR-Image und GitHub Release-Assets. `onekit-release.json` enthält Version, Quell-Commit, Asset-Checksummen und Download-URLs. Veröffentlichungsversuche müssen vorhandene unveränderliche Assets beibehalten; Codeänderungen erfordern eine neue Version.

<a id="pypi-license-metadata"></a>
## PyPI license metadata

Das PyPI Paket ist Open Source (PolyForm Shield 1.0.0), mit der Wettbewerbsbeschränkung, die in README auf der Projektseite erklärt wird. `project.license` verwendet `LicenseRef-PolyForm-Shield-1.0.0`; das wheel und das Quellarchiv enthalten die komplette LICENSE und NOTICE. Die Projekt-Metadaten verlinken zur Lizenz und Dokumentation. Fügen Sie keinen von OSI genehmigten Lizenz-Classifier hinzu: diese Lizenz schränkt konkurrierende Produkte ein.

Vor der Veröffentlichung: Erstellen Sie die Version aus dem vorgesehenen Release-Commit und überprüfen Sie die tatsächlichen Artefakte:

```sh
uv build
python scripts/check_distribution_licenses.py
```

CI und der Release-Build führen diese Überprüfung durch, bevor Artefakte veröffentlicht werden können. PyPI stellt das verpackte README dar, daher ist ein Neubau erforderlich, nachdem Dokumentation oder Lizenz-Metadaten geändert wurden. Veröffentlichen Sie eine neue, ungenutzte Version, wenn eine bereits veröffentlichte Version ersetzt wird; vorhandene PyPI-Distributionen können nicht überschrieben werden. Bereits verteilte Versionen behalten ihre ursprünglichen Lizenzbedingungen. Die Version des aktuellen Checkouts wird durch eine Lizenzänderung nicht automatisch aktualisiert.

Der Projektinhaber konfiguriert das PyPI-Konto, Trusted Publisher und die Veröffentlichung separat; lokale Vorbereitung lädt keine Pakete hoch oder ändert die live PyPI-Seite.

<a id="weekly-dependency-maintenance"></a>
## Weekly dependency maintenance

Dependabot überwacht die UV-Sperrdatei, CLI Node Engine-Abhängigkeiten, Docker und GitHub Actions. Der geplante Checks-Workflow testet gesperrte Abhängigkeiten und native Engines erneut. Berechtigte Python Lock-Only-Updates bleiben den erfolgreichen Checks und dem Branch-Schutz unterworfen.
