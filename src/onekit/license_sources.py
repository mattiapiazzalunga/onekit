# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Download public sources locally; never send files to an analysis service."""
from __future__ import annotations

import base64
import io
import json
import re
import urllib.parse
import zipfile

from .models import Artifact, OneKitError

LIMIT = 32 * 1024 * 1024
FILE_LIMIT = 1024 * 1024
REPOSITORY_FILES = 40


def checked_url(value):
    if not isinstance(value, str) or len(value) > 2048 or re.search(r"[\x00-\x20\x7f]", value):
        raise OneKitError("Enter one complete HTTP(S) source URL, without spaces or credentials.")
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in ("https", "http") or not parsed.hostname or parsed.username or parsed.password:
        raise OneKitError("Use an HTTP(S) URL without embedded credentials. Private sources can be uploaded instead.")
    try:
        _ = parsed.port
    except ValueError as exc:
        raise OneKitError("Invalid source URL port.") from exc
    return parsed


def source_plan(url, ref=""):
    parsed = checked_url(url)
    parts = [urllib.parse.unquote(part) for part in parsed.path.strip("/").split("/") if part]
    if parsed.hostname.lower() in ("gitlab.com", "www.gitlab.com") and parts and parts[0] == "api":
        return {"kind": "direct", "url": url}
    reference = ref or urllib.parse.parse_qs(parsed.query).get("ref", [""])[0]
    if not isinstance(reference, str) or len(reference) > 200 or re.search(r"[\x00-\x1f]", reference):
        raise OneKitError("Repository reference must be a branch, tag or commit of at most 200 characters.")
    if parsed.hostname.lower() in ("github.com", "www.github.com") and len(parts) >= 2:
        owner, repo = parts[0], parts[1].removesuffix(".git")
        api = "https://api.github.com/repos/" + urllib.parse.quote(owner, safe="") + "/" + urllib.parse.quote(repo, safe="")
        if len(parts) >= 5 and parts[2] == "blob":
            branch = reference or parts[3]
            path = "/".join(urllib.parse.quote(part, safe="") for part in parts[4:])
            return {"kind": "direct", "url": f"https://raw.githubusercontent.com/{owner}/{repo}/{urllib.parse.quote(branch, safe='')}/{path}"}
        if len(parts) == 2 or len(parts) >= 4 and parts[2] == "tree":
            return {"kind": "github", "api": api, "ref": reference or (parts[3] if len(parts) >= 4 else "HEAD")}
    if parsed.hostname.lower() in ("gitlab.com", "www.gitlab.com") and len(parts) >= 2:
        separator = parts.index("-") if "-" in parts else len(parts)
        project = "/".join(parts[:separator]).removesuffix(".git")
        api = "https://gitlab.com/api/v4/projects/" + urllib.parse.quote(project, safe="")
        tail = parts[separator + 1:]
        if len(tail) >= 3 and tail[0] in ("blob", "raw"):
            branch = reference or tail[1]
            return {"kind": "direct", "url": api + "/repository/files/" + urllib.parse.quote("/".join(tail[2:]), safe="") + "/raw?ref=" + urllib.parse.quote(branch, safe="")}
        if not tail or tail[0] == "tree":
            return {"kind": "gitlab", "api": api, "ref": reference or (tail[1] if len(tail) > 1 else "HEAD")}
    return {"kind": "direct", "url": url}


def candidate_rank(path):
    parts = path.replace("\\", "/").split("/")
    if any(part in (".git", "node_modules", ".venv", "vendor") for part in parts):
        return 9
    base = parts[-1].lower()
    if re.match(r"^(licen[sc]e|copying|copyright|notice)([._-]|$)", base) or base.endswith(".license") or base == "reuse.toml":
        return 0
    if base.startswith("readme") or base in ("package.json", "pyproject.toml", "cargo.toml", "composer.json", "datapackage.json", "metadata.json"):
        return 1
    if base.rsplit(".", 1)[-1] in ("py", "js", "ts", "tsx", "jsx", "c", "cpp", "h", "java", "rs", "rb", "go", "sh", "cs", "kt", "swift", "json", "toml"):
        return 2
    return 9


