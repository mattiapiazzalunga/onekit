# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Pinned, isolated Pandoc WASM conversion shared by local processing hosts."""
import hashlib
import json
import os
from pathlib import Path

from ..execution import current_context
from ..models import OneKitError, Result, output

WASM_SHA256 = 'b47c9de52b5b45f103c2dac6fea52591aeafe3dd6cafed13331b67575233a2ff'


def engine_directory():
    return Path(os.environ.get('ONEKIT_PANDOC_ENGINE_PATH', Path.home() / '.cache' / 'onekit' / 'pandoc'))


def engine_ready():
    directory = engine_directory()
    try:
        package = json.loads((directory / 'node_modules/pandoc-wasm/package.json').read_text(encoding='utf-8'))
        return package['version'] == '1.1.0' and hashlib.sha256((directory / 'node_modules/pandoc-wasm/src/pandoc.wasm').read_bytes()).hexdigest() == WASM_SHA256
    except (OSError, ValueError, KeyError):
        return False


def conversion_request(file, target):
    if target not in ('html', 'md'):
        raise OneKitError('Document conversion failed.')
    if len(file.data) > 256 * 1024:
        raise OneKitError('Source is too complex. Split it into smaller files.')
    return {'options': {'from': 'latex', 'to': 'markdown' if target == 'md' else 'html', 'sandbox': True}, 'stdin': file.text()}


def convert(file, target):
    request = conversion_request(file, target)
    service = current_context().document_converter
    if service is not None:
        response = service(request)
    else:
        if os.environ.get('ONEKIT_ALLOW_COPYLEFT') == '0':
            raise OneKitError('A required engine is disabled by ONEKIT_ALLOW_COPYLEFT=0.')
        if not engine_ready():
            raise OneKitError("Install the optional Pandoc WASM engine with 'onekit setup latex-to-html'.")
        from .native import command
        script = Path(__file__).parents[1] / 'data/pandoc-node/runner.mjs'
        data = command('node', [str(script.resolve()), str(engine_directory().resolve())], Path.cwd(), stdin=json.dumps(request).encode('utf-8'), timeout=30)
        response = json.loads(data)
    if not isinstance(response, dict) or not isinstance(response.get('stdout'), str) or response.get('stderr') or response.get('warnings'):
        # No partial conversion when Pandoc reports skipped resources/constructs.
        raise OneKitError('Document conversion failed.')
    data = response['stdout'].encode('utf-8')
    if len(data) > 4 * 1024 * 1024:
        raise OneKitError('Document conversion failed.')
    return Result([output(file, target, data)], details={'engine': 'pandoc', 'version': '3.9', 'distribution': 'pandoc-wasm@1.1.0', 'wasm_sha256': WASM_SHA256})
