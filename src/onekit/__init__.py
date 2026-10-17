# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
"""OneKit's shared, offline processing API."""

__version__ = "0.2.1"

from .api import execute, pipeline
from .models import Artifact, OneKitError, Result

__all__ = ["Artifact", "OneKitError", "Result", "execute", "pipeline"]
