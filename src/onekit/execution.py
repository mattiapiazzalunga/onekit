# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Resource budgets and trusted engine services for processing callers."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field, replace
from types import MappingProxyType

from .models import Artifact, OneKitError

MAX_BYTES = 128 * 1024 * 1024


def _budget(value):
    if type(value) is not int or not 0 < value <= MAX_BYTES:
        raise OneKitError(f"Processing budgets must be integers between 1 and {MAX_BYTES} bytes.")


@dataclass(frozen=True)
class ToolLimits:
    max_file_bytes: int = MAX_BYTES
    max_total_bytes: int = MAX_BYTES

    def __post_init__(self):
        _budget(self.max_file_bytes)
        _budget(self.max_total_bytes)
        if self.max_file_bytes > self.max_total_bytes:
            raise OneKitError("A per-file budget cannot exceed the total budget.")


@dataclass(frozen=True)
class DocumentLimits:
    max_nodes: int = 100_000
    max_depth: int = 128
    max_blocks: int = 10_000
    max_pages: int = 256

    def __post_init__(self):
        for name in ('max_nodes', 'max_depth', 'max_blocks', 'max_pages'):
            value = getattr(self, name)
            if type(value) is not int or not 1 <= value <= 1_000_000:
                raise OneKitError(f'{name} must be a positive bounded integer.')
        if self.max_depth > 128:
            raise OneKitError('Document nesting cannot exceed 128 levels.')


@dataclass(frozen=True)
class ExecutionContext:
    """A caller may narrow limits and supply trusted local engine primitives.

    Services are separate from untrusted tool options. Limits cannot raise the
    catalog's resource ceilings. Contexts are immutable and scoped to each call.

    symbol_reader returns text/format records for ``qr`` or ``linear`` symbols.
    ocr_reader returns per-page text and, when requested, searchable PDF bytes;
    optional width/height are the physical page dimensions in PDF points.
    speech_reader returns language and start/end/text segment records.
    foreground_reader returns an encoded grayscale mask at the oriented image size.
    pdf_renderer returns losslessly encoded raster data and physical
    width/height in points. Callers must bound engine memory and execution time;
    the processing API still validates the original inputs and final artifacts.
    svg_renderer receives validated, self-contained SVG and bounded dimensions,
    and returns PNG bytes, which the shared handler verifies before exporting.
    portable_documents selects the bounded Python document exporter instead of
    native document executables; document_limits supplies its structural budgets.
    """

    max_batch_bytes: int = MAX_BYTES
    tool_limits: Mapping[str, ToolLimits] = field(default_factory=dict)
    media_probe: Callable[[Artifact], dict] | None = None
    symbol_reader: Callable[[Artifact, str], list[dict]] | None = None
    ocr_reader: Callable[[Artifact, str, int, bool], list[dict]] | None = None
    speech_reader: Callable[[Artifact, str], dict] | None = None
    foreground_reader: Callable[[Artifact], bytes] | None = None
    pdf_renderer: Callable[[Artifact, str, int], list[dict]] | None = None
    svg_renderer: Callable[[dict], bytes] | None = None
    portable_documents: bool = False
    document_limits: DocumentLimits = field(default_factory=DocumentLimits)

    def __post_init__(self):
        _budget(self.max_batch_bytes)
        if type(self.portable_documents) is not bool:
            raise OneKitError('portable_documents must be a boolean.')
        if not isinstance(self.document_limits, DocumentLimits):
            raise OneKitError('document_limits must be DocumentLimits.')
        if any(not isinstance(key, str) or not isinstance(value, ToolLimits)
               for key, value in self.tool_limits.items()):
            raise OneKitError("Tool budgets must map tool identifiers to ToolLimits.")
        if self.media_probe is not None and not callable(self.media_probe):
            raise OneKitError("The media metadata reader must be callable.")
        for name in ("symbol_reader", "ocr_reader", "speech_reader", "foreground_reader", "pdf_renderer", "svg_renderer"):
            service = getattr(self, name)
            if service is not None and not callable(service):
                raise OneKitError(f"{name} must be callable.")
        object.__setattr__(self, "tool_limits", MappingProxyType(dict(self.tool_limits)))

    def constrain(self, tool):
        limits = self.tool_limits.get(tool.id, _DEFAULT_TOOL_LIMITS)
        total = min(tool.max_total_bytes, self.max_batch_bytes, limits.max_total_bytes)
        return replace(tool, max_total_bytes=total,
                       max_file_bytes=min(tool.max_file_bytes, total, limits.max_file_bytes))


_DEFAULT_TOOL_LIMITS = ToolLimits()
DEFAULT_CONTEXT = ExecutionContext()
_context = ContextVar("onekit_execution_context", default=DEFAULT_CONTEXT)


def current_context():
    return _context.get()


@contextmanager
def use_context(context):
    token = _context.set(context)
    try:
        yield
    finally:
        _context.reset(token)
