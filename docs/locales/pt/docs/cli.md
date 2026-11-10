<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-reference"></a>
# Referência da CLI

Use `onekit run pdf-watermark input.pdf -o watermarked.pdf --options '{"text":"CONFIDENTIAL","opacity":0.25}'` para adicionar uma marca d'água de PDF texto. Veja o guia [watermark](watermark.md) para posição, rotação, intervalos de páginas e layouts repetidos.

Redação permanente está disponível em `onekit run pdf-redact` e `onekit run image-redact`, com áreas selecionáveis fornecidas através de `regions`. Veja o guia [redaction](redaction.md) para coordenadas, rasterização e garantias de privacidade dos arquivos exportados.

Use `onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"[0-9]+","flags":"g"}'` para testar JavaScript expressões regulares. Requer Node.js; veja o guia de teste [regex](regex.md) para captura, substituição e limites de execução.

Códigos de barras padrão estão disponíveis através `onekit run text-to-barcode`, `onekit run scan-barcode` e `onekit run barcode-to-text`. Instalar o `barcode` ou `qrcode` Extra. Ver o [configurações de código de barras e padrões suportados](qrcode.md#standard-linear-barcodes).

`onekit --version` relata a versão principal. `python -m onekit` invoca o mesmo CLI.

| Comando | Comportamento |
| --- | --- |
| `onekit list [--group GROUP] [--json]` | Descubra ferramentas, contratos, disponibilidade e fidelidade. |
| `onekit doctor [TOOL_ID] [--json]` | Verifique Python pacotes, motores e blocos de política de licença. |
| `onekit run TOOL_ID INPUTS -o OUTPUT` | Processar arquivos; criptografia também aceita diretórios. |
| `onekit pipeline --steps WORKFLOW INPUTS -o OUTPUT` | Execute 1-16 passos de ferramenta ordenados a partir de um arquivo JSON. |
| `onekit engines install [--directory DIRECTORY]` | Instalar os motores de desenvolvimento do Node bloqueados; requer o Node/npm. |
| `onekit download URL -o OUTPUT [--quality best\|720\|1080] [--force]` | Baixe um único vídeo através do yt-dlp; requer internet e FFmpeg. |

`run` aceita `--options` com um objeto JSON, `--ask-password` e `--force`. Pipelines suportam o prompt de senha e sobrescrever bandeira também. Use um nome de arquivo para uma saída ou um diretório para várias saídas. Destinos sem extensão são diretórios. Os nomes de saída em conflito são rejeitados.

<a id="local-agents-and-automation"></a>
## Agentes locais e automatização

O teu CLI. Seu agente CLI.** OneKit é útil tanto em seu terminal quanto como um kit de ferramentas de processamento de arquivos para agentes locais AI que podem executar comandos shell ou lançar subprocessos. Um agente pode descobrir contratos de ferramenta, verificar os requisitos, executar uma operação selecionada e inspecionar seus arquivos de saída.

```sh
onekit list --json
onekit doctor pdf-merge --json
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit pipeline --steps workflow.1kit input.pdf -o output/
```

`list --json` expõe IDs de ferramentas, entradas aceitas, formatos de saída, opções, limites e notas de fidelidade. `doctor TOOL_ID --json` relata prontidão, dependências em falta e bloqueios de política de licença. Analisar estes JSON respostas em vez das listas de leitura humana. `run` e `pipeline` escrever os seus resultados para o destino fornecido com `-o`; eles não têm um general `--json` Sinal de resposta. Algumas ferramentas produzem JSON apresentar relatórios de ficheiros.

Para um agente local, descubra a ferramenta primeiro, verifique seus requisitos, depois chame-o com caminhos explícitos e um objeto JSON em `--options` onde necessário. Passe os argumentos de subprocesso como uma lista para preservar caminhos e JSON sem cotação shell. Verifique o estado de saída antes de consumir saídas:

| Código de saída | Significado |
| --- | --- |
| `0` | Comando concluído com sucesso. |
| `1` | `doctor` encontraram requisitos em falta ou um bloco de políticas; inspeccione o relatório. |
| `2` | Argumentos inválidos ou um erro de processamento/input/output; leia stderr. |
| `130` | Comando cancelado com uma interrupção do teclado. |

Escolha um caminho de saída novo para cada tarefa; as saídas existentes são preservadas, a menos que `--force` sejam fornecidas. `--ask-password` requer um terminal interativo. Prepare dependências e caches de modelos antes de executar sem vigilância: componentes ausentes podem desencadear configurações automáticas e downloads de rede, e alguns instaladores nativos requerem interação ou privilégios elevados. As ferramentas de rede também entram em contato com suas fontes solicitadas.

O processamento de arquivos é executado na sua máquina. Se o agente usa um modelo remoto, o gerenciamento do agente de conteúdo de arquivo e resultados de comando determina o que é enviado para esse provedor. O mesmo. [PolyForm Shield licença](licenses.md) aplica-se à utilização dirigida pelo agente.

<a id="tool-options"></a>
## Opções das ferramentas

QR geração, vCard/Wi-Fi configuração, digitalização de imagens e decodificação reversa estão documentadas no [QR guia de código](qrcode.md). Instalar o `qrcode` extra, em seguida, usar `onekit run text-to-qrcode input.txt -o code.png` ou `onekit run scan-qrcode photo.jpg -o decoded.json`.

As páginas são uma base. `pages` aceita números e intervalos ascendentes, como `1,3-5`. Ordens e duplicatas intencionais são preservadas para organizar/extrair. A rotação aceita múltiplos de 90 e padrões para todas as páginas. PDF editar adds `text` para `page` em `x`/`y` PDF pontos da origem inferior esquerda; não reflue o conteúdo existente. A assinatura requer um PKCS# 12 `certificate` caminho e sua `password`.

Imagem `format` suportes PNG, JPEG, WebP, TIFF, BMP, ICO, GIF e PDF Se for caso disso. `quality` é de 1 a 100. `box` é `[left, top, right, bottom]` em pixels. Animação / metadados podem ser removidos; transparência é achatada para branco para JPEG/PDF. A compressão pode aumentar um arquivo já otimizado.

Folha de Cálculo `sheet` selecciona uma folha de trabalho, por omissão para a activa. Excel a leitura utiliza valores de fórmula em cache. JSON- Para...Excel espera uma série de objetos. CSV `delimiter` por omissão em vírgula. Fórmula-like XLSX strings permanecem texto; importar não confiável CSV como texto em aplicações de planilha.

Conversão de codificação aceita `source_encoding` e `encoding`. Outras ferramentas de texto usam UTF-8. Para PDF, JPEG e PNG, `metadata` aceita os campos descritivos do texto `Title`, `Author`, `Subject`, `Keywords` e `Comment`. Campos não especificados são retidos; uma string vazia limpa o valor de um campo. O ajudante Python `onekit.tools.file_metadata.read_metadata(artifact)` lê esses campos sem modificar o artefato, incluindo o texto EXIF, PNG suportado e os valores XMP. Outros formatos de metadados usam pares de tags/valores ExifTool opcionais, dentro de sua cobertura de formato. As assinaturas dos inspetores não identificam cada tipo de arquivo proprietário.

Comparação do caderno de notas `mode` é `both`, `markdown` ou `code`. LaTeX modo é `all` ou heurística `text`. PDF/Word comparação extrai texto. Diferenças JSON contém lados normalizados, blocos alterados e um patch unificado, incluindo as diferenças de linha nova. OCR `language` usa códigos Tesseract instalados e `dpi` é 36–300. PDF/A conversão requer uma licença `icc_profile`; valida a saída de arquivo independentemente.

As opções de mídia incluem `format`, `codec` e `bitrate`, dependendo da FFmpeg Construir. Suporte a fontes `ttf`, `otf`, `woff` e `woff2`, preservando a tecnologia de contorno. Suporte aos arquivos ZIP e TAR/gzip/bzip2/xz combinações.

<a id="limits-and-errors"></a>
## Limites e erros

Ver [validação de entrada](input-validation.md) para os tipos de ferramentas, bytes/limites de contagem, verificações de assinatura/contentor e regras de expansão de arquivos. Estas aplicam-se às Python API chamadas e cada passo pipeline, bem como o CLI. Executar `onekit list --json` para contratos legíveis por máquina.

Entradas principais: 256 arquivos e 128 MiB. Pipelines: 16 passos. Imagens/páginas renderizadas: 40 milhões de pixels. Comparações: 10.000 linhas e 2 milhões de caracteres. Expansão do arquivo: 128 MiB, 4096 entradas e verificações de proporção. Os motores externos têm tempo limite. Grandes entradas válidas podem exceder esses limites deliberados.

Códigos de saída: 0 sucesso; 1 relatório médico incompleto; 2 erro de entrada/processamento; 130 cancelamento. Validadores podem emitir `valid: false` com sucesso: inspecionar o relatório em vez de assumir saída 0 significa fonte válida. A verificação de tipo/importação pode exigir um projeto completo. A validação de sintaxe Python nunca executa a entrada.

O inglês é o padrão. As futuras CLI traduções usam o domínio gettext `onekit` em `onekit/locales`; IDs, nomes de comando e JSON chaves permanecem independentes do idioma.

A mesclagem do caderno de notas aceita `merge` com `from` (`left` ou `right`) e a célula de mudança baseada em zero `block` índice, juntamente com `mode`. Ele emite o notebook alvo atualizado e preserva células excluídas e metadados do notebook. Os patches unificados descrevem a representação comparada e não são geralmente os patches em bruto PDF, Word ou contentores de cadernos.

<a id="image-effects"></a>
## Efeitos de imagem

`onekit run image-effects photo.jpg --options '{"effect":"pixelate","strength":16}' -o output` combina borrão, pixelação, caixa desfocada, cobertura sólida e escala de cinza em uma ferramenta. Use `scope: "selected"` com `regions` retangular normalizado para atingir áreas específicas. Veja o guia de efeitos [image](image-effects.md) para todas as opções e limites.

<a id="portable-workflows"></a>
## Fluxos de trabalho portáteis

`onekit workflow export SOURCE -o workflow.1kit` valida um array de passos legado ou um documento de fluxo de trabalho e salva um documento portátil. `onekit workflow import workflow.1kit -o saved.1kit` valida e salva um documento importado. Ambos os comandos omitem senhas e recusam caminhos de saída existentes, a menos que `--force` seja fornecido. Nenhum dos comandos processa ficheiros.

Executar um fluxo de trabalho importado com `onekit pipeline --steps saved.1kit INPUTS -o OUTPUT`. A .1kit extensão identifica OneKit Documentos; legado .json e .onekit.json arquivos de fluxo de trabalho e arrays de etapas permanecem suportados. Os documentos de fluxo de trabalho são UTF-8 JSON, no máximo 1 MiB, com a seguinte estrutura:

```json
{
  "format": "onekit-workflow",
  "version": 1,
  "steps": [{"tool": "dev-format-json", "options": {}}]
}
```

<a id="automatic-setup"></a>
## Configuração automática

`onekit run`, `onekit download` e `onekit pipeline` instalar em falta Python pacotes e motores nativos antes do processamento. As dependências são mantidas no usuário OneKit cache, sem alterar o sistema Python instalação. Os modelos Whisper e U2Net baixam automaticamente no primeiro uso e são armazenados em cache para execução posterior. OCR os dados da língua são obtidos para os idiomas solicitados.

A primeira execução precisa de uma conexão à internet e espaço em disco suficiente. Os motores nativos usam conda-forge através de uma instalação privada de micromamba, ou o gerenciador de pacotes do sistema para os motores indisponível lá; a disponibilidade depende do sistema operacional e arquitetura. As falhas de configuração param o processamento com um erro e podem ser repetidas. `onekit doctor` verifica a prontidão sem instalar nada. `ONEKIT_CACHE` altera o local do cache de configuração. `ONEKIT_ALLOW_COPYLEFT=0` continua a bloquear motores restritos.

<a id="local-license-and-copyright-estimates"></a>
## Estimativas locais de licenças e direitos de autor

O grupo `licenses` fornece `license-pdf`, `license-word`, `license-powerpoint`, `license-excel`, `license-video`, `license-audio`, `license-image`, `license-font`, `license-epub`, `license-code` e `license-dataset`.

```sh
onekit run license-image photo.jpg -o report.json
onekit run license-pdf --url https://example.org/document.pdf -o report.json
onekit run license-code project.zip -o report.json
onekit run license-code ./project -o report.json
onekit run license-code --url https://github.com/owner/repository --options '{"ref":"main"}' -o report.json
onekit run license-code --url https://gitlab.com/group/project -o report.json
onekit run license-dataset data.csv LICENSE metadata.json -o report.json
```

**Cada resultado é uma estimativa não verificada que requer verificação manual.** Ele lista metadados declarados, avisos de direitos autorais, nomes do criador, sintaxe SPDX e tentativas de correspondências de texto-licença com seus locais. Ele nunca certifica a propriedade ou concede permissão para usar um trabalho. Declarações em falta nunca significam domínio público ou livre de usar. Os nomes dos criadores não provam a propriedade de direitos autorais. Reveja a fonte original, termos completos e uso pretendido; dependências do projeto e ativos podem ter licenças separadas. As referências oficiais explicam as normas, e não a autenticidade ou aplicabilidade das declarações em trabalhos carregados.

<a id="downloads-image-transforms-and-url-inspection"></a>
## Transferências, transformações de imagem e inspeção de URL

```sh
onekit run audio-download --url 'https://example.org/audio.flac' -o downloads/
onekit run audio-download --url 'https://example.org/audio.wav' --options '{"format":"mp3","quality":"320"}' -o downloads/
onekit run image-download --url 'https://example.org/photo.jpg' -o downloads/
onekit run image-rotate-flip photo.png --options '{"angle":"90","flip":"horizontal"}' -o rotated.png
onekit run url-inspect --url 'https://example.org/path?x=1#section' -o report.json
```

Baixando uma imagem ou arquivo de áudio não concede direitos de redistribuição ou reutilização.

A rotação da imagem aplica-se primeiramente à orientação de EXIF, gira no sentido horário em 0/90/180/270 graus e depois reflete horizontalmente, verticalmente ou ambos no sistema de coordenadas rotacionadas. Exporta um PNG preservando RGBA pixels decodificados e transparência sem metadados; imagens animadas e multipáginas são rejeitadas. O limite é de 40 milhões de pixels.

<a id="remove-text-formatting"></a>
### Remover formatação de texto

`onekit run text-strip-formatting document.docx -o plain.txt` exportações Word texto do corpo como UTF-8 TXT. TXT, HTML e Markdown arquivos também são suportados, até 8 MiB. Utilização `--options '{"input_format":"html"}'` para interpretar HTML armazenado em uma TXT Arquivo. Não OCR é realizado.

<a id="contribute-to-onekit"></a>
## Contribuir para o OneKit

Ajude a construir a revolução aberta de OneKit: ferramentas diárias para todos, desde tarefas práticas até fluxos de trabalho gerenciados por AI agentes locais. Contribuir para tornar as ferramentas mais eficientes e eficazes: melhorar a velocidade e o uso da memória, corrigir resultados incorretos, adicionar exemplos de regressão ou esclarecer documentação e fluxos de trabalho do agente.

O núcleo é Código Aberto (PolyForm Shield 1.0.0). Ler o [guia de contribuição](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) e encontrar uma tarefa em [GitHub questões](https://github.com/mattiapiazzalunga/onekit/issues), ou sugerir uma melhoria no [placa de solicitação](https://onekit.org/requests/).

Perguntas sobre o Código Aberto (PolyForm Shield 1.0.0) núcleo e contribuições: [developers@onekit.org](mailto:developers@onekit.org). Apoio geral: [support@onekit.org](mailto:support@onekit.org).
