<a id="cli-localization"></a>
# CLI 本地化

语言:`en`;`it`;`fr`;`es`;`de`;`ru`;`zh` (简体中文)`pt` (葡萄牙语)`hi` (Hindi). 选择一个与`onekit --language it ...`或`ONEKIT_LANGUAGE=it`. 操作系统 locale 既不设,也不设时使用。 不支持的本地人使用英语. 命令名称、选项密钥、路径、格式标识符和机器可读性JSON合同保持稳定。 人类的帮助,状态,警告和已知出错都是本地化的. 外部引擎诊断保留了它们的上游文本.

每个人或AI个添加或更改一个工具MUST在同一变化中更新了所有9个演示文稿目录. 姓名、帮助、描述、错误信息、通知、README和工具文档必须保留在一对一的通信中。 不要以英语作为快捷键来填充缺失的翻译 。 保持占位符,代码示例,URL和法律要求的逐字记录完整. 审查上下文的含义和术语。

目录：`src/onekit/locales/{language}.json`。展示层代码：`i18n.py`。英文消息是标准化的键；处理算法保持独立。独立语言注册表为 `src/onekit/locales/languages.json`，包括操作系统别名。添加注册表项和完整目录。已审核术语记录在 `scripts/localization-reviewed.json`；在审核前使用 `python scripts/apply_localization_review.py src/onekit/locales` 应用它。

1. 在原始文件中编辑英文消息或文档。
2. 运行 `python scripts/localization_inventory.py`。
3. 更新其余语言目录并删除过时条目。编写辅助脚本可以生成翻译草稿；生成的文本必须经过审查。
4. 运行 `python scripts/audit_localization.py` 和 `pytest tests/test_i18n.py`。
5. 运行 `python scripts/localize_docs.py`，在 `docs/locales/{language}/` 下重新生成翻译后的 Markdown 文档，并保留原始文档的相对目录结构。

离线创作命令需要一个本地 Argos 模型目录，其后为翻译目录文件所在的目录列表。CTranslate2 和 SentencePiece 是创作依赖，而不是 CLI 的运行时要求。CLI 不会联系任何翻译服务。

CLI 的翻译和文档也是独立维护的，不依赖嵌入处理库的网站。这里只包括公开使用的链接。
