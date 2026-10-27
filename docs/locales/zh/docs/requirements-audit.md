<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="cli-requirements-verification"></a>
# CLI 需求验证

`tests/test_requirements.py` 检查目录覆盖、CLI 调用和格式错误的管道。`tests/test_core.py` 验证处理协议和输出语义。输入验证、归档展开、加密和文件系统保护都有专门的回归测试。

运行 `python -m pytest -q` 执行默认测试套件。单独安装的引擎通过 `python -m pytest -q -m native` 测试；运行这些检查前，请准备好 `docs/engines.md` 中说明的依赖项。默认测试套件通过，并不表示所有外部引擎或所有支持的平台均已验证。
