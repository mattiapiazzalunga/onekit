<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->

Idiomas: [English](../../../README.md) · [Italiano](../it/README.md) · [Français](../fr/README.md) · [Español](../es/README.md) · [Deutsch](../de/README.md) · [Русский](../ru/README.md) · [中文](../zh/README.md) · [Português](README.md) · [हिन्दी](../hi/README.md).

<p align="center">
  <a href="https://onekit.org"><img src="https://raw.githubusercontent.com/mattiapiazzalunga/onekit/main/images/logo.png" alt="OneKit logo" width="112" height="112"></a>
</p>
<h1 align="center">OneKit</h1>
<p align="center">Um conjunto de ferramentas simples. Os seus ficheiros continuam a ser seus.</p>
<p align="center"><a href="https://github.com/mattiapiazzalunga/onekit/stargazers"><img alt="GitHub estrelas" src="https://img.shields.io/github/stars/mattiapiazzalunga/onekit"></a> <a href="https://pypi.org/project/onekit-tools/"><img alt="PyPI" src="https://img.shields.io/pypi/v/onekit-tools"></a> <img alt="PolyForm-Shield-1.0.0" src="https://img.shields.io/badge/license-PolyForm_Shield_1.0.0-blue"> <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-blue"></p>

Um offline Python toolkit com 230 ferramentas para conversões, PDFs, imagens, arquivos, fontes, inspeção de arquivos, criptografia, utilitários de desenvolvimento, OCR e comparações. Usar isto CLI ou a interface gráfica em **[onekit.org](https://onekit.org)**.

** Versão fonte:** `0.6.3`. Os downloads estáveis só existem após o workflow de lançamento terminar. A distribuição é `onekit-tools`; o projeto PyPI de propriedade separada chamado `onekit` não tem relação.

A [guia de contato e mídia](docs/contact-media.md) Abrange o autônomo vCard geração, QR- Para...vCard extração, aumento da imagem, remoção de fundo, compressão de vídeo/velocidade/GIF e transcrição de áudio local.

Veja [Pacotes Android e desfoque facial automático](docs/android-and-face-tools.md).

Verificação da licença: inspecionar PDF, Word, PowerPoint, Excel, vídeo, áudio, imagens, fontes, EPUB, código/projetos e conjuntos de dados de arquivos ou URLs públicas. A análise permanece local; os relatórios são ** estimativas não verificadas, não certificados de propriedade ou permissão para usar**. Ver [Utilização e limites da verificação de licenças](docs/cli.md#local-license-and-copyright-estimates).

** A tua CLI. O seu agente CLI.** Utilização OneKit você mesmo ou deixe um local AI O agente chama-o através de um terminal ou subprocesso. Descubra ferramentas e requisitos como JSON, passe caminhos de entrada/saída explícitos e reutilização salva `.1kit` fluxos de trabalho para tarefas de arquivos repetiveis. Ver [Agentes locais e automação](docs/cli.md#local-agents-and-automation).

<a id="install"></a>
## Instalar

Python 3.11+ é necessário. O universal wheel suporta Windows, macOS e Linux em x64/ARM64. Bibliotecas nativas opcionais e motores externos têm requisitos de plataforma adicionais.

Após publicação:

```sh
python -m pip install onekit-tools
python -m pip install "onekit-tools[pdf,images,documents]"
onekit list
onekit doctor
```

A partir de uma saída de origem:

```sh
python -m pip install -e ".[all,test]"
python -m onekit --help
python -m pytest -q
```

A base CLI tem ** nenhuma dependência de tempo de execução**. Instale apenas os extras que você precisa. `all` inclui a norma Python famílias; download de vídeo, remoção de fundo, transcrição e assinatura criptográfica use o separado `video`, `background`, `transcription` e `signing` Extras. Instale os motores nativos separadamente. Para ferramentas de desenvolvimento baseadas em nós, instale Node.js 24+ e correr `onekit engines install`. A CLI prepara dependências em falta e motores externos na primeira utilização. Remoção de fundo e pesos do modelo de download de transcrição no primeiro uso, em seguida, reutilizar o cache local.

<a id="use"></a>
## Utilização

```sh
onekit run pdf-merge first.pdf second.pdf -o combined.pdf
onekit run pdf-extract-pages document.pdf --options '{"pages":"1,3-5"}' -o selected.pdf
onekit run image-convert image.png --options '{"format":"webp"}' -o image.webp
onekit run diff-notebook before.ipynb after.ipynb --options '{"mode":"code"}' -o changes.json
onekit run security-encrypt private-folder --ask-password -o private.zip
onekit run security-decrypt private.zip --ask-password -o restored
```

As opções são JSON objetos; passe-os como um argumento de shell citado. Use `--ask-password` para segredos. As saídas existentes são preservadas a menos que você passe `--force`.

`onekit list --group pdf`, `onekit list --json` e `onekit doctor TOOL_ID` expor contratos e requisitos. Cada ferramenta tem um diretório sob [ferramentas](../../../tools), contendo metadados e um ponteiro para sua implementação compartilhada. Ver o [CLI guia](docs/cli.md) para opções e limites.

<a id="toolkit"></a>
## Ferramentas

| Família | Capacidades |
| --- | --- |
| Conversores | Markdown, HTML, LaTeX, PDF, Word, PowerPoint, imagens, Base64, Excel, CSV e JSON |
| PDF | Mesclagem/separação, seleção de página/ordem/remoção, compressão, reparação, edição de texto [direct](docs/pdf-editing.md), sobreposições de texto, rotação, assinaturas digitais, criptografia/desbloqueio, [local PDF/A conversão/validação](docs/pdfa.md) |
| Imagens | Extrair imagens embutidas PDF, comprimir, cortar e alterar o formato |
| Mídia | Conversão de áudio/vídeo através de FFmpeg instalados separadamente |
| Arquivos / fontes | ZIP/TAR variantes; TTF/OTF recipientes e WOFF/WOFF2 |
| Inspector/Segurança | Digite assinaturas, estrutura, metadados, codificação, hashes, contagens de texto; arquivos/pastas criptografados autenticados |
| Desenvolvimento | Formatação específica da língua, validação do analisador/compilador e minificação selecionada |
| OCR | Imagens/ imagens digitalizadasPDF para pesquisável PDF, Word, Markdown, LaTeX, HTML e JSON |
| Diferenças | Texto, código, JSON normalizados, cadernos de notas, LaTeX, PDF e Word textos |

<a id="pipelines-and-development"></a>
## Fluxos de trabalho e desenvolvimento

`onekit pipeline --steps workflow.1kit INPUTS -o OUTPUT` aceita um documento de fluxo de trabalho versão `.1kit`. Cada etapa recebe saídas anteriores. Passos de entrada única mapeiam várias saídas; as etapas de mesclagem recebem a coleção. Tipos incompatíveis param de processar.

Comunicar erros e sugestões através [GitHub questões](https://github.com/mattiapiazzalunga/onekit/issues) ou a [placa de solicitação do site](https://onekit.org/requests/). Colaboradores podem encontrar trabalho em qualquer lugar.

<a id="contribute-to-onekit"></a>
## Contribuir para o OneKit

Ajude a construir a revolução aberta de OneKit: ferramentas diárias para todos, desde tarefas práticas até fluxos de trabalho gerenciados por AI agentes locais. Contribuir para tornar as ferramentas mais eficientes e eficazes: melhorar a velocidade e o uso da memória, corrigir resultados incorretos, adicionar exemplos de regressão ou esclarecer documentação e fluxos de trabalho do agente.

O núcleo é Código Aberto (PolyForm Shield 1.0.0). Ler o [guia de contribuição](https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md) e encontrar uma tarefa em [GitHub questões](https://github.com/mattiapiazzalunga/onekit/issues), ou sugerir uma melhoria no [placa de solicitação](https://onekit.org/requests/).

<a id="license-and-creator"></a>
## Licença e criador

Criado por **[Mattia Piazzalunga](mailto:hello@mattiapiazzalunga.com)**. Copyright © 2026 Mattia Piazzalunga. Abrir o Código (PolyForm Shield 1.0.0), licenciado sob a forma de [PolyForm Shield 1.0.0](../../../LICENSE); ver [AVISO](../../../NOTICE), [AUTORES.txt](../../../AUTHORS.txt) e [CONTRIBUIDORES.txt](../../../CONTRIBUTORS.txt). Componentes de terceiros mantêm suas licenças. Motores externos são programas separados com suas próprias obrigações de redistribuição.

Você pode usar, modificar e redistribuir o núcleo para fins permitidos, incluindo uso comercial e interno. Você não pode usá-lo para fornecer um produto ou serviço que compete com o software ou com um produto que o licenciante ou seus afiliados fornece usando o software; ofertas gratuitas e diferentes plataformas ou interfaces também podem competir. Ao compartilhar cópias, inclua o texto da licença ou seus URL e quaisquer linhas de aviso obrigatório fornecidas com o software. A licença completa governa, incluindo suas exceções para produtos novos e descontinuados, termos de patente e dispensa de garantia. Aqui, “Open Source (PolyForm Shield 1.0.0)” descreve fonte publicada sob estes termos; a restrição de não concorrência significa que este é software disponível para fontes em vez de código aberto irrestrito sob a Definição de Código Aberto. Ver [o guia de licenciamento](docs/licenses.md).

Exportar e reimportar fluxos de trabalho sem processar arquivos de entrada:

```sh
onekit workflow export workflow.1kit -o exported-workflow.1kit
onekit workflow import workflow.1kit -o saved-workflow.1kit
onekit pipeline --steps saved-workflow.1kit input.json -o output.json
```

Códigos de barras padrão estão disponíveis no QR códigos de barras e categoria CLI: `text-to-barcode`, `scan-barcode`, `barcode-to-text`. Código 128, código 39, EAN-13, EAN-8, UPC-A, ITF e ISBN-13 apoio PNG/SVG, dimensões configuráveis e validação de check-digit. Instalar `onekit-tools[barcode]` ou `onekit-tools[qrcode]`.

Permanente [PDF e redação da imagem](docs/redaction.md) está disponível através de `pdf-redact` e `image-redact`. Regiões selecionadas tornam-se pixels pretos sólidos em arquivos recém-codificados. Os PDFs são reconstruídos como documentos somente de imagem sem texto original, formulários, comentários, anexos ou metadados; as imagens tornam-se PNGs opacos sem metadados originais ou pixels alfa ocultos. Os ficheiros originais não são alterados.

Adicionar marcas de água de texto configuráveis PDF com `pdf-watermark`: opacidade, cor, fontes, intervalos de página, posições visuais, rotação e grades repetidas. Texto e gráficos permanecem no PDF. Veja o guia [watermark](docs/watermark.md).

<a id="contacts"></a>
## Contactos

- Questões gerais e apoio: [support@onekit.org](mailto:support@onekit.org).
- Perguntas sobre o Código Aberto (PolyForm Shield 1.0.0) núcleo e contribuições: [developers@onekit.org](mailto:developers@onekit.org).
- Privacidade, GDPR e pedidos de dados pessoais: [privacy@onekit.org](mailto:privacy@onekit.org).
- Questões legais, pedidos de licenciamento e permissão: [legal@onekit.org](mailto:legal@onekit.org).
- Vulnerabilidades de segurança e relatórios de abuso: [security@onekit.org](mailto:security@onekit.org).
