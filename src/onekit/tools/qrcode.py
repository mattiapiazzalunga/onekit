# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Local QR generation, contact/Wi-Fi payloads and image decoding."""
import base64
import io
import json
import re
from html import escape
from urllib.parse import urlsplit

from ..models import Artifact, OneKitError, Result, parse_json


def text(value):
    if not isinstance(value, str):
        raise OneKitError("QR fields must contain text.")
    if "\x00" in value:
        raise OneKitError("NUL characters are not supported in QR fields.")
    return value


def web_url(value):
    value = text(value).strip()
    try:
        url = urlsplit(value)
        valid = url.scheme in ("https", "http") and url.hostname and not url.username and not url.password
        valid = valid and (url.port is None or 0 < url.port < 65536)
    except ValueError:
        valid = False
    if not valid or any(char.isspace() for char in value):
        raise OneKitError("Enter a complete HTTP or HTTPS URL without credentials.")
    return value


def object_fields(value, allowed):
    if not isinstance(value, dict):
        raise OneKitError("Expected a JSON object.")
    if extra := value.keys() - set(allowed):
        raise OneKitError(f"Unknown field(s): {', '.join(sorted(extra))}.")
    return value


def wifi_payload(value):
    data = object_fields(value, ["ssid", "password", "security", "hidden", "identity", "anonymous_identity", "eap", "phase2"])
    ssid = text(data.get("ssid", ""))
    if not ssid or len(ssid.encode()) > 32:
        raise OneKitError("Wi-Fi SSID must contain 1–32 UTF-8 bytes.")
    security = data.get("security", "WPA")
    if security not in ("WPA", "WEP", "nopass", "SAE", "WPA2-EAP"):
        raise OneKitError("Choose WPA, WEP, nopass, SAE or WPA2-EAP security.")
    password = text(data.get("password", ""))
    if security != "nopass" and not password:
        raise OneKitError("Enter the Wi-Fi password, or choose an open network.")
    if not isinstance(data.get("hidden", False), bool):
        raise OneKitError("Wi-Fi hidden must be true or false.")
    escape = lambda value: re.sub(r'([\\;,:\"])', r"\\\1", text(value))
    parts = [f"T:{security}", f"S:{escape(ssid)}"]
    if security != "nopass":
        parts.append(f"P:{escape(password)}")
    parts.append(f"H:{str(data.get('hidden', False)).lower()}")
    if security == "WPA2-EAP":
        for key, token in (("eap", "E"), ("phase2", "PH2"), ("identity", "I"), ("anonymous_identity", "A")):
            if data.get(key):
                parts.append(f"{token}:{escape(data[key])}")
        if not data.get("identity") or not data.get("eap"):
            raise OneKitError("Enterprise Wi-Fi needs an identity and EAP method.")
    return "WIFI:" + ";".join(parts) + ";;"


def vescape(value):
    return text(value).replace("\\", "\\\\").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\\n").replace(";", "\\;").replace(",", "\\,")


def fold_line(line):
    # vCard folds at 75 octets; do not split a UTF-8 codepoint.
    lines, current = [], ""
    for char in line:
        if len((current + char).encode()) > 75:
            lines.append(current)
            current = " "
        current += char
    return "\r\n".join([*lines, current])


