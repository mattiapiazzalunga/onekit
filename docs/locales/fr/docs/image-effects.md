<a id="image-effects"></a>
# Effets d'image

```sh
onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output
onekit run image-effects photo.jpg --options '{"effect":"blur","strength":12,"scope":"selected","regions":[{"x":0.1,"y":0.2,"width":0.3,"height":0.25}]}' -o output
```

`strength` est un entier allant de 1 à 100 pixels (au moins 2 pour la pixellisation). `scope` est `all` (par défaut) ou `selected` ; le mode sélectionné nécessite 1–500 rectangles avec des coordonnées 0–1 normalisées et `page: 1` optionnel. `color` utilise `#RRGGBB` pour une couverture solide. L'intensité n'a aucun effet sur le niveau de gris ou la couverture solide. Les zones qui se chevauchent sont traitées à partir des pixels originaux, sans flou cumulatif. Au maximum, 80 millions de pixels sélectionnés sont traités, en comptant les chevauchements.

Le flou et la pixellisation sont des effets visuels et ne garantissent pas la suppression des détails sensibles. Utilisez le masquage définitif des images lorsque le contenu doit être recouvert de façon irréversible.
