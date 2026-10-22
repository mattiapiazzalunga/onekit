# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Generate multi-resolution favicons and a portable website icon bundle."""
import io
import json

from ..models import Artifact, OneKitError, Result
from .images import open_image


def run(tool, files, options):
    from PIL import Image, ImageOps

    format = options.get("format", "ico")
    fit = options.get("fit", "contain")
    if format not in ("ico", "bundle"):
        raise OneKitError("Choose ICO or the website icon bundle.")
    if fit not in ("contain", "cover"):
        raise OneKitError("Choose fit (contain) or fill (cover).")
    image = open_image(files[0]).convert("RGBA")
    square = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    resized = (ImageOps.fit if fit == "cover" else ImageOps.contain)(image, (512, 512), method=Image.Resampling.LANCZOS)
    square.paste(resized, ((512 - resized.width) // 2, (512 - resized.height) // 2))
    stream = io.BytesIO()
    square.save(stream, format="ICO", sizes=[(size, size) for size in (16, 32, 48, 64, 128, 256)])
    outputs = [Artifact("favicon.ico", stream.getvalue())]
    if format == "bundle":
        for name, size in (("favicon-16x16.png", 16), ("favicon-32x32.png", 32), ("apple-touch-icon.png", 180), ("android-chrome-192x192.png", 192), ("android-chrome-512x512.png", 512)):
            stream = io.BytesIO()
            square.resize((size, size), Image.Resampling.LANCZOS).save(stream, format="PNG")
            outputs.append(Artifact(name, stream.getvalue()))
        manifest = {"name": "Your website", "short_name": "Website", "icons": [{"src": f"/android-chrome-{size}x{size}.png", "sizes": f"{size}x{size}", "type": "image/png", "purpose": "any"} for size in (192, 512)], "display": "standalone"}
        outputs.append(Artifact("site.webmanifest", (json.dumps(manifest, indent=2) + "\n").encode()))
        markup = '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n<link rel="manifest" href="/site.webmanifest">\n'
        outputs.append(Artifact("installation.txt", ("Upload these files to your website root. Add the following inside <head>. Adjust paths if you use another folder. Edit site.webmanifest to set your website name.\n\n" + markup).encode()))
    return Result(outputs, details={"icoSizes": [16, 32, 48, 64, 128, 256], "fit": fit})
