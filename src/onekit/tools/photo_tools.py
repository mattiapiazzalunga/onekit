# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Color sampling, median-cut palettes, vector tiles and bounded image restoration."""
import io
import json
import math

from ..models import Artifact, OneKitError, Result, output, parse_json
from .design import contrast, coordinates
from .images import encode, open_image


def number(options, name, default, low, high, integer=False):
    value = options.get(name, default)
    try:
        if isinstance(value, bool):
            raise TypeError
        parsed = float(value)
        if not math.isfinite(parsed) or not low <= parsed <= high or integer and parsed != int(parsed):
            raise ValueError
        return int(parsed) if integer else parsed
    except (ValueError, TypeError, OverflowError):
        raise OneKitError(f"{name} must be {'an integer' if integer else 'a number'} between {low} and {high}.") from None


def visible_rgb(image):
    from PIL import Image
    rgba = image.convert("RGBA")
    base = Image.new("RGBA", rgba.size, "white")
    return Image.alpha_composite(base, rgba).convert("RGB")


def color_info(rgb):
    color = "#" + "".join(f"{v:02X}" for v in rgb)
    black, white = contrast(color, "#000000"), contrast(color, "#FFFFFF")
    return {"hex": color, "rgb": list(rgb), "oklch": list(coordinates(color)),
            "text": "#000000" if black >= white else "#FFFFFF", "contrast": max(black, white)}


