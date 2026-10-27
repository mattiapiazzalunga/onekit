<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->

Langues : [English](../../../README.md) · [Italiano](../it/README.md) · [Français](README.md) · [Español](../es/README.md) · [Deutsch](../de/README.md) · [Русский](../ru/README.md) · [中文](../zh/README.md).

<p align="center">
  <a href="https://onekit.org"><img src="https://raw.githubusercontent.com/mattiapiazzalunga/onekit/main/images/logo.png" alt="OneKit logo" width="112" height="112"></a>
</p>
<h1 align="center">OneKit</h1>
<p align="center">Une seule boîte à outils. Vos fichiers restent les vôtres.</p>
<p align="center"><a href="https://github.com/mattiapiazzalunga/onekit/stargazers"><img alt="Étoiles sur GitHub" src="https://img.shields.io/github/stars/mattiapiazzalunga/onekit"></a> <a href="https://pypi.org/project/onekit-tools/"><img alt="PyPI" src="https://img.shields.io/pypi/v/onekit-tools"></a> <img alt="PolyForm-Shield-1.0.0" src="https://img.shields.io/badge/license-PolyForm_Shield_1.0.0-blue"> <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue"></p>

Une trousse hors ligne Python avec 230 outils pour les conversions, PDF, images, archives, polices, inspection de fichiers, cryptage, utilitaires pour développeurs, OCR et comparaisons. Utilisez ce CLI ou l'interface graphique à **[onekit.org](https://onekit.org)**.

**Version source :** `0.6.1`. Les téléchargements stables existent seulement après la fin du processus de publication. La distribution est `onekit-tools` ; le projet PyPI, appartenant à une entité distincte et appelé `onekit`, n’est pas lié.

Le [guide des contacts et des médias](docs/contact-media.md) présente la création de vCard autonomes, l’extraction de vCard à partir de codes QR, l’agrandissement des images, la suppression de l’arrière-plan, la compression et le réglage de la vitesse des vidéos et GIF, ainsi que la transcription audio locale.

