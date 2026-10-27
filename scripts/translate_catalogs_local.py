"""Offline catalog authoring with Argos CTranslate2 models (not a runtime dependency).

Usage: python translate_catalogs_local.py MODEL_DIRECTORY CATALOG_DIRECTORY [...]
Requires ctranslate2 and sentencepiece in an isolated authoring environment.
Review machine translations before release. Existing translations are preserved.
"""
import concurrent.futures
import json
import os
import re
import sys
from pathlib import Path

import ctranslate2
import sentencepiece

MODEL_ROOT = Path(sys.argv[1])
DIRECTORIES = [Path(value) for value in sys.argv[2:]]
AVAILABLE = sorted({path.stem for directory in DIRECTORIES for path in directory.glob("*.json") if path.stem not in {"en", "languages"}})
LANGUAGES = tuple(os.environ.get("ONEKIT_TRANSLATION_LANGUAGES", ",".join(AVAILABLE)).split(","))
TECHNICAL_ACRONYMS = ('PDF', 'PDF/A', 'DOC', 'DOCX', 'DOCM', 'ODT', 'RTF', 'TXT', 'MD', 'MDX', 'HTML', 'HTM', 'CSS', 'SCSS', 'LESS', 'XML', 'XSD', 'XSLT', 'JSON', 'JSONC', 'JSON5', 'YAML', 'YML', 'TOML', 'HCL', 'CSV', 'TSV', 'XLS', 'XLSX', 'XLSM', 'PPT', 'PPTX', 'ODP', 'EPUB', 'FB2', 'MOBI', 'AZW', 'AZW3', 'PNG', 'JPG', 'JPEG', 'TIFF', 'TIF', 'WEBP', 'AVIF', 'HEIC', 'HEIF', 'GIF', 'SVG', 'BMP', 'ICO', 'ICNS', 'APNG', 'RAW', 'DNG', 'PSD', 'WAV', 'MP3', 'MP4', 'M4A', 'M4V', 'WEBM', 'MOV', 'AVI', 'MKV', 'FLV', 'OGG', 'OGV', 'OPUS', 'FLAC', 'AAC', 'AIFF', 'AU', 'AMR', 'QR', 'AI', 'OCR', 'CLI', 'API', 'SDK', 'HTTP', 'HTTPS', 'FTP', 'SFTP', 'SSH', 'SSL', 'TLS', 'TCP', 'UDP', 'IP', 'DNS', 'URI', 'URL', 'URN', 'SPDX', 'MIME', 'UTF-8', 'UTF‑8', 'ASCII', 'POSIX', 'UNIX', 'ANSI', 'EXIF', 'XMP', 'IPTC', 'GPS', 'ICC', 'ICM', 'RGB', 'RGBA', 'CMYK', 'HSV', 'HSL', 'HSB', 'LAB', 'LCH', 'HEX', 'HSLA', 'ONNX', 'WASM', 'GPU', 'CPU', 'RAM', 'GB', 'MB', 'KB', 'MiB', 'KiB', 'GiB', 'SRT', 'VTT', 'ASS', 'SSA', 'WEBVTT', 'TTF', 'OTF', 'WOFF', 'WOFF2', 'EOT', 'CFF', 'ZIP', 'TAR', 'TGZ', 'GZ', 'BZ2', 'XZ', 'RAR', 'LZMA', 'ZSTD', 'MIT', 'BSD', 'MPL', 'GPL', 'LGPL', 'AGPL', 'OFL', 'PSF', 'ISC', 'CC0', 'CC', 'README', 'GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'DPI', 'NIST', 'BE', 'LE', 'BOM', 'AIF', 'WMA', 'MPEG', 'MPG', 'TS', 'CMU')
PROTECT = re.compile(r"Mattia Piazzalunga|SPDX-License-Identifier|SPDX-FileCopyrightText|MIT-CMU|LicenseRef-[A-Za-z0-9._-]+|\b[A-Za-z][A-Za-z0-9._-]*-\d[0-9.]*(?:-[A-Za-z0-9]+)*\+?|\.1kit\b|Times New Roman|DejaVu Sans|Noto Sans|Courier New|<[^>]+>|`[^`\n]+`|(?<=\]\()[^)]*(?=\))|https?://[^\s<>\])]+|[\w.+-]+@[\w.-]+\.[A-Za-z]+|\{\d+\}|%\([\w]+\)[a-z]|%[a-z]|\bPolyForm Shield(?: 1\.0\.0)?\b|\b(?:AGPL|LGPL|GPL)-\d(?:\.\d+)*(?:-or-later|-only)?\b|\b(?:LaTeX|Markdown|Base64|Jupyter|OpenAPI|AsyncAPI|TypeScript|JavaScript|PowerShell|PowerPoint|Excel|Python|FFmpeg|WebAssembly|Inter|Arial|Helvetica|Georgia|Courier|OneKit|Java|Kotlin|Scala|Swift|Dart|Rust|Ruby|Haskell|Julia|Elixir|Solidity|Svelte|Vue|Lua|Bash|Shell|Terraform|GraphQL|Node\.js|vCard|Wi-Fi|Windows|macOS|Linux|Chrome|Chromium|Firefox|Safari)\b|\bWord\b(?!\s+(?:and [Cc]haracter|count))|\bonekit(?:[.-][a-z0-9]+)*\b|--[a-z][a-z0-9-]*" + r"|\b(?:" + "|".join(re.escape(term) for term in TECHNICAL_ACRONYMS) + r")\b|\b[A-Z][A-Z0-9_+/.:-]*[0-9][A-Z0-9_+/.:-]*\b|\b[A-Z]+(?:_[A-Z0-9]+)+\b")
PROTECT = re.compile(r"\]\([^)]*\)|!?\[|\b(?:PyPI|GitHub|wheel)\b|" + PROTECT.pattern)
SOURCES = {path: json.loads((path / "en.json").read_text(encoding="utf-8")) for path in DIRECTORIES}


def split_sentences(text):
    result, offset = [], 0
    for match in re.finditer(r"[.!?]+[\"')\]]*\s+(?=[A-Z0-9\"'(])", text):
        prefix = text[:match.start()].lower()
        if prefix.endswith(("e.g", "i.e", "etc", "vs", "dr", "mr", "mrs", "ms")):
            continue
        result.append(text[offset:match.end()].strip())
        offset = match.end()
    if text[offset:].strip():
        result.append(text[offset:].strip())
    return result or [text]


def write(path, source, catalog):
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps({key: catalog[key] for key in source if key in catalog}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def run(language):
    base = next((MODEL_ROOT / language).iterdir())
    tokenizer = sentencepiece.SentencePieceProcessor(model_file=str(base / "sentencepiece.model"))
    translator = ctranslate2.Translator(str(base / "model"), device="cpu", compute_type="int8", inter_threads=1, intra_threads=int(os.environ.get("ONEKIT_TRANSLATION_THREADS", "4")))
    catalogs = {path: json.loads((path / f"{language}.json").read_text(encoding="utf-8")) if (path / f"{language}.json").exists() else {} for path in DIRECTORIES}
    combined = {key: value for catalog in catalogs.values() for key, value in catalog.items()}
    keys = sorted({key for source in SOURCES.values() for key in source if key not in combined}, key=len)
    for path, source in SOURCES.items():
        for key in source:
            if key in combined:
                catalogs[path].setdefault(key, combined[key])
        write(path / f"{language}.json", source, catalogs[path])
    print(f"{language}: {len(keys)} unique pending texts", flush=True)

    def infer(texts):
        if not texts:
            return []
        segments = [split_sentences(text) for text in texts]
        sentences = [sentence for group in segments for sentence in group]
        natural = [sentence for sentence in sentences if re.search(r"[A-Za-z]", sentence)]
        encoded = [tokenizer.encode(text, out_type=str) for text in natural]
        if not encoded:
            return texts
        results = translator.translate_batch(encoded, beam_size=3, max_batch_size=32, batch_type="examples", max_input_length=1024, max_decoding_length=min(768, max(32, max(map(len, encoded)) * 3 + 16)), repetition_penalty=1.1, no_repeat_ngram_size=4, replace_unknowns=True)
        decoded = iter(tokenizer.decode(result.hypotheses[0]).replace("▁", " ").strip() for result in results)
        return [" ".join(next(decoded) if re.search(r"[A-Za-z]", sentence) else sentence for sentence in group) for group in segments]

    for start in range(0, len(keys), 32):
        batch = keys[start:start + 32]
        prepared, protected = [], []
        for key in batch:
            tokens = []
            def protect(match):
                tokens.append(match.group())
                return str(975000 + len(tokens) - 1)
            prepared.append(PROTECT.sub(protect, key))
            protected.append(tokens)
        translated = infer(prepared)
        for key, value, tokens in zip(batch, translated, protected):
            valid = True
            for index, token in enumerate(tokens):
                marker = str(975000 + index)
                expression = r"(?<!\d)" + r"[\s,.]*".join(marker) + r"(?!\d)"
                value, count = re.subn(expression, lambda match: token, value)
                if count != 1:
                    valid = False
            if not valid or sorted(re.findall(r"\{\d+\}", key)) != sorted(re.findall(r"\{\d+\}", value)):
                # Retry natural text fragments while carrying code and placeholders verbatim.
                pieces = re.split("(" + PROTECT.pattern + ")", key)
                natural = [piece for piece in pieces[::2] if re.search(r"[A-Za-z]", piece)]
                replacements = iter(infer(natural))
                value = "".join((piece[:len(piece)-len(piece.lstrip())] + next(replacements).strip() + piece[len(piece.rstrip()):]) if index % 2 == 0 and re.search(r"[A-Za-z]", piece) else piece for index, piece in enumerate(pieces))
            if not value.strip():
                value = key
            combined[key] = value
        for path, source in SOURCES.items():
            for key in source:
                if key in combined:
                    catalogs[path].setdefault(key, combined[key])
            write(path / f"{language}.json", source, catalogs[path])
        print(f"{language}: {min(start + 32, len(keys))}/{len(keys)}", flush=True)
    print(f"{language}: complete", flush=True)


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(run, LANGUAGES))
