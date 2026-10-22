# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io

import pytest
from PIL import Image, PngImagePlugin
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, FloatObject, NameObject, TextStringObject
from reportlab.pdfgen import canvas

from onekit import Artifact, OneKitError, execute
from onekit.cli import main

REGION = {"page": 1, "x": .1, "y": .1, "width": .8, "height": .35}


def private_pdf(secret="PRIVATE-ACCOUNT-123"):
    stream = io.BytesIO()
    writer = canvas.Canvas(stream, pagesize=(240, 200))
    writer.drawString(30, 145, secret)
    writer.drawString(30, 35, "PUBLIC CONTENT")
    writer.showPage()
    writer.drawString(30, 145, "SECOND PAGE")
    writer.save()
    source = PdfReader(io.BytesIO(stream.getvalue()))
    document = PdfWriter()
    for page in source.pages:
        document.add_page(page)
    document.add_metadata({"/Author": "HIDDEN-AUTHOR", "/Title": "HIDDEN-TITLE"})
    document.add_attachment("private.txt", b"HIDDEN-ATTACHMENT")
    annotation = DictionaryObject({NameObject("/Type"): NameObject("/Annot"), NameObject("/Subtype"): NameObject("/Text"), NameObject("/Rect"): ArrayObject([FloatObject(10), FloatObject(10), FloatObject(20), FloatObject(20)]), NameObject("/Contents"): TextStringObject("HIDDEN-COMMENT")})
    document.add_annotation(0, annotation)
    output = io.BytesIO()
    document.write(output)
    return Artifact("private.pdf", output.getvalue())


def private_image():
    image = Image.new("RGBA", (100, 80), (220, 20, 90, 255))
    image.putpixel((99, 79), (1, 2, 3, 0))
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Private", "HIDDEN-IMAGE-SECRET")
    stream = io.BytesIO()
    exif = Image.Exif()
    exif[270] = "HIDDEN-EXIF-SECRET"
    image.save(stream, format="PNG", pnginfo=metadata, exif=exif)
    return Artifact("private.png", stream.getvalue())


def test_pdf_contains_only_already_redacted_images_and_no_original_objects():
    original = private_pdf()
    result = execute("pdf-redact", [original], {"regions": [REGION], "dpi": 144})
    assert result.files[0].name == "redacted.pdf"
    output = PdfReader(io.BytesIO(result.files[0].data))
    assert len(output.pages) == 2
    assert all(not page.extract_text().strip() for page in output.pages)
    assert all(not page.get("/Annots") for page in output.pages)
    assert not output.attachments
    assert not output.trailer["/Root"].get("/AcroForm")
    assert not output.metadata and not output.xmp_metadata
    image = output.pages[0].images[0].image.convert("RGB")
    assert image.getpixel((100, 100)) == (0, 0, 0)
    assert image.getpixel((10, 10)) == (255, 255, 255)
    assert "PRIVATE-ACCOUNT-123" in PdfReader(io.BytesIO(original.data)).pages[0].extract_text()
    assert "HIDDEN-AUTHOR" not in repr(output.metadata)
    assert output.pages[0].mediabox.width == 240
    assert output.pages[0].mediabox.height == 200


def test_original_secrets_differ_but_exported_pixels_are_identical():
    first = execute("pdf-redact", [private_pdf("PRIVATE-ACCOUNT-123")], {"regions": [REGION]})
    second = execute("pdf-redact", [private_pdf("SECRET-OTHER-98765")], {"regions": [REGION]})
    a = PdfReader(io.BytesIO(first.files[0].data)).pages[0].images[0].image
    b = PdfReader(io.BytesIO(second.files[0].data)).pages[0].images[0].image
    assert a.tobytes() == b.tobytes()


def test_image_pixels_are_destroyed_and_all_original_metadata_and_alpha_are_removed():
    source = private_image()
    result = execute("image-redact", [source], {"regions": [{"x": .2, "y": .2, "width": .5, "height": .5}]})
    with Image.open(io.BytesIO(result.files[0].data)) as output:
        assert output.mode == "RGB"
        assert output.getpixel((40, 40)) == (0, 0, 0)
        assert output.getpixel((0, 0)) == (220, 20, 90)
        assert output.getpixel((99, 79)) == (255, 255, 255)
        assert not output.info and not output.getexif()
    assert b"HIDDEN-IMAGE-SECRET" not in result.files[0].data
    assert Image.open(io.BytesIO(source.data)).getpixel((40, 40)) == (220, 20, 90, 255)


def test_no_unredacted_animation_frames_are_exported():
    stream = io.BytesIO()
    Image.new("RGB", (100, 80), "red").save(stream, format="GIF", save_all=True, append_images=[Image.new("RGB", (100, 80), "blue")], duration=100)
    with pytest.raises(OneKitError, match="multi-frame"):
        execute("image-redact", [Artifact("animation.gif", stream.getvalue())], {"regions": [REGION]})


@pytest.mark.parametrize("regions", [[], [{}], [{"x": -1, "y": 0, "width": .2, "height": .2}], [{"x": .9, "y": 0, "width": .2, "height": .2}], [{"x": 0, "y": 0, "width": 0, "height": .2}], [{"x": 0, "y": 0, "width": True, "height": .2}], [{"page": 3, "x": 0, "y": 0, "width": .2, "height": .2}]])
def test_invalid_or_missing_areas_fail_without_producing_a_file(regions):
    with pytest.raises(OneKitError):
        execute("pdf-redact", [private_pdf()], {"regions": regions})


