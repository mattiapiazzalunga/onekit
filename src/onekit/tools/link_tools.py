# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Device-to-source downloads and HTTP inspection; no intermediary server."""
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

from ..models import Artifact, OneKitError, Result
from .video_download import validate_url

REDIRECTS = (301, 302, 303, 307, 308)
HEADERS = ("content-type", "content-length", "location", "server", "cache-control", "expires", "last-modified", "etag", "content-encoding", "strict-transport-security", "content-security-policy", "x-content-type-options", "referrer-policy", "access-control-allow-origin")


def download_target(value, kind):
    """Resolve common search-result wrappers without fetching the search page."""
    if kind not in ('image', 'audio', 'video'):
        raise OneKitError('Choose image, audio or video.')
    url = validate_url(value)
    for _ in range(5):
        parsed = urllib.parse.urlsplit(url)
        host = (parsed.hostname or '').lower().rstrip('.')
        google = re.fullmatch(r'(?:[a-z0-9-]+\.)*google\.(?:com|[a-z]{2,3}|co\.[a-z]{2}|com\.[a-z]{2})', host)
        if not google:
            break
        query = dict(urllib.parse.parse_qsl(parsed.query, max_num_fields=1000))
        target = query.get('imgurl') if kind == 'image' else None
        if not target and parsed.path == '/url':
            target = query.get('url') or query.get('q')
        if not target or target == url:
            break
        url = validate_url(target)
    host = (urllib.parse.urlsplit(url).hostname or '').lower().rstrip('.')
    youtube = host in ('youtu.be','youtube.com','youtube-nocookie.com') or host.endswith(('.youtube.com','.youtube-nocookie.com'))
    return {'url':url, 'requires_extractor':kind == 'video' and youtube, 'site':'youtube' if youtube else None}


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
        self.featured, self.picture_depth, self.base_seen = [], 0, False
        self.audio_depth = 0
        self.structured = None

    def add(self, value, priority=False):
        links = self.featured if priority else self.links
        if isinstance(value, str) and value and len(links) < (8 if priority else 32):
            try:
                url = validate_url(urllib.parse.urljoin(self.base, value))
                if url not in links and url != self.base:
                    links.append(url)
            except OneKitError:
                pass

    def structured_sources(self, value, depth=0):
        if depth > 16:
            return
        if isinstance(value, list):
            for item in value[:64]:
                self.structured_sources(item, depth+1)
        elif isinstance(value, dict):
            types = value.get("@type", [])
            if isinstance(types, str):
                types = [types]
            expected = {"audio": "AudioObject", "video": "VideoObject", "image": "ImageObject"}[self.kind]
            if isinstance(types, list) and expected in types:
                self.add(value.get("contentUrl"), priority=self.kind == "image")
            for key in ("@graph", self.kind):
                self.structured_sources(value.get(key), depth+1)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self.structured = []
        if tag == 'base' and not self.base_seen and attrs.get('href'):
            try:
                self.base = validate_url(urllib.parse.urljoin(self.base, attrs['href']))
                self.base_seen = True
            except OneKitError:
                pass
        if tag == 'picture':
            self.picture_depth += 1
        value = None
        if tag == self.kind and self.kind in ("audio", "video"):
            self.audio_depth += 1
        if self.kind in ("audio", "video") and (tag == self.kind or tag == "source" and self.audio_depth):
            value = attrs.get("src")
        if self.kind == "image" and (tag == "img" or tag == "source" and self.picture_depth):
            srcset = attrs.get('data-srcset') or attrs.get('srcset', '')
            candidates = []
            for item in srcset.split(',')[:32]:
                parts = item.strip().split()
                if parts:
                    descriptor = parts[-1] if len(parts) > 1 else '1x'
                    match = re.fullmatch(r'([0-9]+(?:\.[0-9]+)?)[wx]', descriptor)
                    candidates.append((float(match[1]) if match else 0, parts[0]))
            for _, address in sorted(candidates, key=lambda item: -item[0]):
                self.add(address)
            for key in ('data-src', 'data-original', 'data-lazy-src', 'src'):
                self.add(attrs.get(key))
        properties = {"audio": {"og:audio", "og:audio:url", "og:audio:secure_url"},
                      "video": {"og:video", "og:video:url", "og:video:secure_url", "twitter:player:stream"},
                      "image": {"og:image", "og:image:url", "og:image:secure_url", "twitter:image"}}
        if tag == "meta" and (attrs.get("property") or attrs.get("name", "")).lower() in properties[self.kind]:
            self.add(attrs.get("content"), priority=self.kind == "image")
        self.add(value)

    def handle_data(self, data):
        if self.structured is not None:
            self.structured.append(data)

    def handle_endtag(self, tag):
        if tag == "picture":
            self.picture_depth = max(0, self.picture_depth-1)
        if tag == "script" and self.structured is not None:
            try:
                self.structured_sources(json.loads("".join(self.structured)))
            except (ValueError, RecursionError):
                pass
            self.structured = None
        if tag == self.kind and self.kind in ("audio", "video"):
            self.audio_depth = max(0, self.audio_depth - 1)


def source_links(html, base, kind):
    if kind not in ("audio", "video", "image"):
        raise OneKitError("Choose audio, video or image source extraction.")
    parser = Sources(kind, validate_url(base))
    parser.feed(html)
    parser.close()
    return list(dict.fromkeys([*parser.featured, *parser.links]))[:8]


def media_extension(data, kind):
    if kind == "video":
        if data[4:8] == b"ftyp":
            return "mov" if data[8:12] == b"qt  " else "mp4"
        if data.startswith(b"\x1aE\xdf\xa3"):
            return "webm" if b"webm" in data[:4096] else "mkv"
        if data.startswith(b"OggS") and b"theora" in data[:512]:
            return "ogv"
        if data.startswith((b"\x00\x00\x01\xba", b"\x00\x00\x01\xb3")):
            return "mpeg"
        if len(data) > 188 and data[0] == data[188] == 0x47:
            return "ts"
        return None
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
    url = download_target(url, kind)['url']
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
                return source_links(data.decode("utf-8", errors="replace"), final, kind)
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
