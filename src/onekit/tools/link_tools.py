# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Device-to-source downloads and HTTP inspection; no intermediary server."""
import json
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

from ..models import Artifact, OneKitError, Result
from .video_download import validate_url

REDIRECTS = (301, 302, 303, 307, 308)
HEADERS = ("content-type", "content-length", "location", "server", "cache-control", "expires", "last-modified", "etag", "content-encoding", "strict-transport-security", "content-security-policy", "x-content-type-options", "referrer-policy", "access-control-allow-origin")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_chain(url, method="GET"):
    opener = urllib.request.build_opener(NoRedirect())
    hops, seen = [], set()
    for _ in range(11):
        parsed = urllib.parse.urlsplit(validate_url(url))
        host = parsed.hostname.encode("idna").decode("ascii")
        host = "[" + host + "]" if ":" in host else host
        authority = host + (":" + str(parsed.port) if parsed.port else "")
        address = urllib.parse.urlunsplit((parsed.scheme, authority,
                    urllib.parse.quote(parsed.path, safe="/%:@!$&'()*+,;=-._~"),
                    urllib.parse.quote(parsed.query, safe="/%?:@!$&'()*+,;=-._~"), ""))
        if address in seen:
            raise OneKitError("The source has a redirect loop.")
        seen.add(address)
        request = urllib.request.Request(address, method=method, headers={"User-Agent": "OneKit-local-tools/1.0", "Accept": "*/*"})
        try:
            response = opener.open(request, timeout=15)
        except urllib.error.HTTPError as error:
            response = error
        headers = {name.lower(): value for name, value in response.headers.items()}
        hops.append({"url": address, "status": response.code, "headers": {name: headers[name][:4000] for name in HEADERS if name in headers}})
        if response.code not in REDIRECTS or not headers.get("location"):
            return response, hops
        response.close()
        url = urllib.parse.urljoin(address, headers["location"])
    raise OneKitError("The source exceeds the limit of 10 redirects.")


def components(url):
    parsed = urllib.parse.urlsplit(validate_url(url))
    return {"scheme": parsed.scheme, "hostname": parsed.hostname, "port": parsed.port or (443 if parsed.scheme == "https" else 80),
            "path": parsed.path or "/", "decoded_path": urllib.parse.unquote(parsed.path or "/"),
            "query_parameters": [{"name": name, "value": value} for name, value in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True, max_num_fields=1000)],
            "fragment": parsed.fragment, "https": parsed.scheme == "https"}


def inspect_url(url):
    report = {"schema": "onekit-url-inspection/v1", "input_url": url, "components": components(url), "analysis": "local-device",
              "hops": [], "final_url": None, "network_available": False, "redirect_chain_complete": False,
              "limitations": ["The target receives this device's request. No OneKit inspection server is used.", "HTTPS and HTTP headers do not establish a site's trustworthiness. This is not a malware, phishing, DNS or ownership check.", "Results describe one unauthenticated HTTP request; location, time, method and login state can change responses. Fragments are not sent over HTTP."]}
    try:
        response, hops = request_chain(url, "HEAD")
        if response.code in (405, 501):
            response.close()
            response, hops = request_chain(url, "GET")
            report["method"] = "GET (HEAD unsupported; body not read)"
        else:
            report["method"] = "HEAD"
        response.close()
        report.update(hops=hops, final_url=hops[-1]["url"], network_available=True, redirect_chain_complete=True)
    except (OSError, ValueError) as error:
        report["limitations"].append("Network inspection unavailable: " + str(error)[:400])
    return Result([Artifact("url-inspection.json", json.dumps(report, ensure_ascii=False, indent=2).encode())], details=report)


class Sources(HTMLParser):
    def __init__(self, kind, base):
        super().__init__(convert_charrefs=True)
        self.kind, self.base, self.links = kind, base, []
        self.audio_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        value = None
        if tag == "audio":
            self.audio_depth += 1
        if self.kind == "audio" and (tag == "audio" or tag == "source" and self.audio_depth):
            value = attrs.get("src")
        if self.kind == "image" and tag == "img":
            value = attrs.get("src") or attrs.get("data-src")
        if tag == "meta" and (attrs.get("property") or attrs.get("name", "")).lower() in ({"og:audio", "og:audio:url", "og:audio:secure_url"} if self.kind == "audio" else {"og:image", "og:image:url", "og:image:secure_url", "twitter:image"}):
            value = attrs.get("content")
        if value and len(self.links) < 8:
            try:
                url = validate_url(urllib.parse.urljoin(self.base, value))
                if url not in self.links and url != self.base:
                    self.links.append(url)
            except OneKitError:
                pass

    def handle_endtag(self, tag):
        if tag == "audio":
            self.audio_depth = max(0, self.audio_depth - 1)


