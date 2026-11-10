# Android packages and automatic face blur

Packages one standalone APK and its metadata into an XAPK archive without rewriting APK bytes. Split APKs are rejected. Requires an XAPK-compatible installer; signatures are not verified.

Extracts original APKs and OBB data without rewriting APK bytes. Split APKs must be installed together; they are not merged into a universal APK. Signatures are not verified.

Detects faces locally with YuNet and blurs them in a fresh PNG. Review every face before sharing: automatic detection can miss faces and blur does not guarantee anonymity. Single-frame images, up to 16 million pixels.

PNG output omits source metadata. No image is exported when no face is detected.

```sh
onekit run apk-to-xapk app.apk -o app.xapk
onekit run xapk-to-apk app.xapk -o extracted/
onekit run image-blur-faces photo.jpg -o blurred.png
```

Install the optional `faces` extra for local face detection.
