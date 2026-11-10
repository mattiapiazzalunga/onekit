<a id="pdfa-conversion-and-validation"></a>
# PDF/A conversão e validação

A CLI e Python API chamada `onekit.tools.pdfa`. Este módulo não invoca nenhum executável e não abre nenhuma conexão de rede. Conversão utiliza pdftopdfa 0.9.24 para fontes, cor e normalização, seguido de pikepdf 10.17.0 PDF/A preparação e validação dos bytes finais exatos. Não há dependência do Ghostscript.

Suportes de conversão PDF/A-2b (padrão) e 3b. A validação suporta 1b, 2b e 3b. A/U conformidade, PDF/A-4 e OCR estão fora deste adaptador. As construções não suportadas são `not_checked`, não está em conformidade. A `pass` a partir desta lista de allowlist conservadora não é uma certificação arquivística; a validação independente veraPDF permanece recomendada para submissões institucionais.

```
onekit run pdf-to-pdfa input.pdf --options '{"profile":"2b"}' -o output
onekit run pdf-validate-pdfa output/input.pdf -o report
onekit doctor pdf-to-pdfa --json
```

A CLI instala automaticamente um pinado, revisado **non-OCR subconjunto nível-B** dos pacotes upstream. Ele deliberadamente não instala PaddleOCR, OCRmyPDF ou o backend de criptografia para pdfminer não utilizado PDF analisador: nenhuma opção é enviada para upstream OCR ou APIs de marcação A/U. A montante `pdftopdfa` wheel não está modificado. Seus metadados de pacotes incluem requisitos mais amplos para APIs OneKit não invoca. Opcional `[pdfa]` instala extra os pré-requisitos revisados. Para uso directo Python API usar, instalar esse extra e então `pip install --no-deps pdfminer.six==20260107 pdftopdfa==0.9.24`. Não instalar upstream's OCR extras para este adaptador. A montante é obrigatório OCR requisitos atualmente fixar um PyYAML mais antigo incompatível com OneKit. Conversão requer Python 3.12+; trabalhos de validação autónomos Python 3.11+. Executar `python scripts/check_licenses.py --include-pdfa` para auditar o tempo de execução selecionado.

O primeiro `icc_profile` a opção permanece aceita como um local opcional ICC arquivo; o padrão preserva o pacote do conversor, licenciado RGB/CMYK perfis. PDFs criptografados e assinaturas digitais são rejeitados pela conversão. A conversão pode substituir fontes e remover ações não-arquivais ou metadados; avisos acompanham o resultado bem sucedido. Os candidatos com erro ou verificação incompleta nunca são devolvidos como convertidos ficheiros PDF/A. As entradas não são sobrescritas. A JSON relatório de validação preserva o `compliant` e `reports` campo e adiciona o perfil verificado, veredito e motor.