def media_extension(data, kind):
    if kind == "image":
        if data.startswith(b"\x89PNG\r\n\x1a\n"):
            return "png"
        if data.startswith(b"\xff\xd8\xff"):
            return "jpg"
        if data.startswith((b"GIF87a", b"GIF89a")):
            return "gif"
        if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
            return "webp"
        if data.startswith((b"II*\0", b"MM\0*")):
            return "tiff"
        if data.startswith(b"BM"):
            return "bmp"
        if data.startswith(b"\0\0\1\0"):
            return "ico"
        if data[4:8] == b"ftyp" and data[8:12] in (b"avif", b"avis"):
            return "avif"
    else:
        if data.startswith(b"ID3") or len(data) > 1 and data[0] == 255 and data[1] & 0xE0 == 0xE0:
            return "aac" if not data.startswith(b"ID3") and data[1] & 0xF6 == 0xF0 else "mp3"
        if data.startswith(b"RIFF") and data[8:12] == b"WAVE":
            return "wav"
        if data.startswith(b"fLaC"):
            return "flac"
        if data.startswith(b"OggS") and b"theora" not in data[:512]:
            return "ogg"
        if data[4:8] == b"ftyp" and data[8:12] in (b"M4A ", b"M4B ", b"M4P "):
            return "m4a"
        if data.startswith(b"FORM") and data[8:12] in (b"AIFF", b"AIFC"):
            return "aiff"
    return None


def download_source(url, kind, limit):
    def fetch(address, allow_page):
        response, hops = request_chain(address)
        with response:
            if not 200 <= response.code < 300:
                raise OneKitError(f"The source returned HTTP {response.code}. Use a public direct file URL.")
            content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
            page = allow_page and content_type in ("text/html", "application/xhtml+xml")
            maximum = 1024 * 1024 if page else limit
            if int(response.headers.get("Content-Length", "0")) > maximum:
                raise OneKitError("The source exceeds the local download limit.")
            data = response.read(maximum + 1)
            if len(data) > maximum:
                raise OneKitError("The source exceeds the local download limit.")
            final = hops[-1]["url"]
            if page:
                parser = Sources(kind, final)
                parser.feed(data.decode("utf-8", errors="replace"))
                return parser.links
            extension = media_extension(data, kind)
            if not extension:
                raise OneKitError(f"The URL did not return a supported {kind} file. Protected streams, HTML and streaming playlists are not files.")
            return Result([Artifact(f"{kind}.{extension}", data)], details={"source_url": final, "bytes": len(data), "original_bytes": True})
    result = fetch(url, True)
    if isinstance(result, Result):
        return result
    failure = None
    for address in result:
        try:
            return fetch(address, False)
        except (OSError, ValueError) as error:
            failure = error
    raise OneKitError(f"No downloadable {kind} was exposed by this page. Use a public direct file URL. {str(failure)[:200] if failure else ''}")


def run(tool, files, options):
    url = validate_url(files[0].text())
    if tool.id == "url-inspect":
        return inspect_url(url)
    kind = "audio" if tool.id == "audio-download" else "image"
    format = options.get("format", "original")
    quality = str(options.get("quality", "192"))
    if kind == "audio" and (format not in ("original", "mp3") or quality not in ("64", "128", "192", "256", "320")):
        raise OneKitError("Choose original audio or MP3 at 64, 128, 192, 256 or 320 kbps.")
    try:
        result = download_source(url, kind, 128 * 1024 * 1024)
    except OSError as error:
        raise OneKitError("Cannot download directly from this source: " + str(error)[:300]) from error
    if kind == "audio" and format == "mp3":
        from ..api import execute
        result = execute("audio-convert", result.files, {"format": "mp3", "bitrate": quality + "k"})
        result.warnings.append("Re-encoding cannot improve the source's actual quality.")
    return result
