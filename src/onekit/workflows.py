# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Portable .1kit workflow documents for processing pipelines."""
import copy
import json
from pathlib import Path

from .api import validate_steps
from .models import OneKitError

MAX_WORKFLOW_BYTES = 1024 * 1024
WORKFLOW_FILENAME = "workflow.1kit"


def workflow_document(value, *, redact=False):
    if (not isinstance(value, dict) or value.get("format") != "onekit-workflow"
            or type(value.get("version")) is not int or value["version"] != 1):
        raise OneKitError("Expected a onekit-workflow document with version 1.")
    validate_steps(value.get("steps"))
    document = {"format": "onekit-workflow", "version": 1, "steps": copy.deepcopy(value["steps"])}
    if redact:
        for step in document["steps"]:
            step.get("options", {}).pop("password", None)
    return document


def load_workflow(path):
    if Path(path).suffix.lower() != ".1kit":
        raise OneKitError("Choose a .1kit workflow file.")
    with Path(path).open("rb") as stream:
        data = stream.read(MAX_WORKFLOW_BYTES + 1)
    if len(data) > MAX_WORKFLOW_BYTES:
        raise OneKitError("Workflow exceeds the 1 MiB limit.")
    return workflow_document(json.loads(data.decode("utf-8-sig")))


def dump_workflow(value):
    data = (json.dumps(workflow_document(value, redact=True), indent=2, ensure_ascii=False, allow_nan=False)
            + "\n").encode("utf-8")
    if len(data) > MAX_WORKFLOW_BYTES:
        raise OneKitError("Workflow exceeds the 1 MiB limit.")
    return data
