<a id="image-effects"></a>
# Efeitos de imagem

```sh
onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output
onekit run image-effects photo.jpg --options '{"effect":"blur","strength":12,"scope":"selected","regions":[{"x":0.1,"y":0.2,"width":0.3,"height":0.25}]}' -o output
```

`strength` é um inteiro de 1 a 100 pixels (pelo menos 2 para pixelação). `scope` é `all` (por omissão) ou `selected`; modo selecionado requer 1–500 retângulos com coordenadas 0–1 normalizadas e opcional `page: 1`. `color` usos `#RRGGBB` para uma cobertura sólida. A intensidade não tem efeito na escala de cinza ou cobertura sólida. Áreas sobrepostas são processadas a partir de pixels originais, sem borrão cumulativo. No máximo 80 milhões de pixels selecionados são processados, contando sobreposições.

Borrão e pixelação são efeitos visuais e não pode garantir a remoção de detalhes sensíveis. Use a redação permanente da imagem quando o conteúdo deve ser irrecuperávelmente coberto.
