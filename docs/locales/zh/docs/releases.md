<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
<a id="release-operations"></a>
# 发布操作

保护 `main` 和稳定的 `v*` 标签。为仓库 `onekit`、工作流 `release.yml` 和环境 `pypi` 注册 PyPI 可信发布者。更新包版本、锁文件、目录和文档，然后从经审核的提交发布匹配的稳定 SemVer 标签。

发布工作流程会验证标签、运行必需的 CLI 检查，并发布通用 wheel 安装包、源代码分发包、GHCR 镜像和 GitHub 发布资源。`onekit-release.json` 包含版本、源代码提交、资源校验和及下载 URL。发布重试必须保留已有的不可变资源；代码更改需要使用新版本号。

<a id="pypi-license-metadata"></a>
## PyPI license metadata

PyPI 软件包是开源的（PolyForm Shield 1.0.0），非竞争限制在其项目页面显示的 README 中说明。`project.license` 使用了 `LicenseRef-PolyForm-Shield-1.0.0`；wheel 和源代码归档包括完整的 LICENSE 和 NOTICE。项目元数据链接到许可证和文档。不要添加 OSI 批准的许可证分类器：此许可证限制竞争产品。

在发布前，请从预期的发布提交构建并验证实际工件：

```sh
uv build
python scripts/check_distribution_licenses.py
```

CI 和发布构建会在发布构件之前进行此检查。PyPI 渲染了打包好的 README，因此在更改文档或许可证元数据后需要重建。当替换已经发布的版本时，需要发布一个新的、未使用的版本；已存在的 PyPI 分发版无法被覆盖。之前发布的版本保持其原有的许可条款。当前检出的版本不会因为许可证的更改而自动更新。

项目所有者需要分别配置 PyPI 账户、受信任发布者和发布；本地准备不会上传包或更改在线 PyPI 页面。

<a id="weekly-dependency-maintenance"></a>
## Weekly dependency maintenance

Dependabot 监控 uv 锁文件、CLI Node引擎依赖、Docker 和 GitHub 动作。计划中的 Checking 工作流会重新测试锁定的依赖和本地引擎。符合条件Python仅锁定的更新仍需通过成功的检查和分支保护。
