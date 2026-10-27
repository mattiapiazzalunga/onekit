# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Perceptual sRGB palettes using Oklab/OKLCH and WCAG relative luminance.

References: https://bottosson.github.io/posts/oklab/
https://www.w3.org/TR/css-color-4/#ok-lab
https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio
Harmony angles are design heuristics, not guarantees of aesthetic quality.
"""
import json
import math
import re

from ..models import Artifact, OneKitError, Result

HARMONIES = {
    "analogous": (-60, -30, 0, 30, 60),
    "complementary": (0, 0, 0, 180, 180),
    "split-complementary": (0, 0, 0, 150, 210),
    "triadic": (0, 0, 0, 120, 240),
    "tetradic": (90, 0, 0, 180, 270),
    "monochromatic": (0, 0, 0, 0, 0),
}


def linear(value):
    return value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4


def coordinates(color):
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise OneKitError("Use a six-digit hexadecimal color such as #6750A4.")
    rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = map(linear, rgb)
    l = (.4122214708*r + .5363325363*g + .0514459929*b) ** (1/3)
    m = (.2119034982*r + .6806995451*g + .1073969566*b) ** (1/3)
    s = (.0883024619*r + .2817188376*g + .6299787005*b) ** (1/3)
    light = .2104542553*l + .793617785*m - .0040720468*s
    a = 1.9779984951*l - 2.428592205*m + .4505937099*s
    bb = .0259040371*l + .7827717662*m - .808675766*s
    return light, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def rgb_linear(light, chroma, hue):
    a, b = chroma*math.cos(math.radians(hue)), chroma*math.sin(math.radians(hue))
    l = (light + .3963377774*a + .2158037573*b) ** 3
    m = (light - .1055613458*a - .0638541728*b) ** 3
    s = (light - .0894841775*a - 1.291485548*b) ** 3
    return (4.0767416621*l-3.3077115913*m+.2309699292*s,
            -1.2684380046*l+2.6097574011*m-.3413193965*s,
            -.0041960863*l-.7034186147*m+1.707614701*s)


def to_hex(light, chroma, hue):
    # Constant-lightness/hue chroma reduction; not CSS local-MINDE mapping.
    low, high = 0., chroma
    if all(-1e-7 <= v <= 1+1e-7 for v in rgb_linear(light, chroma, hue)):
        low = high
    else:
        for _ in range(24):
            middle = (low+high)/2
            if all(-1e-7 <= v <= 1+1e-7 for v in rgb_linear(light, middle, hue)):
                low = middle
            else:
                high = middle
    rgb = rgb_linear(light, low, hue)
    def encode(v):
        v = min(1., max(0., v))
        return round(255*(12.92*v if v <= .0031308 else 1.055*v**(1/2.4)-.055))
    return "#" + "".join(f"{encode(v):02X}" for v in rgb)


def luminance(color):
    return sum(weight*linear(int(color[i:i+2], 16)/255)
               for weight, i in zip((.2126, .7152, .0722), (1, 3, 5)))


def contrast(first, second):
    return _contrast_ratio(luminance(first), luminance(second))


def _contrast_ratio(first, second):
    a, b = (first, second) if first <= second else (second, first)
    return (b+.05)/(a+.05)


def palette(base, harmony="analogous", lightness=None, chroma=None, hue_override=None):
    light, sat, hue = coordinates(base)
    if harmony not in HARMONIES:
        raise OneKitError("Unknown color harmony.")
    for value, maximum in ((lightness, 1), (chroma, .4), (hue_override, 360)):
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= maximum):
            raise OneKitError("Lightness must be 0–1, chroma 0–0.4 and hue 0–360.")
    light = light if lightness is None else lightness
    sat = sat if chroma is None else chroma
    hue = hue if hue_override is None else hue_override
    colors, luminances = [], []
    black_luminance, white_luminance = luminance("#000000"), luminance("#FFFFFF")
    for i, angle in enumerate(HARMONIES[harmony]):
        shift = ((-.24, -.12, 0, .12, .24)[i] if harmony == "monochromatic"
                 else (-.16, .16, 0, -.08, .08)[i] if harmony != "analogous" else 0)
        # Keep the selected base at index 2 for every scheme.
        if i == 2:
            color = base.upper() if lightness is None and chroma is None and hue_override is None else to_hex(light, sat, hue)
        else:
            color = to_hex(min(1, max(0, light+shift)), sat, hue+angle)
        value = luminance(color)
        luminances.append(value)
        black, white = _contrast_ratio(value, black_luminance), _contrast_ratio(value, white_luminance)
        ratio = max(black, white)
        colors.append({"hex": color, "oklch": list(coordinates(color)),
                       "text": "#000000" if black >= white else "#FFFFFF",
                       "contrast": ratio, "wcag_aa": ratio >= 4.5, "wcag_aaa": ratio >= 7})
    return {"base": base.upper(), "harmony": harmony, "colors": colors,
            "contrast_matrix": [[_contrast_ratio(a, b) for b in luminances] for a in luminances]}


def run(tool, files, options):
    result = palette(files[0].text().strip(), options.get("harmony", "analogous"),
                     options.get("lightness"), options.get("chroma"), options.get("hue"))
    format = options.get("format", "json")
    if format not in ("json", "css", "svg"):
        raise OneKitError("Choose JSON, CSS or SVG output.")
    if format == "css":
        text = ":root {\n" + "".join(f"  --color-{i+1}: {c['hex']};\n" for i, c in enumerate(result["colors"])) + "}\n"
    elif format == "svg":
        text = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 240" role="img" aria-label="Color palette">'
        for i, color in enumerate(result["colors"]):
            text += f'<rect x="{i*200}" width="200" height="240" fill="{color["hex"]}"/><text x="{i*200+100}" y="210" text-anchor="middle" font-family="sans-serif" font-size="22" fill="{color["text"]}">{color["hex"]}</text>'
        text += '</svg>'
    else:
        text = json.dumps(result, indent=2) + "\n"
    return Result([Artifact("palette." + format, text.encode())], details=result)
