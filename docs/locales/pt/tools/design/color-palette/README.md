<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="color-palette-generator"></a>
# Gerador de paletas de cores

Comando: `onekit run color-palette`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **design**. Fidelidade: **Exacto**. Paletas OKLCH de cinco cores com redução de chroma sRGB e contraste de texto WCAG. As regras de harmonia são heurísticas de design, não garantias de acessibilidade.

Tipos aceites: `txt`. Tipo de saída: `json`. Aceita múltiplas entradas: **no**.

Validação de entrada: **text**. Contagem de ficheiros necessária: **1-1**. CLI: **128 bytes por arquivo**, **1.048.576 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `harmony`, `lightness`, `chroma`, `hue`, `format`.

Python pacotes: biblioteca padrão ou motor externo. Motores externos: veja a matriz do motor desenvolvedor para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/design.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
