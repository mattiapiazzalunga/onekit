# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import json
import re
import tempfile
from pathlib import Path

from ..models import Artifact, OneKitError, Result


def run(tool, files, options):
    from faster_whisper import WhisperModel
    language = options.get("language", "auto")
    if not isinstance(language, str) or language != "auto" and not re.fullmatch(r"[a-z]{2,3}", language):
        raise OneKitError("Language must be auto or a lowercase language code such as it or en.")
    with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
        source = Path(directory) / f"input.{files[0].kind}"
        source.write_bytes(files[0].data)
        try:
            model = WhisperModel("tiny", device="cpu", compute_type="int8")
            segments, info = model.transcribe(str(source), language=None if language == "auto" else language,
                                              beam_size=5, condition_on_previous_text=False)
            rows = [{"start": row.start, "end": row.end, "text": row.text.strip()} for row in segments]
        except Exception as exc:
            raise OneKitError("Transcription failed. Check the audio and language; first use requires downloading the Whisper tiny model.") from exc
    transcript = "\n".join(row["text"] for row in rows).strip() + "\n"
    details = {"language": info.language, "segments": rows}
    return Result([Artifact(f"{files[0].stem}.txt", transcript.encode()),
                   Artifact(f"{files[0].stem}-transcript.json", json.dumps(details, ensure_ascii=False, indent=2).encode())],
                  details=details)
