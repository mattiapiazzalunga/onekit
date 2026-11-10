# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ResourceLimits:
    max_bytes: int = 128 * 1024 * 1024
    max_files: int = 256
    max_image_pixels: int = 40_000_000
    max_archive_entries: int = 4096
    max_archive_ratio: int = 1000
    max_android_manifest_bytes: int = 4 * 1024 * 1024
    max_xapk_manifest_bytes: int = 1024 * 1024
    max_android_strings: int = 65536
    max_face_pixels: int = 16_000_000
    max_faces: int = 256
    max_face_candidates: int = 2000
    text_file_bytes: int = 8 * 1024 * 1024
    font_file_bytes: int = 16 * 1024 * 1024
    image_file_bytes: int = 64 * 1024 * 1024


LIMITS = ResourceLimits()


def resource_limits():
    return asdict(LIMITS)
