# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json
import struct

import pytest
from PIL import Image
from onekit import Artifact, OneKitError, execute


def source():
    stream = io.BytesIO()
    Image.new("RGBA", (120, 60), (255, 0, 0, 255)).save(stream, format="PNG")
    return Artifact("logo.png", stream.getvalue())


def test_favicon_has_all_ico_sizes_with_valid_png_frames():
    result = execute("image-to-favicon", [source()])
    assert [file.name for file in result.files] == ["favicon.ico"]
    data = result.files[0].data
    assert struct.unpack_from("<HHH", data) == (0, 1, 6)
    for index, size in enumerate((16, 32, 48, 64, 128, 256)):
        width, height, _, _, planes, depth, length, offset = struct.unpack_from("<BBBBHHII", data, 6 + index * 16)
        assert (width or 256, height or 256, planes, depth) == (size, size, 0, 32)
        image = Image.open(io.BytesIO(data[offset:offset + length]))
        assert image.size == (size, size)
        assert image.getpixel((size // 2, 0))[3] == 0
        assert image.getpixel((size // 2, size // 2)) == (255, 0, 0, 255)


def test_bundle_fills_square_and_manifest_references_real_outputs():
    result = execute("image-to-favicon", [source()], {"format": "bundle", "fit": "cover"})
    outputs = {file.name: file.data for file in result.files}
    assert len(outputs) == 8
    manifest = json.loads(outputs["site.webmanifest"])
    for icon in manifest["icons"]:
        name = icon["src"].lstrip("/")
        image = Image.open(io.BytesIO(outputs[name]))
        assert f"{image.width}x{image.height}" == icon["sizes"]
        assert image.getpixel((0, 0)) == (255, 0, 0, 255)
    assert b'favicon.ico' in outputs['installation.txt']


@pytest.mark.parametrize("options", [{"format": "exe"}, {"fit": "stretch"}])
def test_favicon_rejects_invalid_options(options):
    with pytest.raises(OneKitError):
        execute("image-to-favicon", [source()], options)
