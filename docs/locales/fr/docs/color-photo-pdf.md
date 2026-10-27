<a id="color-photo-restoration-and-pdf-forms"></a>
# Couleur, restauration de photo et formulaires PDF

Ces outils sont accessibles via la commande standard `onekit run TOOL ... --options JSON` et Python `execute` API. Voir `onekit run --help` pour les arguments d'entrée/sortie. Toutes les coordonnées ci-dessous se réfèrent à l'image après l'orientation EXIF ou à la page affichée PDF après rotation.

- `color-picker` : inspecter un fichier UTF-8 contenant `#RRGGBB`, ou échantillonner une image avec des coordonnées entières de pixels `x` et `y` (au centre par défaut). Indique HEX, RGB, OKLCH, contraste texte noir/blanc et RGBA original pour les images. Les couleurs visibles sont composées sur fond blanc.
- `image-extract-colors` : `colors` (2–32, par défaut 6). Quantification par coupe médiane d’une miniature limitée à 256 × 256. Les pixels entièrement transparents sont exclus ; l’alpha partiel est composé sur blanc. Les fractions décrivent cet échantillon.
- `jpg-to-svg` : `colors` (2–32, par défaut 16), `resolution` (32–512, par défaut 256). Quantifie une image limitée, fusionne verticalement les suites horizontales de même couleur et écrit des chemins SVG remplis. Aucun bitmap n'est intégré. Cela produit des tuiles vectorielles avec un aspect postérisé, pas un tracé de courbes lisses.
- `image-repair` : sans `regions`, applique un filtre médian de `size` 3 ou 5 aux taches isolées. Avec des régions, reconstruit les pixels sélectionnés en utilisant les pixels environnants fixes et la diffusion harmonique discrète (`iterations` 10–500, par défaut 200).
- `image-remove-watermark` : nécessite `regions` ; utilise la même reconstruction locale. Il estime les pixels manquants et ne peut pas récupérer le contenu original caché. La texture, les grandes marques et les arrière-plans complexes peuvent produire de mauvais résultats.
- `image-sharpen` : `method` vaut `unsharp` (par défaut) ou `deconvolution`. `radius`, entre 0.3 et 5, définit le rayon du masque flou ou l’étalement gaussien estimé d’un point. Pour le masque flou, `amount` varie de 0 à 300 pour cent (150 par défaut). Richardson–Lucy utilise de 1 à 30 `iterations` (10 par défaut), un prolongement des bords par réflexion et une convolution FFT, jusqu’à un million de pixels source. Il suppose un flou gaussien et ne corrige pas les mouvements arbitraires. Les deux méthodes peuvent amplifier le bruit et les halos.
- `pdf-remove-watermark` : par défaut, `mode: "remove"` supprime les groupes `/Artifact` marqués `/Subtype /Watermark` (y compris les ressources de propriété nommées) et les annotations `/Watermark`. Le paramètre facultatif `text` recherche des objets textuels complets après normalisation des espaces et décodage des glyphes à l’aide de l’encodage de la police ou de la table ToUnicode. Les objets XObject de type Form imbriqués sont traités de manière récursive. Utilisez `mode: "inspect"` pour obtenir un rapport JSON des IDs de texte, d'image et d'appel de Form XObject ; passez les IDs sélectionnés comme `objects` en mode suppression. La sélection d’un objet Form XObject supprime tout son groupe graphique. Les objets Form XObject modifiés sont copiés par appel, donc les utilisations non sélectionnées d’une ressource partagée restent inchangées. Les IDs font référence au même PDF d’origine et doivent être réexaminés après les modifications. Il s'agit de la suppression d'objets de dessin, pas du masquage sécurisé des données : des objets de ressources inutilisés peuvent rester dans le résultat. Cela n'identifie pas automatiquement le contenu non étiqueté comme un filigrane, et une marque fusionnée dans une image numérisée ne peut pas être séparée de cette image. Un rapport contient jusqu'à 2 000 éléments candidats, la récursion est limitée à 12 niveaux et le traitement à 300 000 opérations graphiques. Si aucune correspondance n’est trouvée, une erreur explicite est produite.
- `pdf-make-fillable` : `fields` est un tableau JSON de composants AcroForm standard. Chaque composant possède un `name` ASCII unique, un `type` (`text`, `checkbox`, `choice`), une `page` numérotée à partir de 1 et des coordonnées normalisées `x`, `y`, `width`, `height`. Sont pris en charge le paramètre facultatif `required`, `multiline` pour le texte et `choices` pour les listes de choix. Les champs existants et le contenu des pages sont préservés. Les noms en double, les PDF chiffrés et XFA sont refusés. Aucune détection automatique des espaces vides.

Les régions d'image sont des tableaux d'objets tels que `{"page":1,"x":0.2,"y":0.3,"width":0.1,"height":0.05}`. Les coordonnées sont normalisées à 0–1 depuis le coin supérieur gauche. La reconstruction prend en charge jusqu'à 100 rectangles, au maximum 35 % de l'image et une boîte englobante (y compris le remplissage) d'un million de pixels. Seules RGB à l'intérieur du masque changent ; l'alpha d'origine est conservé. Les sorties sont PNG sans métadonnées source. Les images animées/multicadres sont rejetées. Le décodage général d'images est limité à 40 millions de pixels. Les PDFs sont limités à 256 pages et les formulaires à 200 nouveaux champs.

Exemple d'utilisation de Python :

```python
from onekit import Artifact, execute

result = execute("pdf-make-fillable", [Artifact("source.pdf", pdf_bytes)], {
    "fields": [{"name": "Name", "type": "text", "page": 1,
                "x": 0.1, "y": 0.2, "width": 0.4, "height": 0.05}]
})
```

Passez en revue les fichiers résultants et conservez les originaux. Un lecteur PDF compatible est nécessaire pour remplir et enregistrer les formulaires.
