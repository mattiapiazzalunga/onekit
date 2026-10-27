# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import base64
import io
import json
import zipfile

import pytest

from onekit import Artifact, execute
from onekit.license_sources import download_license_source, source_plan
from onekit.models import OneKitError


def archive(entries):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as output:
        for name, value in entries.items():
            output.writestr(name, value)
    return buffer.getvalue()


def samples():
    from fontTools.ttLib import TTFont, newTable
    from PIL import Image, PngImagePlugin
    from pypdf import PdfWriter

    metadata = '<m xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:creator>Alice</dc:creator><dc:rights>MIT</dc:rights></m>'
    pdf = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(72, 72)
    writer.add_metadata({"/Author": "Alice", "/Copyright": "Copyright 2026 Alice", "/License": "MIT"})
    writer.write(pdf)
    png = io.BytesIO()
    info = PngImagePlugin.PngInfo()
    info.add_text("Author", "Alice")
    info.add_text("License", "MIT")
    Image.new("RGB", (2, 2)).save(png, format="PNG", pnginfo=info)
    font = TTFont()
    font["name"] = newTable("name")
    font["name"].names = []
    for number, value in ((0, "Copyright 2026 Alice"), (9, "Alice"), (13, "MIT")):
        font["name"].setName(value, number, 3, 1, 0x409)
    ttf = io.BytesIO()
    font.save(ttf)
    return {
        "pdf": ("sample.pdf", pdf.getvalue()),
        "word": ("sample.docx", archive({"docProps/core.xml": metadata, "word/document.xml": "<doc/>"})),
        "powerpoint": ("sample.pptx", archive({"docProps/core.xml": metadata, "ppt/presentation.xml": "<doc/>"})),
        "excel": ("sample.xlsx", archive({"docProps/core.xml": metadata, "xl/workbook.xml": "<doc/>"})),
        "epub": ("sample.epub", archive({"mimetype": "application/epub+zip", "OEBPS/package.opf": metadata})),
        "image": ("sample.png", png.getvalue()),
        "font": ("sample.ttf", ttf.getvalue()),
        "code": ("sample.zip", archive({"LICENSE": "MIT", "main.py": "# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0\n# Copyright 2026 Alice\n"})),
        "dataset": ("sample.json", b'{"license":"MIT", "creator":"Alice", "data":[{"copyright":"row only"}]}'),
    }


@pytest.mark.parametrize("kind", ["pdf", "word", "powerpoint", "excel", "epub", "image", "font", "code", "dataset"])
def test_formats_return_evidence_without_certification(kind, monkeypatch):
    import socket
    monkeypatch.setattr(socket, "create_connection", lambda *a, **k: pytest.fail("Inspection must not use the network"))
    name, data = samples()[kind]
    result = execute("license-" + kind, [Artifact(name, data)])
    report = json.loads(result.files[0].data)
    assert report["analysis"] == "local-only"
    assert report["is_estimate"] and report["requires_manual_verification"]
    assert report["permission_to_use"] == "not-determined"
    assert "Missing metadata never means" in report["disclaimer"]
    assert any(item["spdx_expression"] == "MIT" for item in report["declared_licenses"])
    assert all(item["verified"] is False for item in report["declared_licenses"])
    assert all(item["value"] != "row only" for item in report["copyright_notices"])
    assert len(report["files"][0]["sha256"]) == 64


@pytest.mark.parametrize("kind", ["audio", "video"])
def test_media_tags_use_ffprobe(kind, monkeypatch):
    from onekit.tools import native
    metadata = {"streams": [{"codec_type": kind, "tags": {"artist": "Alice"}}], "format": {"tags": {"license": "MIT"}}}
    calls = []
    monkeypatch.setattr(native, "command", lambda engine, args, cwd, **kwargs: calls.append((engine, args)) or json.dumps(metadata).encode())
    name = "sample.mp4" if kind == "video" else "sample.mp3"
    result = execute("license-" + kind, [Artifact(name, b"metadata fixture")])
    assert result.details["declared_creators"][0]["value"] == "Alice"
    assert result.details["declared_licenses"][0]["value"] == "MIT"
    assert len(calls) == 1 and calls[0][0] == "ffprobe"
    assert "file,pipe" in calls[0][1]


