<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="release-operations"></a>
# Opérations de publication

Protégez la branche `main` et les tags stables `v*`. Enregistrez l’éditeur de confiance PyPI pour le dépôt `onekit`, le flux de travail `release.yml` et l’environnement `pypi`. Mettez à jour la version du package, le fichier de verrouillage, le catalogue et la documentation, puis publiez un tag SemVer stable correspondant à partir d’un commit révisé.

Le workflow de publication vérifie le tag, exécute les vérifications CLI requises et publie les distributions universelles wheel/source, l'image GHCR et les ressources de publication GitHub. `onekit-release.json` contient la version, le commit source, les sommes de contrôle des ressources et les URL de téléchargement. Les tentatives de publication doivent préserver les ressources immuables existantes ; les modifications du code nécessitent une nouvelle version.

<a id="pypi-license-metadata"></a>
## PyPI license metadata

Le paquet PyPI est Open Source (PolyForm Shield 1.0.0), avec la restriction de non-concurrence expliquée dans le README affiché sur sa page de projet. `project.license` utilise `LicenseRef-PolyForm-Shield-1.0.0` ; le wheel et l’archive source incluent le LICENSE et le NOTICE complets. Les métadonnées du projet renvoient à la licence et à la documentation. N’ajoutez pas de classificateur de licence approuvé par l’OSI : cette licence restreint les produits concurrents.

Avant publication, construisez à partir du commit de la version souhaitée et validez les artefacts réels :

```sh
uv build
python scripts/check_distribution_licenses.py
```

L'intégration continue et la version de publication exécutent cette vérification avant que les artefacts puissent être publiés. PyPI affiche le rendu du README inclus dans le paquet, donc il faut reconstruire après avoir modifié la documentation ou les métadonnées de licence. Publiez une nouvelle version, non utilisée, lorsque vous remplacez une version déjà publiée ; les distributions PyPI existantes ne peuvent pas être écrasées. Les versions distribuées précédemment conservent leurs conditions de licence originales. La version du checkout actuel n'est pas automatiquement mise à jour par un changement de licence.

Le propriétaire du projet configure le compte PyPI, l'Éditeur de confiance et la publication séparément ; la préparation locale n’envoie pas de paquets ni ne modifie la page PyPI en direct.

<a id="weekly-dependency-maintenance"></a>
## Weekly dependency maintenance

Dependabot surveille le fichier de verrouillage uv, les dépendances du moteur CLI Node, Docker et GitHub Actions. Le flux de travail Vérifications planifié reteste les dépendances verrouillées et les moteurs natifs. Les mises à jour éligibles Python uniquement verrouillées restent soumises à des vérifications réussies et à la protection des branches.
