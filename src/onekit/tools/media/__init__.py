# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import json
import tempfile
from pathlib import Path

from ...models import Artifact, OneKitError, Result
from ..native import command


def conversion_arguments(group, options):
    """Validate a media conversion request and build engine-independent options."""
    format = options.get("format", "mp4" if group == "video" else "wav")
    if format not in ("mp4", "webm", "mkv", "mov", "avi", "gif", "mp3", "wav", "flac", "ogg", "aac", "m4a"):
        raise OneKitError("Choose a supported audio or video output format.")
    arguments = []
    if group == "audio" and format != "mp4":
        arguments += ["-vn"]
    if options.get("codec"):
        codec = str(options["codec"])
        if not codec.replace("_", "").isalnum():
            raise OneKitError("Invalid codec name.")
        arguments += ["-c:a" if group == "audio" else "-c:v", codec]
    if options.get("bitrate"):
        import re
        bitrate = str(options["bitrate"])
        if not re.fullmatch(r"[1-9][0-9]{0,5}[kKmM]?", bitrate):
            raise OneKitError("Invalid bitrate.")
        arguments += ["-b:a" if group == "audio" else "-b:v", bitrate]
    return {"format": format, "args": arguments}


def run(tool, files, options):
    plan = conversion_arguments(tool.group, options)
    format = plan["format"]
    with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
        work = Path(directory)
        source = work / f"input.{files[0].kind or 'bin'}"
        source.write_bytes(files[0].data)
        report = json.loads(command("ffprobe", ["-v", "error", "-protocol_whitelist", "file,pipe", "-show_entries", "stream=codec_type:stream_disposition=attached_pic", "-of", "json", source.name], directory, timeout=30))
        streams = report.get("streams", [])
        video = any(stream.get("codec_type") == "video" and not stream.get("disposition", {}).get("attached_pic") for stream in streams)
        audio = any(stream.get("codec_type") == "audio" for stream in streams)
        if tool.group == "video" and not video or tool.group == "audio" and (not audio or video):
            raise OneKitError(f"The input does not contain a supported {tool.group} stream for this tool.")
        arguments = ["-nostdin", "-hide_banner", "-loglevel", "error", "-protocol_whitelist", "file,pipe", "-i", source.name, "-map_metadata", "-1"]
        arguments += plan["args"]
        arguments += ["-fs", str(128 * 1024 * 1024), f"output.{format}"]
        command("ffmpeg", arguments, directory, timeout=300)
        return Result([Artifact(f"{files[0].stem}.{format}", (work / f"output.{format}").read_bytes())])
