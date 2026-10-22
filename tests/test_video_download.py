# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from onekit.cli import main
from onekit.models import OneKitError
from onekit.tools.video_download import validate_url


@pytest.mark.parametrize("url", ["file:///tmp/test", "javascript:alert(1)", "https://a:b@example.com/video", "https://example.com/a\nb", "https://example.com:bad"])
def test_rejects_invalid_video_urls(url):
    with pytest.raises(OneKitError):
        validate_url(url)


def fake_downloader(monkeypatch, info=None):
    class Downloader:
        def __init__(self, settings):
            self.settings = settings

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def extract_info(self, url, download):
            assert not download
            return info or {"id": "test"}

        def process_ie_result(self, info, download):
            assert download
            Path(self.settings["outtmpl"].replace("%(ext)s", "mp4")).write_bytes(b"video fixture")

    monkeypatch.setitem(sys.modules, "yt_dlp", SimpleNamespace(YoutubeDL=Downloader))
    monkeypatch.setattr("onekit.tools.native.executable", lambda name: "/fake/ffmpeg")
    return Downloader


def test_download_command_and_existing_output_protection(monkeypatch, tmp_path):
    fake_downloader(monkeypatch)
    target = tmp_path / "video.mp4"
    args = ["download", "https://example.com/video", "-o", str(target), "--quality", "720"]
    assert main(args) == 0
    assert target.read_bytes() == b"video fixture"
    target.write_bytes(b"keep")
    assert main(args) == 2
    assert target.read_bytes() == b"keep"


@pytest.mark.parametrize("info", [{"_type": "playlist"}, {"is_live": True}])
def test_rejects_playlists_and_live_streams_before_download(monkeypatch, tmp_path, info):
    fake_downloader(monkeypatch, info)
    assert main(["download", "https://example.com/video", "-o", str(tmp_path / "video.mp4")]) == 2
    assert not list(tmp_path.iterdir())


def test_login_cookies_are_opt_in_and_original_file_is_not_modified(monkeypatch, tmp_path):
    downloader = fake_downloader(monkeypatch)
    seen = {}
    original = downloader.__init__
    def capture(self, settings):
        original(self, settings)
        seen.update(settings)
        if settings.get("cookiefile"):
            assert Path(settings["cookiefile"]).read_text() == "# Netscape HTTP Cookie File\n"
            Path(settings["cookiefile"]).write_text("changed by downloader")
    monkeypatch.setattr(downloader, "__init__", capture)
    cookies = tmp_path / "cookies.txt"
    cookies.write_text("# Netscape HTTP Cookie File\n")
    assert main(["download", "https://example.com/video", "--cookies", str(cookies), "--format-id", "137+140", "--quality", "480", "-o", str(tmp_path / "out.mp4")]) == 0
    assert cookies.read_text() == "# Netscape HTTP Cookie File\n"
    assert seen["format"] == "137+140"
    assert "cookiesfrombrowser" not in seen
    assert not Path(seen["cookiefile"]).exists()


def test_formats_can_be_inspected_without_downloading_or_requiring_ffmpeg(monkeypatch, tmp_path):
    import json
    fake_downloader(monkeypatch, {"title": "Example", "formats": [{"format_id": "22", "height": 720, "ext": "mp4"}]})
    monkeypatch.setattr("onekit.tools.native.executable", lambda *_: pytest.fail("Format inspection needs no FFmpeg"))
    target = tmp_path / "formats.json"
    assert main(["download", "https://example.com/video", "--list-formats", "-o", str(target)]) == 0
    assert json.loads(target.read_text())["formats"][0]["format_id"] == "22"
