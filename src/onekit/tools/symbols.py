# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""ZXing input preparation and settings shared by processing callers."""
import io

from ..models import OneKitError


def input_image(file, max_pixels=None):
    from PIL import Image, ImageOps
    with Image.open(io.BytesIO(file.data)) as source:
        if max_pixels is not None and source.width*source.height > max_pixels:
            raise OneKitError(f'Symbol images must contain at most {max_pixels//1000000} million pixels.')
        image = ImageOps.exif_transpose(source).convert('RGBA')
        return Image.alpha_composite(Image.new('RGBA', image.size, 'white'), image).convert('RGB')


def pixel_input(file, max_pixels=None):
    image = input_image(file, max_pixels)
    return {'data': image.convert('RGBA').tobytes(), 'width': image.width, 'height': image.height}


def reader_parameters(kind):
    if kind not in ('qr', 'linear'):
        raise OneKitError('Choose QR or linear barcode reading.')
    return {'formats': ['QRCode'] if kind == 'qr' else ['Code128', 'Code39', 'EAN13', 'EAN8', 'UPCA', 'ITF'],
            'try_rotate': True, 'try_invert': True}


def read_native(image, kind):
    import zxingcpp
    settings = reader_parameters(kind)
    return zxingcpp.read_barcodes(image,
                                  formats=tuple(getattr(zxingcpp.BarcodeFormat, name) for name in settings['formats']),
                                  try_rotate=settings['try_rotate'], try_invert=settings['try_invert'])
