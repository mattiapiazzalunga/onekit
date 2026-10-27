<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-reference"></a>
# Référence de la CLI

Utilisez `onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","opacity":0.25}'` pour ajouter un filigrane texte PDF. Consultez le [guide des filigranes](watermark.md) pour la position, la rotation, les plages de pages et les mises en page répétées.

Le masquage définitif est disponible avec `onekit run pdf-redact` et `onekit run image-redact` ; les zones à masquer sont fournies dans `regions`. Le [guide du masquage définitif](redaction.md) décrit les coordonnées, la rastérisation et les garanties de confidentialité des fichiers exportés.

Utilisez `onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"[0-9]+","flags":"g"}'` pour tester des expressions régulières JavaScript. Nécessite Node.js ; consultez le [guide du testeur d’expressions régulières](regex.md) pour les captures, remplacements et limites d’exécution.

Les codes-barres standard sont disponibles via `onekit run text-to-barcode`, `onekit run scan-barcode` et `onekit run barcode-to-text`. Installez le complément `barcode` ou `qrcode`. Voir [les paramètres des codes-barres et les normes prises en charge](qrcode.md#standard-linear-barcodes).

`onekit --version` rapporte la version du noyau. `python -m onekit` invoque le même CLI.

| Commande | Comportement |
| --- | --- |
| `onekit list [--group GROUP] [--json]` | Découvrir les outils, les contrats, la disponibilité et la fidélité. |
| `onekit doctor [TOOL_ID] [--json]` | Vérifiez les packages, moteurs et blocs de politique de licence Python. |
| `onekit run TOOL_ID INPUTS -o OUTPUT` | Traite les fichiers ; le chiffrement accepte aussi les dossiers. |
| `onekit pipeline --steps WORKFLOW INPUTS -o OUTPUT` | Exécute de 1 à 16 étapes ordonnées, définies dans un fichier JSON. |
| `onekit engines install [--directory DIRECTORY]` | Installez les moteurs développeurs Node verrouillés ; nécessite Node/npm. |
| `onekit download URL -o OUTPUT [--quality best\|720\|1080] [--force]` | Télécharger une seule vidéo via yt-dlp ; nécessite internet et FFmpeg. |

`run` accepte `--options` avec un objet JSON, `--ask-password` et `--force`. Les pipelines prennent également en charge l’invite de mot de passe et le drapeau de remplacement. Utilisez un nom de fichier pour une sortie ou un répertoire pour plusieurs sorties. Les destinations sans extension sont des répertoires. Les noms de sortie conflictuels sont refusés.

<a id="local-agents-and-automation"></a>
## Local agents and automation

**Votre CLI. Votre CLI agentique.** OneKit est utile à la fois sur votre terminal et comme boîte à outils de traitement de fichiers pour les agents locaux AI qui peuvent exécuter des commandes shell ou lancer des sous-processus. Un agent peut découvrir les contrats des outils, vérifier les exigences, exécuter une opération sélectionnée et inspecter ses fichiers de sortie.

```sh
onekit list --json
onekit doctor pdf-merge --json
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit pipeline --steps workflow.1kit input.pdf -o output/
```

`list --json` expose les identifiants des outils, les entrées acceptées, les formats de sortie, les options, les limites et les notes de fidélité. `doctor TOOL_ID --json` rapporte l'état de préparation, les dépendances manquantes et les blocages liés à la politique de licence. Analysez ces réponses JSON plutôt que les listes lisibles par l'homme. `run` et `pipeline` écrivent leurs résultats dans la destination fournie avec `-o` ; ils n'ont pas de drapeau de réponse `--json` général. Certains outils produisent des fichiers de rapport JSON.

Pour un agent local, découvrez d'abord l'outil, vérifiez ses exigences, puis appelez-le avec des chemins explicites et un objet JSON dans `--options` là où c'est nécessaire. Passez les arguments du sous-processus sous forme de liste pour préserver les chemins et JSON sans avoir à gérer les guillemets du shell. Vérifiez le statut de sortie avant de traiter les résultats :

| Code de sortie | Signification |
| --- | --- |
| `0` | Commande terminée avec succès. |
| `1` | `doctor` a trouvé des exigences manquantes ou un bloc de politique ; inspectez le rapport. |
| `2` | Arguments invalides ou erreur de traitement/lecture/écriture ; consultez stderr. |
| `130` | Commande annulée par une interruption clavier. |

Choisissez un nouveau chemin de sortie pour chaque tâche ; les sorties existantes sont conservées sauf si `--force` est fourni. `--ask-password` nécessite un terminal interactif. Préparez les dépendances et les caches de modèles avant les exécutions non surveillées : les composants manquants peuvent déclencher une configuration automatique et des téléchargements depuis le réseau, et certains installateurs natifs nécessitent une interaction ou des privilèges élevés. Les outils réseau contactent également leurs sources demandées.

Le traitement des fichiers s’exécute sur votre machine. Si l’agent utilise un modèle distant, la gestion par l’agent du contenu des fichiers et des résultats des commandes détermine ce qui est envoyé à ce fournisseur. La même licence [PolyForm Shield](licenses.md) s’applique pour une utilisation pilotée par l’agent.

<a id="tool-options"></a>
## Tool options

La génération QR, la configuration vCard/Wi-Fi, la numérisation d'images et le décodage inversé sont documentés dans le guide de code [QR](qrcode.md). Installez le complément `qrcode`, puis utilisez `onekit run text-to-qrcode input.txt -o code.png` ou `onekit run scan-qrcode photo.jpg -o decoded.json`.

Les pages sont numérotées à partir de 1. `pages` accepte des numéros et des plages croissantes, comme `1,3-5`. Les opérations d’organisation et d’extraction conservent l’ordre et les doublons intentionnels. La rotation accepte les multiples de 90 et s’applique par défaut à toutes les pages. La modification des PDF ajoute `text` à `page` aux coordonnées `x`/`y`, exprimées en points PDF depuis l’angle inférieur gauche ; elle ne redistribue pas le contenu existant. La signature nécessite le chemin d’un `certificate` PKCS#12 et son `password`.

L'image `format` prend en charge PNG, JPEG, WebP, TIFF, BMP, ICO, GIF et PDF selon le cas. `quality` est 1–100. `box` est `[left, top, right, bottom]` en pixels. L'animation/les métadonnées peuvent être supprimées ; la transparence est aplatie en blanc pour JPEG/PDF. La compression peut augmenter un fichier déjà optimisé.

L’option `sheet` sélectionne une feuille de calcul, celle active par défaut. La lecture Excel utilise les valeurs de formule mises en cache. JSON-à-Excel attend un tableau d’objets. CSV `delimiter` par défaut à la virgule. Les chaînes type formule XLSX restent du texte ; importer le CSV non fiable comme texte dans les applications de feuille de calcul.

La conversion d'encodage accepte `source_encoding` et `encoding`. D'autres outils de texte utilisent UTF-8.. Pour PDF, JPEG et PNG, `metadata` accepte les champs de texte descriptifs `Title`, `Author`, `Subject`, `Keywords` et `Comment`. Les champs non spécifiés sont conservés ; une chaîne vide efface la valeur d'un champ. L'assistant Python `onekit.tools.file_metadata.read_metadata(artifact)` lit ces champs sans modifier l'artefact, y compris le texte et les valeurs EXIF, PNG et XMP pris en charge. D'autres formats de métadonnées utilisent des paires tag/valeur ExifTool optionnelles, dans leur couverture de format. Les signatures des inspecteurs n'identifient pas tous les types de fichiers propriétaires.

La comparaison de carnet `mode` est `both`, `markdown` ou `code`. Le mode LaTeX est `all` ou heuristique `text`. La comparaison PDF/Word extrait le texte. Le diff JSON contient les côtés normalisés, les blocs modifiés et un patch unifié, y compris les différences de nouvelle ligne finale. OCR `language` utilise les codes Tesseract installés et `dpi` est 36–300. La conversion PDF/A nécessite un `icc_profile` sous licence ; validez le résultat d'archivage indépendamment.

Les options média incluent `format`, `codec` et `bitrate`, selon la version FFmpeg. Les polices supportent `ttf`, `otf`, `woff` et `woff2`, en conservant la technologie des contours. Les archives supportent ZIP et les combinaisons TAR/gzip/bzip2/xz.

<a id="limits-and-errors"></a>
## Limits and errors

Voir [validation d'entrée](input-validation.md) pour les types appliqués par outil, les limites en octets/nombre de fichiers, les vérifications de signature/conteneur et les règles d'expansion d'archives. Cela s'applique aux appels directs Python API ainsi qu'à chaque étape du pipeline et au CLI. Exécutez `onekit list --json` pour obtenir des contrats exacts lisibles par machine.

Entrées du cœur : 256 fichiers et 128 MiB. Pipelines : 16 étapes. Images et pages rendues : 40 millions de pixels. Comparaisons : 10 000 lignes et 2 millions de caractères. Décompression des archives : 128 MiB, 4096 entrées et contrôle du taux d’expansion. Les moteurs externes ont des limites de temps. Des entrées valides mais volumineuses peuvent dépasser ces limites délibérées.

Codes de sortie : 0 succès ; 1 rapport de diagnostic de doctor incomplet ; 2 erreur d’entrée/traitement ; 130 annulation. Les validateurs peuvent émettre avec succès `valid: false` : inspectez le rapport plutôt que de supposer que le code de sortie 0 signifie source valide. La vérification de type/importation peut nécessiter un projet complet. La validation de la syntaxe Python n’exécute jamais l’entrée.

L'anglais est la langue par défaut. Les futures traductions CLI utilisent le domaine gettext `onekit` sous `onekit/locales` ; les ID, noms de commandes et clés JSON restent indépendants de la langue.

La fusion de cahiers accepte `merge` avec `from` (`left` ou `right`) et l’index de cellule modifiée basé sur zéro `block`, ainsi que `mode`. Elle génère le cahier cible mis à jour et conserve les cellules exclues ainsi que les métadonnées du cahier. Les correctifs unifiés décrivent la représentation comparée et ne sont généralement pas des correctifs pour PDF, Word ou les conteneurs de cahiers bruts.

<a id="image-effects"></a>
## Image effects

`onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output` combine flou, pixelisation, flou en boîte, couverture solide et niveaux de gris dans un seul outil. Utilisez `scope: "selected"` avec des rectangles à coordonnées normalisées dans `regions` pour cibler des zones spécifiques. Consultez le [guide des effets d’image](image-effects.md) pour toutes les options et limites.

<a id="portable-workflows"></a>
## Portable workflows

`onekit workflow export SOURCE -o workflow.1kit` valide un tableau d’étapes hérité ou un document de workflow et sauvegarde un document portable. `onekit workflow import workflow.1kit -o saved.1kit` valide et sauvegarde un document importé. Les deux commandes omettent les mots de passe et refusent les chemins de sortie existants sauf si `--force` est fourni. Aucune des deux commandes ne traite les fichiers.

Exécutez un workflow importé avec `onekit pipeline --steps saved.1kit INPUTS -o OUTPUT`. L'extension .1kit identifie les documents OneKit ; les fichiers de workflow .json et .onekit.json ainsi que les tableaux d'étapes hérités restent pris en charge. Les documents de workflow sont UTF-8 JSON, au maximum 1 MiB, avec la structure suivante :

```json
{
  "format": "onekit-workflow",
  "version": 1,
  "steps": [{"tool": "dev-format-json", "options": {}}]
}
```

<a id="automatic-setup"></a>
## Automatic setup

`onekit run`, `onekit download` et `onekit pipeline` installent les packages manquants Python et les moteurs natifs avant le traitement. Les dépendances sont conservées dans le cache utilisateur OneKit, sans modifier l'installation système Python. Les modèles Whisper et U2Net se téléchargent automatiquement lors de la première utilisation et sont mis en cache pour les utilisations ultérieures. Les données linguistiques OCR sont récupérées pour les langues demandées.

La première exécution nécessite une connexion Internet et suffisamment d'espace disque. Les moteurs natifs utilisent conda-forge via une installation privée de micromamba, ou le gestionnaire de paquets du système pour les moteurs non disponibles là-bas ; la disponibilité dépend du système d'exploitation et de l'architecture. Les échecs de configuration arrêtent le traitement avec une erreur et peuvent être réessayés. `onekit doctor` vérifie la préparation sans rien installer. `ONEKIT_CACHE` change l'emplacement du cache de configuration. `ONEKIT_ALLOW_COPYLEFT=0` continue de bloquer les moteurs restreints.

<a id="local-license-and-copyright-estimates"></a>
## Local license and copyright estimates

Le groupe `licenses` fournit `license-pdf`, `license-word`, `license-powerpoint`, `license-excel`, `license-video`, `license-audio`, `license-image`, `license-font`, `license-epub`, `license-code` et `license-dataset`.

```sh
onekit run license-image photo.jpg -o report.json
onekit run license-pdf --url https://example.org/document.pdf -o report.json
onekit run license-code project.zip -o report.json
onekit run license-code ./project -o report.json
onekit run license-code --url https://github.com/owner/repository --options '{"ref":"main"}' -o report.json
onekit run license-code --url https://gitlab.com/group/project -o report.json
onekit run license-dataset data.csv LICENSE metadata.json -o report.json
```

**Chaque résultat est une estimation non vérifiée nécessitant une vérification manuelle.** Il liste les métadonnées déclarées, les avis de droit d'auteur, les noms des créateurs, la syntaxe SPDX et les correspondances potentielles de texte de licence avec leurs emplacements. Cela ne certifie jamais la propriété ni n'accorde la permission d'utiliser une œuvre. L'absence de déclarations ne signifie jamais domaine public ou utilisation libre. Les noms de créateurs ne prouvent pas la propriété du droit d'auteur. Consultez la source originale, les termes complets et l'utilisation prévue ; les dépendances et les ressources du projet peuvent avoir des licences séparées. Les références officielles expliquent les normes, pas l'authenticité ou l'applicabilité des déclarations dans une œuvre importée.

<a id="downloads-image-transforms-and-url-inspection"></a>
## Downloads, image transforms and URL inspection

```sh
onekit run audio-download --url 'https://example.org/audio.flac' -o downloads/
onekit run audio-download --url 'https://example.org/audio.wav' --options '{"format":"mp3","quality":"320"}' -o downloads/
onekit run image-download --url 'https://example.org/photo.jpg' -o downloads/
onekit run image-rotate-flip photo.png --options '{"angle":"90","flip":"horizontal"}' -o rotated.png
onekit run url-inspect --url 'https://example.org/path?x=1#section' -o report.json
```

Télécharger une image ou un fichier audio ne donne pas le droit de redistribution ou de réutilisation.

La rotation d'image applique d'abord l'orientation EXIF, tourne dans le sens des aiguilles d'une montre de 0/90/180/270 degrés, puis se reflète horizontalement, verticalement ou les deux dans le système de coordonnées tourné. Elle exporte une PNG en préservant les pixels RGBA décodés et la transparence sans métadonnées ; les images animées et multipages sont rejetées. La limite est de 40 millions de pixels.

<a id="remove-text-formatting"></a>
### Remove text formatting

`onekit run text-strip-formatting document.docx -o plain.txt` exporte le texte principal Word en UTF-8 TXT. Les fichiers TXT, HTML et Markdown sont également pris en charge, jusqu’à 8 MiB. Utilisez `--options '{"input_format":"html"}'` pour interpréter HTML stocké dans un fichier TXT. Aucune OCR n’est effectuée.

<a id="contribute-to-onekit"></a>
## Contribute to OneKit

Aidez à construire la révolution ouverte de OneKit : des outils quotidiens pour tout le monde, des tâches pratiques aux workflows gérés par les agents locaux AI. Contribuez pour rendre les outils plus efficaces : améliorez la vitesse et l'utilisation de la mémoire, corrigez les résultats incorrects, ajoutez des exemples de régression ou clarifiez la documentation et les workflows des agents.

Le cœur est Open Source (PolyForm Shield 1.0.0). Lisez le [guide de contribution](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) et trouvez une tâche dans [tickets GitHub](https://github.com/mattiapiazzalunga/onekit/issues), ou suggérez une amélioration sur le [tableau des demandes](https://onekit.org/requests/).

Questions sur le cœur Open Source (PolyForm Shield 1.0.0) et les contributions : [developers@onekit.org](mailto:developers@onekit.org). Support général : [support@onekit.org](mailto:support@onekit.org).
