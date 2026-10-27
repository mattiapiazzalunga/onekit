# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json
import shutil
import subprocess

import pytest
from PIL import Image, ImageChops
from pypdf import PdfReader, PdfWriter
from test_core import pdf

from onekit import Artifact, OneKitError, execute
from onekit.tools.video_edit import arguments


def test_image_text_changes_pixels_preserves_size_and_rejects_overflow():
    stream = io.BytesIO()
    source = Image.new("RGB", (320,160), "blue")
    source.save(stream, "PNG")
    file = Artifact("photo.png", stream.getvalue())
    result = execute("image-add-text", [file], {"text":"Ciao OneKit", "color":"#ffffff"})
    image = Image.open(io.BytesIO(result.files[0].data)).convert("RGB")
    assert image.size == source.size
    assert ImageChops.difference(source, image).getbbox()
    with pytest.raises(OneKitError, match="fit"):
        execute("image-add-text", [file], {"text":"Huge text", "font_size":300})
    with pytest.raises(OneKitError):
        execute("image-add-text", [file], {"text":"Hello", "font_size":"nan"})


def test_image_text_multiple_boxes_keep_independent_positions_colors_and_sizes():
    stream = io.BytesIO()
    Image.new('RGB', (640, 320), 'white').save(stream, 'PNG')
    file = Artifact('photo.png', stream.getvalue())
    boxes = [dict(text='First', x=20, y=20, font_size=32, color='#ff0000'),
             dict(text='Second', x=300, y=180, font_size=48, color='#0000ff')]
    result = execute('image-add-text', [file], {'text_boxes': boxes})
    image = Image.open(io.BytesIO(result.files[0].data)).convert('RGB')
    assert image.size == (640, 320)
    assert any(r > b and r > g for r, g, b in image.crop((20, 20, 200, 100)).get_flattened_data())
    assert any(b > r and b > g for r, g, b in image.crop((300, 180, 600, 280)).get_flattened_data())
    for invalid in [[], [{}]*51, [None], {'text': 'wrong'}, [{'text': ''}]]:
        with pytest.raises(OneKitError):
            execute('image-add-text', [file], {'text_boxes': invalid})


@pytest.mark.parametrize("rotation", [0,90,180,270])
def test_pdf_numbers_preserve_text_and_apply_only_to_selected_page(rotation):
    writer = PdfWriter(clone_from=io.BytesIO(pdf().data))
    writer.pages[1].rotate(rotation)
    stream = io.BytesIO(); writer.write(stream)
    result = execute("pdf-page-numbers", [Artifact("source.pdf",stream.getvalue())],
                     {"pages":"2", "start_number":7, "number_style":"page-of-total"})
    pages = PdfReader(io.BytesIO(result.files[0].data)).pages
    assert len(pages) == 2
    assert "OneKit regression document" in pages[0].extract_text()
    assert "7 / 7" not in pages[0].extract_text()
    assert "Second page" in pages[1].extract_text()
    assert "7 / 7" in pages[1].extract_text()
    assert pages[1].rotation == rotation


@pytest.mark.parametrize("options", [{"start":2,"end":1},{"start":-1},{"end":"nan"},{"end":True}])
def test_trim_rejects_invalid_ranges(options):
    with pytest.raises(OneKitError):
        arguments("video-trim", options)


def test_extract_rejects_silent_video():
    with pytest.raises(OneKitError, match="no audio"):
        arguments("video-extract-audio", {}, audio=False)


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="FFmpeg required")
def test_native_video_artifacts_have_expected_streams_and_duration(tmp_path):
    source = tmp_path/"sample.mp4"
    subprocess.run(["ffmpeg","-v","error","-f","lavfi","-i","color=c=blue:s=96x64:r=10:d=2",
                    "-f","lavfi","-i","sine=frequency=440:duration=2","-c:v","libx264","-c:a","aac","-shortest",str(source)],check=True)
    file = Artifact("sample.mp4",source.read_bytes())
    for tool, options, kinds in [("video-extract-audio",{},["audio"]),("video-mute",{},["video"]),
                                 ("video-trim",{"start":.5,"end":1.5},["video","audio"])]:
        result = execute(tool,[file],options)
        target = tmp_path/result.files[0].name; target.write_bytes(result.files[0].data)
        probe = json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(target)]))
        assert sorted(row["codec_type"] for row in probe["streams"]) == sorted(kinds)
        if tool == "video-trim":
            assert abs(float(probe["format"]["duration"])-1) < .2
    with pytest.raises(OneKitError, match="within"):
        execute("video-trim",[file],{"start":1,"end":3})


def test_image_text_uses_explicit_box_coordinates_and_clamps_at_edges():
    stream = io.BytesIO()
    source = Image.new('RGB', (320, 160), 'blue')
    source.save(stream, 'PNG')
    file = Artifact('photo.png', stream.getvalue())
    for x, y in [(57, 42), (320, 160)]:
        result = execute('image-add-text', [file], {'text': 'OneKit', 'font_size': 12, 'x': x, 'y': y})
        image = Image.open(io.BytesIO(result.files[0].data)).convert('RGB')
        box = ImageChops.difference(source, image).getbbox()
        assert box is not None
        if x == 57:
            assert box[:2] == (57, 42)
        else:
            assert box[2:] == (320, 160)
    for settings in [{'x': 10}, {'x': -1, 'y': 0}, {'x': 'nan', 'y': 0}]:
        with pytest.raises(OneKitError):
            execute('image-add-text', [file], {'text': 'OneKit', **settings})


def test_existing_image_compression_exports_decodable_smaller_jpeg():
    stream = io.BytesIO()
    Image.effect_noise((256,256),100).convert("RGB").save(stream,"JPEG",quality=100)
    file = Artifact("photo.jpg",stream.getvalue())
    result = execute("image-compress",[file],{"format":"jpeg","quality":55})
    assert len(result.files[0].data) < len(file.data)
    assert Image.open(io.BytesIO(result.files[0].data)).size == (256,256)

def test_short_frame_sampling_rounds_the_end_up():
    from onekit.tools.video_edit import arguments
    plan = arguments('video-to-frames', {'duration': 0.2, 'fps': 1, 'width': 96})
    assert 'fps=1:round=up,scale=96:-1' in plan
    original = arguments('video-to-frames', {'duration': 0.2, 'all_frames': True, 'width': 96})
    assert not any('fps=' in value for value in original)
