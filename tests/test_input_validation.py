# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import io
import json
import zipfile
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_core import pdf, png

from onekit import Artifact, OneKitError, Result, execute, pipeline
from onekit.catalog import TOOLS
from onekit.cli import read_files
from onekit.validation import validate_zip


def no_engine(monkeypatch):
    monkeypatch.setattr("onekit.api.importlib.import_module", lambda *_: pytest.fail("Rejected inputs must not reach a processing engine"))


def test_catalog_has_an_explicit_bounded_contract_for_every_tool():
    unrestricted = {"file-inspect", "file-metadata-set", "file-metadata-remove", "security-encrypt", "text-strip-formatting"}
    for tool in TOOLS.values():
        assert tool.input_mode in ("any", "text", "encoded-text", "typed")
        assert 1 <= tool.min_files <= tool.max_files <= 256
        assert 0 < tool.max_file_bytes <= tool.max_total_bytes <= 128 * 1024 * 1024
        if tool.input_mode == "any":
            assert tool.id in unrestricted or tool.group == "licenses"
        if tool.input_mode == "typed":
            assert tool.accepts != ("*",)


@pytest.mark.parametrize("tool", TOOLS.values(), ids=lambda tool: tool.id)
def test_every_tool_rejects_oversized_files_before_processing(tool, monkeypatch):
    monkeypatch.setitem(TOOLS, tool.id, replace(tool, max_file_bytes=1))
    no_engine(monkeypatch)
    name = "input." + (tool.accepts[0] if tool.accepts[0] != "*" else "bin")
    with pytest.raises(OneKitError, match="per-file limit"):
        execute(tool.id, [Artifact(name, b"xx")] * tool.min_files)


@pytest.mark.parametrize("tool", TOOLS.values(), ids=lambda tool: tool.id)
def test_every_tool_enforces_file_counts_before_processing(tool, monkeypatch):
    no_engine(monkeypatch)
    with pytest.raises(OneKitError):
        execute(tool.id, [])
    with pytest.raises(OneKitError):
        execute(tool.id, [Artifact("input.txt", b"")] * (tool.max_files + 1))


@pytest.mark.parametrize("tool", [tool for tool in TOOLS.values() if tool.accepts != ("*",)], ids=lambda tool: tool.id)
def test_every_restricted_tool_rejects_wrong_extensions(tool, monkeypatch):
    no_engine(monkeypatch)
    with pytest.raises(OneKitError, match="Expected file types"):
        execute(tool.id, [Artifact("input.forbidden", b"content")] * tool.min_files)


@pytest.mark.parametrize("tool", [tool for tool in TOOLS.values() if tool.input_mode in ("text", "encoded-text")], ids=lambda tool: tool.id)
def test_all_text_tools_reject_disguised_binary_input(tool, monkeypatch):
    no_engine(monkeypatch)
    name = "input." + (tool.accepts[0] if tool.accepts[0] != "*" else "txt")
    with pytest.raises(OneKitError):
        execute(tool.id, [Artifact(name, b"%PDF-1.7\n\x00binary")] * tool.min_files)


@pytest.mark.parametrize("tool,name,data", [
    ("pdf-split", "fake.pdf", b"hello"),
    ("pdf-to-png", "fake.pdf", b"%PDF-1.4\nnot a real PDF\n%%EOF"),
    ("image-convert", "fake.png", b"\x89PNG\r\n\x1a\nnot a real image"),
    ("font-convert", "fake.woff", b"wOFF" + b"\0" * 44),
    ("security-decrypt", "fake.onekit", b"not encrypted"),
    ("archive-convert", "fake.zip", b"not a ZIP"),
    ("docx-to-pdf", "fake.docx", b"PK\x03\x04not an Office document"),
    ("audio-convert", "fake.wav", b"not a WAVE file"),
    ("video-convert", "fake.mp4", b"not an MP4 file"),
])
def test_corrupt_and_renamed_binary_formats_never_reach_the_engine(tool, name, data, monkeypatch):
    no_engine(monkeypatch)
    with pytest.raises(OneKitError):
        execute(tool, [Artifact(name, data)])


def test_valid_image_cannot_be_disguised_as_pdf_or_other_image_format():
    for name, tool in (("image.pdf", "pdf-to-png"), ("image.jpeg", "image-convert")):
        with pytest.raises(OneKitError):
            execute(tool, [Artifact(name, png().data)])


def test_office_containers_are_not_interchangeable():
    from openpyxl import Workbook
    stream = io.BytesIO()
    Workbook().save(stream)
    with pytest.raises(OneKitError, match="not a DOCX"):
        execute("docx-to-pdf", [Artifact("workbook.docx", stream.getvalue())])


def test_real_pdf_can_be_rendered_and_wrong_file_cannot_be_added_to_merge():
    assert execute("pdf-to-png", [pdf()]).files[0].data.startswith(b"\x89PNG")
    with pytest.raises(OneKitError, match="not a PDF"):
        execute("pdf-merge", [pdf(), Artifact("fake.pdf", b"text")])


