# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""The public dispatcher owns processing even with caller-supplied engines."""
import io
import json
import zipfile

import pytest
from PIL import Image
from pypdf import PdfReader, PdfWriter

from onekit import Artifact, execute
from onekit.execution import ExecutionContext
from onekit.models import OneKitError


def image_file(mode="RGB", color="white"):
    stream = io.BytesIO()
    Image.new(mode, (32, 24), color).save(stream, format="PNG")
    return Artifact("scan.png", stream.getvalue())


def pdf_file():
    writer = PdfWriter()
    writer.add_blank_page(width=320, height=240)
    stream = io.BytesIO()
    writer.write(stream)
    return Artifact("scan.pdf", stream.getvalue())


@pytest.mark.parametrize("identifier", ["scan-qrcode", "reverse-qrcode", "qrcode-to-text", "qrcode-to-json", "qrcode-to-vcard"])
def test_symbol_engine_uses_public_payload_interpretation(identifier, monkeypatch):
    from onekit.tools import qrcode
    raw = "BEGIN:VCARD\r\nVERSION:3.0\r\nFN:Ada\r\nEND:VCARD\r\n" if identifier.endswith("vcard") else '{"value":42}'
    calls = []
    describe = qrcode.describe_payload
    monkeypatch.setattr(qrcode, "describe_payload", lambda text: (calls.append(text), describe(text))[1])
    context = ExecutionContext(symbol_reader=lambda file, kind: [{"text": raw}, {"text": raw}])
    result = execute(identifier, [image_file()], context=context)
    assert calls == [raw]
    assert result.details["count"] == 1
    assert result.files[0].name.endswith("vcf" if identifier.endswith("vcard") else "txt" if identifier.endswith("text") else "json")


@pytest.mark.parametrize("identifier", ["scan-barcode", "barcode-to-text"])
def test_public_barcode_normalization_is_shared(identifier):
    context = ExecutionContext(symbol_reader=lambda file, kind: [{"text": "0123456789012", "format": "EAN13"}] * 2)
    result = execute(identifier, [image_file()], context=context)
    assert result.details == {"count": 1, "codes": [{"text": "123456789012", "format": "UPCA"}]}


@pytest.mark.parametrize("target", ["md", "html", "latex", "json", "docx", "pdf"])
def test_recognition_uses_public_document_converters(target):
    text = "Città <script> & 50%\x00"
    pages = [{"text": text, "pdf": pdf_file().data, "width": 160, "height": 120}]
    context = ExecutionContext(ocr_reader=lambda file, language, dpi, pdf: pages)
    result = execute("ocr-to-" + target, [image_file()], {"language": "ita"}, context=context)
    data = result.files[0].data
    if target == "pdf":
        page = PdfReader(io.BytesIO(data)).pages[0]
        assert (float(page.mediabox.width), float(page.mediabox.height)) == (160, 120)
    elif target == "docx":
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            xml = archive.read("word/document.xml").decode()
            assert "&lt;script&gt;" in xml
    elif target == "json":
        assert json.loads(data) == {"pages": [text[:-1]], "language": "ita"}
    elif target == "html":
        assert b"&lt;script&gt;" in data and b"<script>" not in data
    elif target == "latex":
        assert b"50\\%" in data
    else:
        assert "Città" in data.decode() and b"\x00" not in data


@pytest.mark.parametrize("target", ["png", "jpeg", "webp", "tiff", "pptx"])
def test_raster_engine_uses_public_converter_and_slide_assembly(target):
    image = image_file()
    calls = []

    def render(file, format, dpi):
        calls.append((format, dpi))
        stream = io.BytesIO()
        with Image.open(io.BytesIO(image.data)) as pixels:
            pixels.save(stream, format="PNG" if target == "pptx" else format.upper())
        return [{"data": stream.getvalue(), "width": 320, "height": 240}]

    result = execute("pdf-to-" + target, [pdf_file()], {"dpi": 72}, context=ExecutionContext(pdf_renderer=render))
    assert calls == [("png" if target == "pptx" else target, 72)]
    assert result.files[0].name == ("scan.pptx" if target == "pptx" else "scan.page-1." + target)
    if target == "pptx":
        with zipfile.ZipFile(io.BytesIO(result.files[0].data)) as archive:
            assert b"<p:pic>" in archive.read("ppt/slides/slide1.xml")


