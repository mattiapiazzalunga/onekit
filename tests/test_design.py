# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import json
import math

import pytest

from onekit import Artifact, execute
from onekit.models import OneKitError
from onekit.tools.design import HARMONIES, contrast, coordinates, palette, to_hex


def test_reference_coordinates_and_contrast():
    assert coordinates('#FF0000') == pytest.approx((.62795536, .2576833, 29.233885), abs=1e-6)
    assert contrast('#000000', '#FFFFFF') == pytest.approx(21)
    assert contrast('#6750A4', '#6750A4') == pytest.approx(1)


@pytest.mark.parametrize('base', ['#000000', '#FFFFFF', '#FF0000', '#00FF00', '#0000FF', '#6750A4'])
def test_roundtrip_and_all_harmonies(base):
    assert to_hex(*coordinates(base)) == base
    for harmony in HARMONIES:
        result = palette(base, harmony)
        assert result['colors'][2]['hex'] == base
        assert len(result['colors']) == 5
        for i, color in enumerate(result['colors']):
            assert color['contrast'] >= 4.5
            assert result['contrast_matrix'][i][i] == 1
            assert all(math.isfinite(v) for v in color['oklch'])


@pytest.mark.parametrize('options', [{'harmony':'unknown'}, {'lightness':float('nan')}, {'chroma':-.1}, {'hue':361}, {'lightness':True}, {'format':'html'}])
def test_invalid_options(options):
    with pytest.raises(OneKitError):
        execute('color-palette', [Artifact('color.txt', b'#123456')], options)


@pytest.mark.parametrize('format', ['json', 'css', 'svg'])
def test_public_dispatch_and_exports(format):
    result = execute('color-palette', [Artifact('color.txt', b'#6750A4')], {'format':format, 'harmony':'triadic'})
    assert result.files[0].name == 'palette.'+format
    assert len(result.details['colors']) == 5
    if format == 'json':
        assert json.loads(result.files[0].text()) == result.details
    elif format == 'css':
        assert '--color-5:' in result.files[0].text()
    else:
        from xml.etree import ElementTree
        assert len(ElementTree.fromstring(result.files[0].text())) == 10


def test_out_of_gamut_mapping():
    result = palette('#6750A4', chroma=.4, lightness=.7, hue_override=140)
    for color in result['colors']:
        assert color['oklch'][1] <= .400001
    assert result['colors'][2]['oklch'][0] == pytest.approx(.7, abs=.003)


@pytest.mark.parametrize('base', ['red', '#123', '#12345678', '#GGGGGG', '<script>'])
def test_invalid_base(base):
    with pytest.raises(OneKitError):
        palette(base)
