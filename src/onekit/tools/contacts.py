# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import re

from ..models import Artifact, OneKitError, Result, parse_json
from .qrcode import vcard_payload


def extract_vcard(raw):
    value = raw.strip().replace("\r\n", "\n").replace("\r", "\n")
    unfolded = re.sub(r"\n[ \t]", "", value)
    if (not unfolded.startswith("BEGIN:VCARD\n") or not unfolded.endswith("\nEND:VCARD")
            or unfolded.count("BEGIN:VCARD") != 1 or unfolded.count("END:VCARD") != 1
            or not re.search(r"^VERSION:(?:3\.0|4\.0)$", unfolded, re.MULTILINE)
            or not re.search(r"^FN(?:;[^:\n]*)?:[^\n]+$", unfolded, re.MULTILINE)
            or any((ord(char) < 32 and char not in "\n\t" or ord(char) == 127) for char in value)):
        raise OneKitError("The QR code must contain a complete vCard 3.0 or 4.0 with a display name; links and other payloads are not contacts.")
    return value.replace("\n", "\r\n") + "\r\n"


def run(tool, files, options):
    payload = vcard_payload(parse_json(files[0].text()))
    return Result([Artifact(f"{files[0].stem}.vcf", payload.encode("utf-8"))])