def test_public_redaction_masks_supplied_rasters_and_removes_original_objects():
    image = image_file(color="red")
    context = ExecutionContext(pdf_renderer=lambda file, format, dpi: [{"data": image.data, "width": 32, "height": 24}])
    result = execute("pdf-redact", [pdf_file()], {"dpi": 72, "regions": [{"x": 0, "y": 0, "width": 1, "height": 1}]}, context=context)
    document = PdfReader(io.BytesIO(result.files[0].data))
    assert result.details["metadataRemoved"] is True
    assert float(document.pages[0].mediabox.width) == 32
    images = list(document.pages[0].images)
    assert len(images) == 1
    with Image.open(io.BytesIO(images[0].data)) as raster:
        assert raster.convert("RGB").getextrema() == ((0, 0), (0, 0), (0, 0))


def test_public_foreground_compositing_preserves_existing_transparency():
    stream = io.BytesIO()
    Image.new("L", (32, 24), 128).save(stream, format="PNG")
    context = ExecutionContext(foreground_reader=lambda file: stream.getvalue())
    result = execute("image-remove-background", [image_file("RGBA", (255, 0, 0, 128))], context=context)
    with Image.open(io.BytesIO(result.files[0].data)) as image:
        assert image.getpixel((0, 0))[3] == 64


def test_public_transcript_formatting_and_language_validation():
    data = b"RIFF" + bytes(4) + b"WAVE" + bytes(32)
    context = ExecutionContext(speech_reader=lambda file, language: {"language": language, "segments": [{"start": 0, "end": 1, "text": "Hello"}]})
    result = execute("audio-to-text", [Artifact("voice.wav", data)], {"language": "en"}, context=context)
    assert result.files[0].data == b"Hello\n"
    assert json.loads(result.files[1].data)["language"] == "en"
    with pytest.raises(OneKitError, match="Language"):
        execute("audio-to-text", [Artifact("voice.wav", data)], {"language": "EN"}, context=context)


@pytest.mark.parametrize("name", ["symbol_reader", "ocr_reader", "speech_reader", "foreground_reader", "pdf_renderer"])
def test_engine_services_must_be_trusted_callables(name):
    with pytest.raises(OneKitError, match="callable"):
        ExecutionContext(**{name: {"untrusted": True}})


@pytest.mark.parametrize("kind,type_name,tag,extension", [
    ("audio", "AudioObject", "audio", "mp3"),
    ("video", "VideoObject", "video", "mp4"),
    ("image", "ImageObject", "img", "png"),
])
def test_public_source_extraction_handles_structured_data_and_rejects_active_urls(kind, type_name, tag, extension):
    from onekit.tools.link_tools import source_links
    html = (f'<{tag} src="/file.{extension}"></{tag}>'
            f'<script type="application/ld+json">{{"@graph":[{{"@type":["{type_name}"],"contentUrl":"/other.{extension}"}}]}}</script>'
            f'<meta property="og:{kind}" content="javascript:alert(1)">'
            f'<meta property="og:{kind}" content="https://user:pass@example.com/secret">')
    expected = [f"https://example.com/file.{extension}", f"https://example.com/other.{extension}"]
    assert source_links(html, "https://example.com/page", kind) == (expected[::-1] if kind == "image" else expected)


def test_public_media_signatures_and_conversion_plans_reject_disguised_inputs():
    from onekit.tools.link_tools import media_extension
    from onekit.tools.media import conversion_arguments
    assert media_extension(b"<html>Not a video</html>", "video") is None
    assert media_extension(b"\0\0\0\x18ftypisom", "video") == "mp4"
    assert media_extension(b"\x1aE\xdf\xa3\x00webm", "video") == "webm"
    plan = conversion_arguments("audio", {"format": "mp3", "codec": "libmp3lame", "bitrate": "192k"})
    assert plan == {"format": "mp3", "args": ["-vn", "-c:a", "libmp3lame", "-b:a", "192k"]}
    with pytest.raises(OneKitError, match="codec"):
        conversion_arguments("audio", {"codec": "-i https://example.com"})
    with pytest.raises(OneKitError, match="bitrate"):
        conversion_arguments("video", {"bitrate": "2000k -i secret"})
