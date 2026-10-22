# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Opt-in network video downloads, isolated from the offline tools."""
import json
import re
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from ..models import Artifact, OneKitError, Result


def validate_url(value):
    url = value.strip()
    try:
        parsed = urlsplit(url)
        valid = parsed.scheme in ("http", "https") and parsed.hostname and not parsed.username and not parsed.password
        valid = valid and (parsed.port is None or 0 < parsed.port < 65536)
    except ValueError:
        valid = False
    if not valid or any(character.isspace() or ord(character) < 32 for character in url):
        raise OneKitError("Enter one HTTP or HTTPS video URL without credentials.")
    return url


def run(tool, files, options):
    url = validate_url(files[0].text())
    quality = options.get("quality", "best")
    if quality not in ("best", "360", "480", "720", "1080", "1440", "2160"):
        raise OneKitError("Video quality must be best, 360, 480, 720, 1080, 1440 or 2160.")
    cookies, browser = options.get("cookies"), options.get("cookies_from_browser")
    if cookies and browser:
        raise OneKitError("Choose either a cookies file or cookies from a local browser.")
    if browser and browser not in ("firefox", "chrome", "edge", "chromium", "brave", "opera", "vivaldi", "safari"):
        raise OneKitError("Choose a supported browser for local login cookies.")
    if cookies and (not isinstance(cookies, str) or not Path(cookies).is_file()):
        raise OneKitError("The cookies file does not exist. Use a Netscape-format cookies file.")
    format_id = options.get("format_id")
    if format_id and (not isinstance(format_id, str) or not re.fullmatch(r"[a-zA-Z0-9_.-]+(?:\+[a-zA-Z0-9_.-]+)?", format_id)):
        raise OneKitError("Use a format ID or VIDEO_ID+AUDIO_ID.")
    referer = validate_url(options["referer"]) if options.get("referer") else None
    from yt_dlp import YoutubeDL

    from .native import executable
    ffmpeg = executable("ffmpeg") if not options.get("list_formats") else None
    limit = options.get("_max_expanded_bytes", 128 * 1024 * 1024)

    transferred = {}
    def check_progress(progress):
        transferred[progress.get("filename", "video")] = progress.get("downloaded_bytes", 0)
        if sum(transferred.values()) > limit:
            raise OneKitError("Video exceeds the 128 MiB download limit.")

    selector = "bv*+ba/b" if quality == "best" else f"bv*[height<={quality}]+ba/b[height<={quality}]"
    with tempfile.TemporaryDirectory(prefix="onekit-video-") as temporary:
        settings = {
            "outtmpl": str(Path(temporary) / "video.%(ext)s"),
            "format": format_id or selector,
            "noplaylist": True, "playlistend": 1,
            "max_filesize": limit, "socket_timeout": 30, "retries": 2,
            "quiet": True, "noprogress": True, "restrictfilenames": True,
            "progress_hooks": [check_progress], "merge_output_format": "mp4/mkv",
            "js_runtimes": {"deno": {}, "node": {}},
        }
        if ffmpeg:
            settings["ffmpeg_location"] = str(ffmpeg)
        if cookies:
            # yt-dlp writes updated cookies on exit; work on a private temporary copy.
            import shutil
            private_cookies = Path(temporary) / "cookies.txt"
            shutil.copyfile(cookies, private_cookies)
            settings["cookiefile"] = str(private_cookies)
        if browser:
            settings["cookiesfrombrowser"] = (browser,)
        if referer:
            settings["http_headers"] = {"Referer": referer}
        with YoutubeDL(settings) as downloader:
            info = downloader.extract_info(url, download=False)
            if not info or info.get("_type") in ("playlist", "multi_video"):
                raise OneKitError("Provide a link to one video, rather than a playlist or profile.")
            if info.get("is_live"):
                raise OneKitError("Live streams are not supported. Provide a completed video.")
            if options.get("list_formats"):
                formats = [{key: value.get(key) for key in ("format_id", "ext", "width", "height", "fps", "vcodec", "acodec", "filesize", "filesize_approx")} for value in info.get("formats", [])]
                return Result([Artifact("formats.json", json.dumps({"title": info.get("title"), "formats": formats}, indent=2).encode())])
            downloader.process_ie_result(info, download=True)
        outputs = [path for path in Path(temporary).glob("video.*") if path.suffix not in (".part", ".ytdl")]
        if len(outputs) != 1 or not outputs[0].stat().st_size:
            raise OneKitError("No video downloaded. The video may exceed 128 MiB or be unavailable.")
        if outputs[0].stat().st_size > limit:
            raise OneKitError("Video exceeds the 128 MiB download limit.")
        return Result([Artifact(outputs[0].name, outputs[0].read_bytes())], warnings=[tool.note])
