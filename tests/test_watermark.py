# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json

import pytest
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, RectangleObject
from test_core import pdf

from onekit import Artifact, OneKitError, execute
from onekit.cli import main


def test_watermark_changes_only_selected_pages_preserving_source_text_and_transparency():
    source = pdf()
    result = execute("pdf-watermark", [source], {"text": "RISERVATO – società", "pages": "2", "opacity": .3, "angle": 45})
    document = PdfReader(io.BytesIO(result.files[0].data))
    assert len(document.pages) == 2
    assert "RISERVATO" not in document.pages[0].extract_text()
    assert "OneKit regression document" in document.pages[0].extract_text()
    assert "Second page" in document.pages[1].extract_text()
    assert "RISERVATO – società" in document.pages[1].extract_text()
    states = document.pages[1]["/Resources"]["/ExtGState"]
    assert any(float(state.get_object().get("/ca", 1)) == .3 for state in states.values())
    assert "RISERVATO" not in PdfReader(io.BytesIO(source.data)).pages[1].extract_text()


def test_repeated_watermark_and_multiline_text():
    result = execute("pdf-watermark", [pdf()], {"text": "DRAFT\nINTERNAL", "layout": "repeat", "pages": "1"})
    document = PdfReader(io.BytesIO(result.files[0].data))
    text = document.pages[0].extract_text()
    assert text.count("DRAFT") == 12 and text.count("INTERNAL") == 12
    assert "DRAFT" not in document.pages[1].extract_text()


@pytest.mark.parametrize("rotation", [0, 90, 180, 270])
def test_rotated_crop_page_retains_geometry_and_uses_visual_coordinate_transform(rotation):
    source = PdfReader(io.BytesIO(pdf().data))
    writer = PdfWriter()
    page = source.pages[0]
    page.cropbox = RectangleObject([20, 40, 500, 700])
    page.rotate(rotation)
    writer.add_page(page)
    stream = io.BytesIO()
    writer.write(stream)
    result = execute("pdf-watermark", [Artifact("rotated.pdf", stream.getvalue())], {"text": "TEST", "position": "top-left", "angle": 0})
    output = PdfReader(io.BytesIO(result.files[0].data))
    page = output.pages[0]
    assert page.rotation == rotation
    assert list(page.cropbox) == [20, 40, 500, 700]
    assert "OneKit regression document" in page.extract_text()
    assert "TEST" in page.extract_text()
    transforms = [list(args) for args, op in ContentStream(page.get_contents(), output).operations if op == b"cm"]
    expected = {0: [1, 0, 0, 1, 20, 40], 90: [0, 1, -1, 0, 500, 40], 180: [-1, 0, 0, -1, 500, 700], 270: [0, -1, 1, 0, 20, 700]}[rotation]
    assert expected in transforms


@pytest.mark.parametrize("options,match", [({"text": ""}, "watermark characters"), ({"text": "Secret 🌍"}, "Western"), ({"opacity": 0}, "opacity"), ({"angle": float("inf")}, "angle"), ({"color": "red"}, "hexadecimal"), ({"position": "unknown"}, "supported"), ({"pages": "3"}, "Page ranges"), ({"margin": 144, "layout": "repeat", "text": "A"*200}, "legibly")])
def test_invalid_watermark_settings_fail_clearly(options, match):
    with pytest.raises(OneKitError, match=match):
        execute("pdf-watermark", [pdf()], options)


def test_cli_watermark_export_and_original_metadata_preservation(tmp_path):
    source = tmp_path / "original.pdf"
    source.write_bytes(pdf().data)
    target = tmp_path / "watermarked.pdf"
    assert main(["run", "pdf-watermark", str(source), "--options", json.dumps({"text": "CONFIDENTIAL", "pages": "1", "position": "bottom-right", "angle": 0}), "-o", str(target)]) == 0
    assert "CONFIDENTIAL" in PdfReader(target).pages[0].extract_text()
    assert "CONFIDENTIAL" not in PdfReader(source).pages[0].extract_text()


def test_image_watermark_is_embedded_only_on_selected_pages():
    import base64
    from PIL import Image
    stream = io.BytesIO()
    Image.new("RGBA", (20, 10), (255, 0, 0, 128)).save(stream, "PNG")
    result = execute("pdf-watermark", [pdf()], {"watermark_type": "image", "image_base64": base64.b64encode(stream.getvalue()).decode(), "pages": "2", "angle": 0})
    document = PdfReader(io.BytesIO(result.files[0].data))
    assert "Second page" in document.pages[1].extract_text()
    assert "DRAFT" not in document.pages[1].extract_text()
    assert len(document.pages[0].images) == len(PdfReader(io.BytesIO(pdf().data)).pages[0].images)
    assert all(image.image.size != (20, 10) for image in document.pages[0].images)
    assert any(image.image.size == (20, 10) for image in document.pages[1].images)


@pytest.mark.parametrize("options", [{"watermark_type": "other"}, {"watermark_type": "image"}, {"watermark_type": "image", "image_base64": "invalid"}])
def test_invalid_image_watermark_is_rejected(options):
    with pytest.raises(OneKitError):
        execute("pdf-watermark", [pdf()], options)
