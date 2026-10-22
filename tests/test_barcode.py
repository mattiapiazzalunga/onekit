# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json

import pytest
from PIL import Image

from onekit import Artifact, OneKitError, execute, pipeline
from onekit.cli import doctor, main

CASES = [("code128", "OneKit-123", "OneKit-123"), ("code39", "ONEKIT-123", "ONEKIT-123"),
         ("ean13", "400638133393", "4006381333931"), ("ean8", "9638507", "96385074"),
         ("upca", "03600029145", "036000291452"), ("itf", "001234567890", "001234567890"),
         ("isbn13", "978030640615", "9780306406157")]


@pytest.mark.parametrize("kind,value,expected", CASES)
def test_standard_barcodes_generate_and_decode_exact_identifiers(kind, value, expected):
    result = execute("text-to-barcode", [Artifact("input.txt", value.encode())], {"barcode_type": kind})
    assert result.details["payload"] == expected
    assert result.files[0].name == "barcode.png"
    assert execute("barcode-to-text", result.files).files[0].text() == expected
    scanned = execute("scan-barcode", result.files)
    assert scanned.details["codes"][0]["text"] == expected
    svg = execute("text-to-barcode", [Artifact("input.txt", expected.encode())], {"barcode_type": kind, "format": "svg", "show_text": False})
    assert b"<svg" in svg.files[0].data
    assert b"<text" not in svg.files[0].data


@pytest.mark.parametrize("value,options,match", [
    ("4006381333932", {"barcode_type": "ean13"}, "check digit"),
    ("400638133393123", {"barcode_type": "ean13"}, "requires"),
    ("123", {"barcode_type": "itf"}, "even number"),
    ("abc", {"barcode_type": "code39"}, "uppercase"),
    ("Caffè", {}, "ASCII"),
    ("123456789012", {"barcode_type": "isbn13"}, "978"),
    ("123", {"quiet_zone": 0}, "quiet_zone"),
    ("123", {"module_width": 1, "quiet_zone": 3}, "quiet_zone"),
    ("123", {"dpi": 99999}, "dpi"),
    ("123", {"format": "jpg"}, "PNG, JPEG or SVG"),
])
def test_invalid_data_and_unsafe_rendering_settings(value, options, match):
    with pytest.raises(OneKitError, match=match):
        execute("text-to-barcode", [Artifact("input.txt", value.encode())], options)


@pytest.mark.parametrize("kind,value,expected", CASES)
def test_jpeg_barcodes_decode_and_preserve_identifiers(kind, value, expected):
    result = execute("text-to-barcode", [Artifact("input.txt", value.encode())], {"barcode_type": kind, "format": "jpeg"})
    assert result.files[0].name == "barcode.jpeg"
    with Image.open(io.BytesIO(result.files[0].data)) as image:
        assert image.format == "JPEG"
        assert image.mode == "RGB"
        assert image.info["dpi"] == (300, 300)
    assert execute("barcode-to-text", result.files).files[0].text() == expected


def test_barcode_pipeline_cli_and_dependency_diagnosis(tmp_path):
    source = tmp_path / "code.txt"
    source.write_text("000123456789")
    target = tmp_path / "code.png"
    assert main(["run", "text-to-barcode", str(source), "--options", '{"barcode_type":"itf"}', "-o", str(target)]) == 0
    decoded = tmp_path / "decoded.json"
    assert main(["run", "scan-barcode", str(target), "-o", str(decoded)]) == 0
    assert json.loads(decoded.read_text())["codes"][0]["text"] == "000123456789"
    assert doctor("text-to-barcode")[0]["ready"]
    result = pipeline([{"tool": "text-to-barcode"}, {"tool": "barcode-to-text"}], [Artifact("code.txt", b"OneKit-123")])
    assert result.files[0].text() == "OneKit-123"


def test_rotated_barcode_and_empty_image():
    image = execute("text-to-barcode", [Artifact("code.txt", b"OneKit-123")]).files[0]
    rotated = io.BytesIO()
    Image.open(io.BytesIO(image.data)).rotate(90, expand=True).save(rotated, format="PNG")
    assert execute("barcode-to-text", [Artifact("rotated.png", rotated.getvalue())]).files[0].text() == "OneKit-123"
    blank = io.BytesIO()
    Image.new("RGB", (300, 150), "white").save(blank, format="PNG")
    with pytest.raises(OneKitError, match="No readable barcode"):
        execute("scan-barcode", [Artifact("blank.png", blank.getvalue())])
