# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import json
import math
import tempfile
from pathlib import Path

from ..models import Artifact, OneKitError, Result
from .native import command


def number(options, key, default, low, high, *, integer=False):
    value = options.get(key, default)
    try:
        result = float(value)
    except (ValueError, TypeError):
        raise OneKitError(f"{key} must be a number between {low} and {high}.") from None
    if isinstance(value, bool) or not math.isfinite(result) or not low <= result <= high or integer and result != int(result):
        raise OneKitError(f"{key} must be {'an integer' if integer else 'a number'} between {low} and {high}.")
    return int(result) if integer else result


def arguments(tool_id, options, *, audio=True):
    """Validated FFmpeg arguments, for media processing."""
    if tool_id == "video-to-gif":
        start = number(options, "start", 0, 0, 86400)
        duration = number(options, "duration", 5, .1, 30)
        fps = number(options, "fps", 12, 1, 30, integer=True)
        width = number(options, "width", 480, 64, 1280, integer=True)
        filters = (f"[0:v:0]fps={fps},scale={width}:-1:flags=lanczos,split[a][b];"
                   "[a]palettegen[p];[b][p]paletteuse[vout]")
        return ["-ss", str(start), "-t", str(duration), "-an", "-filter_complex", filters, "-map", "[vout]", "-loop", "0"]
    result = ["-map", "0:v:0", "-map", "0:a:0?", "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p"]
    if tool_id == "video-compress":
        level = options.get("compression_level", "balanced")
        if level not in ("light", "balanced", "maximum"):
            raise OneKitError("Choose light, balanced or maximum compression.")
        result += ["-crf", {"light": "23", "balanced": "28", "maximum": "34"}[level], "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2"]
    else:
        speed = number(options, "speed", 2, .25, 4)
        factors, remaining = [], speed
        while remaining > 2:
            factors.append("atempo=2")
            remaining /= 2
        while remaining < .5:
            factors.append("atempo=0.5")
            remaining /= .5
        factors.append(f"atempo={remaining:g}")
        result += ["-crf", "20", "-vf", f"setpts=(PTS-STARTPTS)/{speed:g},pad=ceil(iw/2)*2:ceil(ih/2)*2"]
        if audio:
            result += ["-af", "asetpts=PTS-STARTPTS," + ",".join(factors)]
    return result + ["-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart"]


def run(tool, files, options):
    with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
        work = Path(directory)
        source = work / f"input.{files[0].kind}"
        source.write_bytes(files[0].data)
        probe = json.loads(command("ffprobe", ["-v", "error", "-protocol_whitelist", "file,pipe", "-show_streams", "-of", "json", source.name], directory, timeout=30))
        streams = probe.get("streams", [])
        if not any(row.get("codec_type") == "video" and not row.get("disposition", {}).get("attached_pic") for row in streams):
            raise OneKitError("The input must contain a video stream.")
        args = arguments(tool.id, options, audio=any(row.get("codec_type") == "audio" for row in streams))
        target = f"output.{tool.produces}"
        command("ffmpeg", ["-nostdin", "-hide_banner", "-loglevel", "error", "-protocol_whitelist", "file,pipe", "-i", source.name,
                           "-map_metadata", "-1", *args, "-fs", str(128*1024*1024), target], directory, timeout=600)
        data = (work / target).read_bytes()
        if tool.id == "video-compress" and len(data) >= len(files[0].data):
            return Result([files[0]], ["The original is already smaller; returned the unchanged original."],
                          details={"inputBytes": len(files[0].data), "outputBytes": len(files[0].data), "originalRetained": True})
        return Result([Artifact(f"{files[0].stem}-{tool.id.removeprefix('video-')}.{tool.produces}", data)],
                      details={"inputBytes": len(files[0].data), "outputBytes": len(data)})