def test_cli_rejects_weight_and_extension_before_reading(tmp_path, monkeypatch):
    source = tmp_path / "input.pdf"
    source.write_bytes(b"too large")
    monkeypatch.setattr(Path, "open", lambda *_args, **_kwargs: pytest.fail("The file must not be read"))
    with pytest.raises(OneKitError, match="size limit"):
        read_files([source], tool=replace(TOOLS["pdf-split"], max_file_bytes=1))
    with pytest.raises(OneKitError, match="Expected file types"):
        read_files([source], tool=TOOLS["image-convert"])
    with pytest.raises(OneKitError, match="requires"):
        read_files([source, source], tool=TOOLS["pdf-split"])




def test_pipeline_checks_aggregate_outputs_incrementally(monkeypatch):
    monkeypatch.setattr("onekit.validation.MAX_BYTES", 3)
    calls = []
    def handler(_tool, files, _options):
        calls.append(files[0].name)
        return Result([Artifact(files[0].name, b"xx")])
    monkeypatch.setattr("onekit.api.importlib.import_module", lambda *_: SimpleNamespace(run=handler))
    with pytest.raises(OneKitError, match="Output exceeds"):
        pipeline([{"tool": "file-count"}], [Artifact(f"{index}.txt", b"x") for index in range(3)])
    assert len(calls) == 2


def test_archives_cannot_expand_past_the_budget():
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("large.txt", b"x" * 1000)
    with pytest.raises(OneKitError, match="expansion"):
        validate_zip(stream.getvalue(), 100)




@pytest.mark.parametrize("tool", ["file-inspect", "security-encrypt"])
def test_any_file_tools_still_accept_arbitrary_binary_data(tool):
    assert execute(tool, [Artifact("unknown.bin", b"\0\xff\x01")], {"password": "long-test-password"}).files


def test_validators_still_report_invalid_syntax_as_a_result():
    result = execute("dev-validate-json", [Artifact("invalid.json", b"{broken")])
    assert json.loads(result.files[0].text())["valid"] is False


def test_plain_text_identifiers_are_not_misclassified_as_binary():
    assert execute("dev-validate-python", [Artifact("input.py", b"ID3 = 1\nRIFF = 2\nwOFF = 3")]).details["valid"]


@pytest.mark.parametrize("compression", ["gz", "bz2", "xz"])
def test_compressed_tar_bombs_are_bounded_before_parsing(compression):
    import bz2
    import gzip
    import lzma

    from onekit.tools.archives import tar_payload
    compress = {"gz": gzip.compress, "bz2": bz2.compress, "xz": lzma.compress}[compression]
    compressed = compress(b"x" * (4 * 1024 * 1024 + 1000))
    with pytest.raises(OneKitError, match="expansion"):
        tar_payload(compressed, 100)


def test_forged_zip_entry_counts_are_rejected_before_directory_allocation(monkeypatch):
    import struct
    data = b"PK\x05\x06" + struct.pack("<4H2LH", 0, 0, 65535, 65535, 0, 0, 0)
    monkeypatch.setattr(zipfile, "ZipFile", lambda *_: pytest.fail("Do not allocate an oversized directory"))
    with pytest.raises(OneKitError, match="directory"):
        validate_zip(data, 128 * 1024 * 1024)


@pytest.mark.parametrize("group", ["audio", "video"])
def test_media_probe_blocks_wrong_stream_types_before_conversion(group, monkeypatch):
    calls = []
    def probe(engine, _args, _directory, **_kwargs):
        calls.append(engine)
        assert engine == "ffprobe"
        return json.dumps({"streams": [{"codec_type": "video" if group == "audio" else "audio"}]}).encode()
    monkeypatch.setattr("onekit.tools.media.command", probe)
    file = Artifact("input.wav", b"RIFF\x00\x00\x00\x00WAVE") if group == "audio" else Artifact("input.mp4", b"\x00\x00\x00\x18ftypisom")
    with pytest.raises(OneKitError, match="stream"):
        execute(f"{group}-convert", [file])
    assert calls == ["ffprobe"]


def test_compressed_font_declared_expansion_is_bounded():
    from test_core import processing_case
    files, options = processing_case(TOOLS["font-convert"])
    woff = execute("font-convert", files, options).files[0]
    assert execute("font-convert", [woff], {"format": "ttf"}).files
    data = bytearray(woff.data)
    data[16:20] = (100 * 1024 * 1024).to_bytes(4, "big")
    with pytest.raises(OneKitError, match="font header"):
        execute("font-convert", [Artifact("huge.woff", bytes(data))])


def test_text_control_scanning_preserves_unicode_and_encoded_text_rules():
    forbidden = {*range(9), 11, *range(14, 32), 127}
    for code in range(256):
        source = Artifact("text.txt", chr(code).encode("utf-8"))
        if code in forbidden:
            with pytest.raises(OneKitError, match="binary"):
                execute("file-count", [source])
        else:
            assert execute("file-count", [source]).details["characters"] == 1
    assert execute("file-encoding-convert", [Artifact("text.txt", "OneKit".encode("utf-16"))], {"source_encoding": "utf-16"}).files[0].data == b"OneKit"
    with pytest.raises(OneKitError, match="binary"):
        execute("file-encoding-convert", [Artifact("text.txt", b"+AAA-")], {"source_encoding": "utf-7"})