def vcard_payload(value):
    data = object_fields(value, ["version", "formatted_name", "first_name", "last_name", "middle_name", "prefix", "suffix", "nickname", "organization", "department", "title", "role", "birthday", "anniversary", "gender", "language", "timezone", "uid", "note", "categories", "phones", "emails", "urls", "addresses", "social_profiles", "photo_url", "latitude", "longitude"])
    version = data.get("version", "3.0")
    if version not in ("3.0", "4.0"):
        raise OneKitError("vCard version must be 3.0 or 4.0.")
    fn = data.get("formatted_name") or " ".join(text(data.get(key, "")).strip() for key in ("prefix", "first_name", "middle_name", "last_name", "suffix") if data.get(key)).strip()
    if not fn:
        raise OneKitError("Enter a display name or a first/last name.")
    lines = ["BEGIN:VCARD", "VERSION:" + version, "FN:" + vescape(fn), "N:" + ";".join(vescape(data.get(key, "")) for key in ("last_name", "first_name", "middle_name", "prefix", "suffix"))]
    for key, prop in (("nickname", "NICKNAME"), ("title", "TITLE"), ("role", "ROLE"), ("note", "NOTE"), ("uid", "UID"), ("timezone", "TZ"), ("language", "LANG")):
        if data.get(key):
            lines.append(prop + ":" + vescape(data[key]))
    if data.get("organization") or data.get("department"):
        lines.append("ORG:" + vescape(data.get("organization", "")) + ";" + vescape(data.get("department", "")))
    for key, prop in (("birthday", "BDAY"), ("anniversary", "ANNIVERSARY")):
        if data.get(key):
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text(data[key])):
                raise OneKitError(f"{key} must use YYYY-MM-DD.")
            from datetime import date
            date.fromisoformat(data[key])
            lines.append((prop if version == "4.0" or key == "birthday" else "X-ANNIVERSARY") + ":" + data[key])
    if data.get("gender"):
        if data["gender"] not in ("M", "F", "O", "N", "U"):
            raise OneKitError("Gender must be M, F, O, N or U.")
        lines.append(("GENDER" if version == "4.0" else "X-GENDER") + ":" + data["gender"])
    if data.get("categories"):
        if not isinstance(data["categories"], list):
            raise OneKitError("Categories must be an array of text values.")
        lines.append("CATEGORIES:" + ",".join(vescape(item) for item in data["categories"]))
    group_number = 0
    for key, prop in (("phones", "TEL"), ("emails", "EMAIL"), ("urls", "URL"), ("social_profiles", "X-SOCIALPROFILE"), ("addresses", "ADR")):
        entries = data.get(key, [])
        if not isinstance(entries, list) or len(entries) > 20:
            raise OneKitError(f"{key} must be an array with at most 20 entries.")
        for entry in entries:
            if isinstance(entry, str):
                entry = {"value": entry}
            object_fields(entry, ["value", "type", "preferred", "label", "po_box", "extended", "street", "city", "region", "postal_code", "country"])
            kind = text(entry.get("type", "home"))
            if not re.fullmatch(r"[a-zA-Z0-9-]+(?:,[a-zA-Z0-9-]+)*", kind):
                raise OneKitError("Contact types must contain letters, numbers, hyphens or commas.")
            header = prop + (";VALUE=text" if version == "4.0" and key == "phones" else "") + ";TYPE=" + kind.upper()
            if not isinstance(entry.get("preferred", False), bool):
                raise OneKitError("Contact preferred must be true or false.")
            if entry.get("preferred"):
                header += ";PREF=1" if version == "4.0" else ",PREF"
            if entry.get("label"):
                group_number += 1
                header = f"item{group_number}." + header
                # RFC 6868 parameter encoding; v3 labels use a separate property below.
                label = text(entry["label"]).replace("^", "^^").replace('"', "^'").replace("\r", "").replace("\n", "^n")
                if version == "4.0" and key == "addresses":
                    header += ';LABEL="' + label + '"'
            if key == "addresses":
                content = ";".join(vescape(entry.get(field, "")) for field in ("po_box", "extended", "street", "city", "region", "postal_code", "country"))
            else:
                content = text(entry.get("value", ""))
                if not content:
                    raise OneKitError(f"Every {key} entry needs a value.")
                if key in ("urls", "social_profiles"):
                    content = web_url(content)
                if key not in ("urls", "social_profiles"):
                    content = vescape(content)
            lines.append(header + ":" + content)
            if entry.get("label"):
                lines.append(f"item{group_number}.X-ABLabel:" + vescape(entry["label"]))
            if entry.get("label") and version == "3.0" and key == "addresses":
                lines.append("LABEL;TYPE=" + kind.upper() + ":" + vescape(entry["label"]))
    if data.get("photo_url"):
        lines.append(("PHOTO;VALUE=uri:" if version == "3.0" else "PHOTO:") + web_url(data["photo_url"]))
    if "latitude" in data or "longitude" in data:
        lat, lon = float(data.get("latitude", "nan")), float(data.get("longitude", "nan"))
        if not -90 <= lat <= 90 or not -180 <= lon <= 180:
            raise OneKitError("Enter valid latitude and longitude coordinates.")
        lines.append(f"GEO:geo:{lat},{lon}" if version == "4.0" else f"GEO:{lat};{lon}")
    lines.append("END:VCARD")
    return "\r\n".join(fold_line(line) for line in lines) + "\r\n"


