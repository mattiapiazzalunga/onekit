# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Any
import json


class OneKitError(ValueError):
    """An actionable processing error, safe to show in the CLI or UI."""


@dataclass(frozen=True)
class Artifact:
    name: str
    data: bytes

    def __post_init__(self):
        name = self.name.replace("\\", "/")
        if not name or name.startswith("/") or ".." in name.split("/") or ":" in name:
            raise OneKitError("File names must be relative and cannot traverse directories.")
        reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
        if any(ord(char) < 32 for char in name) or any(part.split(".")[0].upper() in reserved or part.endswith((" ", ".")) for part in name.split("/")):
            raise OneKitError("This file name is not portable across supported operating systems.")
        object.__setattr__(self, "name", name)

    @property
    def kind(self) -> str:
        aliases = {"jpg": "jpeg", "htm": "html", "markdown": "md", "yml": "yaml", "tex": "latex"}
        ext = PurePosixPath(self.name).suffix.lower().lstrip(".")
        return aliases.get(ext, ext)

    @property
    def stem(self) -> str:
        return PurePosixPath(self.name).stem

    def text(self) -> str:
        try:
            return self.data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise OneKitError("This operation requires UTF-8 text. Convert the encoding first.") from exc


@dataclass
class Result:
    files: list[Artifact]
    warnings: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)


def output(source: Artifact, extension: str, data: str | bytes) -> Artifact:
    return Artifact(f"{source.stem}.{extension}", data.encode("utf-8") if isinstance(data, str) else data)


def require(options: dict, key: str):
    value = options.get(key)
    if value is None or value == "":
        raise OneKitError(f"The '{key}' option is required.")
    return value


def parse_json(text: str):
    def constant(value):
        raise OneKitError(f"{value} is not valid standard JSON.")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise OneKitError(f"Duplicate JSON key: {key}.")
            result[key] = value
        return result

    return json.loads(text, parse_constant=constant, object_pairs_hook=pairs)
