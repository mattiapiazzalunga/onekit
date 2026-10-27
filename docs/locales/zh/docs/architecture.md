<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="architecture-and-extension-guide"></a>
# 架构和扩展指南

`Artifact(name, data)` 是一个不可变的命名字节负载。`Result(files, warnings, details)` 携带输出和保真通知。`execute(tool_id, files, options)` 验证合同并延迟导入处理适配器。`pipeline(steps, files)` 组合操作并通过单输入步骤映射多个输出。

目录定义了稳定 ID、族、接受和输出类型、多重性、选项、保真度、限制和依赖关系。处理适配器与 CLI 文件系统访问无关。可移植名称禁止遍历和保留设备名。CLI 输出写入默认会保留已有文件。原生引擎调用使用参数数组、临时目录和有限超时。

要添加工具，请实现它的家族适配器，声明目录条目，添加语义和无效输入回归测试，声明可选依赖项并审核许可证。使用 `python scripts/tool_docs.py` 重新生成工具目录。记录保真度和平台要求。


处理 API v1在 `contracts/processing-v1.json` 中描述。提交更改前请运行 `python scripts/check_contracts.py`。添加工具、格式和选项是兼容的；移除现有 ID/选项、更改输出类型或缩小输入约束需要明确的版本迁移。内部算法和处理器组织可能会变化而不改变公开接口约定。

`ExecutionContext` 允许 Python 调用者降低批处理和每个工具的预算，并提供可信的本地媒体元数据读取器。它不接受通过用户提供的工具选项的引擎服务。上下文是不可变的，仅限一次执行，并由流水线步骤共享。CLI 使用默认的本地引擎服务。

Node 源适配器将格式化和压缩规则委托给 `tools/developer/source_engine.mjs`。它的引擎加载器是进程级依赖；源文本不能随意选择软件包或可执行命令。
