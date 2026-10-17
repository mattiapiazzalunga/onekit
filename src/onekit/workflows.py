# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
"""Portable .1kit workflow documents shared by the CLI and browser editor."""
import copy
import json
import math
from pathlib import Path

from .api import validate_steps
from .models import OneKitError

MAX_WORKFLOW_BYTES = 1024 * 1024
WORKFLOW_FILENAME = "workflow.1kit"


def workflow_document(value, *, redact=False):
    if isinstance(value, list):
        value = {"format": "onekit-workflow", "version": 1, "steps": value}
    if (not isinstance(value, dict) or value.get("format") != "onekit-workflow"
            or type(value.get("version")) is not int or value["version"] != 1):
        raise OneKitError("Expected a onekit-workflow document with version 1.")
    validate_steps(value.get("steps"))
    document = {"format": "onekit-workflow", "version": 1, "steps": copy.deepcopy(value["steps"])}
    layout = value.get("layout")
    if layout is not None:
        nodes = layout.get("nodes") if isinstance(layout, dict) else None
        if not isinstance(nodes, list) or len(nodes) != len(document["steps"]) + 2:
            raise OneKitError("Workflow layout must contain one node per step, plus input and actions.")
        for node in nodes:
            if (not isinstance(node, dict) or type(node.get("expanded")) is not bool
                    or any(type(node.get(key)) not in (int, float) or not math.isfinite(node[key])
                           or abs(node[key]) > 10000 for key in ("x", "y"))):
                raise OneKitError("Invalid workflow node position or expanded state.")
        document["layout"] = copy.deepcopy(layout)
    if redact:
        for step in document["steps"]:
            step.get("options", {}).pop("password", None)
    return document


def load_workflow(path):
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