def test_no_metadata_does_not_mean_free_and_dataset_rows_are_not_rights():
    for name, data in [("data.json", b'[{"license":"MIT"}]'), ("data.json", b'{"data":[{"license":"MIT","text":"licensed under MIT"}]}'), ("data.csv", b'license,author\nMIT,Alice')]:
        result = execute("license-dataset", [Artifact(name, data)])
        assert result.details["status"] == "rights-undetermined"
        assert not result.details["declared_licenses"]
        assert result.details["permission_to_use"] == "not-determined"


def test_spdx_expressions_unknown_terms_and_creator_are_separate():
    data = b'{"license":"MIT OR Apache-2.0", "author":"Alice", "rights":"CUSTOM-EULA"}'
    report = execute("license-dataset", [Artifact("metadata.json", data)]).details
    assert report["declared_licenses"][0]["license_ids"] == ["MIT", "Apache-2.0"]
    assert not report["declared_licenses"][1]["spdx_syntax_valid"]
    assert report["declared_creators"][0]["value"] == "Alice"
    assert report["copyright_notices"] == []


def test_archive_paths_limits_and_reuse_ignore():
    with pytest.raises(OneKitError, match="Unsafe archive path"):
        execute("license-code", [Artifact("bad.zip", archive({"../LICENSE": "MIT"}))])
    with pytest.raises(OneKitError, match="2048"):
        execute("license-code", [Artifact("many.zip", archive({str(i): "" for i in range(2049)}))])
    data = b"REUSE-IgnoreStart\nSPDX-License-Identifier: MIT\nREUSE-IgnoreEnd\nSPDX-License-Identifier: Apache-2.0\n"
    result = execute("license-code", [Artifact("source.py", data)])
    assert [item["value"] for item in result.details["declared_licenses"]] == ["Apache-2.0"]


def test_archive_prioritizes_licenses_and_does_not_execute_code():
    entries = {f"src/{i}.py": "raise RuntimeError('must never run')" for i in range(270)}
    entries["LICENSE"] = "MIT"
    report = execute("license-code", [Artifact("project.zip", archive(entries))]).details
    assert report["declared_licenses"][0]["value"] == "MIT"
    assert report["coverage"]["skipped"]


def test_xml_external_entities_are_rejected():
    data = b'<!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///secret">]><svg><rights>&xxe;</rights></svg>'
    with pytest.raises(OneKitError):
        execute("license-image", [Artifact("bad.svg", data)])


@pytest.mark.parametrize("url", ["file:///secret", "https://user:password@example.org/x", "https://example.org:bad/x", "https://example.org/a\nb"])
def test_source_rejects_invalid_urls(url):
    with pytest.raises(OneKitError):
        source_plan(url)


def test_github_gitlab_blob_and_tree_source_plans():
    assert source_plan("https://github.com/owner/repo")["kind"] == "github"
    assert source_plan("https://github.com/owner/repo/blob/main/LICENSE")["url"].endswith("/owner/repo/main/LICENSE")
    plan = source_plan("https://gitlab.com/group/sub/project/-/tree/dev")
    assert plan["kind"] == "gitlab" and plan["ref"] == "dev" and "group%2Fsub%2Fproject" in plan["api"]
    assert source_plan("https://gitlab.com/g/p/-/blob/main/a.csv")["kind"] == "direct"


@pytest.mark.parametrize("host", ["github", "gitlab"])
def test_repository_download_only_fetches_raw_sources_and_reports_partial(host):
    calls = []
    def fetch(address, limit):
        calls.append(address)
        if "/git/trees/" in address:
            value = {"sha": "revision", "tree": [{"path": "LICENSE", "sha": "blob", "type": "blob", "size": 3}]}
        elif "/git/blobs/" in address:
            value = {"encoding": "base64", "content": base64.b64encode(b"MIT").decode()}
        elif "/commits/" in address:
            value = {"id": "revision"}
        elif "/repository/tree?" in address:
            value = [{"path": "LICENSE", "id": "blob", "type": "blob"}]
        else:
            return b"MIT", {}, address
        return json.dumps(value).encode(), {}, address
    files, source = download_license_source(f"https://{host}.com/owner/repo", "license-code", fetcher=fetch)
    report = execute("license-code", files, {"_source": source}).details
    assert "Partial repository" in report["coverage"]["source_download"]
    assert report["declared_licenses"][0]["value"] == "MIT"
    assert all("/license" not in address for address in calls)


