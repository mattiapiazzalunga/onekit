# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json

import pytest
from PIL import Image, ImageOps

from onekit import Artifact, OneKitError, execute, pipeline
from onekit.cli import main
from onekit.tools.qrcode import describe_payload, vcard_payload, wifi_payload


def qr(tool, content, options=None):
    suffix = "json" if isinstance(content, dict) else "txt"
    data = json.dumps(content).encode() if isinstance(content, dict) else content.encode()
    return execute(tool, [Artifact(f"input.{suffix}", data)], options)


@pytest.mark.parametrize("content", ["Ciao 🌍 — città, 日本語", "  spaces\nand lines\n", "https://example.org/?a=1&b=2"])
def test_real_qr_generation_and_exact_text_decoding(content):
    generated = qr("text-to-qrcode", content)
    assert execute("qrcode-to-text", generated.files).files[0].text() == content
    assert generated.details["payload"] == content


def test_wifi_special_characters_and_hidden_network_round_trip():
    network = {"ssid": 'Caffè;"A\\B:1', "password": 'p;:,"\\value', "security": "WPA", "hidden": True}
    image = qr("wifi-to-qrcode", network)
    code = execute("reverse-qrcode", image.files).details["codes"][0]
    assert code["type"] == "wifi"
    assert {key: code["data"][key] for key in network} == network
    assert "P:" not in wifi_payload({"ssid": "Open", "security": "nopass", "password": "ignored"})


def test_vcard_multiple_typed_fields_folded_utf8_and_no_property_injection():
    contact = {
        "version": "4.0", "formatted_name": "É"*60, "first_name": "Ada", "last_name": "Lovelace",
        "phones": [{"value": "+390123", "type": "work,voice", "preferred": True}, {"value": "+390456", "type": "cell"}],
        "emails": [{"value": "ada@example.org", "type": "work"}],
        "urls": ["https://example.org/a;b?x=1,2"],
        "addresses": [{"street": "First; street", "city": "Milano", "country": "Italia", "label": 'Work "HQ"'}],
        "birthday": "1815-12-10", "anniversary": "1835-07-08", "categories": ["Friends", "Work, projects"],
        "note": "line\r\nURL:https://injected.example", "latitude": 45.46, "longitude": 9.19,
    }
    payload = vcard_payload(contact)
    assert all(len(line.encode()) <= 75 for line in payload.split("\r\n"))
    assert ";PREF=1" in payload and "TEL;VALUE=text;TYPE=WORK,VOICE" in payload
    assert "URL;TYPE=HOME:https://example.org/a;b?x=1,2" in payload
    assert "\r\nURL:https://injected" not in payload
    generated = qr("vcard-to-qrcode", contact, {"include_payload": True})
    assert generated.files[1].name == "payload.vcf"
    assert generated.files[1].text() == payload
    decoded = execute("qrcode-to-text", [generated.files[0]])
    assert decoded.files[0].text() == payload


@pytest.mark.parametrize("value", [{"hello": "世界", "data": [1, True, None]}, [1, 2], None, 42, "hello"])
def test_text_qr_json_pipeline_recovers_structured_value(value):
    result = pipeline([{"tool": "text-to-qrcode"}, {"tool": "qrcode-to-json"}], [Artifact("input.txt", json.dumps(value).encode())])
    assert json.loads(result.files[0].text()) == value


def test_scanner_handles_rotated_and_inverted_qr_images(tmp_path):
    file = qr("url-to-qrcode", "https://example.org/test").files[0]
    image = Image.open(io.BytesIO(file.data)).convert("RGB")
    inverted = ImageOps.invert(image).rotate(90, expand=True)
    path = tmp_path / "photo.png"
    inverted.save(path)
    target = tmp_path / "decoded.json"
    assert main(["run", "scan-qrcode", str(path), "-o", str(target)]) == 0
    assert json.loads(target.read_text())["codes"][0]["type"] == "url"


def test_svg_export_is_vector_and_does_not_embed_input_markup():
    result = qr("text-to-qrcode", '<script>alert("test")</script>', {"format": "svg", "dark": "#123456", "light": "#ffffff"})
    assert result.files[0].name == "qrcode.svg"
    assert b"<svg" in result.files[0].data
    assert b"<script" not in result.files[0].data