def extract(image, count):
    from PIL import Image
    # Exclude fully transparent pixels; partially transparent pixels are composited on white.
    sample = image.convert("RGBA")
    sample.thumbnail((256, 256), Image.Resampling.LANCZOS)
    pixels = [pixel for pixel in (sample.get_flattened_data() if hasattr(sample, "get_flattened_data") else sample.getdata()) if pixel[3] > 0]
    if not pixels:
        raise OneKitError("This image has no visible pixels.")
    strip = Image.new("RGBA", (len(pixels), 1))
    strip.putdata(pixels)
    indexed = visible_rgb(strip).quantize(colors=count, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    palette = indexed.getpalette()
    return [{**color_info(palette[index*3:index*3+3]), "fraction": total/len(pixels)}
            for total, index in sorted(indexed.getcolors(), key=lambda pair: (-pair[0], pair[1]))]


def vectorize(image, count, resolution):
    from PIL import Image
    rgb = visible_rgb(image)
    rgb.thumbnail((resolution, resolution), Image.Resampling.LANCZOS)
    indexed = rgb.quantize(colors=count, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    width, height = indexed.size
    pixels, palette = list(indexed.get_flattened_data() if hasattr(indexed, "get_flattened_data") else indexed.getdata()), indexed.getpalette()
    # Merge equal horizontal palette runs vertically into filled vector rectangles.
    active, rectangles = {}, []
    for y in range(height):
        runs, x = {}, 0
        while x < width:
            start, color = x, pixels[y*width+x]
            while x < width and pixels[y*width+x] == color:
                x += 1
            key = (start, x, color)
            runs[key] = (active.pop(key)[0], y+1) if key in active else (y, y+1)
        rectangles.extend((key, bounds) for key, bounds in active.items())
        active = runs
    rectangles.extend(active.items())
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{image.width}" height="{image.height}" viewBox="0 0 {width} {height}" shape-rendering="crispEdges">']
    for (left, right, color), (top, bottom) in rectangles:
        hex_color = "#" + "".join(f"{v:02x}" for v in palette[color*3:color*3+3])
        parts.append(f'<path fill="{hex_color}" d="M{left} {top}h{right-left}v{bottom-top}H{left}z"/>')
    parts.append('</svg>')
    return ''.join(parts).encode(), len(rectangles)


def restore(image, regions, iterations):
    import numpy as np
    from PIL import Image, ImageDraw
    if isinstance(regions, str):
        regions = parse_json(regions)
    if not isinstance(regions, list) or not 1 <= len(regions) <= 100:
        raise OneKitError("Select 1–100 areas to reconstruct.")
    mask_image = Image.new("L", image.size)
    draw = ImageDraw.Draw(mask_image)
    for region in regions:
        if not isinstance(region, dict) or isinstance(region.get("page"), bool) or region.get("page", 1) != 1:
            raise OneKitError("Image regions must use page 1.")
        values = [region.get(key) for key in ("x", "y", "width", "height")]
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
            raise OneKitError("Region coordinates must be finite numbers normalized to 0–1.")
        x, y, w, h = values
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x+w > 1+1e-9 or y+h > 1+1e-9:
            raise OneKitError("Reconstruction areas must fit inside the image.")
        box = (math.floor(x*image.width), math.floor(y*image.height), min(image.width-1, math.ceil((x+w)*image.width)-1), min(image.height-1, math.ceil((y+h)*image.height)-1))
        draw.rectangle(box, fill=255)
    mask = np.array(mask_image) > 0
    selected_pixels = int(mask.sum())
    if selected_pixels > image.width*image.height*.35:
        raise OneKitError("Reconstruct at most 35% of the image; choose smaller areas.")
    rgba = image.convert("RGBA")
    source = np.array(rgba)
    # Solve the discrete Laplace equation with fixed surrounding pixels.
    # Operate only on a padded bounding box, never on unrelated image regions.
    bounds = mask_image.getbbox()
    left, top, right, bottom = max(0, bounds[0]-2), max(0, bounds[1]-2), min(image.width, bounds[2]+2), min(image.height, bounds[3]+2)
    local = mask[top:bottom, left:right]
    if local.size > 1000000:
        raise OneKitError("Selected areas span more than one million pixels. Process nearby areas separately.")
    rgb = source[top:bottom, left:right, :3].astype(np.float32)
    if not (~local).any():
        raise OneKitError("Keep visible pixels around the selected area.")
    rgb[local] = rgb[~local].mean(axis=0)
    pad = np.empty((rgb.shape[0]+2, rgb.shape[1]+2, 3), dtype=rgb.dtype)
    average = np.empty_like(rgb)
    for _ in range(iterations):
        pad[1:-1, 1:-1] = rgb
        pad[0, 1:-1], pad[-1, 1:-1] = rgb[0], rgb[-1]
        pad[1:-1, 0], pad[1:-1, -1] = rgb[:, 0], rgb[:, -1]
        # Preserve the original float32 operation order, reusing the buffers.
        np.add(pad[:-2, 1:-1], pad[2:, 1:-1], out=average)
        np.add(average, pad[1:-1, :-2], out=average)
        np.add(average, pad[1:-1, 2:], out=average)
        np.multiply(average, .25, out=average)
        rgb[local] = average[local]
    source[top:bottom, left:right, :3][local] = np.clip(np.rint(rgb[local]), 0, 255).astype(np.uint8)
    return Image.fromarray(source), selected_pixels


def run(tool, files, options):
    from PIL import Image, ImageFilter
    file = files[0]
    if tool.id == "color-picker" and file.kind == "txt":
        color = file.text().strip()
        coordinates(color)
        report = color_info([int(color[i:i+2], 16) for i in (1, 3, 5)])
    else:
        with Image.open(io.BytesIO(file.data)) as original:
            if getattr(original, "n_frames", 1) > 1:
                raise OneKitError("Use a single-frame image.")
        image = open_image(file)
        if tool.id == "color-picker":
            x = number(options, "x", image.width//2, 0, image.width-1, True)
            y = number(options, "y", image.height//2, 0, image.height-1, True)
            pixel = image.crop((x, y, x+1, y+1))
            report = {**color_info(visible_rgb(pixel).getpixel((0, 0))), "x": x, "y": y,
                      "rgba": list(pixel.convert("RGBA").getpixel((0, 0)))}
        elif tool.id == "image-extract-colors":
            report = {"colors": extract(image, number(options, "colors", 6, 2, 32, True))}
        elif tool.id == "jpg-to-svg":
            data, shapes = vectorize(image, number(options, "colors", 16, 2, 32, True), number(options, "resolution", 256, 32, 512, True))
            return Result([output(file, "svg", data)], details={"shapes": shapes}, warnings=["Palette-based vector tiles; photographic gradients and fine detail are approximated. No bitmap is embedded."])
        elif tool.id in ("image-repair", "image-remove-watermark"):
            regions = options.get("regions")
            if tool.id == "image-repair" and (not regions or regions == "[]"):
                size = number(options, "size", 3, 3, 5, True)
                if size not in (3, 5):
                    raise OneKitError("Median size must be 3 or 5.")
                rgb = image.convert("RGB").filter(ImageFilter.MedianFilter(size))
                if "A" in image.getbands() or "transparency" in image.info:
                    rgb.putalpha(image.convert("RGBA").getchannel("A"))
                repaired, pixels = rgb, image.width*image.height
            else:
                repaired, pixels = restore(image, regions, number(options, "iterations", 200, 10, 500, True))
            return Result([output(file, "png", encode(repaired))], details={"processedPixels": pixels}, warnings=["Reconstruction estimates missing pixels; it cannot recover the original detail under a mark. Median cleanup can soften texture."])
        else:
            method = options.get("method", "unsharp")
            if method not in ("unsharp", "deconvolution"):
                raise OneKitError("Choose unsharp or deconvolution.")
            radius = number(options, "radius", 1.5, .3, 5)
            rgb = image.convert("RGB")
            if method == "unsharp":
                rgb = rgb.filter(ImageFilter.UnsharpMask(radius, number(options, "amount", 150, 0, 300, True), 3))
            else:
                import numpy as np
                if image.width*image.height > 1000000:
                    raise OneKitError("Deconvolution supports at most one million pixels; use unsharp for larger images.")
                border = math.ceil(radius*3)
                observed = np.pad(np.asarray(rgb).astype(np.float32)/255, ((border, border), (border, border), (0, 0)), mode="reflect")
                estimate = np.maximum(observed, .001)
                fy = np.fft.fftfreq(observed.shape[0])[:, None]
                fx = np.fft.rfftfreq(observed.shape[1])[None, :]
                transfer = np.exp(-2*math.pi**2*radius**2*(fx*fx+fy*fy))[:, :, None]
                # Richardson–Lucy with an estimated symmetric Gaussian PSF.
                def blur(array):
                    return np.fft.irfft2(np.fft.rfft2(array, axes=(0, 1))*transfer, s=array.shape[:2], axes=(0, 1)).real
                for _ in range(number(options, "iterations", 10, 1, 30, True)):
                    estimate *= blur(observed/np.maximum(blur(estimate), .001))
                    estimate = np.clip(estimate, 0, 1)
                rgb = Image.fromarray(np.rint(estimate[border:-border, border:-border]*255).astype(np.uint8))
            if "A" in image.getbands() or "transparency" in image.info:
                rgb.putalpha(image.convert("RGBA").getchannel("A"))
            return Result([output(file, "png", encode(rgb))], warnings=["Sharpening cannot restore detail that was never captured. Strong settings can create halos or amplify noise."])
    return Result([Artifact("colors.json", (json.dumps(report, indent=2)+"\n").encode())], details=report)