def make_payload(tool_id, file):
    raw = file.text()
    if tool_id == "url-to-qrcode":
        return web_url(raw)
    if tool_id == "wifi-to-qrcode":
        return wifi_payload(parse_json(raw))
    if tool_id == "vcard-to-qrcode":
        if file.kind == "vcf":
            if not raw.strip().startswith("BEGIN:VCARD") or not raw.strip().endswith("END:VCARD"):
                raise OneKitError("Expected a complete vCard file.")
            return raw
        return vcard_payload(parse_json(raw))
    if not raw:
        raise OneKitError("Enter content for the QR code.")
    return raw


def split_escaped(value, delimiter):
    parts, current, escaped = [], "", False
    for char in value:
        if escaped:
            current += "\n" if char in ("n", "N") else char
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == delimiter:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current + ("\\" if escaped else ""))
    return parts


def describe_payload(raw):
    if raw.startswith("WIFI:"):
        fields = dict(part.split(":", 1) for part in split_escaped(raw[5:], ";") if ":" in part)
        data = {key: fields.get(token, "") for key, token in (("ssid", "S"), ("security", "T"), ("password", "P"), ("identity", "I"), ("eap", "E"), ("phase2", "PH2"), ("anonymous_identity", "A"))}
        data["hidden"] = fields.get("H", "false").lower() == "true"
        return {"text": raw, "type": "wifi", "data": data}
    if raw.strip().startswith("BEGIN:VCARD"):
        unfolded = re.sub(r"\r?\n[ \t]", "", raw)
        properties = []
        for line in unfolded.splitlines():
            if ":" in line:
                header, value = line.split(":", 1)
                properties.append({"name": header.split(";")[0], "parameters": header.split(";")[1:], "value": value})
        return {"text": raw, "type": "vcard", "data": {"properties": properties}}
    try:
        return {"text": raw, "type": "json", "data": parse_json(raw)}
    except (OneKitError, ValueError):
        pass
    try:
        web_url(raw)
        return {"text": raw, "type": "url", "data": {"url": raw}}
    except OneKitError:
        return {"text": raw, "type": "text", "data": raw}


def decode_result(tool_id, texts):
    codes = [describe_payload(raw) for raw in texts]
    if not codes:
        raise OneKitError("No readable QR code found. Use a sharper image with the complete code and its border.")
    report = {"count": len(codes), "codes": codes}
    if tool_id == "qrcode-to-vcard":
        from .contacts import extract_vcard
        return Result([Artifact(f"contact-{index}.vcf", extract_vcard(raw).encode())
                       for index, raw in enumerate(texts, 1)], details=report)
    if tool_id == "qrcode-to-text":
        return Result([Artifact("decoded.txt", "\n".join(texts).encode())], details=report)
    data = codes[0]["data"] if tool_id == "qrcode-to-json" and len(codes) == 1 and codes[0]["type"] == "json" else report
    return Result([Artifact("decoded.json", json.dumps(data, ensure_ascii=False, indent=2).encode())], details=report)


