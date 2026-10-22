# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import pytest

from onekit import Artifact
from onekit.tools.inspector import inspect


@pytest.mark.parametrize("character", [chr(value) for value in range(128)] + ["è", "🧰", "\u2028"])
def test_inspector_preserves_text_classification(character):
    text = "prefix" + character + "suffix"
    result = inspect(Artifact("input.txt", text.encode()))
    is_text = not any(ord(char) < 32 and char not in "\t\n\r\f" for char in text)
    assert (result["mime"] == "text/plain") == is_text
    assert result["encoding"] == ("UTF-8" if is_text else None)
