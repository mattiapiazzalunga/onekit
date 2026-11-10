# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Local YuNet detection and shared, bounded image redaction."""
import hashlib
import io
from importlib.resources import files as resources

from ..models import Artifact, OneKitError, Result
from ..limits import LIMITS

MODEL = {'name': 'yunet', 'sha256': '8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4'}
SOURCE = 'https://github.com/opencv/opencv_zoo/tree/f12e12798e8314f7c074a6656816c048dcc95b7a/models/face_detection_yunet'
SIZE = 640
REVIEW = 'Automatic detection can miss faces. Review every face before sharing; blur does not guarantee anonymity.'


def image_input(file):
    import numpy as np
    from PIL import Image, ImageOps
    with Image.open(io.BytesIO(file.data)) as source:
        if getattr(source, 'n_frames', 1) != 1 or source.width * source.height > LIMITS.max_face_pixels:
            raise OneKitError('Face blur supports single-frame images up to 16 million pixels.')
        image = ImageOps.exif_transpose(source).convert('RGB')
        width, height = image.size
        ratio = min(SIZE / width, SIZE / height)
        scaled = image.resize((max(1, round(width * ratio)), max(1, round(height * ratio))), Image.Resampling.BILINEAR)
        canvas = Image.new('RGB', (SIZE, SIZE))
        canvas.paste(scaled, (0, 0))
        pixels = np.asarray(canvas, dtype=np.float32)[..., ::-1].transpose(2, 0, 1)[None]
        return {'data': np.ascontiguousarray(pixels, dtype='<f4').tobytes(), 'shape': [1, 3, SIZE, SIZE],
                'width': width, 'height': height, 'ratio': ratio, 'model': MODEL}


def decode_predictions(raw, geometry):
    import numpy as np
    boxes = []
    ratio, width, height = geometry['ratio'], geometry['width'], geometry['height']
    for stride in (8, 16, 32):
        count = (SIZE // stride) ** 2
        values = {}
        for key, size in (('cls', 1), ('obj', 1), ('bbox', 4)):
            value = np.frombuffer(bytes(raw[f'{key}_{stride}']), dtype='<f4')
            if value.size != count * size or not np.isfinite(value).all():
                raise OneKitError('The face detector returned invalid results.')
            values[key] = value.reshape(count, size)
        scores = np.sqrt(np.clip(values['cls'][:, 0], 0, 1) * np.clip(values['obj'][:, 0], 0, 1))
        for index in np.flatnonzero(scores >= .6):
            index = int(index)
            dx, dy, dw, dh = values['bbox'][index]
            cx = (index % (SIZE // stride) + float(dx)) * stride / ratio
            cy = (index // (SIZE // stride) + float(dy)) * stride / ratio
            bw, bh = float(np.exp(np.clip(dw, -20, 20))) * stride / ratio, float(np.exp(np.clip(dh, -20, 20))) * stride / ratio
            left, top, right, bottom = max(0., cx - bw / 2), max(0., cy - bh / 2), min(width, cx + bw / 2), min(height, cy + bh / 2)
            if right > left and bottom > top:
                boxes.append({'x': left, 'y': top, 'width': right - left, 'height': bottom - top, 'score': float(scores[index])})
    selected = []
    for box in sorted(boxes, key=lambda value: value['score'], reverse=True)[:LIMITS.max_face_candidates]:
        def overlaps(other):
            area = max(0, min(box['x'] + box['width'], other['x'] + other['width']) - max(box['x'], other['x'])) * max(0, min(box['y'] + box['height'], other['y'] + other['height']) - max(box['y'], other['y']))
            return area / max(1e-6, box['width'] * box['height'] + other['width'] * other['height'] - area) > .3
        if not any(overlaps(other) for other in selected):
            selected.append(box)
        if len(selected) == LIMITS.max_faces:
            break
    return selected


def detect(file):
    import numpy as np
    import onnxruntime as ort
    ort.disable_telemetry_events()
    model = resources('onekit').joinpath('data/yunet.onnx').read_bytes()
    if hashlib.sha256(model).hexdigest() != MODEL['sha256']:
        raise OneKitError('The face detection model failed its integrity check.')
    session = ort.InferenceSession(model, providers=['CPUExecutionProvider'])
    geometry = image_input(file)
    outputs = session.run(None, {session.get_inputs()[0].name: np.frombuffer(geometry['data'], dtype='<f4').reshape(geometry['shape'])})
    raw = {item.name: np.asarray(value, dtype='<f4').tobytes() for item, value in zip(session.get_outputs(), outputs)}
    return decode_predictions(raw, geometry)


def run(tool, files, options):
    import math
    from PIL import Image, ImageFilter, ImageOps
    from ..execution import current_context
    file = files[0]
    geometry = image_input(file)
    reader = current_context().face_reader
    boxes = reader(file) if reader else detect(file)
    if not isinstance(boxes, list) or len(boxes) > LIMITS.max_faces:
        raise OneKitError('The face detector returned invalid results.')
    if not boxes:
        raise OneKitError('No faces were detected. Use manual image redaction and review the image before sharing.')
    with Image.open(io.BytesIO(file.data)) as source:
        image = ImageOps.exif_transpose(source).convert('RGBA')
    image.info.clear()
    image.getexif().clear()
    original = image.copy()
    for box in boxes:
        try:
            x, y, width, height = (float(box[key]) for key in ('x', 'y', 'width', 'height'))
            if not all(math.isfinite(value) for value in (x, y, width, height)) or width <= 0 or height <= 0:
                raise ValueError()
        except (KeyError, TypeError, ValueError) as error:
            raise OneKitError('The face detector returned invalid results.') from error
        region = (max(0, math.floor(x - width * .2)), max(0, math.floor(y - height * .25)),
                  min(geometry['width'], math.ceil(x + width * 1.2)), min(geometry['height'], math.ceil(y + height * 1.2)))
        if region[2] <= region[0] or region[3] <= region[1]:
            raise OneKitError('The face detector returned invalid results.')
        crop = original.crop(region)
        blurred = crop.filter(ImageFilter.GaussianBlur(max(12, min(width, height) * .22)))
        blurred.putalpha(crop.getchannel('A'))
        image.paste(blurred, region[:2])
    stream = io.BytesIO()
    image.save(stream, format='PNG')
    return Result([Artifact(file.stem + '-faces-blurred.png', stream.getvalue())], [REVIEW], {'faces': len(boxes)})
