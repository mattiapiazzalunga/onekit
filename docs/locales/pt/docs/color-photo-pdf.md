<a id="color-photo-restoration-and-pdf-forms"></a>
# Cor, restauração de fotos e PDF formulários

Estas ferramentas são expostas através do padrão `onekit run TOOL ... --options JSON` comando e o Python `execute` API. Ver `onekit run --help` Para os argumentos de entrada/saída. Todas as coordenadas abaixo referem-se à imagem após EXIF orientação ou o mostrado PDF página após rotação.

- `color-picker`: inspeccionar a UTF-8 arquivo contendo `#RRGGBB`, ou amostrar uma imagem com opções de pixel inteiro `x` e `y` (centro por padrão). Relatórios HEX, RGB, OKLCH, contraste texto preto/branco e original RGBA para imagens. As cores visíveis são compostas em branco.
- `image-extract-colors`: `colors` (2–32, padrão 6). Quantificação mediana-cortada de uma miniatura limitada a 256 × 256. São excluídos os pixels totalmente transparentes; o alfa parcial é composto em branco. Fracções descrevem esta amostra.
- `jpg-to-svg`: `colors` (2–32, padrão 16), `resolution` (32–512, padrão 256). Quantiza uma imagem delimitada, funde horizontalmente igual-color executa verticalmente e escreve SVG caminhos preenchidos. Nenhum bitmap está incorporado. Isto produz azulejos vetoriais com uma aparência posterizada, não traçado de curvas suaves.
- `image-repair`: sem `regions`, aplica um filtro mediano de `size` 3 ou 5 a manchas isoladas. Com regiões, reconstrui pixels selecionados usando pixels fixos ao redor e difusão harmônica discreta (`iterations` 10–500, padrão 200).
- `image-remove-watermark`: requer `regions`; usa a mesma reconstrução local. Estima os pixels em falta e não consegue recuperar o conteúdo original oculto. Textura, grandes marcas e fundos intrincados podem dar resultados ruins.
- `image-sharpen`: `method` é `unsharp` (por omissão) ou `deconvolution`. `radius` 0.3–5 define o raio não-afiado ou estimativa Gaussian point spread. Não Afiado `amount` 0–300 por cento (padrão 150). Richardson–Lucy usa 1–30 `iterations` (default 10), refletindo enchimento e convolução FFT, até um milhão de pixels fonte. Ele assume o borrão gaussiano e não corrige o movimento arbitrário. Ambos podem amplificar o ruído e halos.
- `pdf-remove-watermark`: padrão `mode: "remove"` remove `/Artifact` grupos marcados `/Subtype /Watermark` (incluindo os recursos de propriedades nomeados) e `/Watermark` Anotações. Opcional `text` corresponde a objetos de texto completos com espaços em branco normalizados, decodificando glifos através de sua codificação de fonte / mapa ToUnicode. Forma Aninhada XObjects são processados recursivamente. Utilização `mode: "inspect"` para obter um JSON relatório de IDs de texto, imagem e invocação do formulário; passe IDs selecionados como `objects` em modo de remoção. A seleção de um formulário remove todo o seu grupo gráfico. Os formulários modificados são copiados por invocação para que os usos não selecionados de um recurso compartilhado permaneçam inalterados. IDs referem-se ao mesmo original PDF e deve ser reinspeccionado após as mudanças. Isto é remoção de desenho-objeto, não redação segura: objetos de recursos não utilizados podem permanecer na saída. Ele não identifica o conteúdo arbitrário desmarcado como uma marca d'água automaticamente, e uma marca fundida em uma imagem digitalizada não pode ser separada dessa imagem. Um relatório contém até 2.000 candidatos, a recursão é limitada a 12 níveis e processamento para 300.000 operações de desenho. Zero correspondências produz um erro explícito.
- `pdf-make-fillable`: `fields` é uma matriz JSON de widgets padrão AcroForm com único ASCII `name`, `type` (`text`, `checkbox`, `choice`), 1 base `page`, normalizado `x`, `y`, `width`, `height`. Opcional `required`, texto `multiline` e escolha `choices` são suportados. Campos existentes e conteúdo de página são preservados. Duplicar nomes, PDFs criptografados e XFA são rejeitados. Sem reconhecimento automático em branco.

Regiões de imagem são arrays de objetos como `{"page":1,"x":0.2,"y":0.3,"width":0.1,"height":0.05}`. As coordenadas são normalizadas para 0-1 a partir da parte superior esquerda. A reconstrução suporta até 100 retângulos, no máximo 35% da imagem e uma caixa delimitadora (incluindo estofamento) de um milhão de pixels. Apenas RGB dentro da máscara muda; o alfa original é retido. As saídas são PNG sem metadados de origem. Imagens animadas/multiframe são rejeitadas. A decodificação geral da imagem é limitada a 40 milhões de pixels. PDFs são limitados a 256 páginas e formulários para 200 novos campos.

Exemplo Python de utilização:

```python
from onekit import Artifact, execute

result = execute("pdf-make-fillable", [Artifact("source.pdf", pdf_bytes)], {
    "fields": [{"name": "Name", "type": "text", "page": 1,
                "x": 0.1, "y": 0.2, "width": 0.4, "height": 0.05}]
})
```

Revise os arquivos resultantes e mantenha os originais. Um leitor compatível PDF é necessário para preencher e salvar formulários.
