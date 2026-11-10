# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import json
import shutil
from pathlib import Path

import pytest

from onekit.api import execute
from onekit.catalog import TOOLS
from onekit.models import Artifact, OneKitError
from onekit.tools.developer import engine_for, external, node_engines_ready


@pytest.mark.parametrize('language', ['kotlin', 'ruby'])
def test_portable_formatter_uses_shared_node_driver(monkeypatch, tmp_path, language):
    (tmp_path / 'node_modules').mkdir()
    monkeypatch.setenv('ONEKIT_NODE_ENGINE_PATH', str(tmp_path))
    monkeypatch.setattr('onekit.tools.developer.node_engines_ready', lambda language: True)
    seen = []

    def command(engine, arguments, directory, *, stdin):
        seen.append((engine, arguments, directory, json.loads(stdin)))
        return b'formatted\n'

    monkeypatch.setattr('onekit.tools.native.command', command)
    assert engine_for(TOOLS['dev-format-' + language]) == 'node'
    assert external('format', language, 'source') == 'formatted\n'
    engine, arguments, directory, request = seen[0]
    assert engine == 'node' and Path(arguments[0]).name == 'node-engine.mjs'
    assert directory == tmp_path
    assert request == {'operation': 'format', 'language': language, 'text': 'source'}
    with pytest.raises(OneKitError, match='Source is too complex'):
        execute('dev-format-' + language, [Artifact('input.txt', b'x' * (256 * 1024 + 1))])


@pytest.mark.parametrize('language', ['kotlin', 'ruby'])
def test_old_engine_installation_requires_the_pinned_formatter(monkeypatch, tmp_path, language):
    monkeypatch.setenv('ONEKIT_NODE_ENGINE_PATH', str(tmp_path))
    package = tmp_path / 'node_modules/@scalar' / (language + '-fmt') / 'package.json'
    package.parent.mkdir(parents=True)
    assert not node_engines_ready(language)
    package.write_text('{"version":"0.0.0"}', encoding='utf-8')
    assert not node_engines_ready(language)
    expected = json.loads(Path(__file__).parents[1].joinpath('src/onekit/tools/developer/node/package.json').read_text())['dependencies']['@scalar/' + language + '-fmt']
    package.write_text(json.dumps({'version': expected}), encoding='utf-8')
    assert node_engines_ready(language)


@pytest.fixture
def installed_formatters(monkeypatch):
    directory = Path(__file__).parents[1] / 'src/onekit/tools/developer/node'
    if not shutil.which('node') or not (directory / 'node_modules/@scalar/ruby-fmt').is_dir():
        pytest.skip('Optional pinned Node formatter packages')
    monkeypatch.setenv('ONEKIT_NODE_ENGINE_PATH', str(directory))


@pytest.mark.parametrize('language,source,expected', [
    ('kotlin', 'fun main(){println("OneKit")}', 'fun main() {\n  println("OneKit")\n}\n'),
    ('ruby', 'class Example\ndef value;[1,2,3].map{|x| x*2};end\nend\n',
     'class Example\n  def value\n    [1, 2, 3].map { |x| x * 2 }\n  end\nend\n'),
])
def test_real_formatter_output_is_idempotent_and_invalid_source_fails(installed_formatters, language, source, expected):
    tool = 'dev-format-' + language
    result = execute(tool, [Artifact('input.txt', source.encode())])
    assert result.files[0].data.decode() == expected
    assert execute(tool, result.files).files[0].data == result.files[0].data
    with pytest.raises(OneKitError):
        execute(tool, [Artifact('input.txt', b'fun broken( {' if language == 'kotlin' else b'def broken(\n')])
