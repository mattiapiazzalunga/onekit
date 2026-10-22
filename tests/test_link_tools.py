# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image

from onekit import Artifact, OneKitError, execute
from onekit.cli import main
from onekit.tools import link_tools


def image_bytes():
    stream = io.BytesIO()
    image = Image.new("RGBA", (2, 3))
    image.putdata([(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (255, 255, 0, 255), (255, 0, 255, 128), (0, 255, 255, 0)])
    image.save(stream, format="PNG")
    return stream.getvalue()


@pytest.fixture
def source_server():
    image = image_bytes()
    wav = b"RIFF" + (40).to_bytes(4, "little") + b"WAVEfmt " + b"test audio bytes"
    requests = []
    class Handler(BaseHTTPRequestHandler):
        def do_HEAD(self):
            self.respond(False)
        def do_GET(self):
            self.respond(True)
        def respond(self, body):
            requests.append((self.command, self.path))
            path = self.path.split("?", 1)[0]
            if path in ("/redirect", "/loop"):
                self.send_response(302)
                self.send_header("Location", "/final" if path == "/redirect" else "/loop")
                self.end_headers()
                return
            if path == "/head-unsupported" and not body:
                self.send_response(405)
                self.end_headers()
                return
            self.send_response(200)
            data, type = (image, "image/png") if path == "/image.png" else (wav, "audio/wav") if path == "/audio.wav" else (b'<html><meta property="og:image" content="/image.png"><audio src="/audio.wav"></audio></html>', "text/html") if path == "/page" else (b"not audio or image", "text/plain")
            self.send_header("Content-Type", type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            if body:
                self.wfile.write(data)
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", image, wav, requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


@pytest.mark.parametrize("kind", ["audio", "image"])
def test_downloads_original_bytes_from_file_and_page_without_a_proxy(source_server, kind):
    base, image, audio, requests = source_server
    direct = "/image.png" if kind == "image" else "/audio.wav"
    for path in (direct, "/page"):
        result = execute(kind + "-download", [Artifact("url.txt", (base + path).encode())])
        assert result.files[0].data == (image if kind == "image" else audio)
        assert result.details["original_bytes"]
    assert all(method == "GET" for method, _ in requests)


def test_url_inspector_records_real_redirects_headers_queries_and_head_fallback(source_server):
    base, _, _, requests = source_server
    report = execute("url-inspect", [Artifact("url.txt", (base + "/redirect?x=1&x=2#part").encode())]).details
    assert [hop["status"] for hop in report["hops"]] == [302, 200]
    assert report["final_url"] == base + "/final"
    assert report["redirect_chain_complete"]
    assert report["components"]["query_parameters"] == [{"name": "x", "value": "1"}, {"name": "x", "value": "2"}]
    assert report["components"]["fragment"] == "part"
    assert report["hops"][-1]["headers"]["x-content-type-options"] == "nosniff"
    report = execute("url-inspect", [Artifact("url.txt", (base + "/head-unsupported").encode())]).details
    assert report["method"].startswith("GET")
    assert ("HEAD", "/head-unsupported") in requests and ("GET", "/head-unsupported") in requests


def test_url_loop_returns_an_explicit_partial_report_and_invalid_download_is_rejected(source_server):
    base, *_ = source_server
    report = execute("url-inspect", [Artifact("url.txt", (base + "/loop").encode())]).details
    assert not report["network_available"] and not report["redirect_chain_complete"]
    assert any("loop" in item for item in report["limitations"])
    with pytest.raises(OneKitError, match="supported audio"):
        execute("audio-download", [Artifact("url.txt", (base + "/final").encode())])


@pytest.mark.parametrize("tool", ["audio-download", "image-download", "url-inspect", "audio-youtube-download"])
@pytest.mark.parametrize("url", ["file:///secret", "https://user:password@example.com/path", "javascript:alert(1)", "https://example.com/a\nb"])
def test_invalid_urls_are_rejected_before_network_access(tool, url, monkeypatch):
    monkeypatch.setattr(link_tools, "request_chain", lambda *args: pytest.fail("Invalid URL reached the network"))
    with pytest.raises(OneKitError):
        execute(tool, [Artifact("url.txt", url.encode())])


@pytest.mark.parametrize("angle", [0, 90, 180, 270])
@pytest.mark.parametrize("flip", ["none", "horizontal", "vertical", "both"])
def test_rotate_and_reflect_asymmetric_pixels_and_transparency(angle, flip):
    source = image_bytes()
    result = execute("image-rotate-flip", [Artifact("image.png", source)], {"angle": angle, "flip": flip})
    image = Image.open(io.BytesIO(result.files[0].data))
    original = list(Image.open(io.BytesIO(source)).get_flattened_data())
    width, height = (3, 2) if angle % 180 else (2, 3)
    assert image.size == (width, height)
    for y in range(3):
        for x in range(2):
            target = {0: (x, y), 90: (2-y, x), 180: (1-x, 2-y), 270: (y, 1-x)}[angle]
            tx, ty = target
            if flip in ("horizontal", "both"):
                tx = width - 1 - tx
            if flip in ("vertical", "both"):
                ty = height - 1 - ty
            assert image.getpixel((tx, ty)) == original[y * 2 + x]
    assert not image.info.get("exif")


def test_rotation_rejects_animation_and_unsupported_angles():
    frames = [Image.new("RGB", (2, 2), color) for color in ("red", "blue")]
    stream = io.BytesIO()
    frames[0].save(stream, format="GIF", save_all=True, append_images=frames[1:])
    with pytest.raises(OneKitError, match="single-frame"):
        execute("image-rotate-flip", [Artifact("animated.gif", stream.getvalue())])
    with pytest.raises(OneKitError, match="rotation"):
        execute("image-rotate-flip", [Artifact("image.png", image_bytes())], {"angle": 45})


@pytest.mark.parametrize("quality", ["64", "128", "192", "256", "320"])
@pytest.mark.parametrize("format", ["original", "mp3"])
def test_youtube_audio_selectors_postprocessing_and_limits(quality, format, monkeypatch):
    captured = {}
    class Downloader:
        def __init__(self, settings):
            captured.update(settings)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def extract_info(self, url, download):
            assert url.startswith("https://www.youtube.com/") and not download
            return {"title": "Owned sample", "id": "sample"}
        def process_ie_result(self, info, download):
            extension = "mp3" if format == "mp3" else "opus"
            Path(captured["outtmpl"].replace("%(ext)s", extension)).write_bytes(b"audio output fixture")
    monkeypatch.setitem(sys.modules, "yt_dlp", SimpleNamespace(YoutubeDL=Downloader))
    monkeypatch.setattr("onekit.tools.audio_youtube.executable", lambda name: "/local/" + name)
    result = execute("audio-youtube-download", [Artifact("url.txt", b"https://www.youtube.com/watch?v=owned")], {"format": format, "quality": quality})
    assert result.files[0].name.endswith(".mp3" if format == "mp3" else ".opus")
    assert captured["format"] == "bestaudio/best"
    assert captured["postprocessors"][0]["preferredquality"] == quality
    assert captured["noplaylist"] and captured["max_filesize"] == 128 * 1024 * 1024
    assert "remote_components" not in captured and "cookiefile" not in captured
    with pytest.raises(OneKitError, match="128 MiB"):
        captured["progress_hooks"][0]({"downloaded_bytes": 129 * 1024 * 1024})


def test_cli_url_downloader_and_url_inspection(source_server, tmp_path):
    base, image, *_ = source_server
    target = tmp_path / "image.png"
    assert main(["run", "image-download", "--url", base + "/image.png", "-o", str(target)]) == 0
    assert target.read_bytes() == image
    target = tmp_path / "report.json"
    assert main(["run", "url-inspect", "--url", base + "/redirect", "-o", str(target)]) == 0
    assert json.loads(target.read_text(encoding="utf-8"))["redirect_chain_complete"]