Vérifications de licence : inspectez PDF, Word, PowerPoint, Excel, vidéo, audio, images, polices, EPUB, code/projets et ensembles de données à partir de fichiers ou d’URL publiques. L'analyse reste locale ; les rapports sont des **estimations non vérifiées, pas des certificats de propriété ni une autorisation d'utilisation**. Voir [usage et limites de la vérification de licence](docs/cli.md#local-license-and-copyright-estimates).

**Votre CLI. Votre CLI, aussi pour vos agents IA.** Utilisez OneKit vous-même ou laissez un agent IA local l’appeler depuis un terminal ou un sous-processus. Découvrez les outils et leurs prérequis au format JSON, indiquez explicitement les chemins d’entrée et de sortie et réutilisez les flux de travail `.1kit` enregistrés pour répéter vos traitements de fichiers. Consultez la section [agents locaux et automatisation](docs/cli.md#local-agents-and-automation).

<a id="install"></a>
## Install

Python 3.11 ou une version ultérieure est requis. Le paquet wheel universel prend en charge Windows, macOS et Linux sur x64/ARM64. Les bibliothèques natives facultatives et les moteurs externes imposent des exigences supplémentaires selon la plateforme.

Après la publication :

```sh
python -m pip install onekit-tools
python -m pip install "onekit-tools[pdf,images,documents]"
onekit list
onekit doctor
```

Depuis une copie du dépôt source :

```sh
python -m pip install -e ".[all,test]"
python -m onekit --help
python -m pytest -q
```

La base CLI **n'a aucune dépendance à l'exécution**. Installez uniquement les extras dont vous avez besoin. `all` inclut les familles standard Python ; le téléchargement vidéo, la suppression d'arrière-plan, la transcription et la signature cryptographique utilisent les extras séparés `video`, `background`, `transcription` et `signing`. Installez les moteurs natifs séparément. Pour les outils de développement basés sur Node, installez Node.js 24+ et exécutez `onekit engines install`. CLI prépare les dépendances manquantes et les moteurs externes lors de la première utilisation. La suppression d'arrière-plan et la transcription téléchargent les poids des modèles lors de la première utilisation, puis réutilisent le cache local.

<a id="use"></a>
## Use

```sh
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit run pdf-extract-pages document.pdf --options '{"pages":"1,3-5"}' -o selected.pdf
onekit run image-convert image.png --options '{"format":"webp"}' -o image.webp
onekit run diff-notebook before.ipynb after.ipynb --options '{"mode":"code"}' -o changes.json
onekit run security-encrypt private-folder --ask-password -o private.zip
onekit run security-decrypt private.zip --ask-password -o restored
```

Les options sont des objets JSON ; passez-les comme un seul argument shell entre guillemets. Utilisez `--ask-password` pour les secrets. Les sorties existantes sont préservées à moins que vous ne passiez `--force`.

`onekit list --group pdf`, `onekit list --json` et `onekit doctor TOOL_ID` exposent les contrats et les exigences. Chaque outil a un répertoire dans [tools](../../../tools), contenant les métadonnées et un pointeur vers son implémentation partagée. Voir le guide [CLI guide](docs/cli.md) pour les options et les limites.

<a id="toolkit"></a>
## Toolkit

| Famille | Capacités |
| --- | --- |
| Convertisseurs | Markdown, HTML, LaTeX, PDF, Word, PowerPoint, images, Base64, Excel, CSV et JSON |
| PDF | Fusion/division, sélection/ordre/suppression des pages, compression, réparation, [édition directe de texte](docs/pdf-editing.md), superpositions de texte, rotation, signatures numériques, cryptage/déverrouillage, [conversion et validation locales PDF/A](docs/pdfa.md) |
| Images | Extraire les images intégrées PDF, compresser, recadrer et changer de format |
| Médias | Conversion audio/vidéo via FFmpeg installé séparément |
| Archives / polices | Variantes ZIP/TAR ; conteneurs TTF/OTF et WOFF/WOFF2 |
| Inspecteur / sécurité | Tapez les signatures, la structure, les métadonnées, l'encodage, les hachages, les décomptes de texte ; archives de fichiers/dossiers chiffrées et authentifiées |
| Développeur | Formatage spécifique à la langue, validation du parseur/compilateur et minification sélectionnée |
| OCR | Images scannées/PDF en PDF, Word, Markdown, LaTeX, HTML et JSON recherchables |
| Diff | Texte, code, JSON normalisé, carnets, LaTeX, PDF et Word texte |

<a id="pipelines-and-development"></a>
## Pipelines and development

`onekit pipeline --steps workflow.1kit INPUTS -o OUTPUT` accepte un document de workflow `.1kit` versionné. Chaque étape reçoit les sorties précédentes. Les étapes à entrée unique s’appliquent sur plusieurs sorties ; les étapes de fusion reçoivent toute la collection. Les types incompatibles arrêtent le traitement.

Signalez des bugs et des suggestions via [GitHub issues](https://github.com/mattiapiazzalunga/onekit/issues) ou le [site web pour les demandes](https://onekit.org/requests/). Les contributeurs peuvent trouver du travail dans l’un ou l’autre endroit.

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

Aidez à construire la révolution ouverte de OneKit : des outils quotidiens pour tout le monde, des tâches pratiques aux workflows gérés par les agents locaux AI. Contribuez pour rendre les outils plus efficaces : améliorez la vitesse et l'utilisation de la mémoire, corrigez les résultats incorrects, ajoutez des exemples de régression ou clarifiez la documentation et les workflows des agents.

Le cœur est Open Source (PolyForm Shield 1.0.0). Lisez le [guide de contribution](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) et trouvez une tâche dans [tickets GitHub](https://github.com/mattiapiazzalunga/onekit/issues), ou suggérez une amélioration sur le [tableau des demandes](https://onekit.org/requests/).

<a id="license-and-creator"></a>
## License and creator

Créé par **[Mattia Piazzalunga](mailto:hello@mattiapiazzalunga.com)**. Copyright © 2026 Mattia Piazzalunga. Open Source (PolyForm Shield 1.0.0), licencié sous [PolyForm Shield 1.0.0](../../../LICENSE) ; voir [NOTICE](../../../NOTICE), [AUTHORS.txt](../../../AUTHORS.txt) et [CONTRIBUTORS.txt](../../../CONTRIBUTORS.txt). Les composants tiers conservent leurs licences. Les moteurs externes sont des programmes séparés avec leurs propres obligations de redistribution.

Vous pouvez utiliser, modifier et redistribuer le cœur pour les usages autorisés, y compris à des fins commerciales et internes. Vous ne pouvez pas l’utiliser pour fournir un produit ou un service qui concurrence le logiciel ou un produit que le concédant ou ses affiliés proposent en utilisant le logiciel ; les offres gratuites et les différentes plateformes ou interfaces peuvent aussi être en concurrence. Lors du partage de copies, incluez le texte de la licence ou son URL et toutes les lignes d’avis requis fournies avec le logiciel. La licence complète s’applique, y compris ses exceptions pour les produits nouveaux et abandonnés, les conditions de brevet et la clause de non-garantie. Ici, « Open Source (PolyForm Shield 1.0.0) » décrit le code source publié selon ces termes ; la restriction de non-concurrence signifie qu’il s’agit d’un logiciel dont le code est disponible plutôt que d’un open source sans restriction selon la Définition de l’Open Source. Voir [le guide de licence](docs/licenses.md).

Exportez et réimportez des flux de travail sans traiter les fichiers d'entrée :

```sh
onekit workflow export workflow.1kit -o exported-workflow.1kit
onekit workflow import workflow.1kit -o saved-workflow.1kit
onekit pipeline --steps saved-workflow.1kit input.json -o output.json
```

Les codes-barres standard sont disponibles dans la catégorie Codes QR et codes-barres et dans la CLI : `text-to-barcode`, `scan-barcode`, `barcode-to-text`. Code 128, Code 39, EAN-13, EAN-8, UPC-A, ITF et ISBN-13 prennent en charge PNG/SVG, dimensions configurables et validation du chiffre de contrôle. Installez `onekit-tools[barcode]` ou `onekit-tools[qrcode]`.

Le [masquage définitif des PDF et des images](docs/redaction.md) est disponible avec `pdf-redact` et `image-redact`. Les zones sélectionnées deviennent des pixels noirs opaques dans les nouveaux fichiers. Les PDF sont reconstruits sous forme de documents composés uniquement d’images, sans texte, formulaires, commentaires, pièces jointes ni métadonnées d’origine ; les images deviennent des PNG opaques sans métadonnées d’origine ni pixels cachés par la transparence. Les fichiers originaux restent inchangés.

Ajouter des filigranes textuels PDF configurables avec `pdf-watermark` : opacité, couleur, polices, plages de pages, positions visuelles, rotation et grilles répétées. Le texte et les graphiques restent dans le PDF. Voir le [guide des filigranes](docs/watermark.md).

<a id="contacts"></a>
## Contacts

- Questions générales et support : [support@onekit.org](mailto:support@onekit.org).
- Questions sur le noyau Open Source (PolyForm Shield 1.0.0) et les contributions : [developers@onekit.org](mailto:developers@onekit.org).
- Confidentialité, RGPD et demandes de données personnelles : [privacy@onekit.org](mailto:privacy@onekit.org).
- Questions juridiques, licences et demandes d’autorisation : [legal@onekit.org](mailto:legal@onekit.org).
- Vulnérabilités de sécurité et signalements d'abus : [security@onekit.org](mailto:security@onekit.org).