def test_direct_download_and_cli_url(tmp_path, monkeypatch):
    from onekit import cli, license_sources, setup
    files, source = download_license_source("https://example.org/data.json", "license-dataset", fetcher=lambda url, limit: (b'{"license":"MIT"}', {}, url))
    assert files[0].name == "data.json"
    monkeypatch.setattr(license_sources, "download_license_source", lambda *a, **k: (files, source))
    monkeypatch.setattr(setup, "ensure_tool", lambda *a, **k: None)
    target = tmp_path / "report.json"
    assert cli.main(["run", "license-dataset", "--url", "https://example.org/data.json", "-o", str(target)]) == 0
    assert json.loads(target.read_text(encoding="utf-8"))["permission_to_use"] == "not-determined"


@pytest.mark.parametrize("flavor", [None, "woff", "woff2"])
def test_font_container_variants(flavor):
    from fontTools.ttLib import TTFont
    from test_core import processing_case

    from onekit.catalog import TOOLS
    files, _ = processing_case(TOOLS["font-convert"])
    font = TTFont(io.BytesIO(files[0].data))
    font["name"].setName("MIT", 13, 3, 1, 0x409)
    font.flavor = flavor
    stream = io.BytesIO()
    from onekit.tools.font_brotli import font_brotli
    with font_brotli():
        font.save(stream)
    report = execute("license-font", [Artifact("font." + (flavor or "ttf"), stream.getvalue())]).details
    assert report["declared_licenses"][0]["spdx_expression"] == "MIT"


def test_otf_name_records():
    from fontTools.ttLib import TTFont
    font = TTFont(io.BytesIO(samples()["font"][1]))
    font.sfntVersion = "OTTO"
    stream = io.BytesIO()
    font.save(stream)
    report = execute("license-font", [Artifact("font.otf", stream.getvalue())]).details
    assert report["declared_licenses"][0]["spdx_expression"] == "MIT"


@pytest.mark.parametrize("extension", ["doc", "ppt", "xls"])
def test_legacy_office_metadata_uses_olefile(extension, monkeypatch):
    from types import SimpleNamespace

    import olefile
    class Document:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def get_metadata(self):
            return SimpleNamespace(author=b"Alice", comments=b"SPDX-License-Identifier: MIT", last_saved_by=None)
    monkeypatch.setattr(olefile, "OleFileIO", lambda *_: Document())
    kind = {"doc": "word", "ppt": "powerpoint", "xls": "excel"}[extension]
    report = execute("license-" + kind, [Artifact("legacy." + extension, b"\xd0\xcf\x11\xe0fixture")]).details
    assert report["declared_creators"][0]["value"] == "Alice"
    assert report["declared_licenses"][0]["spdx_expression"] == "MIT"
    assert any("Legacy Office" in item["reason"] for item in report["coverage"]["skipped"])


@pytest.mark.parametrize("name", ["license_check.py", "license.js", "copyright.ts", "notice.go", "copying.rs"])
def test_source_named_like_license_is_not_a_license_document(name):
    from pathlib import Path
    from onekit.tools import license_check

    source = Path(license_check.__file__).read_bytes()
    report = execute("license-code", [Artifact("repository.zip", archive({"src/" + name: source}))]).details
    assert report["estimated_license_matches"] == []
    assert any(item["value"] == "LicenseRef-PolyForm-Shield-1.0.0" for item in report["declared_licenses"])


@pytest.mark.parametrize("name", ["LICENSE", "LICENSE.txt", "LICENSE-MIT", "COPYING.md", "NOTICE.rst", "source.py.license"])
def test_license_documents_still_report_tentative_matches(name):
    text = "Permission is hereby granted without restriction. The software is provided as is."
    report = execute("license-code", [Artifact("repository.zip", archive({name: text}))]).details
    assert [item["value"] for item in report["estimated_license_matches"]] == ["MIT"]
    assert report["estimated_license_matches"][0]["verified"] is False
