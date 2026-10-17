# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
import json

import pytest

from onekit.cli import main
from onekit.models import OneKitError
from onekit.workflows import dump_workflow, load_workflow, workflow_document


def document():
    return {"format": "onekit-workflow", "version": 1,
            "steps": [{"tool": "dev-format-json", "options": {}}],
            "layout": {"nodes": [{"x": 20, "y": 10, "expanded": True}] * 3}}


@pytest.mark.parametrize("extension", [".1kit", ".onekit.json", ".json"])
def test_cli_roundtrip_and_execution(tmp_path, extension):
    source = tmp_path / ("web" + extension)
    source.write_text(json.dumps(document()), encoding="utf-8")
    imported, exported = tmp_path / "imported.1kit", tmp_path / "exported.1kit"
    assert main(["workflow", "import", str(source), "-o", str(imported)]) == 0
    assert main(["workflow", "export", str(imported), "-o", str(exported)]) == 0
    assert load_workflow(exported) == document()
    input_file = tmp_path / "input.json"
    input_file.write_text('{"hello":1}', encoding="utf-8")
    output = tmp_path / "output.json"
    assert main(["pipeline", "--steps", str(exported), str(input_file), "-o", str(output)]) == 0
    assert json.loads(output.read_text()) == {"hello": 1}
    assert main(["workflow", "export", str(source), "-o", str(exported)]) == 2


def test_cli_directory_export_uses_1kit_filename(tmp_path):
    source = tmp_path / "legacy.json"
    source.write_text(json.dumps(document()), encoding="utf-8")
    output = tmp_path / "exports"
    assert main(["workflow", "export", str(source), "-o", str(output)]) == 0
    assert load_workflow(output / "workflow.1kit") == document()


def test_legacy_and_password_redaction():
    steps = [{"tool": "pdf-unlock", "options": {"password": "private"}}]
    result = json.loads(dump_workflow(steps))
    assert result["steps"][0]["options"] == {}
    assert steps[0]["options"]["password"] == "private"
    assert workflow_document(steps)["steps"] == steps


@pytest.mark.parametrize("mutate", [
    lambda value: value.update(version=2),
    lambda value: value.update(steps=[]),
    lambda value: value["steps"][0].update(tool="unknown"),
    lambda value: value["steps"][0].update(options=[]),
    lambda value: value["layout"]["nodes"].pop(),
    lambda value: value["layout"]["nodes"][0].update(x=float("inf")),
])
def test_invalid_documents(mutate):
    value = document()
    mutate(value)
    with pytest.raises(OneKitError):
        workflow_document(value)


def test_oversize_and_invalid_import_do_not_write(tmp_path):
    source, output = tmp_path / "source.json", tmp_path / "out.json"
    for data in ["null", "{" , " " * (1024 * 1024 + 1)]:
        source.write_text(data)
        assert main(["workflow", "import", str(source), "-o", str(output)]) == 2
        assert not output.exists()
