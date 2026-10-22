# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Use Node's built-in Brotli when no Python Brotli wheel is available."""
from contextlib import contextmanager
from types import SimpleNamespace


def convert(data, *, compress=False):
    from .native import command
    script = (
        "const fs=require('node:fs'),z=require('node:zlib');"
        "const input=fs.readFileSync(0);"
        "if(input.length>33554432)throw Error('Webfont exceeds 32 MiB');"
        "const output=z." + ("brotliCompressSync" if compress else "brotliDecompressSync") +
        "(input,{maxOutputLength:33554432});process.stdout.write(output);"
    )
    return command("node", ["-e", script], None, stdin=data, timeout=30)


@contextmanager
def font_brotli():
    """Limit this compatibility bridge to fontTools, without a fake global package."""
    from fontTools.ttLib import woff2
    if woff2.haveBrotli:
        yield
        return
    previous = getattr(woff2, "brotli", None)
    woff2.brotli = SimpleNamespace(MODE_FONT=2, decompress=convert, compress=lambda data, **_: convert(data, compress=True))
    woff2.haveBrotli = True
    try:
        yield
    finally:
        woff2.haveBrotli = False
        if previous is None:
            del woff2.brotli
        else:
            woff2.brotli = previous