def test_cli_exports_a_new_redacted_file(tmp_path):
    import json
    source = tmp_path / "private.pdf"
    source.write_bytes(private_pdf().data)
    target = tmp_path / "redacted.pdf"
    assert main(["run", "pdf-redact", str(source), "--options", json.dumps({"regions": [REGION]}), "-o", str(target)]) == 0
    assert "PRIVATE" not in PdfReader(target).pages[0].extract_text()


def test_exif_orientation_is_applied_before_image_redaction():
    source = Image.new("RGB", (40, 20), "red")
    exif = Image.Exif()
    exif[274] = 6
    exif[270] = "PRIVATE-ORIENTATION-METADATA"
    stream = io.BytesIO()
    source.save(stream, format="JPEG", exif=exif)
    result = execute("image-redact", [Artifact("rotated.jpg", stream.getvalue())], {"regions": [{"x": 0, "y": 0, "width": 1, "height": .5}]})
    with Image.open(io.BytesIO(result.files[0].data)) as output:
        assert output.size == (20, 40)
        assert output.getpixel((10, 10)) == (0, 0, 0)
        assert output.getpixel((10, 35))[0] > 200
        assert not output.getexif()


def test_rotated_and_cropped_pdf_preserves_visual_dimensions_and_mask_coordinates():
    from pypdf.generic import RectangleObject
    document = PdfWriter()
    source = PdfReader(io.BytesIO(private_pdf().data)).pages[0]
    source.cropbox = RectangleObject([10, 10, 220, 190])
    source.rotate(90)
    document.add_page(source)
    stream = io.BytesIO()
    document.write(stream)
    result = execute("pdf-redact", [Artifact("rotated.pdf", stream.getvalue())], {"regions": [{"x": 0, "y": 0, "width": .5, "height": .5}]})
    page = PdfReader(io.BytesIO(result.files[0].data)).pages[0]
    assert (float(page.mediabox.width), float(page.mediabox.height)) == (180, 210)
    image = page.images[0].image.convert("RGB")
    assert image.getpixel((10, 10)) == (0, 0, 0)
    assert not page.extract_text().strip()


def test_existing_opaque_annotation_cover_is_not_removed_to_reveal_private_text():
    from pypdf.generic import DecodedStreamObject, NumberObject, RectangleObject
    source = PdfReader(io.BytesIO(private_pdf().data))
    writer = PdfWriter()
    writer.add_page(source.pages[0])
    appearance = DecodedStreamObject()
    appearance.set_data(b"0 0 0 rg 0 0 185 35 re f")
    appearance.update({NameObject("/Type"): NameObject("/XObject"), NameObject("/Subtype"): NameObject("/Form"), NameObject("/BBox"): RectangleObject([0, 0, 185, 35])})
    annotation = DictionaryObject({NameObject("/Type"): NameObject("/Annot"), NameObject("/Subtype"): NameObject("/Square"), NameObject("/Rect"): RectangleObject([25, 130, 210, 165]), NameObject("/F"): NumberObject(4), NameObject("/AP"): DictionaryObject({NameObject("/N"): writer._add_object(appearance)})})
    writer.add_annotation(0, annotation)
    stream = io.BytesIO()
    writer.write(stream)
    result = execute("pdf-redact", [Artifact("covered.pdf", stream.getvalue())], {"regions": [{"x": 0, "y": .9, "width": 1, "height": .1}]})
    output = PdfReader(io.BytesIO(result.files[0].data))
    assert output.pages[0].images[0].image.convert("RGB").getpixel((100, 100)) == (0, 0, 0)
    assert not output.pages[0].get("/Annots")


@pytest.mark.parametrize("mode", ["RGB", "L", "RGBA", "LA", "P"])
@pytest.mark.parametrize("transparent", [False, True])
def test_mask_image_preserves_flattening_and_removes_metadata(mode, transparent):
    from PIL import Image, ImageDraw
    from onekit.tools.redaction import mask_image, pixel_box

    source = Image.new(mode, (17, 13))
    if mode == "P":
        source.putpalette([value for i in range(256) for value in (i, 255-i, i//2)])
    for y in range(source.height):
        for x in range(source.width):
            source.putpixel((x, y), (x*11, y*13, 90) if mode == "RGB" else
                            (x*11, y*13, 90, (x+y)*8) if mode == "RGBA" else
                            (x*11, (x+y)*8) if mode == "LA" else x*11)
    source.info["comment"] = "private"
    if transparent and mode in ("RGB", "L", "P"):
        source.info["transparency"] = source.getpixel((0, 0))
    regions = [{"page": 1, "x": .2, "y": .2, "width": .3, "height": .4}]
    expected = Image.new("RGB", source.size, "white")
    rgba = source.convert("RGBA")
    expected.paste(rgba, mask=rgba.getchannel("A"))
    left, top, right, bottom = pixel_box(regions[0], *source.size)
    ImageDraw.Draw(expected).rectangle((left, top, right-1, bottom-1), fill="black")
    actual = mask_image(source, regions)
    assert actual.tobytes() == expected.tobytes()
    assert actual.info == {}
    assert source.info["comment"] == "private"
