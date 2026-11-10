<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="edit-pdf"></a>
# Editar PDF

Comando: `onekit run pdf-edit`. Use `onekit run --help` para argumentos de entrada e saída.

Categoria: **pdf**. Fidelidade: ** compromisso**. Edite as caixas de texto suportadas usando o tipo de letra original. O texto mais longo é ajustado à sua largura original. Escaneamentos, texto dentro de formulários reutilizáveis e caracteres de fonte não disponíveis não podem ser editados. Esta não é uma ferramenta de redação. A opção texto legado adiciona uma sobreposição.

Tipos aceites: `pdf`. Tipo de saída: `pdf`. Aceita múltiplas entradas: **no**.

Validação de entrada: **typed**. Contagem de ficheiros necessária: **1-1**. CLI: **134.217.728 bytes por arquivo**, **134.217.728 bytes total**. As verificações de conteúdo são realizadas antes do processamento. Renomear um arquivo não altera seu formato atual.

Opções: `mode`, `edits`, `password`, `text`, `x`, `y`, `page`.

Python pacotes: pycryptodome, pypdf, reportlab. Motores externos: veja a matriz do motor de desenvolvimento para adaptadores de linguagem.

Execução da transformação: [adaptador de família compartilhado](../../../../../../src/onekit/tools/pdf/__init__.py). Contratos e dispositivos de regressão: [testes](../../../../../../tests/test_core.py). Configuração do motor e licenças: [guia do motor](../../../docs/engines.md).

Este diretório é gerado a partir do catálogo compartilhado por `python scripts/tool_docs.py`. Edite o registro e adaptador de família, adicione dispositivos de regressão e, em seguida, regenere o diretório.
