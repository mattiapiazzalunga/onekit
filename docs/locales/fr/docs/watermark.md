<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-watermark"></a>
# Filigrane PDF

Dans la catégorie PDF, téléversez un PDF, saisissez du texte et ajustez l'opacité, la couleur, la police, la rotation et la position. L'aperçu montre la position du filigrane sur une page choisie. Exportez pour vérifier le rendu final de la police PDF. Choisissez un seul filigrane ou une grille répétée 3 × 4. Le texte est automatiquement réduit si nécessaire pour s'adapter à la page ou à la cellule, jusqu'à une limite de lisibilité de six points. Les PDF cryptés doivent d'abord être déverrouillés. Les signatures numériques existantes ne sont plus valides après la modification d'un document ; l'outil avertit lorsque des champs de signature sont présents.

```sh
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","pages":"1,3-5","opacity":0.25,"angle":45}'
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"DRAFT","layout":"repeat","color":"#b00000"}'
```

| Option | Valeurs / par défaut |
| --- | --- |
| `text` | 1–200 caractères, jusqu'à cinq lignes ; DÉFAUT BOURRÉE |
| `pages` | Plages basées sur un, par ex. `1,3-5` ; vide ou omis signifie tout |
| `font` | Helvetica-Gras (par défaut), Helvetica, Times-Roman, Courier |
| `font_size` | 8–160 points ; défaut 48, ajusté automatiquement si nécessaire |
| `color` | Hexadécimal à six chiffres ; par défaut #666666 |
| `opacity` | 0.05–1 ; par défaut 0.25 |
| `angle` | -180–180 degrés, dans le sens antihoraire ; 45 par défaut |
| `position` | centre, haut-gauche/centre/droite, milieu-gauche/droite, bas-gauche/centre/droite |
| `layout` | simple (par défaut) ou répéter (3 × 4 grille ; la position est ignorée) |
| `margin` | 0–144 points ; par défaut 24 |

Les polices prennent en charge les caractères et ponctuations d’Europe occidentale, y compris les accents italiens. Les caractères non pris en charge échouent explicitement. Jusqu’à 512 pages peuvent être traitées. Le placement utilise la boîte de découpe visuellement orientée, en conservant la rotation originale et les coordonnées des annotations. Un filigrane étiquette le contenu visible ; il ne supprime pas le contenu sous-jacent.