@pytest.mark.parametrize("shape", ["square", "rounded", "dots"])
@pytest.mark.parametrize("scale", [2, 8])
def test_module_shapes_preserve_decodable_payload_and_dimensions(shape, scale):
    content = "Ciao OneKit — https://example.org/形"
    generated = qr("text-to-qrcode", content, {"shape": shape, "scale": scale})
    assert execute("qrcode-to-text", generated.files).files[0].text() == content
    with Image.open(io.BytesIO(generated.files[0].data)) as image:
        assert image.size == ((generated.details["modules"] + 8) * scale,) * 2
    assert generated.details["shape"] == shape


@pytest.mark.parametrize("shape,element", [("rounded", "rect"), ("dots", "circle")])
def test_styled_svg_contains_shapes_and_square_position_markers(shape, element):
    from xml.etree import ElementTree
    generated = qr("text-to-qrcode", "OneKit", {"shape": shape, "format": "svg"})
    root = ElementTree.fromstring(generated.files[0].data)
    assert root.findall(f".//{{http://www.w3.org/2000/svg}}{element}")
    assert any("rx" not in rect.attrib for rect in root.findall(".//{http://www.w3.org/2000/svg}rect"))
    assert root.attrib["width"] == str((generated.details["modules"] + 8) * 8)


@pytest.mark.parametrize("shape", ["square", "rounded", "dots"])
def test_transparent_png_preserves_alpha_and_decodes(shape):
    generated = qr("text-to-qrcode", "Transparent OneKit", {"shape": shape, "transparent_background": "true", "light": "#000000"})
    with Image.open(io.BytesIO(generated.files[0].data)) as source:
        image = source.convert("RGBA")
        assert image.getpixel((0, 0))[3] == 0
        assert image.getchannel("A").getextrema() == (0, 255)
    assert execute("qrcode-to-text", generated.files).files[0].text() == "Transparent OneKit"
    assert generated.details["transparentBackground"] is True


@pytest.mark.parametrize("shape", ["square", "rounded", "dots"])
def test_transparent_svg_omits_background(shape):
    generated = qr("text-to-qrcode", "Transparent SVG", {"shape": shape, "format": "svg", "transparent_background": True})
    assert b"#ffffff" not in generated.files[0].data
    assert b'fill="None"' not in generated.files[0].data


def test_false_transparency_preserves_opaque_background():
    generated = qr("text-to-qrcode", "Opaque", {"transparent_background": "false"})
    with Image.open(io.BytesIO(generated.files[0].data)) as source:
        assert source.convert("RGBA").getpixel((0, 0)) == (255, 255, 255, 255)


@pytest.mark.parametrize("shape", ["square", "rounded", "dots"])
def test_jpeg_export_has_correct_format_dimensions_and_readable_content(shape):
    generated = qr("text-to-qrcode", "JPEG OneKit — città", {"format": "jpeg", "shape": shape})
    assert generated.files[0].name == "qrcode.jpeg"
    with Image.open(io.BytesIO(generated.files[0].data)) as image:
        assert image.format == "JPEG"
        assert image.mode == "RGB"
        assert image.size == ((generated.details["modules"] + 8) * 8,) * 2
    assert execute("qrcode-to-text", generated.files).files[0].text() == "JPEG OneKit — città"


@pytest.mark.parametrize("shape", ["square", "rounded", "dots"])
@pytest.mark.parametrize("fmt", ["png", "jpeg"])
@pytest.mark.parametrize("overlay", ["none", "text", "image"])
def test_rounded_finders_and_center_marks_remain_readable(shape, fmt, overlay):
    import base64
    logo = io.BytesIO()
    Image.new("RGB", (40, 20), "#2264d9").save(logo, format="PNG")
    options = {"shape": shape, "format": fmt, "corner_style": "rounded", "overlay_type": overlay,
               "overlay_text": "OK", "overlay_image_base64": base64.b64encode(logo.getvalue()).decode(), "overlay_size": 20}
    payload = "OneKit custom QR — https://example.org/" + "a" * 200
    generated = qr("text-to-qrcode", payload, options)
    assert execute("qrcode-to-text", generated.files).files[0].text() == payload
    assert generated.details["cornerStyle"] == "rounded"
    if overlay != "none":
        assert generated.details["errorCorrection"] == "H"


