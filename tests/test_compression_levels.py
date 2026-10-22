import io

import pytest
from pypdf import PdfReader
from reportlab.pdfgen import canvas

from onekit import Artifact, OneKitError, execute


@pytest.mark.parametrize("level", ["light", "balanced", "maximum"])
def test_pdf_compression_levels_preserve_text_and_report_actual_sizes(level):
    stream = io.BytesIO()
    document = canvas.Canvas(stream, pageCompression=0)
    document.drawString(40, 700, "OneKit compression preserves this text.")
    document.save()
    original = stream.getvalue()
    result = execute("pdf-compress", [Artifact("input.pdf", original)], {"compression_level": level})
    output = result.files[0].data
    assert "OneKit compression preserves this text." in PdfReader(io.BytesIO(output)).pages[0].extract_text()
    assert result.details["inputBytes"] == len(original)
    assert result.details["outputBytes"] == len(output)
    assert len(output) <= len(original)


def test_invalid_pdf_compression_level_is_rejected():
    stream = io.BytesIO()
    document = canvas.Canvas(stream)
    document.drawString(40, 700, "Test")
    document.save()
    with pytest.raises(OneKitError, match="light, balanced or maximum"):
        execute("pdf-compress", [Artifact("input.pdf", stream.getvalue())], {"compression_level": "unknown"})


def image_pdf(alpha=False):
    import random

    from PIL import Image
    from reportlab.lib.utils import ImageReader

    pixels = random.Random(42).randbytes(1600 * 1200 * 3)
    image = Image.frombytes("RGB", (1600, 1200), pixels)
    if alpha:
        image.putalpha(128)
    stream = io.BytesIO()
    document = canvas.Canvas(stream)
    for index in range(2):
        document.drawImage(ImageReader(image), 30, 150, width=500, height=375, mask="auto")
        document.drawString(40, 700, f"Searchable page {index + 1}")
        document.rect(20, 20, 40, 40)
        document.showPage()
    document.save()
    return Artifact("illustrated.pdf", stream.getvalue())


def test_image_presets_reduce_size_without_rasterizing_pages_or_changing_geometry():
    original = image_pdf()
    source = PdfReader(io.BytesIO(original.data))
    outputs = {}
    for level in ("light", "balanced", "maximum"):
        result = execute("pdf-compress", [original], {"compression_level": level})
        outputs[level] = result.files[0].data
        reader = PdfReader(io.BytesIO(outputs[level]))
        assert len(reader.pages) == 2
        assert len(outputs[level]) <= len(original.data)
        for index, page in enumerate(reader.pages):
            assert f"Searchable page {index + 1}" in page.extract_text()
            assert page.mediabox == source.pages[index].mediabox
            assert len(page.images) == 1
        if level == "light":
            assert reader.pages[0].images[0].data == source.pages[0].images[0].data
        else:
            assert result.details["imagesOptimized"] == 1  # shared image optimized once
    assert len(outputs["maximum"]) < len(outputs["balanced"]) < len(outputs["light"])
    assert PdfReader(io.BytesIO(outputs["maximum"])).pages[0].images[0].image.width == 1400


def test_transparent_images_are_preserved_and_metadata_survives():
    original = image_pdf(alpha=True)
    result = execute("pdf-compress", [original], {"compression_level": "maximum"})
    assert result.details["imagesOptimized"] == 0
    reader = PdfReader(io.BytesIO(result.files[0].data))
    source = PdfReader(io.BytesIO(original.data))
    assert reader.pages[0].images[0].data == source.pages[0].images[0].data
    assert reader.metadata.title == source.metadata.title


def test_already_optimized_output_is_never_larger_and_can_keep_original_bytes():
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(100, 100)
    stream = io.BytesIO()
    writer.write(stream)
    original = Artifact("minimal.pdf", stream.getvalue())
    result = execute("pdf-compress", [original], {"compression_level": "maximum"})
    assert len(result.files[0].data) <= len(original.data)
    if result.details["originalRetained"]:
        assert result.files[0].data == original.data
        assert any("original file" in warning for warning in result.warnings)


def test_shared_page_content_streams_remain_visible_on_every_page():
    from pypdf import PdfWriter
    from pypdf.generic import NameObject
    source = io.BytesIO()
    document = canvas.Canvas(source, pageCompression=0)
    document.drawString(40, 700, "Shared text on both pages")
    document.save()
    reader = PdfReader(io.BytesIO(source.getvalue()))
    writer = PdfWriter()
    first = writer.add_page(reader.pages[0])
    second = writer.add_blank_page(float(first.mediabox.width), float(first.mediabox.height))
    second[NameObject("/Resources")] = first.raw_get("/Resources")
    second[NameObject("/Contents")] = first.raw_get("/Contents")
    stream = io.BytesIO()
    writer.write(stream)
    result = execute("pdf-compress", [Artifact("shared.pdf", stream.getvalue())], {"compression_level": "maximum"})
    output = PdfReader(io.BytesIO(result.files[0].data))
    assert len(output.pages) == 2
    assert all("Shared text on both pages" in page.extract_text() for page in output.pages)
