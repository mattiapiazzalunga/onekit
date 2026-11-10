<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="external-engines-and-licenses"></a>
# Motores externos e licenças

O proprietário aprovou separadamente os motores de código aberto instalados. Eles não são empacotados no Python wheel, download de fonte ou imagem inicial do Docker. `onekit doctor` relatórios de requisitos. `ONEKIT_ALLOW_COPYLEFT=0` desactiva explicitamente os adaptadores copyleft listados. Mantenha as ferramentas upstream atualizadas; subprocessos locais não são uma área de areia completa para documentos hostis.

| Motor | Comando | Considerações de uso / licença |
| --- | --- | --- |
| LibreOffice | `soffice` / `libreoffice` | Escritório → PDF/imagens; MPL e avisos de terceiros. |
| Pandoc | `pandoc` | Conversão de marcação avançada; GPL. |
| TeX Live/pdfTeX | `pdflatex` | LaTeX/Pandoc PDF; motor, macros e fontes têm licenças separadas. |
| FFmpeg | `ffmpeg` | Meios de comunicação; LGPL ou GPL dependendo da construção e codecs. |
| veraPDF | `verapdf` | Verificação independente opcional das saídas arquivísticas; requisitos a montante GPL/MPL e Java. |
| ExifTool | `exiftool` | Metadados em tipos de ficheiros suportados; licenciamento Perl a montante. |
| Tesseract | `tesseract` | OCR; motor Apache e dados de idioma licenciados separadamente. |

Se distribuir esses programas, incluindo dentro do Docker, preserve suas licenças/notificações e forneça os materiais correspondentes de origem/construção necessários. Avaliar AGPL integrações de rede separadamente. O uso comercial e as obrigações de fonte/redistribuição são questões diferentes. Processos separados não eliminam universalmente as obrigações. Leia com autoridade [FFmpeg](https://ffmpeg.org/legal.html), [LibreOffice](https://www.libreoffice.org/licenses/), [Ghostscript](https://www.ghostscript.com/licensing/) e [MPL](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) material antes de criar uma distribuição agrupada.

A fidelidade do escritório depende de fontes e recursos. PDF- Para...Word Exporta o texto extraído; PDF- Para...PowerPoint cria slides de imagem. PDF reparação é o melhor esforço; compressão é sem perdas. [PDF/A conversão e validação](pdfa.md) usar separado MPL bibliotecas através do compartilhado Python adaptador, com pacote licenciado ICC perfis. Ghostscript não é necessário. A validação de normas independentes permanece recomendada. OCR A precisão depende da qualidade da varredura e dos pacotes de linguagem.

<a id="developer-tools"></a>
## Ferramentas de programação

Formata Kotlin com ktfmt e Ruby com Syntax Tree e RuboCop através de pacotes WASM com versões fixadas. Execute `onekit engines install`. Até 256 KiB por ficheiro de entrada; a configuração do projeto não é carregada.

Formata LaTeX com tex-fmt e definições fixas. A configuração do projeto não é carregada. Até 256 KiB por ficheiro de entrada.

Converte documentos LaTeX autónomos com Pandoc 3.9. Não suporta ficheiros externos nem compilação TeX. Até 256 KiB por ficheiro de entrada.

`dev-format-latex`: `Node.js 24+`; `tex-fmt` WASM, MIT. `latex-to-html`, `latex-to-md`: `onekit setup latex-to-html`; `pandoc-wasm@1.1.0`, GPL-2.0-or-later; `ONEKIT_PANDOC_ENGINE_PATH`, `ONEKIT_ALLOW_COPYLEFT=0`.

Instalar Node.js 24+ e correr `onekit engines install` para Prettier/plugins bloqueados, esbuild, HTML minifier, SVGO e GraphQL.Js. Eles instalam no usuário OneKit cache, não globalmente. `ONEKIT_NODE_ENGINE_PATH` seleciona uma alternativa. Repetir o instalador após uma atualização do motor aprovada. O grupo de análise abrange JS/TS/JSX/TSX, marcação, folhas de estilo, Markdown/MDX, GraphQL, Vue, Svelte, Astro, Solidity e PHP.

Instale compiladores/lançamentos upstream para o seu sistema operacional e adicione os comandos documentados ao PATH. Alguns arquivos isolados precisam de suas dependências do projeto ou exato nome de arquivo da classe Java. A validação de formatação/parser não prova a exatidão do tipo em todo o projeto.

Ligado Windows, Bash/Shell os adaptadores preferem um intérprete real no PATH e depois detectam o Git para Windows Nos seus diretórios de instalação normalizados do sistema/usuário. O lançador WSL System32 não é tratado como um analisador local compatível. PowerShell a validação de sintaxe requer `pwsh`; formatação adicional requer PSScriptAnalyzer (`Install-Module PSScriptAnalyzer -Scope CurrentUser`). `onekit doctor dev-format-powershell` verifica esse módulo separadamente e reporta o seu comando de configuração. Esses programas/módulos não são baixados durante o processamento de arquivos.

<a id="platform-qualifications"></a>
## Compatibilidade das plataformas

Verificações de licença CI também instalar e atravessar o extra assinatura separada (`scripts/check_licenses.py --include-signing`). MIT-0 é reconhecida como uma licença permissiva ([SPDX texto](https://spdx.org/licenses/MIT-0.html)). A travada `certifi` 2026.7.22 Dados da Mozilla trust-store é uma versão específica explícita MPL-2.0 Exceção; manter a sua licença/notificações a montante não modificadas ao redistribuí-la ([Comunicação a montante](https://github.com/certifi/python-certifi/blob/master/LICENSE)). Novas versões exigem outra revisão. Esta excepção não admite geralmente outros MPL pacotes ou alterações OneKit's PolyForm-Shield-1.0.0 licença.

O universal Python suportes de núcleo Linux, Windows e macOS incluindo ARM64. Extras nativos e motores externos determinam requisitos adicionais. O IC declara corredores x64/ARM em todas as três famílias do sistema operacional. Ligado Windows ARM, Brotli/WOFF2 e a pilha de criptografia de assinatura separada pode exigir ferramentas de construção nativas ou x64 Python sob emulação. WOFF/TTF/OTF não exigir a WOFF2 Codificador. A `all` extra exclui assinatura separada. Relatar estas restrições opcionais em vez de reivindicar um nativo wheel existe quando não existe.
