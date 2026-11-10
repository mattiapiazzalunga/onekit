<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="input-validation"></a>
# Validação de entrada

Cada entrada de catálogo declara formatos aceitos, contagens de arquivos e limites de byte. `onekit list --json` expõe os valores. Tanto a execução direta como os pipelines impõem os contratos.

<a id="limits"></a>
## Limites

O teto global de lote é 128 MiB e 256 arquivos. Entradas de texto são limitadas a 8 MiB por arquivo, imagens raster para 64 MiB e fontes para 16 MiB. Uma diff requer exatamente duas entradas. As imagens raster decodificadas são limitadas a 40 milhões de pixels através das molduras. A expansão do arquivo e do escritório é limitada a 128 MiB e 4096 entradas.

Ferramentas de entrada única rejeitam arquivos extras. O mapeamento de tubulação aplica deliberadamente um único passo de entrada em cada saída anterior. Coleções de saída são verificadas incrementalmente para que uma etapa mapeada não possa acumular dados devolvidos ilimitados. CLI contagens de arquivos, extensões e tamanhos são verificados antes de ler o conteúdo do arquivo, e os bytes reais lidos são limitados mesmo se um arquivo cresce durante a leitura.

<a id="content-rules"></a>
## Regras de conteúdo

- PDF ferramentas requerem PDF cabeçalhos e uma localização de referência cruzada final coerente. `pdf-repair` permite deliberadamente que as referências cruzadas sejam danificadas após verificação da PDF header; seu analisador ainda tem que recuperar um real PDF. Imagens renomeadas para `.pdf` são rejeitados.
- As entradas raster são verificadas com Pillow para o formato real, estrutura e dimensões decodificadas. Um PNG renomeado para JPEG é rejeitado. Base64 exportação também decodifica a imagem antes de aceitá-la.
- Word, Excel e PowerPoint exigir distinta ZIP peças do recipiente e nome espaçado XML raízes. Renomeação Excel para `.docx` não o transforma em Word. Contagens de diretórios e orçamentos de expansão são inspecionados antes de alocar ZIP tabela de entrada ou partes do documento de leitura.
- Os tipos de letra requerem cabeçalhos SFNT/WOFF correspondentes, faixas de tabela delimitadas válidas e tamanhos coerentes compressed-font. Declarada expansão WOFF não pode exceder o orçamento do bytes de fonte.
- Entradas de mídia têm extensões explícitas de áudio/vídeo e assinaturas de container. A FFprobe verifica os tipos de fluxo antes da conversão FFmpeg; a conversão de vídeo requer vídeo, e a conversão de áudio requer áudio sem fluxos de vídeo comuns. É permitida uma imagem de capa incorporada. Ambos os executáveis são reportados por `doctor`.
- Arquivos rejeitam caminhos inseguros/duplicados, links simbólicos, criptografados ZIP entradas, diretórios inválidos, multi- volume/ZIP64 diretórios e fluxos comprimidos concatenados não suportados. ZIP as razões de expansão são limitadas. TAR a descompressão é limitada antes da análise do membro/PAX, com uma fixação adicional 4 MiB Subsídio de TAR cabeçalhos/padding; XZ A memória do decodificador também é limitada.
- A descodificação aceita apenas o formato codificado OneKit e autentica seu conteúdo antes da restauração limitada do arquivo. As opções do usuário não podem aumentar o orçamento de expansão forçada.
- Ferramentas de texto requerem texto decodificado sem bytes de controle binário. Ferramentas de desenvolvimento aceitam suas extensões de linguagem e entrada neutra `.txt`; adaptadores shell/Dockerfile também permitem fonte sem extensão. Ferramentas de validação aceitam intencionalmente fonte sintática inválida e retornam `valid: false`. A conversão da codificação usa a codificação de origem seleccionada; outras ferramentas de texto requerem UTF-8.
- Inspeção, adaptadores de metadados e criptografia aceitam intencionalmente tipos de arquivos arbitrários. Seus limites de contagem/byte ainda se aplicam. Inspecionar um arquivo danificado ou desconhecido é uma operação suportada, ao invés de uma razão para rejeitá-lo apenas pelo seu conteúdo.
