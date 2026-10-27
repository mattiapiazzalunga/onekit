<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="external-engines-and-licenses"></a>
# Moteurs externes et licences

Le propriétaire a approuvé des moteurs open-source installés séparément. Ils ne sont pas inclus dans le wheel Python, le téléchargement du code source ou l'image Docker initiale. `onekit doctor` signale des exigences. `ONEKIT_ALLOW_COPYLEFT=0` désactive explicitement les adaptateurs copyleft listés. Gardez les outils en amont à jour ; les sous-processus locaux ne constituent pas un bac à sable complet pour des documents hostiles.

| Moteur | Commande | Utilisez / considérations de licence |
| --- | --- | --- |
| LibreOffice | `soffice` / `libreoffice` | Bureau → PDF/images ; MPL et avis de tiers. |
| Pandoc | `pandoc` | Conversion avancée de balisage ; GPL. |
| TeX Live/pdfTeX | `pdflatex` | LaTeX/Pandoc PDF ; le moteur, les macros et les polices ont des licences séparées. |
| FFmpeg | `ffmpeg` | Médias ; LGPL ou GPL selon la version et les codecs. |
| veraPDF | `verapdf` | Vérification indépendante optionnelle des sorties archivées ; exigences en amont GPL/MPL et Java. |
| ExifTool | `exiftool` | Métadonnées dans les types de fichiers pris en charge ; licence Perl en amont. |
| Tesseract | `tesseract` | OCR; moteur Apache et données linguistiques sous licence séparée. |

Si vous distribuez ces programmes, même à l'intérieur de Docker, conservez leurs licences/avis et fournissez les sources/matériaux de construction correspondants requis. Évaluez les intégrations du réseau AGPL séparément. L'utilisation commerciale et les obligations de source/rediffusion sont des questions différentes. Des processus séparés n'éliminent pas universellement les obligations. Lisez les documents officiels [FFmpeg](https://ffmpeg.org/legal.html), [LibreOffice](https://www.libreoffice.org/licenses/), [Ghostscript](https://www.ghostscript.com/licensing/) et [MPL](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) avant de créer une distribution groupée.

La fidélité des documents Office dépend des polices et des ressources. PDF vers Word exporte le texte extrait ; PDF vers PowerPoint crée des diapositives contenant des images. La réparation des PDF n’est pas garantie ; la compression est sans perte. La [conversion et la validation PDF/A](pdfa.md) utilisent des bibliothèques MPL distinctes via l’adaptateur Python partagé, avec des profils ICC inclus sous licence. Ghostscript n’est pas nécessaire. Une validation indépendante des normes reste recommandée. La précision de l’OCR dépend de la qualité de numérisation et des données linguistiques.

<a id="developer-tools"></a>
## Developer tools

Installez Node.js 24+ et lancez `onekit engines install` pour Prettier/plugins verrouillés, esbuild, le minificateur HTML, SVGO et GraphQL.js. Ils s’installent dans le cache OneKit de l’utilisateur, pas globalement. `ONEKIT_NODE_ENGINE_PATH` permet de choisir une alternative. Relancez l’installateur après une mise à jour approuvée du moteur. Le groupe de parseurs couvre JS/TS/JSX/TSX, le balisage, les feuilles de style, Markdown/MDX, GraphQL, Vue, Svelte, Astro, Solidity et PHP.

Installez les compilateurs/lanceurs upstream pour votre OS et ajoutez les commandes documentées au PATH. Certains fichiers isolés ont besoin de leurs dépendances de projet ou du nom de fichier exact de la classe Java. La validation du formatage/parseur ne prouve pas la correction des types sur l’ensemble du projet.

Sur Windows, les adaptateurs Bash/Shell préfèrent un interpréteur réel dans le PATH, puis détectent Git pour Windows dans ses répertoires d’installation système/utilisateur standard. Le lanceur WSL de System32 n’est pas considéré comme un parseur local compatible. La validation de la syntaxe PowerShell nécessite `pwsh` ; le formatage nécessite en plus PSScriptAnalyzer (`Install-Module PSScriptAnalyzer -Scope CurrentUser`). `onekit doctor dev-format-powershell` vérifie ce module séparément et indique sa commande de configuration. Ces programmes/modules ne sont pas téléchargés lors du traitement des fichiers.

<a id="platform-qualifications"></a>
## Platform qualifications

Les contrôles des licences dans la CI installent et examinent également l’extra de signature séparé (`scripts/check_licenses.py --include-signing`). MIT-0 est reconnue comme une licence permissive ([texte SPDX](https://spdx.org/licenses/MIT-0.html)). Les données du magasin de confiance Mozilla de la version figée de `certifi`, 2026.7.22, constituent une exception MPL-2.0 explicite, propre à cette version ; conservez leur licence et leurs mentions d’origine sans modification lors de leur redistribution ([mention d’origine](https://github.com/certifi/python-certifi/blob/master/LICENSE)). Les nouvelles versions nécessitent un nouvel examen. Cette exception n’autorise pas de manière générale d’autres paquets MPL et ne modifie pas la licence PolyForm-Shield-1.0.0 de OneKit.

Le cœur universel Python prend en charge Linux, Windows et macOS, y compris ARM64. Les extras natifs et les moteurs externes déterminent les besoins supplémentaires. CI déclare les runners x64/ARM sur les trois familles de systèmes d'exploitation. Sur Windows ARM, Brotli/WOFF2 et la pile de cryptographie de signature séparée peuvent nécessiter des outils de compilation natifs ou x64 Python sous émulation. WOFF/TTF/OTF ne nécessitent pas l'encodeur WOFF2. L'extra `all` exclut la signature séparée. Signalez ces contraintes optionnelles plutôt que d'affirmer qu'un wheel natif existe lorsqu'il n'existe pas.