def source_name(url, headers, kind, data):
    parsed = checked_url(url)
    disposition = {name.lower(): value for name, value in headers.items()}.get("content-disposition", "")
    match = re.search(r"filename\*?=(?:UTF-8''|\")?([^\";]+)", disposition, re.IGNORECASE)
    name = urllib.parse.unquote(match[1] if match else parsed.path.rsplit("/", 1)[-1])
    name = re.sub(r"[\\/:\x00-\x1f]", "_", name).strip(" .")[:160] or "source"
    if "." not in name:
        extension = {"pdf": "pdf", "word": "docx", "powerpoint": "pptx", "excel": "xlsx", "image": "png", "font": "ttf", "epub": "epub", "audio": "mp3", "video": "mp4", "dataset": "json", "code": "txt"}[kind]
        if data.startswith(b"PK\x03\x04") and kind == "code":
            extension = "zip"
        elif data.startswith(b"\xff\xd8\xff"):
            extension = "jpg"
        elif data.startswith(b"\x89PNG"):
            extension = "png"
        elif data.startswith(b"OTTO"):
            extension = "otf"
        elif data.startswith(b"wOF2"):
            extension = "woff2"
        elif data.startswith(b"wOFF"):
            extension = "woff"
        name += "." + extension
    return name


def download_license_source(url, tool_id, *, ref="", fetcher=None):
    import urllib.request
    plan = source_plan(url, ref)

    def download(address, limit=LIMIT):
        checked_url(address)
        if fetcher:
            return fetcher(address, limit)
        request = urllib.request.Request(address, headers={"User-Agent": "OneKit-local-license-inspector", "Accept": "application/vnd.github+json, */*"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                checked_url(response.url)
                if int(response.headers.get("Content-Length", "0")) > limit:
                    raise OneKitError("Source exceeds the local download limit. Upload a smaller file.")
                data = response.read(limit + 1)
                if len(data) > limit:
                    raise OneKitError("Source exceeds the local download limit.")
                return data, dict(response.headers), response.url
        except OSError as exc:
            raise OneKitError(f"Cannot download this public source locally: {exc}. Upload the file instead.") from exc

    def api(address):
        return json.loads(download(address, 4 * 1024 * 1024)[0])

    kind = tool_id.removeprefix("license-")
    if plan["kind"] == "direct":
        data, headers, final = download(plan["url"])
        return [Artifact(source_name(final, headers, kind, data), data)], {"url": url, "download_url": final, "coverage": "Downloaded one public source file directly. No remote analysis service was used."}
    if kind != "code":
        raise OneKitError("Repository links belong in the code/project license checker. Use a direct file URL here.")
    from .tools.license_check import safe_entry
    reference = urllib.parse.quote(plan["ref"], safe="")
    if plan["kind"] == "github":
        tree = api(plan["api"] + "/git/trees/" + reference + "?recursive=1")
        entries = [{"path": entry["path"], "id": entry["sha"], "size": entry.get("size", 0)} for entry in tree.get("tree", [])[:20000] if entry.get("type") == "blob"]
        revision = tree.get("sha", plan["ref"])
    else:
        revision = api(plan["api"] + "/repository/commits/" + reference).get("id", plan["ref"])
        entries = []
        for page in range(1, 6):
            values = api(plan["api"] + "/repository/tree?recursive=true&per_page=100&page=" + str(page) + "&ref=" + urllib.parse.quote(revision, safe=""))
            entries.extend(entry for entry in values if entry.get("type") == "blob")
            if len(values) < 100:
                break
    selected = sorted((entry for entry in entries if candidate_rank(entry["path"]) < 9 and entry.get("size", 0) <= FILE_LIMIT), key=lambda entry: (candidate_rank(entry["path"]), entry["path"]))[:REPOSITORY_FILES]
    if not selected:
        raise OneKitError("No inspectable licensing or source files were found in this public repository.")
    stream = io.BytesIO()
    total = 0
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for entry in selected:
            path = safe_entry(entry["path"])
            if plan["kind"] == "github":
                value = api(plan["api"] + "/git/blobs/" + urllib.parse.quote(entry["id"], safe=""))
                if value.get("encoding") != "base64":
                    continue
                data = base64.b64decode(value.get("content", ""))
            else:
                data = download(plan["api"] + "/repository/blobs/" + urllib.parse.quote(entry["id"], safe="") + "/raw", FILE_LIMIT)[0]
            total += len(data)
            if len(data) > FILE_LIMIT or total > LIMIT:
                raise OneKitError("Repository download exceeded the local inspection limit. Upload a smaller archive.")
            archive.writestr(path, data)
    coverage = f"Partial repository snapshot at {revision}: selected up to {REPOSITORY_FILES} license, README, manifest and small source files. Dependencies and a full compliance audit were not included."
    return [Artifact("repository.zip", stream.getvalue())], {"url": url, "download_url": plan["api"], "revision": revision, "coverage": coverage}
