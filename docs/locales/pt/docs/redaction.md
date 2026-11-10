<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="permanent-redaction"></a>
# Redação permanente

<a id="pdf"></a>
## PDF

Cada página é renderizada, os pixels selecionados são substituídos por preto opaco, e uma nova PDF é construída a partir das imagens já redatadas. Nenhum objeto PDF original é copiado. Isto remove texto selecionável original, OCR camadas, camadas ocultas, campos de forma, objetos de anotações/comentários, links, scripts, anexos, metadados, miniaturas e histórico de gravação incremental da saída. As aparências de anotações visíveis são achatadas em pixels para que uma anotação opaca existente não revele inesperadamente o conteúdo que cobriu. Reveja a pré-visualização para diferenças de aparência de campo/anotação; nenhum objeto interativo é retido. O conteúdo da página visível não selecionado permanece como pixels.

<a id="images"></a>
## Imagens

Pixels são substituídos por preto sólido antes de codificar um novo opaco RGB PNG. Não há sobreposição removível, camada original ou dados originais de pixels desmascarados nas regiões codificadas. Origem EXIF, GPS, XMP, comentários, perfis, miniaturas e outros metadados originais não são copiados. Transparência é composta em branco, descartando escondido RGB valores sob pixels transparentes. EXIF a orientação é aplicada antes de interpretar as áreas. Entradas animadas e multi-frame são rejeitadas, de modo que quadros extras não podem permanecer não editados; exporte um frame primeiro.

<a id="cli-and-workflows"></a>
## CLI e fluxos de trabalho

Instalar `onekit-tools[pdf]` em vez PDF redaction ou `onekit-tools[images]` para imagens. Ambas as ferramentas aceitam `regions`, uma matriz de retângulos, opcionalmente serializados como um JSON Cordel. Cada retângulo tem `page` (um baseado, padrão 1), `x`, `y`, `width`, `height`. As coordenadas são frações da página/imagem visualmente orientada com origem no canto superior esquerdo: `0.1` significa 10%. Para imagens, `page` deve ser 1. Até 500 retângulos podem ser selecionados. Limites devem caber dentro da página; máscaras redondas para fora e expandir um pixel de saída para cobrir bordas fracionárias.

```sh
onekit run pdf-redact private.pdf -o redacted.pdf --options '{"regions":[{"page":1,"x":0.1,"y":0.2,"width":0.5,"height":0.1}],"dpi":200}'
onekit run image-redact private.jpg -o redacted.png --options '{"regions":[{"x":0.2,"y":0.2,"width":0.3,"height":0.2}]}'
```
