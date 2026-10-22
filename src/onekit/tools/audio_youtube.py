# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Local audio extraction for authorized use; availability varies by source."""
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from ..models import Artifact, OneKitError, Result
from .native import executable
from .video_download import validate_url


def run(tool, files, options):
    url = validate_url(files[0].text())
    host = urlsplit(url).hostname.lower()
    if not (host == "youtu.be" or host == "youtube.com" or host.endswith(".youtube.com")):
        raise OneKitError("Enter a YouTube video URL. Use Download audio for other direct audio sources.")
    format, quality = options.get("format", "mp3"), str(options.get("quality", "192"))
    if format not in ("original", "mp3") or quality not in ("64", "128", "192", "256", "320"):
        raise OneKitError("Choose original audio or MP3 at 64, 128, 192, 256 or 320 kbps.")
    from yt_dlp import YoutubeDL
    limit = 128 * 1024 * 1024
    def progress(event):
        if event.get("downloaded_bytes", 0) > limit:
            raise OneKitError("The source exceeds the 128 MiB download limit.")
    with tempfile.TemporaryDirectory(prefix="onekit-audio-") as directory:
        settings = {"outtmpl": str(Path(directory, "audio.%(ext)s")), "format": "bestaudio/best", "noplaylist": True,
                    "playlistend": 1, "max_filesize": limit, "socket_timeout": 30, "retries": 2,
                    "quiet": True, "noprogress": True, "restrictfilenames": True, "progress_hooks": [progress],
                    "ffmpeg_location": executable("ffmpeg"), "js_runtimes": {"node": {"path": executable("node")}},
                    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "best" if format == "original" else "mp3", "preferredquality": quality}]}
        with YoutubeDL(settings) as downloader:
            info = downloader.extract_info(url, download=False)
            if not info or info.get("_type") in ("playlist", "multi_video") or info.get("is_live"):
                raise OneKitError("Choose one completed video, not a playlist, channel or live stream.")
            if info.get("has_drm"):
                raise OneKitError("DRM-protected content is not supported.")
            downloader.process_ie_result(info, download=True)
        outputs = [path for path in Path(directory).iterdir() if path.suffix.lower() in (".mp3", ".m4a", ".opus", ".ogg", ".aac", ".wav", ".flac", ".webm")]
        if len(outputs) != 1 or not 0 < outputs[0].stat().st_size <= limit:
            raise OneKitError("No audio downloaded within the 128 MiB limit. The source may be unavailable or restricted.")
        return Result([Artifact(outputs[0].name, outputs[0].read_bytes())], warnings=[tool.note, *(["The selected MP3 bitrate cannot restore detail absent from the source."] if format == "mp3" else [])],
                      details={"format": format, "mp3_bitrate_kbps": int(quality) if format == "mp3" else None, "source_title": str(info.get("title", ""))[:300]})
