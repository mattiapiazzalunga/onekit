<a id="cli-localization"></a>
# CLI 本地化

语言：`en`、`it`、`fr`、`es`、`de`、`ru`、`zh`（简体中文）。选择 `onekit --language it ...` 或 `ONEKIT_LANGUAGE=it`。两者都未设置时使用操作系统的区域设置。不支持的区域设置使用英语。命令名称、选项键、路径、格式标识符和机器可读的 JSON 合同保持不变。人工帮助、状态、警告和已知错误会本地化。外部引擎诊断保留其上游文本。

任何人或 AI 在添加或修改工具时，都必须在同一次更改中更新全部七种语言的文本目录。名称、帮助、描述、错误消息、提示、README 和工具文档必须保持一一对应。不得用英语文本代替缺失的翻译。占位符、代码示例、URL 及依法必须逐字保留的声明应保持原样。请结合上下文审查含义和术语。

目录：`src/onekit/locales/{language}.json`。展示层代码：`i18n.py`。英文消息是标准化的键；处理算法保持独立。独立语言注册表为 `src/onekit/locales/languages.json`，包括操作系统别名。添加注册表项和完整目录。已审核术语记录在 `scripts/localization-reviewed.json`；在审核前使用 `python scripts/apply_localization_review.py src/onekit/locales` 应用它。

1. 在原始文件中编辑英文消息或文档。
2. 运行 `python scripts/localization_inventory.py`。
3. 更新其余语言目录并删除过时条目。编写辅助脚本可以生成翻译草稿；生成的文本必须经过审查。
4. 运行 `python scripts/audit_localization.py` 和 `pytest tests/test_i18n.py`。
5. 运行 `python scripts/localize_docs.py`，在 `docs/locales/{language}/` 下重新生成翻译后的 Markdown 文档，并保留原始文档的相对目录结构。

离线创作命令需要一个本地 Argos 模型目录，其后为翻译目录文件所在的目录列表。CTranslate2 和 SentencePiece 是创作依赖，而不是 CLI 的运行时要求。CLI 不会联系任何翻译服务。

CLI 的翻译和文档也是独立维护的，不依赖嵌入处理库的网站。这里只包括公开使用的链接。
