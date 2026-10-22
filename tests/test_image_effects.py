# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io

import pytest
from PIL import Image, PngImagePlugin

from onekit import Artifact, OneKitError, execute


def source():
    image = Image.new("RGBA", (64, 48))
    for y in range(48):
        for x in range(64):
            image.putpixel((x, y), (255 if x % 2 else 0, y * 5, 80, 255))
    image.putpixel((63, 47), (99, 42, 13, 0))
    meta = PngImagePlugin.PngInfo()
    meta.add_text("private", "HIDDEN-metadata")
    stream = io.BytesIO()
    image.save(stream, "PNG", pnginfo=meta)
    return Artifact("private.png", stream.getvalue())


def apply(**options):
    result = execute("image-effects", [source()], options)
    return Image.open(io.BytesIO(result.files[0].data)), result


@pytest.mark.parametrize("effect", ["blur", "box-blur", "pixelate", "solid", "grayscale"])
def test_effects_have_real_pixel_output_and_clean_metadata(effect):
    image, result = apply(effect=effect, strength=8, color="#123456")
    assert image.size == (64, 48)
    assert image.mode == "RGB"
    assert not image.info
    assert b"HIDDEN" not in result.files[0].data
    assert image.getpixel((30, 20)) != (0, 100, 80)
    if effect == "solid":
        assert image.getpixel((30, 20)) == (18, 52, 86)
    elif effect == "grayscale":
        assert len(set(image.getpixel((30, 20)))) == 1
    elif effect == "pixelate":
        assert image.getpixel((0, 0)) == image.getpixel((7, 7))
    assert any(warning.startswith("Blur and pixelation are visual effects") for warning in result.warnings) == (effect in ("blur", "box-blur", "pixelate"))


def test_selected_area_preserves_outside_and_removes_hidden_alpha():
    image, result = apply(effect="solid", scope="selected", regions=[{"x": .25, "y": .25, "width": .25, "height": .25}])
    assert image.getpixel((20, 16)) == (0, 0, 0)
    assert image.getpixel((0, 0)) == (0, 0, 80)
    assert image.getpixel((63, 47)) == (255, 255, 255)
    assert result.details["areas"] == 1


@pytest.mark.parametrize("options", [
    {"effect": "unknown"}, {"scope": "unknown"}, {"scope": "selected"},
    {"strength": 0}, {"strength": 101}, {"strength": True}, {"strength": "bad"},
    {"strength": None}, {"strength": 2.5}, {"strength": "nan"},
    {"effect": "pixelate", "strength": 1}, {"color": "red"},
    {"scope": "selected", "regions": [{"page": 2, "x": 0, "y": 0, "width": 1, "height": 1}]},
])
def test_invalid_effect_options_fail(options):
    with pytest.raises(OneKitError):
        apply(**options)


def test_animated_input_is_rejected():
    stream = io.BytesIO()
    Image.new("RGB", (4, 4), "red").save(stream, "GIF", save_all=True, append_images=[Image.new("RGB", (4, 4), "blue")])
    with pytest.raises(OneKitError, match="multi-frame"):
        execute("image-effects", [Artifact("animated.gif", stream.getvalue())], {})
