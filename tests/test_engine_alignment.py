# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Inference hosts must consume exactly the same public preprocessing contract."""
import io
import sys
from types import SimpleNamespace

import pytest
from PIL import Image

from onekit import Artifact, execute
from onekit.models import OneKitError
from onekit.tools import background, symbols, transcription


def test_u2net_native_and_supplied_inference_use_identical_tensor_and_mask(monkeypatch):
    np = pytest.importorskip('numpy')
    image = Image.new('RGB', (37, 23), (90, 160, 230))
    stream = io.BytesIO()
    image.save(stream, format='PNG')
    file = Artifact('subject.png', stream.getvalue())
    inputs = background.foreground_input(file)
    tensor = np.frombuffer(inputs['data'], dtype='<f4').reshape(inputs['shape'])
    assert tensor.dtype == np.float32
    np.testing.assert_array_equal(tensor, background.prepare_foreground(image))
    prediction = np.linspace(0, 1, 320*320, dtype=np.float32).reshape(1, 1, 320, 320)

    class Session:
        def __init__(self, path, providers):
            assert providers == ['CPUExecutionProvider']

        def get_inputs(self):
            return [SimpleNamespace(name='input')]

        def run(self, names, values):
            np.testing.assert_array_equal(values['input'], tensor)
            return [prediction]

    monkeypatch.setitem(sys.modules, 'onnxruntime', SimpleNamespace(InferenceSession=Session))
    monkeypatch.setitem(sys.modules, 'pooch', SimpleNamespace(
        retrieve=lambda **kwargs: 'verified-model.onnx', os_cache=lambda name: name))
    native = background.foreground_mask(image)
    supplied = Image.open(io.BytesIO(background.foreground_output(file, prediction.tobytes())))
    np.testing.assert_array_equal(np.asarray(native), np.asarray(supplied))
    assert inputs['model']['sha256'] == background.MODEL['sha256']


def test_u2net_invalid_predictions_are_not_accepted():
    np = pytest.importorskip('numpy')
    with pytest.raises(ValueError):
        background.prediction_mask(np.full((320, 320), np.nan), (20, 20))
    with pytest.raises(ValueError):
        background.prediction_mask(np.zeros(2), (20, 20))
    assert not np.asarray(background.prediction_mask(np.zeros((320, 320)), (20, 20))).any()


def test_speech_contract_exposes_the_native_model_and_decoding_parameters():
    settings = transcription.recognition_parameters('it')
    assert settings == {'model': 'tiny', 'language': 'it', 'beam_size': 5,
                        'condition_on_previous_text': False, 'sample_rate': 16000}
    assert transcription.recognition_parameters()['language'] is None
    with pytest.raises(OneKitError):
        transcription.recognition_parameters('it; invalid')


def test_native_symbol_reader_consumes_the_shared_detection_settings(monkeypatch):
    calls = []
    formats = {name: name for name in symbols.reader_parameters('linear')['formats']}
    formats['QRCode'] = 'QRCode'
    monkeypatch.setitem(sys.modules, 'zxingcpp', SimpleNamespace(
        BarcodeFormat=SimpleNamespace(**formats),
        read_barcodes=lambda image, **options: calls.append(options)))
    symbols.read_native(None, 'qr')
    symbols.read_native(None, 'linear')
    for kind, options in zip(('qr', 'linear'), calls, strict=True):
        settings = symbols.reader_parameters(kind)
        assert options['formats'] == tuple(settings['formats'])
        assert options['try_rotate'] == settings['try_rotate']
        assert options['try_invert'] == settings['try_invert']


def test_symbol_pixels_use_public_orientation_alpha_and_size_handling():
    stream = io.BytesIO()
    image = Image.new('RGBA', (4, 3), (255, 0, 0, 0))
    exif = image.getexif()
    exif[274] = 6
    image.save(stream, format='PNG', exif=exif)
    file = Artifact('transparent.png', stream.getvalue())
    pixels = symbols.pixel_input(file)
    assert (pixels['width'], pixels['height']) == (3, 4)
    assert pixels['data'] == bytes([255])*3*4*4
    with pytest.raises(OneKitError, match='pixels'):
        symbols.pixel_input(file, max_pixels=10)


def test_symbol_format_aliases_are_normalized_in_the_public_result_handler():
    from onekit.tools.barcode import decode_result
    result = decode_result('scan-barcode', [{'text': 'TEST', 'format': 'Code39Std'},
                                          {'text': 'TEST', 'format': 'CODE39'}])
    assert result.details == {'count': 1, 'codes': [{'text': 'TEST', 'format': 'CODE39'}]}


def test_sql_formatter_uses_the_cli_sqlparse_engine_in_process(monkeypatch):
    sqlparse = pytest.importorskip('sqlparse')
    monkeypatch.setattr('onekit.tools.native.command', lambda *args, **kwargs: pytest.fail('Unexpected executable'))
    source = 'select name from users where id=1;'
    result = execute('dev-format-sql', [Artifact('query.sql', source.encode())])
    assert result.files[0].text() == sqlparse.format(source, reindent=True)


def test_sqlfluff_validation_shares_native_dialects_and_errors(monkeypatch):
    pytest.importorskip('sqlfluff')
    monkeypatch.setattr('onekit.tools.native.command', lambda *args, **kwargs: pytest.fail('Unexpected executable'))
    for text, dialect, valid in [('SELECT 1;', 'ansi', True), ('SELECT FROM WHERE;', 'ansi', False),
                                  ('SELECT value::text FROM things;', 'postgres', True)]:
        result = execute('dev-validate-sql', [Artifact('query.sql', text.encode())], {'dialect': dialect})
        assert result.details['valid'] is valid
