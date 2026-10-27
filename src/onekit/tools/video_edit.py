# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
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
    if tool_id == 'video-to-frames':
        start = number(options,'start',0,0,86400)
        duration = number(options,'duration',5,.1,30)
        all_frames = str(options.get('all_frames', 'false')).lower() == 'true'
        fps = None if all_frames else number(options,'fps',1,.1,240)
        width = number(options,'width',1280,64,1920,integer=True)
        if fps is not None and math.ceil(duration*fps)>120:
            raise OneKitError('Extract at most 120 frames; reduce duration or frame rate.')
        filters = f'scale={width}:-1' if all_frames else f'fps={fps:g}:round=up,scale={width}:-1'
        # The extra frame detects overflow instead of silently truncating an
        # all-frames extraction. No FPS filter may drop or duplicate frames.
        return ['-ss',str(start),'-t',str(duration),'-map','0:v:0','-an','-vf',filters,
                *(['-fps_mode','passthrough'] if all_frames else []),'-frames:v',str(121 if all_frames else 120),'-c:v','bmp','-threads','1']
    if tool_id in ("video-extract-audio", "mp4-to-mp3"):
        if not audio:
            raise OneKitError("This video has no audio stream.")
        return ["-map", "0:a:0", "-vn", "-c:a", "libmp3lame", "-b:a", "192k"]
    if tool_id == "video-mute":
        return ["-map", "0:v:0", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-movflags", "+faststart"]
    if tool_id == "video-trim":
        start = number(options, "start", 0, 0, 86400)
        end = number(options, "end", 5, 0, 86400)
        if end <= start:
            raise OneKitError("End time must be after start time.")
        return ["-ss", str(start), "-t", str(end-start), "-map", "0:v:0", "-map", "0:a:0?", "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart"]
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
    elif tool_id == "video-speed":
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
    else:
        raise OneKitError("Unknown video operation.")
    return result + ["-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart"]


def source_frame_plan(probe):
    """Describe source cadence without confusing it with resampling."""
    video = next((row for row in probe.get('streams', []) if row.get('codec_type') == 'video'
                  and not row.get('disposition', {}).get('attached_pic')), None)
    if video is None:
        raise OneKitError('This file does not contain a video stream.')
    try:
        duration = float(video.get('duration') or probe.get('format', {}).get('duration', 0))
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError
    except (ValueError, TypeError):
        raise OneKitError('Cannot determine the source frame rate and duration.') from None
    fps = 0
    for key in ('avg_frame_rate', 'r_frame_rate'):
        try:
            numerator, _, denominator = str(video.get(key, '0')).partition('/')
            candidate = float(numerator) / float(denominator or 1)
            if math.isfinite(candidate) and candidate > 0:
                fps = candidate
                break
        except (ValueError, TypeError, ZeroDivisionError):
            continue
    if not fps:
        raise OneKitError('Cannot determine the source frame rate and duration.')
    try:
        count = int(video.get('nb_frames', 0))
    except (ValueError, TypeError):
        count = 0
    return {'fps': fps, 'duration': duration, 'frames': count if count > 0 else math.ceil(duration*fps),
            'estimated': count <= 0}


def frames_result(file, frames):
    """Encode engine-provided lossless frames through the shared image encoder."""
    from PIL import Image

    from .images import encode
    if not 1 <= len(frames) <= 120 or sum(map(len,frames))>128*1024*1024:
        raise OneKitError('Extract between 1 and 120 frames, up to 128 MiB of decoded frame data.')
    artifacts = []
    for index,data in enumerate(frames,1):
        with Image.open(io.BytesIO(data)) as image:
            if image.format != 'BMP' or image.width*image.height>40000000:
                raise OneKitError('The video engine returned an invalid frame image.')
            artifacts.append(Artifact(f'{file.stem}-frame-{index:04d}.png',encode(image,'png')))
    return Result(artifacts,details={'frames':len(artifacts)})


def run(tool, files, options):
    with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
        work = Path(directory)
        source = work / f"input.{files[0].kind}"
        source.write_bytes(files[0].data)
        probe = json.loads(command("ffprobe", ["-v", "error", "-protocol_whitelist", "file,pipe", "-show_streams", "-show_format", "-of", "json", source.name], directory, timeout=30))
        streams = probe.get("streams", [])
        if not any(row.get("codec_type") == "video" and not row.get("disposition", {}).get("attached_pic") for row in streams):
            raise OneKitError("The input must contain a video stream.")
        args = arguments(tool.id, options, audio=any(row.get("codec_type") == "audio" for row in streams))
        if tool.id == "video-trim":
            duration = float(probe.get("format", {}).get("duration", 0))
            if not math.isfinite(duration) or duration <= 0 or float(options.get("start", 0)) >= duration or float(options.get("end", 5)) > duration+.05:
                raise OneKitError("Choose start and end times within the video duration.")
        target = 'frame-%04d.bmp' if tool.id == 'video-to-frames' else f"output.{tool.produces}"
        command("ffmpeg", ["-nostdin", "-hide_banner", "-loglevel", "error", "-protocol_whitelist", "file,pipe", "-i", source.name,
                           "-map_metadata", "-1", *args, "-fs", str(128*1024*1024), target], directory, timeout=600)
        if tool.id == 'video-to-frames':
            frames = sorted(work.glob('frame-*.bmp'))
            if not frames:
                raise OneKitError('No frames were extracted. Choose a start time within the video.')
            return frames_result(files[0],[frame.read_bytes() for frame in frames])
        data = (work / target).read_bytes()
        if tool.id == "video-compress" and len(data) >= len(files[0].data):
            return Result([files[0]], ["The original is already smaller; returned the unchanged original."],
                          details={"inputBytes": len(files[0].data), "outputBytes": len(files[0].data), "originalRetained": True})
        return Result([Artifact(f"{files[0].stem}-{tool.id.removeprefix('video-')}.{tool.produces}", data)],
                      details={"inputBytes": len(files[0].data), "outputBytes": len(data)})
