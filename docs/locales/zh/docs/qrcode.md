<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="qr-codes"></a>
# 二维码

<a id="standard-linear-barcodes"></a>
## Standard linear barcodes

```sh
onekit run text-to-barcode identifier.txt -o barcode.png --options '{"barcode_type":"ean13"}'
onekit run text-to-barcode identifier.txt -o barcode.svg --options '{"barcode_type":"code128","format":"svg"}'
onekit run scan-barcode photo.jpg -o decoded.json
onekit run barcode-to-text photo.jpg -o identifier.txt
```

标准：`code128`（默认，最多 60 个可打印 ASCII 字符），`code39`（最多 48 大写字母/数字及支持的符号，无可选的 Mod-43 校验码），`ean13`（12 位数字，或包含校验码的 13 位数字），`ean8`（7/8），`upca`（11/12），`itf`（偶数位数字，最多 80），`isbn13`（EAN-13 起始 978/979）。提供的零售校验码必须正确；它们不会被默默替换。缺失的数字会被计算。标识符不由 OneKit 分配或注册。

安装 `python -m pip install "onekit-tools[qrcode]"`。所有 QR 处理都是本地的，并且在安装依赖后可以离线使用。QR 生成使用 Segno；CLI 扫描使用 ZXing-C++ 和 Pillow。

| 工具 | 输入 | 输出 |
| --- | --- | --- |
| `text-to-qrcode` | UTF-8 TXT | PNG 或 SVG |
| `url-to-qrcode` | TXT 包含一个 HTTP(S) URL | PNG 或 SVG |
| `wifi-to-qrcode` | Wi-Fi JSON | PNG 或 SVG |
| `vcard-to-qrcode` | 联系 JSON 或现有 VCF | PNG 或 SVG |
| `scan-qrcode` | PNG、JPEG、WebP、BMP 或 GIF | JSON 报告 |
| `reverse-qrcode` | 二维码图片 | JSON 中的原始和解释内容 |
| `qrcode-to-text` | 二维码图片 | 精确存储文本 |
| `qrcode-to-json` | 二维码图片 | 原始 JSON 值，或者其他有效载荷的报告 |

```sh
onekit run text-to-qrcode message.txt -o code.png
onekit run url-to-qrcode link.txt -o code.svg --options '{"format":"svg","error_correction":"Q"}'
onekit run wifi-to-qrcode network.json -o wifi.png
onekit run vcard-to-qrcode contact.json -o output/ --options '{"include_payload":true}'
onekit run scan-qrcode photo.jpg -o decoded.json
onekit run qrcode-to-json code.png -o recovered.json
```

生成选项：`format` (`png`/`svg`), `error_correction` (`L`/`M`/`Q`/`H`), `scale` (每模块 2–16 像素), `border` (4–16 模块), `dark` 和 `light` (六位十六进制， 对比度 ≥4.5:1), 以及 `include_payload` (同时导出编码的 TXT/JSON/VCF)。默认值：PNG, M, 缩放 8, 边框 4, 白底黑色。SVG 适合打印。输入限制为 16 KiB，但 QR 容量更小且依赖纠错；过大的联系人请缩短或降低纠错等级。照片 URL 会被存储，但不会抓取图片。

Wi-Fi 示例：

```json
{"ssid":"Guest Wi-Fi","security":"WPA","password":"example-password","hidden":false}
```

安全性：`WPA`（WPA/WPA2 个人），`WEP`，`nopass`（公开），`SAE`（WPA3），`WPA2-EAP`（企业）。企业版添加了 `identity`、`anonymous_identity`、`eap`、`phase2`。WPA3 和企业支持因手机而异。密码在 QR 有效载荷中保持可读。特殊字符使用 [ZXing Wi-Fi 转义约定](https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11)。

联系示例：

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

额外字段：`prefix`、`middle_name`、`suffix`、`nickname`、`department`、`title`、`role`、`anniversary`、`gender`（M/F/O/N/U）、`language`、`timezone`、`uid`、`photo_url`、`latitude`、`longitude`。日期使用 YYYY-MM-DD。地址还支持 `po_box`、`extended`、`region`、`label`、`preferred`。重复的电话/邮箱/URL/社交条目可接受 `value`、`type`、`label`、`preferred`，每个列表最多可有 20 个条目。也可以接受简单的字符串条目。vCard 3.0 是默认值；4.0 使用现代偏好和文本值参数。UTF-8 行折叠和文本转义遵循 [vCard](https://www.rfc-editor.org/rfc/rfc6350)。 自定义标签使用分组的 X-ABLabel 属性；可选字段的支持情况取决于读取软件。

反向操作显示存储的文本并分类链接，Wi-Fi、vCard 和 JSON。它无法恢复生成器、原始设置、源照片或 URL 背后的内容。当找到一个 JSON 符号时，`qrcode-to-json` 会返回原始的 JSON；否则返回带有原始文本和解释字段的 `{ "count": ..., "codes": [...] }`。

模块形状：`shape=square`（默认）、`shape=rounded` 或 `shape=dots`。所选形状适用于 PNG 和 SVG 导出的数据模块和纠错模块。定位标记默认保持方形，也可以使用 `corner_style=rounded` 圆角。对齐、定时及其他功能图案保持方形。PNG 尺寸仍遵循 `scale` 和 `border`。

JPEG 导出 (`format=jpeg`) 可用于所有模块形状和纯色背景。当需要透明时，请使用 PNG 或 SVG。

为三个定位标记选择 `corner_style=square`（默认）或 `rounded`，与数据模块的形状无关。使用 `overlay_type=text` 和 `overlay_text`（1–16 个字符）添加中心内容，或使用 `overlay_type=image` 和 `overlay_image_base64` 添加图像（base64 编码的 PNG/JPEG，最多 2 MiB 和 400 万像素）。`overlay_size` 为二维码大小的 10–20%，默认值为 16。添加中心内容会强制使用 H 级纠错。渲染器会查找仅包含数据模块的中心区域，并可缩小或轻微移动中心内容，以保留功能图案。即使导出透明背景，中心内容仍有浅色底衬。所有这些选项均支持 PNG、JPEG 和 SVG。
