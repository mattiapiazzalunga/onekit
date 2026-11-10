<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="qr-codes"></a>
# QR códigos

<a id="standard-linear-barcodes"></a>
## Códigos de barras lineares padrão

```sh
onekit run text-to-barcode identifier.txt -o barcode.png --options '{"barcode_type":"ean13"}'
onekit run text-to-barcode identifier.txt -o barcode.svg --options '{"barcode_type":"code128","format":"svg"}'
onekit run scan-barcode photo.jpg -o decoded.json
onekit run barcode-to-text photo.jpg -o identifier.txt
```

Normas: `code128` (por omissão, até 60 imprimíveis ASCII caracteres), `code39` (até 48 letras/dígitos maiúsculas e símbolos suportados, sem opção Mod-43 soma de cheques), `ean13` (12 dígitos ou 13, incluindo o somatório de controlo), `ean8` (7/8), `upca` (11/12), `itf` (um número par de dígitos, até 80), `isbn13` (EAN-13 início de 978/979). Os algarismos de verificação fornecidos a retalho devem estar correctos; nunca são substituídos silenciosamente. Os algarismos por omissão são calculados. Os identificadores não são atribuídos ou registados por OneKit.

Instale `python -m pip install "onekit-tools[qrcode]"`. Todo o processamento QR é local e funciona offline após dependências serem instaladas. A geração QR usa o Segno; CLI a varredura usa ZXing-C++ e Pillow.

| Ferramenta | Entrada | Saída |
| --- | --- | --- |
| `text-to-qrcode` | UTF-8 TXT | PNG ou SVG |
| `url-to-qrcode` | TXT contendo um HTTP(S) URL | PNG ou SVG |
| `wifi-to-qrcode` | Wi-Fi JSON | PNG ou SVG |
| `vcard-to-qrcode` | Contacto JSON ou VCF existente | PNG ou SVG |
| `scan-qrcode` | PNG, JPEG, WebP, BMP ou GIF | Relatório JSON |
| `reverse-qrcode` | QR imagem | Teor bruto e interpretado em JSON |
| `qrcode-to-text` | QR imagem | Texto gravado exato |
| `qrcode-to-json` | QR imagem | Valor original de JSON, ou um relatório para outras cargas |

```sh
onekit run text-to-qrcode message.txt -o code.png
onekit run url-to-qrcode link.txt -o code.svg --options '{"format":"svg","error_correction":"Q"}'
onekit run wifi-to-qrcode network.json -o wifi.png
onekit run vcard-to-qrcode contact.json -o output/ --options '{"include_payload":true}'
onekit run scan-qrcode photo.jpg -o decoded.json
onekit run qrcode-to-json code.png -o recovered.json
```

Opções de geração: `format` (`png`/`svg`), `error_correction` (`L`/`M`/`Q`/`H`), `scale` (2–16 pixels por módulo), `border` (4–16 módulos), `dark` e `light` (hex de seis dígitos, contraste ≥4,5:1) e `include_payload` (também codificado para exportação TXT/JSON/VCF). Predefinição: PNG, M, escala 8, borda 4, preto sobre branco. SVG escalas para impressão. A entrada é limitada a 16 KiB, mas QR capacidade é menor e depende de correção; encurtar contatos superdimensionados ou menor correção. URLs de fotos são armazenadas sem obter a imagem.

Wi-Fi exemplo:

```json
{"ssid":"Guest Wi-Fi","security":"WPA","password":"example-password","hidden":false}
```

Segurança: `WPA` (WPA/WPA2 pessoal), `WEP`, `nopass` (aberto), `SAE` (WPA3), `WPA2-EAP` (empresa). Empresa adiciona `identity`, `anonymous_identity`, `eap`, `phase2`. WPA3 e o apoio à empresa varia por telefone. As senhas permanecem legíveis no QR Carga útil. Caracteres especiais usam o [ZXing Wi-Fi Convenção de fuga](https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11).

Exemplo de contacto:

```json
{
  "version":"4.0", "formatted_name":"Ada Lovelace",
  "first_name":"Ada", "last_name":"Lovelace", "organization":"Example",
  "phones":[{"value":"+390123456789","type":"work,voice","preferred":true,"label":"Office"}],
  "emails":[{"value":"ada@example.org","type":"work"}],
  "urls":["https://example.org"],
  "addresses":[{"street":"Example Street 1","city":"Milano","postal_code":"20100","country":"Italy","type":"work"}],
  "social_profiles":[{"value":"https://www.linkedin.com/in/example","type":"linkedin"}],
  "birthday":"1815-12-10", "categories":["Work","Research"], "note":"Example contact"
}
```

Domínios adicionais: `prefix`, `middle_name`, `suffix`, `nickname`, `department`, `title`, `role`, `anniversary`, `gender` (M/F/O/N/U), `language`, `timezone`, `uid`, `photo_url`, `latitude`, `longitude`. Datas de uso AAAA-MM-DD. Endereços também suportam `po_box`, `extended`, `region`, `label`, `preferred`. Telefone/e-mail repetidoURL/entradas sociais aceitam `value`, `type`, `label`, `preferred`, com até 20 entradas por lista. Entradas simples de string também são aceitas. vCard 3.0 é o padrão; 4.0 usa parâmetros modernos de preferência e valor de texto. UTF-8 Dobrar e texto escapando seguir [vCard](https://www.rfc-editor.org/rfc/rfc6350). As etiquetas personalizadas usam as propriedades agrupadas do X-ABLabel; os campos opcionais dependem do leitor.

Reverte revela texto armazenado e classifica links, Wi-Fi, vCard e JSON. Ele não pode recuperar o gerador, configurações originais, foto fonte ou conteúdo por trás de um URL. `qrcode-to-json` retorna o original JSON quando um JSON o símbolo é encontrado; caso contrário ele retorna `{ "count": ..., "codes": [...] }` com texto bruto e campos interpretados.

Formas do módulo: `shape=square` (por omissão), `shape=rounded`, ou `shape=dots`. A forma selecionada aplica-se aos módulos de correção de erros e dados em PNG e SVG exportações. Marcadores de localização permanecem quadrados por padrão e podem usar cantos arredondados com `corner_style=rounded`. Alinhamento, timing e outros padrões de função permanecem quadrados. PNG as dimensões ainda seguem `scale` e `border`.

JPEG exportação (`format=jpeg`) está disponível com todas as formas de módulo e um fundo sólido. Use PNG ou SVG quando a transparência é necessária.

Escolher `corner_style=square` (por omissão) ou `rounded` para os três marcadores localizadores, independentemente da forma do módulo. Adicionar uma marca central com `overlay_type=text` e `overlay_text` (1–16 caracteres), ou `overlay_type=image` e `overlay_image_base64` (uma base64 PNG/JPEG, até 2 MiB e 4 milhões de pixels). `overlay_size` é 10–20 por cento do QR símbolo, padrão 16. Marcas centrais forçam correção de erro H. O renderizador encontra uma área central somente de dados e pode encolher ou mudar ligeiramente a marca para preservar padrões de função. A marca tem um apoio ligeiro, mesmo para exportações transparentes. Todas estas opções funcionam com PNG, JPEG e SVG.
