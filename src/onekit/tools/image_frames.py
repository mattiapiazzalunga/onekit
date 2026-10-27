# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io

from ..models import Artifact, OneKitError, Result
from .images import encode


def run(tool, files, options):
    from PIL import Image
    file = files[0]
    frames, durations = [], []
    with Image.open(io.BytesIO(file.data)) as image:
        count = getattr(image,'n_frames',1)
        if count>120 or image.width*image.height*count>40000000:
            raise OneKitError('Extract at most 120 GIF frames and 40 million total pixels.')
        for index in range(count):
            image.seek(index)
            # Pillow composes GIF disposal and partial-frame updates at seek time.
            frames.append(Artifact(f'{file.stem}-frame-{index+1:04d}.png',encode(image.convert('RGBA'),'png')))
            durations.append(image.info.get('duration',0))
    return Result(frames,details={'frames':len(frames),'durationsMs':durations})
