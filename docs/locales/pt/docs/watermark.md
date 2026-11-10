<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="pdf-watermark"></a>
# PDF marca d'água

Na categoria PDF, carregue um PDF, digite texto e ajuste opacidade, cor, fonte, rotação e posição. A visualização mostra a posição da marca d'água em uma página escolhida. Exportar para inspecionar a renderização final de fonte PDF. Escolha uma única marca d'água ou uma rede de 3 × 4. O texto é automaticamente reduzido quando necessário para caber a página ou célula, até um limite de legibilidade de seis pontos. PDFs criptografados devem ser desbloqueados primeiro. As assinaturas digitais existentes já não verificam depois de modificar um documento; a ferramenta avisa quando os campos de assinatura estão presentes.

```sh
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","pages":"1,3-5","opacity":0.25,"angle":45}'
onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"DRAFT","layout":"repeat","color":"#b00000"}'
```

| Opção | Valores / padrão |
| --- | --- |
| `text` | 1–200 caracteres, até cinco linhas; DRAFT padrão |
| `pages` | Gamas de uma base, p. ex. `1,3-5`; vazio ou omitido significa tudo |
| `font` | Helvetica-Bold (padrão), Helvetica, Times-Roman, Courier |
| `font_size` | 8–160 pontos; padrão 48, montado automaticamente quando necessário |
| `color` | Hex de seis dígitos; padrão #666666 |
| `opacity` | 0,05-1; padrão 0.25 |
| `angle` | -180-180 graus, no sentido anti- horário; padrão 45 |
| `position` | centro, superior esquerdo/centro/direita, médio-esquerda/direita, inferior-esquerdo/centro/direito |
| `layout` | única (padrão) ou repetição (3 × 4 grade; a posição é ignorada) |
| `margin` | 0–144 pontos; padrão 24 |

Fontes suportam caracteres da Europa Ocidental e pontuação, incluindo acentos italianos. Os caracteres não suportados falham explicitamente. Até 512 páginas podem ser processadas. A colocação utiliza a caixa de recorte orientada visualmente, mantendo as coordenadas de rotação e anotação originais. Uma marca d'água etiqueta o conteúdo visível; não remove o conteúdo subjacente.
