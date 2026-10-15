# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
import io

from ...models import OneKitError, Result, output


def run(tool, files, options):
    from fontTools.ttLib import TTFont
    target = options.get("format", "woff")
    if target not in ("ttf", "otf", "woff", "woff2"):
        raise OneKitError("Font format must be ttf, otf, woff or woff2.")
    font = TTFont(io.BytesIO(files[0].data))
    if target == "otf" and "CFF " not in font and "CFF2" not in font:
        raise OneKitError("This font has TrueType outlines. Use ttf or woff; converting outlines is not supported.")
    if target == "ttf" and "glyf" not in font:
        raise OneKitError("This font has CFF outlines. Use otf or woff; converting outlines is not supported.")
    font.flavor = target if target.startswith("woff") else None
    stream = io.BytesIO()
    font.save(stream)
    font.close()
    return Result([output(files[0], target, stream.getvalue())])
