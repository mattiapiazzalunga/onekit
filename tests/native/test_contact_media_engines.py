# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json
import shutil

import pytest
from PIL import Image

from onekit import Artifact, execute
from onekit.tools.native import command

pytestmark = pytest.mark.native


@pytest.fixture(params=[True, False], ids=["with-audio", "silent-video"])
def clip(request, tmp_path):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        pytest.skip("Install FFmpeg and ffprobe for native media integration tests.")
    args = ["-f", "lavfi", "-i", "testsrc=size=96x64:rate=12"]
    if request.param:
        args += ["-f", "lavfi", "-i", "sine=frequency=440:sample_rate=16000"]
    command("ffmpeg", ["-nostdin", "-y", "-loglevel", "error", *args, "-t", "2", "-c:v", "libx264",
                       "-pix_fmt", "yuv420p", "-c:a", "aac", "input.mp4"], tmp_path)
    return Artifact("input.mp4", (tmp_path / "input.mp4").read_bytes())


@pytest.mark.parametrize("speed", [.5, 4])
def test_native_video_speed_changes_both_stream_durations(clip, speed, tmp_path):
    result = execute("video-speed", [clip], {"speed": speed})
    (tmp_path / "result.mp4").write_bytes(result.files[0].data)
    report = json.loads(command("ffprobe", ["-v", "error", "-show_streams", "-of", "json", "result.mp4"], tmp_path))
    for stream in report["streams"]:
        assert float(stream["duration"]) == pytest.approx(2 / speed, abs=.3)


def test_native_gif_exports_selected_size_and_compression_keeps_smaller_original(clip):
    result = execute("video-to-gif", [clip], {"width": 96, "duration": .5, "fps": 6})
    with Image.open(io.BytesIO(result.files[0].data)) as image:
        assert image.format == "GIF" and image.width == 96
        assert image.n_frames >= 2
    compressed = execute("video-compress", [clip])
    assert len(compressed.files[0].data) <= len(clip.data)
