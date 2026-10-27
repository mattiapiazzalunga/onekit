<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="regex-tester"></a>
# 正则测试器

```sh
onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"(?<word>\\w+)","flags":"g","enable_replacement":true,"replacement":"[$<word>]"}'
onekit doctor dev-regex-test
```

JSON 报告包括模式、标志、匹配数量、截断状态、精确匹配的文本、起止位置、编号捕获组和命名组。未匹配的组为 null。位置使用 UTF-16 代码单元，就像 JavaScript 一样，所以Unicode 辅助平面字符会占用两个单元。空的全局匹配也能正确推进，包括开启 Unicode 标志的情况。

将 `enable_replacement` 设为 true，并提供 `replacement` 来预览替换。支持的替换标记与 JavaScript 字符串替换一致：`$$`、`$&`、`$1`–`$99`、`$<name>`、`$'`，以及由美元符号加反引号组成的前缀标记。替换操作绝不会更改测试输入。匹配结果被截断时，不会提供替换结果，以免显示不完整的内容。