def center_box(matrix, percent):
    """Find the nearest central data-only square, preserving every function pattern."""
    from segno.consts import TYPE_DATA_DARK, TYPE_DATA_LIGHT
    n = len(matrix)
    summed = [[0] * (n + 1) for _ in range(n + 1)]
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            summed[y + 1][x + 1] = (value not in (TYPE_DATA_DARK, TYPE_DATA_LIGHT)) + summed[y][x + 1] + summed[y + 1][x] - summed[y][x]
    for side in range(max(3, int(n * percent / 100)), 2, -1):
        positions = sorted(((x, y) for y in range(n // 4, n * 3 // 4 - side + 1)
                            for x in range(n // 4, n * 3 // 4 - side + 1)),
                           key=lambda pos: (pos[0] + side / 2 - n / 2) ** 2 + (pos[1] + side / 2 - n / 2) ** 2)
        for x, y in positions:
            if summed[y + side][x + side] - summed[y][x + side] - summed[y + side][x] + summed[y][x] == 0:
                return x, y, side
    raise OneKitError("No space for a center mark in this QR code. Shorten the content or remove the center mark.")


def center_image(value):
    from PIL import Image, ImageOps
    if not isinstance(value, str) or len(value) > 2800000:
        raise OneKitError("Choose a PNG or JPEG center image up to 2 MiB.")
    try:
        data = base64.b64decode(value, validate=True)
        if not data or len(data) > 2 * 1024 * 1024:
            raise ValueError("size")
        with Image.open(io.BytesIO(data)) as source:
            if source.format not in ("PNG", "JPEG") or source.width * source.height > 4000000:
                raise ValueError("format or dimensions")
            image = ImageOps.exif_transpose(source).convert("RGBA")
        image.thumbnail((512, 512), Image.Resampling.LANCZOS)
        return image
    except Exception as exc:
        raise OneKitError("Choose a valid PNG or JPEG center image, up to 2 MiB and 4 million pixels.") from exc


def rounded_path(x, y, side, radius):
    r = radius
    return f"M{x+r} {y}h{side-2*r}a{r} {r} 0 0 1 {r} {r}v{side-2*r}a{r} {r} 0 0 1 {-r} {r}h{-side+2*r}a{r} {r} 0 0 1 {-r} {-r}v{-side+2*r}a{r} {r} 0 0 1 {r} {-r}z"


def styled_image(qr, fmt, scale, border, dark, light, shape, corners="square", center=None):
    """Style modules and finder corners; keep the center clear of function patterns."""
    from PIL import Image, ImageDraw, ImageFont
    from segno.consts import TYPE_DATA_DARK, TYPE_FINDER_PATTERN_DARK

    matrix = list(qr.matrix_iter(border=0, verbose=True))
    n = len(matrix)
    size = n + border * 2
    box = center_box(matrix, center["size"]) if center else None
    modules = []
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if not value >> 8 or corners == "rounded" and value == TYPE_FINDER_PATTERN_DARK:
                continue
            if box and box[0] <= x < box[0] + box[2] and box[1] <= y < box[1] + box[2]:
                continue
            modules.append((x + border, y + border, shape if value == TYPE_DATA_DARK else "square"))
    finders = [(border, border), (border + n - 7, border), (border, border + n - 7)] if corners == "rounded" else []
    if fmt == "svg":
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size * scale}" height="{size * scale}" viewBox="0 0 {size} {size}">']
        if light is not None:
            parts.append(f'<path fill="{light}" d="M0 0h{size}v{size}H0z"/>')
        parts.append(f'<g fill="{dark}">')
        for x, y, kind in modules:
            if kind == "dots":
                parts.append(f'<circle cx="{x + .5}" cy="{y + .5}" r="0.5"/>')
            else:
                radius = ' rx="0.25"' if kind == "rounded" else ""
                parts.append(f'<rect x="{x}" y="{y}" width="1" height="1"{radius}/>')
        for x, y in finders:
            parts.append(f'<path fill-rule="evenodd" d="{rounded_path(x,y,7,1.5)}{rounded_path(x+1,y+1,5,.8)}"/><rect x="{x+2}" y="{y+2}" width="3" height="3" rx="0.6"/>')
        parts.append("</g>")
        if center:
            x, y, side = box
            x, y = x + border, y + border
            parts.append(f'<rect x="{x}" y="{y}" width="{side}" height="{side}" rx="0.4" fill="{light or "#ffffff"}"/>')
            if "image" in center:
                stream = io.BytesIO()
                center["image"].save(stream, format="PNG")
                data = base64.b64encode(stream.getvalue()).decode()
                parts.append(f'<image x="{x+.5}" y="{y+.5}" width="{side-1}" height="{side-1}" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}"/>')
            else:
                font_size = min((side - 1) / max(1, len(center["text"]) * .7), (side - 1) * .6)
                parts.append(f'<text x="{x+side/2}" y="{y+side/2}" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="{font_size}" font-weight="bold" textLength="{min(side-1,len(center["text"])*font_size*.7)}" lengthAdjust="spacingAndGlyphs" fill="{dark}">{escape(center["text"])}</text>')
        return ("".join(parts) + "</svg>").encode()

    unit = scale * 3
    image = Image.new("RGBA" if light is None else "RGB", (size * unit, size * unit), light or (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    for x, y, kind in modules:
        bounds = (x * unit, y * unit, (x + 1) * unit - 1, (y + 1) * unit - 1)
        if kind == "dots":
            draw.ellipse(bounds, fill=dark)
        elif kind == "rounded":
            draw.rounded_rectangle(bounds, radius=unit / 4, fill=dark)
        else:
            draw.rectangle(bounds, fill=dark)
    for x, y in finders:
        for offset, side, radius, fill in [(0, 7, 1.5, dark), (1, 5, .8, light or (0,0,0,0)), (2, 3, .6, dark)]:
            draw.rounded_rectangle(((x+offset)*unit, (y+offset)*unit, (x+offset+side)*unit-1, (y+offset+side)*unit-1), radius=radius*unit, fill=fill)
    if center:
        x, y, side = box
        x, y = (x + border) * unit, (y + border) * unit
        extent = side * unit
        draw.rounded_rectangle((x,y,x+extent-1,y+extent-1), radius=unit*.4, fill=light or "#ffffff")
        if "image" in center:
            stamp = center["image"].copy()
            ratio = (extent-unit) / max(stamp.size)
            stamp = stamp.resize((max(1,round(stamp.width*ratio)),max(1,round(stamp.height*ratio))), Image.Resampling.LANCZOS)
            image.paste(stamp, (x+(extent-stamp.width)//2,y+(extent-stamp.height)//2), stamp)
        else:
            font_size = max(1, int(extent*.6))
            while True:
                font = ImageFont.load_default(size=font_size)
                bounds = draw.textbbox((0,0), center["text"], font=font)
                if bounds[2]-bounds[0] <= extent-unit or font_size <= 1:
                    break
                font_size -= 1
            draw.text((x+(extent-bounds[2]+bounds[0])/2-bounds[0],y+(extent-bounds[3]+bounds[1])/2-bounds[1]), center["text"], fill=dark, font=font)
    image = image.resize((size * scale, size * scale), Image.Resampling.LANCZOS)
    stream = io.BytesIO()
    if fmt == "jpeg":
        image.save(stream, format="JPEG", quality=95, subsampling=0)
    else:
        image.save(stream, format="PNG")
    return stream.getvalue()


def run(tool, files, options):
    if tool.id in ("scan-qrcode", "reverse-qrcode", "qrcode-to-text", "qrcode-to-json", "qrcode-to-vcard"):
        import zxingcpp
        from PIL import Image, ImageOps
        with Image.open(io.BytesIO(files[0].data)) as source:
            image = ImageOps.exif_transpose(source).convert("RGBA")
            image = Image.alpha_composite(Image.new("RGBA", image.size, "white"), image).convert("RGB")
            results = zxingcpp.read_barcodes(image, formats=zxingcpp.BarcodeFormat.QRCode, try_rotate=True, try_invert=True)
        return decode_result(tool.id, list(dict.fromkeys(result.text for result in results if result.valid)))
    import segno
    payload = make_payload(tool.id, files[0])
    fmt = options.get("format", "png")
    shape = options.get("shape", "square")
    if shape not in ("square", "rounded", "dots"):
        raise OneKitError("Choose square, rounded or dots for the QR module shape.")
    corners = options.get("corner_style", "square")
    if corners not in ("square", "rounded"):
        raise OneKitError("Choose square or rounded QR corners.")
    overlay_type = options.get("overlay_type", "none")
    if overlay_type not in ("none", "image", "text"):
        raise OneKitError("Choose none, image or text for the center mark.")
    center = None
    if overlay_type != "none":
        percent = int(options.get("overlay_size", 16))
        if not 10 <= percent <= 20:
            raise OneKitError("Center size must be 10–20 percent.")
        center = {"type": overlay_type, "size": percent}
        if overlay_type == "image":
            center["image"] = center_image(options.get("overlay_image_base64", ""))
        else:
            label = text(options.get("overlay_text", "")).strip()
            if not 1 <= len(label) <= 16 or any(ord(char) < 32 for char in label):
                raise OneKitError("Enter 1–16 characters for the center text, without line breaks.")
            center["text"] = label
            if options.get("overlay_image_base64"):
                center["image"] = center_image(options["overlay_image_base64"])
    error = "H" if center else options.get("error_correction", "M")
    if fmt not in ("png", "jpeg", "svg") or error not in ("L", "M", "Q", "H"):
        raise OneKitError("Choose PNG, JPEG or SVG and error correction L, M, Q or H.")
    scale, border = int(options.get("scale", 8)), int(options.get("border", 4))
    if not 2 <= scale <= 16 or not 4 <= border <= 16:
        raise OneKitError("QR scale must be 2–16 and quiet-zone border 4–16 modules.")
    dark, light = options.get("dark", "#000000"), options.get("light", "#ffffff")
    transparent = options.get("transparent_background", False)
    if transparent not in (True, False, "true", "false"):
        raise OneKitError("Transparent background must be true or false.")
    transparent = transparent in (True, "true")
    if fmt == "jpeg" and transparent:
        raise OneKitError("JPEG does not support transparency. Choose PNG or SVG, or use a solid background.")
    def luminance(color):
        if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
            raise OneKitError("QR colors must be six-digit hexadecimal colors.")
        channels = [int(color[index:index+2], 16)/255 for index in (1, 3, 5)]
        return sum(weight * (part/12.92 if part <= .04045 else ((part+.055)/1.055)**2.4) for weight, part in zip((.2126, .7152, .0722), channels))
    foreground, background = luminance(dark), luminance("#ffffff" if transparent else light)
    if foreground >= background or (background+.05)/(foreground+.05) < 4.5:
        raise OneKitError("Use dark modules on a light background with contrast of at least 4.5:1.")
    if transparent:
        light = None
    try:
        qr = segno.make(payload, error=error, micro=False, encoding="utf-8", boost_error=False)
    except segno.DataOverflowError as exc:
        raise OneKitError("Content exceeds QR capacity. Shorten it or lower error correction; photos must use a URL.") from exc
    stream = io.BytesIO()
    if shape == "square" and corners == "square" and not center and fmt != "jpeg":
        qr.save(stream, kind=fmt, scale=scale, border=border, dark=dark, light=light)
    else:
        stream.write(styled_image(qr, fmt, scale, border, dark, light, shape, corners, center))
    outputs = [Artifact(f"qrcode.{fmt}", stream.getvalue())]
    if options.get("include_payload") in (True, "true"):
        suffix = "vcf" if tool.id == "vcard-to-qrcode" else "txt"
        outputs.append(Artifact(f"payload.{suffix}", payload.encode()))
    return Result(outputs, details={"payload": payload, "bytes": len(payload.encode()), "version": qr.version, "errorCorrection": error, "modules": len(qr.matrix), "shape": shape, "transparentBackground": transparent, "cornerStyle": corners, "overlayType": overlay_type})
