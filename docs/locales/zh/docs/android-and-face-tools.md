<a id="android-packages-and-automatic-face-blur"></a>
# Android 安装包与自动人脸模糊

将一个独立 APK 及其元数据打包为 XAPK 归档，不改写 APK 字节。拒绝拆分 APK。需要支持 XAPK 的安装程序；不验证签名。

提取原始 APK 和 OBB 数据，不改写 APK 字节。拆分 APK 必须一起安装，不会合并为单个通用 APK。不验证签名。

使用 YuNet 在本地检测人脸并模糊处理，导出新的 PNG。分享前请逐一检查人脸：自动检测可能遗漏人脸，模糊处理不能保证匿名。仅支持不超过 1600 万像素的单帧图像。

导出的 PNG 不包含原始元数据。未检测到人脸时不会导出图像。

```sh
onekit run apk-to-xapk app.apk -o app.xapk
onekit run xapk-to-apk app.xapk -o extracted/
onekit run image-blur-faces photo.jpg -o blurred.png
```

安装可选的 `faces` 依赖组以在本地检测人脸。
