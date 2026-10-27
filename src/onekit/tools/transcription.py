# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import json
import re
import tempfile
from pathlib import Path

from ..models import Artifact, OneKitError, Result


def recognition_parameters(language='auto'):
    if not isinstance(language, str) or language != 'auto' and not re.fullmatch(r'[a-z]{2,3}', language):
        raise OneKitError('Language must be auto or a lowercase language code such as it or en.')
    return {'model': 'tiny', 'language': None if language == 'auto' else language,
            'beam_size': 5, 'condition_on_previous_text': False, 'sample_rate': 16000}


def run(tool, files, options):
    from ..execution import current_context
    language = options.get("language", "auto")
    parameters = recognition_parameters(language)
    reader = current_context().speech_reader
    if reader:
        details = reader(files[0], language)
        return transcript_result(files[0], details)
    from faster_whisper import WhisperModel
    with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
        source = Path(directory) / f"input.{files[0].kind}"
        source.write_bytes(files[0].data)
        try:
            model = WhisperModel(parameters['model'], device="cpu", compute_type="int8")
            segments, info = model.transcribe(str(source), language=parameters['language'],
                                              beam_size=parameters['beam_size'],
                                              condition_on_previous_text=parameters['condition_on_previous_text'])
            rows = [{"start": row.start, "end": row.end, "text": row.text.strip()} for row in segments]
        except Exception as exc:
            raise OneKitError("Transcription failed. Check the audio and language; first use requires downloading the Whisper tiny model.") from exc
    details = {"language": info.language, "segments": rows}
    return transcript_result(files[0], details)


def transcript_result(file, details):
    transcript = "\n".join(row["text"] for row in details["segments"]).strip() + "\n"
    return Result([Artifact(f"{file.stem}.txt", transcript.encode()),
                   Artifact(f"{file.stem}-transcript.json", json.dumps(details, ensure_ascii=False, indent=2).encode())],
                  details=details)
