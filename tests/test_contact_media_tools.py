# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json
import sys
from types import SimpleNamespace

import pytest
from PIL import Image

from onekit import Artifact, OneKitError, execute, pipeline
from onekit.tools.contacts import extract_vcard
from onekit.tools.video_edit import arguments


def test_vcard_generate_qr_extract_round_trip():
    contact = Artifact("contact.json", json.dumps({"first_name": "Ada", "last_name": "Lovelace",
                       "note": "line one\nline two; comma, slash\\", "emails": ["ada@example.org"]}).encode())
    card = execute("vcard-generate", [contact]).files[0]
    assert card.name == "contact.vcf"
    assert "FN:Ada Lovelace\r\n" in card.text()
    assert "NOTE:line one\\nline two\\; comma\\, slash\\\\" in card.text()
    result = pipeline([{"tool": "vcard-to-qrcode"}, {"tool": "qrcode-to-vcard"}], [card])
    assert result.files[0].text() == card.text()


@pytest.mark.parametrize("value", ["https://example.org/contact.vcf", "hello", "BEGIN:VCARD\nVERSION:2.1\nFN:Ada\nEND:VCARD",
                                    "BEGIN:VCARD\nVERSION:3.0\nEND:VCARD"])
def test_non_contacts_cannot_be_exported_as_vcards(value):
    with pytest.raises(OneKitError, match="complete vCard"):
        extract_vcard(value)


def image_file(size=(12, 9)):
    stream = io.BytesIO()
    Image.new("RGBA", size, (120, 30, 90, 100)).save(stream, "PNG")
    return Artifact("portrait.png", stream.getvalue())


def test_upscale_preserves_transparency_and_bounds_output():
    result = execute("image-upscale", [image_file()], {"scale": 3})
    with Image.open(io.BytesIO(result.files[0].data)) as image:
        assert image.size == (36, 27)
        assert image.getpixel((10, 10))[3] == 100
    with pytest.raises(OneKitError, match="40 million"):
        execute("image-upscale", [image_file((2000, 2000))], {"scale": 4})


@pytest.mark.parametrize("scale", [True, 0, 1, 2.5, 5, "nan", None])
def test_upscale_rejects_invalid_factors(scale):
    with pytest.raises(OneKitError, match="factor"):
        execute("image-upscale", [image_file()], {"scale": scale})


@pytest.mark.parametrize("speed,filters", [(.25, "atempo=0.5,atempo=0.5"), (4, "atempo=2,atempo=2")])
def test_video_speed_preserves_audio_pitch_and_supports_silent_video(speed, filters):
    args = arguments("video-speed", {"speed": speed})
    assert filters in args[args.index("-af") + 1]
    assert "setpts=(PTS-STARTPTS)/" in args[args.index("-vf") + 1]
    assert "-af" not in arguments("video-speed", {"speed": speed}, audio=False)


@pytest.mark.parametrize("id,options", [("video-speed", {"speed": "nan"}), ("video-speed", {"speed": True}),
    ("video-compress", {"compression_level": "invalid"}), ("video-to-gif", {"duration": 31}),
    ("video-to-gif", {"fps": 2.5}), ("video-to-gif", {"start": -1})])
def test_video_options_are_checked_before_execution(id, options):
    with pytest.raises(OneKitError):
        arguments(id, options)


def test_background_adapter_uses_a_local_model_and_transparent_png(monkeypatch):
    from onekit.tools import background
    monkeypatch.setattr(background, "foreground_mask", lambda image: Image.new("L", image.size, 0))
    result = execute("image-remove-background", [image_file()])
    with Image.open(io.BytesIO(result.files[0].data)) as image:
        assert image.mode == "RGBA"
        assert image.getpixel((0, 0))[3] == 0


def test_transcription_consumes_lazy_segments_before_removing_the_audio(monkeypatch):
    class Model:
        def __init__(self, name, **options):
            assert name == "tiny" and options["compute_type"] == "int8"

        def transcribe(self, source, **options):
            from pathlib import Path
            def segments():
                assert Path(source).is_file()
                yield SimpleNamespace(start=0., end=1., text=" Ciao mondo ")
            assert options["language"] == "it"
            return segments(), SimpleNamespace(language="it")
    monkeypatch.setitem(sys.modules, "faster_whisper", SimpleNamespace(WhisperModel=Model))
    import wave
    stream = io.BytesIO()
    with wave.open(stream, "wb") as audio:
        audio.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
        audio.writeframes(bytes(32000))
    result = execute("audio-to-text", [Artifact("voice.wav", stream.getvalue())], {"language": "it"})
    assert result.files[0].text() == "Ciao mondo\n"
    assert json.loads(result.files[1].text())["segments"][0]["start"] == 0
