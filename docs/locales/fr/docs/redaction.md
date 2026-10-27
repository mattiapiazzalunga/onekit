<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanent-redaction"></a>
# Masquage définitif

<a id="pdf"></a>
## PDF

Chaque page est rendue, les pixels sélectionnés sont remplacés par du noir opaque, et un nouveau PDF est construit à partir des images déjà expurgées. Aucun objet PDF original n’est copié. Cela supprime le texte sélectionnable original, les couches OCR, les couches cachées, les champs de formulaire, les objets d’annotation/commentaire, les liens, les scripts, les pièces jointes, les métadonnées, les vignettes et l’historique des enregistrements incrémentiels de la sortie. Les apparences d’annotation visibles sont aplaties en pixels afin qu’une annotation opaque existante ne révèle pas de manière inattendue le contenu qu’elle recouvrait. Vérifiez l’aperçu pour détecter les différences d’apparences des champs/annotations ; aucun objet interactif n’est conservé. Le contenu de page visible non sélectionné reste sous forme de pixels.

<a id="images"></a>
## Images

Les pixels sont remplacés par du noir solide avant de coder un nouveau RGB PNG opaque. Il n'y a pas de superposition amovible, de calque original ou de données de pixels originales non masquées dans les zones codées. Source EXIF, GPS, XMP, commentaires, profils, vignettes et autres métadonnées originales ne sont pas copiés. La transparence est fusionnée sur du blanc, en supprimant les valeurs RGB cachées sous les pixels transparents. L'orientation EXIF est appliquée avant l'interprétation des zones. Les entrées animées et multi-images sont refusées afin qu'aucune image supplémentaire ne reste non censurée ; exportez d'abord une seule image.

<a id="cli-and-workflows"></a>
## CLI and workflows

Installez `onekit-tools[pdf]` pour le masquage définitif des PDF ou `onekit-tools[images]` pour les images. Les deux outils acceptent `regions`, un tableau de rectangles, éventuellement sérialisé sous forme de chaîne JSON. Chaque rectangle a `page` (basé sur un index commençant à un, par défaut 1), `x`, `y`, `width`, `height`. Les coordonnées sont des fractions de la page/image orientée visuellement avec l'origine en haut à gauche : `0.1` signifie 10%. Pour les images, `page` doit être 1. Jusqu'à 500 rectangles peuvent être sélectionnés. Les limites doivent tenir à l'intérieur de la page ; les limites des masques sont arrondies vers l’extérieur et élargies d’un pixel de sortie pour recouvrir aussi les fractions de pixels sur les bords.

```sh
onekit run pdf-redact private.pdf -o redacted.pdf --options '{"regions":[{"page":1,"x":0.1,"y":0.2,"width":0.5,"height":0.1}],"dpi":200}'
onekit run image-redact private.jpg -o redacted.png --options '{"regions":[{"x":0.2,"y":0.2,"width":0.3,"height":0.2}]}'
```
