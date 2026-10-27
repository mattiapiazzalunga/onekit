# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import sys
from types import SimpleNamespace

import pytest
from PIL import Image

from onekit import Artifact, OneKitError, execute
from onekit.tools.background import foreground_mask

np = pytest.importorskip("numpy")


def model(monkeypatch, prediction):
    def retrieve(**options):
        assert options["known_hash"] == "sha256:8d10d2f3bb75ae3b6d527c77944fc5e7dcd94b29809d47a739a7a728a912b491"
        assert options["url"].startswith("https://github.com/")
        return "cached-u2net.onnx"

    class Session:
        def __init__(self, path, providers):
            assert path == "cached-u2net.onnx"
            assert providers == ["CPUExecutionProvider"]

        def get_inputs(self):
            return [SimpleNamespace(name="input")]

        def run(self, outputs, inputs):
            assert inputs["input"].shape == (1, 3, 320, 320)
            assert inputs["input"].dtype == np.float32
            assert np.isfinite(inputs["input"]).all()
            return [prediction]

    monkeypatch.setitem(sys.modules, "onnxruntime", SimpleNamespace(InferenceSession=Session))
    monkeypatch.setitem(sys.modules, "pooch", SimpleNamespace(retrieve=retrieve, os_cache=lambda name: name))


def test_model_normalizes_black_input_and_returns_a_resized_mask(monkeypatch):
    model(monkeypatch, np.linspace(0, 1, 320 * 320, dtype=np.float32).reshape(1, 1, 320, 320))
    mask = foreground_mask(Image.new("RGB", (12, 9)))
    assert mask.mode == "L" and mask.size == (12, 9)
    assert mask.getextrema()[1] > mask.getextrema()[0]


def test_constant_model_output_does_not_divide_by_zero(monkeypatch):
    model(monkeypatch, np.zeros((1, 1, 320, 320), dtype=np.float32))
    assert foreground_mask(Image.new("RGB", (12, 9))).getextrema() == (0, 0)


def test_invalid_model_output_is_reported_without_exporting_an_image(monkeypatch):
    model(monkeypatch, np.full((1, 1, 320, 320), np.nan, dtype=np.float32))
    source = io.BytesIO()
    Image.new("RGB", (12, 9)).save(source, format="PNG")
    with pytest.raises(OneKitError, match="Cannot load or run U2Net"):
        execute("image-remove-background", [Artifact("source.png", source.getvalue())])


def test_background_removal_preserves_existing_transparency(monkeypatch):
    from onekit.tools import background

    monkeypatch.setattr(background, "foreground_mask", lambda image: Image.new("L", image.size, 128))
    source = io.BytesIO()
    Image.new("RGBA", (12, 9), (20, 30, 40, 100)).save(source, format="PNG")
    result = execute("image-remove-background", [Artifact("source.png", source.getvalue())])
    with Image.open(io.BytesIO(result.files[0].data)) as image:
        assert image.getpixel((0, 0))[3] == 50