def test_center_box_preserves_function_modules_in_large_symbols():
    import segno
    from segno.consts import TYPE_DATA_DARK, TYPE_DATA_LIGHT

    from onekit.tools.qrcode import center_box
    symbol = segno.make("x" * 700, error="H", micro=False)
    matrix = list(symbol.matrix_iter(border=0, verbose=True))
    x, y, side = center_box(matrix, 20)
    assert all(value in (TYPE_DATA_DARK, TYPE_DATA_LIGHT) for row in matrix[y:y+side] for value in row[x:x+side])


def test_svg_center_text_is_escaped_and_rounded_finders_are_vector():
    result = qr("text-to-qrcode", "Test", {"format": "svg", "corner_style": "rounded", "overlay_type": "text", "overlay_text": "<b>&"})
    assert b"&lt;b&gt;&amp;" in result.files[0].data
    assert b'fill-rule="evenodd"' in result.files[0].data
    assert b"<b>" not in result.files[0].data


def test_small_logos_scale_to_fit_the_center_area():
    import base64
    source = io.BytesIO()
    Image.new("RGB", (1, 1), "blue").save(source, format="PNG")
    generated = qr("text-to-qrcode", "Logo", {"overlay_type": "image", "overlay_image_base64": base64.b64encode(source.getvalue()).decode(), "overlay_size": 20})
    with Image.open(io.BytesIO(generated.files[0].data)) as image:
        assert sum(blue > 200 and red < 30 for red, green, blue in image.convert("RGB").get_flattened_data()) > 50


@pytest.mark.parametrize("tool,content,options,match", [
    ("url-to-qrcode", "javascript:alert(1)", {}, "HTTP"),
    ("wifi-to-qrcode", {"ssid": "test", "security": "WPA"}, {}, "password"),
    ("wifi-to-qrcode", {"ssid": "test", "security": "WPA2-EAP", "password": "x"}, {}, "identity"),
    ("vcard-to-qrcode", {"formatted_name": "A", "birthday": "2020-99-01"}, {}, "process"),
    ("vcard-to-qrcode", {"formatted_name": "A", "unknown": "value"}, {}, "Unknown"),
    ("text-to-qrcode", "test", {"border": 0}, "quiet-zone"),
    ("text-to-qrcode", "test", {"shape": "triangle"}, "shape"),
    ("text-to-qrcode", "test", {"transparent_background": "yes"}, "true or false"),
    ("text-to-qrcode", "test", {"format": "jpeg", "transparent_background": True}, "JPEG does not support transparency"),
    ("text-to-qrcode", "test", {"corner_style": "invalid"}, "corners"),
    ("text-to-qrcode", "test", {"overlay_type": "invalid"}, "center mark"),
    ("text-to-qrcode", "test", {"overlay_type": "text", "overlay_text": ""}, "1–16"),
    ("text-to-qrcode", "test", {"overlay_type": "text", "overlay_text": "a"*17}, "1–16"),
    ("text-to-qrcode", "test", {"overlay_type": "text", "overlay_text": "A", "overlay_size": 40}, "10–20"),
    ("text-to-qrcode", "test", {"overlay_type": "image", "overlay_image_base64": "invalid"}, "valid PNG or JPEG"),
    ("text-to-qrcode", "test", {"dark": "#aaaaaa", "light": "#ffffff"}, "contrast"),
    ("text-to-qrcode", "test", {"dark": 'red\" onload=\"x'}, "hexadecimal"),
    ("text-to-qrcode", "a"*4000, {"error_correction": "H"}, "capacity"),
])
def test_invalid_payloads_and_qr_options_are_rejected(tool, content, options, match):
    with pytest.raises(OneKitError, match=match):
        qr(tool, content, options)


def test_no_code_image_is_an_actionable_error():
    stream = io.BytesIO()
    Image.new("RGB", (100, 100), "white").save(stream, format="PNG")
    with pytest.raises(OneKitError, match="No readable QR"):
        execute("reverse-qrcode", [Artifact("blank.png", stream.getvalue())])
    assert describe_payload("not JSON")["type"] == "text"
