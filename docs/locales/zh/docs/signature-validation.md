<a id="digital-signature-validation"></a>
# 数字签名验证

CLI 和浏览器运行相同的 Python 验证引擎，不上传文档。系统检查欧盟信任列表的签名和有效期，并排除不支持的服务。

密码学完整性与 AdES 验证是两个独立结果。验证使用本地证据和经过真实性核验的欧盟信任列表。缺少证据时，结果为不确定。尚未认证与 DSS 等效。

在本地检查 PDF 和 CMS 签名并执行 AdES 验证。分离式签名需要原始文件。可另附一个签名证据 ZIP。缺少信任或吊销证据时，结果为不确定。

使用此命令更新公开信任列表，不会发送文档或签名者数据。

```sh
python -m pip install "onekit-tools[verification,trustlists]"
python -m onekit.signature_evidence eu-trust-lists.zip
onekit run signature-verify signed.pdf eu-trust-lists.zip -o report
```

证据 ZIP 的清单采用以下结构。补充证书不会被任意当作信任锚。

```json
{"schema":"onekit-signature-evidence-v1","lotl":"lotl.xml","trusted_lists":[{"url":"https://official.example/list.xml","path":"tl/list.xml"}],"certificates":[],"crls":[],"ocsps":[]}
```

Windows ARM64 原生 Python 可能需要编译工具来安装 cryptography。没有可用二进制 wheel 时，请使用 x64 Python。

当前快照包含 30 个地区。受支持的 TakenOverBy 扩展保留服务历史，不会将信任转移给其他服务提供商。

算法的接受条件采用固定版本 DSS 6.5.1 的阈值；数学完整性单独报告。

在 Windows 上，trustlists 可选组件通过操作系统证书存储启用经过验证的 TLS。

信任快照的覆盖范围有限。缺少证据时，结果仍为不确定。所选 DSS 对照测试不能证明全面符合 eIDAS 或与 PAdES 完全等效。
