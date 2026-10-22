# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import copy
import json
from pathlib import Path

import pytest

from onekit.contracts import compatibility_errors, contract_manifest


def test_published_contract_is_preserved():
    previous = json.loads((Path(__file__).parents[1] / "contracts/processing-v1.json").read_text(encoding="utf-8"))
    assert compatibility_errors(previous, json.loads(json.dumps(contract_manifest()))) == []


@pytest.mark.parametrize("change", [
    lambda c: c["tools"].pop(),
    lambda c: c["tools"][0].update(produces="changed"),
    lambda c: c["tools"][0].update(accepts=[]),
    lambda c: c["tools"][0].update(max_total_bytes=1),
    lambda c: c.update(apiVersion=2),
])
def test_breaking_changes_are_detected(change):
    previous = json.loads(json.dumps(contract_manifest()))
    current = copy.deepcopy(previous)
    change(current)
    assert compatibility_errors(previous, current)


def test_additive_changes_and_algorithm_refactors_remain_compatible():
    previous = json.loads(json.dumps(contract_manifest()))
    current = copy.deepcopy(previous)
    current["tools"][0]["options"].append("additional_option")
    current["tools"][0]["accepts"].append("additional_format")
    current["tools"].append({**current["tools"][0], "id": "new-tool"})
    assert not compatibility_errors(previous, current)
