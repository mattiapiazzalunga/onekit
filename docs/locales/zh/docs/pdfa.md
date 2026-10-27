<a id="pdfa-conversion-and-validation"></a>
# PDF/A 转换和验证

CLI 和 Python API 调用 `onekit.tools.pdfa`。这个模块不会调用可执行文件，也不会打开网络连接。转换使用 pdftopdfa 0.9.24 处理字体、颜色和规范化，然后是 pikepdf 10.17.0 PDF/A 准备和验证最终字节的准确性。没有 Ghostscript 依赖。

转换支持 PDF/A-2b（默认）和 3b。验证支持 1b、2b 和 3b。A/U 一致性、PDF/A-4 和 OCR 不在此适配器范围内。不支持的结构标记为 `not_checked`，而非合规。这个保守允许列表中的 `pass` 不是归档认证；对于机构提交，仍然建议进行独立的 veraPDF 验证。

```
onekit run pdf-to-pdfa input.pdf --options '{"profile":"2b"}' -o output
onekit run pdf-validate-pdfa output/input.pdf -o report
onekit doctor pdf-to-pdfa --json
```

CLI 会自动安装上游软件包中已固定、已审核的 **非 OCR 级别 B 子集**。它故意不安装 PaddleOCR、OCRmyPDF 或 pdfminer 中未使用的 PDF 解析器的加密后端：不会将任何选项传递给上游 OCR 或 A/U 标记 API。上游的 `pdftopdfa` wheel 未做修改。它的包元数据包含了 OneKit 不会调用的更广泛 API 要求。可选的 `[pdfa]` 附加包会安装已审核的前置条件。要直接使用 Python API，先安装那个附加包，然后再安装 `pip install --no-deps pdfminer.six==20260107 pdftopdfa==0.9.24`。不要为这个适配器安装上游的 OCR 附加包。 上游的强制性 OCR 要求目前固定了一个较旧的 PyYAML，与 OneKit 不兼容。转换需要 Python 3.12+；独立验证在 Python 3.11+ 上可用。运行 `python scripts/check_licenses.py --include-pdfa` 来审核所选的运行时。

以前的 `icc_profile` 选项仍然可以接受，作为可选的本地 ICC 文件；默认情况下会保留转换器自带的、已授权的 RGB/CMYK 配置文件。加密的 PDF 和数字签名无法转换。转换可以替换字体并移除非归档操作或元数据；成功输出时会有警告提示。转换失败或检查不完整的候选文件绝不会作为 PDF/A 文件返回。输入文件不会被覆盖。JSON 验证报告会保留 `compliant` 和 `reports` 字段，并添加已检查的配置文件、结果和引擎信息。
