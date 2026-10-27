# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Run regression tests while recording actual API/CLI execution by catalog ID.

Native test failures remain visible. Trusted injected services are recorded
separately from executions using installed native engines.
"""
import functools
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import pytest
import onekit
from onekit import api
from onekit.catalog import TOOLS

destination = Path('.artifacts/all-tools-core-audit.json')
rows = {key: {'tool': key, 'handler': tool.handler, 'calls': [],
              'sourceSha256': hashlib.sha256(Path('src/onekit/tools', tool.handler.replace('.', '/'), '__init__.py').read_bytes()
                 if Path('src/onekit/tools', tool.handler.replace('.', '/'), '__init__.py').exists()
                 else Path('src/onekit/tools', tool.handler.replace('.', '/') + '.py').read_bytes()).hexdigest()}
        for key, tool in TOOLS.items()}
original = api.execute


@functools.wraps(original)
def recorded(tool_id, *args, **kwargs):
    start = time.perf_counter()
    call = {'injectedContext': kwargs.get('context') is not None,
            'test': os.environ.get('PYTEST_CURRENT_TEST', '')}
    try:
        result = original(tool_id, *args, **kwargs)
        call.update(status='returned', outputs=[file.name for file in result.files])
        return result
    except Exception as error:
        call.update(status='raised', error=str(error)[:600])
        raise
    finally:
        call['durationMs'] = (time.perf_counter() - start) * 1000
        if isinstance(tool_id, str) and tool_id in rows:
            rows[tool_id]['calls'].append(call)


api.execute = onekit.execute = recorded
tests = []


class Results:
    def pytest_runtest_logreport(self, report):
        if report.when == 'call' or report.failed:
            tests.append({'test': report.nodeid, 'phase': report.when, 'outcome': report.outcome})


code = pytest.main(sys.argv[1:] or ['tests', '-q'], plugins=[Results()])
from onekit.cli import doctor
availability = doctor()
destination.parent.mkdir(exist_ok=True)
destination.write_text(json.dumps({'pytestExitCode': int(code), 'tests': tests,
    'availability': availability, 'rows': list(rows.values())}, indent=2), encoding='utf-8')
print('Recorded catalog entries:', len(rows), 'with successful calls:', sum(any(c['status'] == 'returned' for c in row['calls']) for row in rows.values()))
raise SystemExit(code)
