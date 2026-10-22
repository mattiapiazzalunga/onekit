# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Tool registry and processing contracts for the CLI and Python API."""
from dataclasses import asdict, dataclass, replace


@dataclass(frozen=True)
class Tool:
    id: str
    name: str
    group: str
    handler: str
    accepts: tuple[str, ...] = ("*",)
    produces: str = "*"
    fidelity: str = "exact"
    note: str = "Preserves the selected content; validate important outputs."
    packages: tuple[str, ...] = ()
    engines: tuple[str, ...] = ()
    multiple: bool = False
    options: tuple[str, ...] = ()
    input_mode: str = "typed"
    min_files: int = 1
    max_files: int = 1
    max_file_bytes: int = 128 * 1024 * 1024
    max_total_bytes: int = 128 * 1024 * 1024



TOOLS: dict[str, Tool] = {}


def add(id, name, group, handler, accepts=("*",), produces="*", **kwargs):
    TOOLS[id] = Tool(id, name, group, handler, tuple(accepts), produces, **kwargs)


CONVERSIONS = {
    "md": ["latex", "json", "html", "pdf", "docx"],
    "pdf": ["pdfa", "png", "jpeg", "webp", "tiff", "docx", "html", "pptx", "md"],
    "image": ["base64", "pdf", "pptx"], "base64": ["image"],
    "docx": ["pdf", "png", "md"], "pptx": ["pdf", "png"],
    "latex": ["html", "pdf", "md"], "html": ["pdf", "latex", "json", "md"],
    "xlsx": ["pdf", "csv", "json"], "json": ["xlsx"], "csv": ["xlsx", "json"],
}
LABELS = {"md": "Markdown", "latex": "LaTeX", "docx": "Word", "pptx": "PowerPoint", "xlsx": "Excel", "image": "Image", "base64": "Base64", "pdfa": "PDF/A", "json": "JSON", "pdf": "PDF", "notebook": "Jupyter notebook", "word": "Word"}
IMAGE_TYPES = ("png", "jpeg", "webp", "gif", "bmp", "tiff", "ico")
PURE = {("md", "json"), ("html", "json"), ("csv", "json"), ("base64", "image"), ("image", "base64")}
for source, targets in CONVERSIONS.items():
    for target in targets:
        pair = (source, target)
        structured = pair in PURE or pair in {("md", "html"), ("html", "md"), ("image", "pdf"), ("xlsx", "csv"), ("xlsx", "json"), ("json", "xlsx"), ("csv", "xlsx")}
        packages = ("markdown-it-py",) if pair == ("md", "html") else ("markdownify",) if pair == ("html", "md") else ("Pillow",) if source == "image" and target != "base64" else ("openpyxl",) if "xlsx" in pair else ()
        native = not structured
        engine = ("pandoc",) if source in ("md", "latex", "html") and target != "pdf" else ("pdflatex",) if pair == ("latex", "pdf") else ("soffice",) if source in ("docx", "pptx", "xlsx") else ()
        if source == "pdf":
            packages = ("pypdfium2", "Pillow") if target in IMAGE_TYPES else ("pypdf",) if target in ("md", "html", "docx") else ("pypdfium2", "Pillow", "python-pptx") if target == "pptx" else ()
            engine = ("gs",) if target == "pdfa" else ()
        if pair == ("md", "pdf") or pair == ("html", "pdf"):
            engine = ("pandoc", "pdflatex")
        if pair == ("image", "pptx"):
            packages = ("python-pptx", "Pillow")
        if pair == ("pdf", "docx"):
            packages = ("pypdf", "python-docx")
        add(f"{source}-to-{target}", f"{LABELS.get(source, source.upper())} to {LABELS.get(target, target.upper())}", "converters", "converters", IMAGE_TYPES if source == "image" else (source,), target, packages=packages, engines=engine, fidelity="exact" if pair in PURE and source != "html" else "compromise", note="Formatting, fonts, layout, formulas or unsupported elements may change. Scanned PDFs require OCR first." if pair not in PURE else "Structured conversion; the output represents the source data.", options=("sheet",) if source == "xlsx" else ())

PDF_OPS = ["merge", "split", "remove-pages", "organize", "extract-pages", "compress", "repair", "edit", "rotate", "sign", "protect", "unlock", "validate-pdfa"]
for operation in PDF_OPS:
    native = operation in ("sign", "validate-pdfa")
    add(f"pdf-{operation}", f"{operation.replace('-', ' ').capitalize()} PDF", "pdf", "pdf", ("pdf",), "pdf" if operation != "validate-pdfa" else "json", packages=("pypdf", "reportlab") if operation == "edit" else ("pypdf",) if not native else ("pyhanko",) if operation == "sign" else (), engines=("verapdf",) if operation == "validate-pdfa" else (), multiple=operation == "merge", fidelity="compromise" if operation in ("compress", "repair", "edit", "sign") else "exact", note="Repair is best effort. Editing adds text overlays. Signing requires a PKCS#12 certificate." if operation in ("repair", "edit", "sign") else "Compression is lossless and may not reduce already optimized files." if operation == "compress" else "Page operations preserve content. Encryption permissions are advisory.", options=("pages",) if operation in ("remove-pages", "organize", "extract-pages") else ("angle",) if operation == "rotate" else ("password",) if operation in ("protect", "unlock") else ("text", "x", "y", "page") if operation == "edit" else ("certificate", "password") if operation == "sign" else ())

for op in ("compress", "crop", "convert"):
    add(f"image-{op}", f"{op.capitalize()} image", "images", "images", IMAGE_TYPES, "image", packages=("Pillow",), fidelity="compromise" if op == "compress" else "exact", note="Lossy formats discard detail. Animation and metadata can be removed; use a lossless format to preserve pixels.", options=("format", "quality") if op != "crop" else ("box",))
add("image-extract-pdf", "Extract images from PDF", "images", "images", ("pdf",), "image", packages=("pypdf", "Pillow"))
add("image-to-favicon", "Image to favicon", "images", "favicon", IMAGE_TYPES, "*", packages=("Pillow",), fidelity="compromise", note="Resizes the first image frame to square icons. Fit keeps the whole image with transparent padding; fill crops the edges. Original files stay unchanged.", options=("format", "fit"))
for group, formats in (("video", ("mp4", "webm", "mkv", "mov", "avi", "gif")), ("audio", ("mp3", "wav", "flac", "ogg", "aac", "m4a", "mp4"))):
    add(f"{group}-convert", f"Convert {group}", group, "media", ("*",), "*", engines=("ffmpeg",), fidelity="compromise", note="Available codecs depend on your FFmpeg build; re-encoding can lose quality.", options=("format", "codec", "bitrate"))
add("archive-convert", "Convert archive", "archives", "archives", ("zip", "tar", "gz", "bz2", "xz"), "*", note="ZIP and TAR variants are supported. Archive links and unsafe paths are rejected.", options=("format",))
add("font-convert", "Convert font", "fonts", "fonts", ("ttf", "otf", "woff", "woff2"), "*", packages=("fonttools",), note="Changes font containers; does not transform TrueType outlines into CFF outlines or vice versa.", options=("format",))
for op in ("inspect", "metadata-set", "metadata-remove", "count", "encoding-convert"):
    add(f"file-{op}", {"inspect": "Inspect file", "metadata-set": "Set metadata", "metadata-remove": "Remove metadata", "count": "Count text", "encoding-convert": "Convert text encoding"}[op], "inspector", "inspector", produces="json" if op in ("inspect", "count") else "*", engines=("exiftool",) if op.startswith("metadata") else (), options=("metadata",) if op == "metadata-set" else ("encoding",) if op == "encoding-convert" else ())
for op in ("encrypt", "decrypt"):
    add(f"security-{op}", f"{op.capitalize()} files or folders", "security", "security", produces="zip" if op == "encrypt" else "*", packages=("pycryptodome", "stream-zip", "stream-unzip"), options=("password",), multiple=op == "encrypt", note="AES-256 encrypted ZIP, compatible with 7-Zip. File names remain visible. Losing the password makes recovery impossible.")

LANGUAGES = ["JavaScript", "TypeScript", "JSX", "TSX", "Python", "Java", "C", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Kotlin", "Swift", "Dart", "Scala", "Lua", "Bash", "Shell", "PowerShell", "SQL", "HTML", "CSS", "SCSS", "Less", "XML", "SVG", "JSON", "JSON5", "JSONC", "YAML", "TOML", "Markdown", "MDX", "LaTeX", "GraphQL", "Vue", "Svelte", "Astro", "Solidity", "HCL", "Terraform", "Dockerfile", "R", "Julia", "Elixir", "Haskell"]
VALIDATORS = LANGUAGES + ["XSD", "JSON-Schema", "CSV", "OpenAPI", "AsyncAPI"]
MINIFIERS = ["JavaScript", "TypeScript", "JSX", "TSX", "HTML", "CSS", "JSON", "SVG", "GraphQL"]
for operation, languages in (("format", LANGUAGES), ("validate", VALIDATORS), ("minify", MINIFIERS)):
    for language in languages:
        slug = language.lower().replace("++", "pp").replace("#", "sharp")
        add(f"dev-{operation}-{slug}", f"{operation.capitalize()} {language.replace('-', ' ')}", "developer", "developer", produces="json" if operation == "validate" else "*", fidelity="compromise" if operation == "minify" else "exact", note="Validation checks the configured parser or compiler; project-wide types, imports and dependencies may require a local project.", options=())
for target in ("pdf", "docx", "md", "latex", "html", "json"):
    add(f"ocr-to-{target}", f"OCR to {LABELS.get(target, target.upper())}", "ocr", "ocr", ("pdf",) + IMAGE_TYPES, target, packages=("pytesseract", "Pillow", "pypdfium2", "python-docx"), engines=("tesseract",), fidelity="compromise", note="Recognition depends on scan quality and installed language packs. Equations and layout may need manual correction.", options=("language", "dpi"))
for kind in ("text", "json", "notebook", "latex", "pdf", "word", "code"):
    add(f"diff-{kind}", f"Compare {LABELS.get(kind, kind).replace('word', 'Word')} files", "diff", "diff", produces="json", packages=("pypdf",) if kind == "pdf" else ("python-docx",) if kind == "word" else (), multiple=True, fidelity="compromise" if kind in ("pdf", "word", "latex") else "exact", note="Compares extracted text, not visual layout." if kind in ("pdf", "word") else "Notebook comparison can include Markdown, code or both. LaTeX text mode omits commands.", options=("mode",) if kind in ("notebook", "latex") else ())


for id in ("docx-to-md", "md-to-docx", "image-to-pptx", "pdf-to-md", "pdf-to-html", "pdf-to-docx", "pdf-protect", "pdf-unlock", "diff-pdf", "diff-word", "font-convert", "dev-format-xml", "dev-format-svg", "dev-format-toml", "dev-validate-json5", "dev-validate-jsonc", "dev-validate-yaml", "dev-validate-json-schema", "dev-validate-xsd"):
    TOOLS[id] = replace(TOOLS[id], engines=())
for id, packages in {"docx-to-md": ("python-docx",), "md-to-docx": ("python-docx",), "font-convert": ("fonttools", "brotli"), "dev-format-toml": ("tomli-w",), "dev-validate-json5": ("json5",), "dev-validate-jsonc": ("json5",), "dev-validate-yaml": ("PyYAML",), "dev-validate-json-schema": ("jsonschema",), "dev-validate-xsd": ("xmlschema",)}.items():
    TOOLS[id] = replace(TOOLS[id], packages=packages)
for id, tool in list(TOOLS.items()):
    if "pypdf" in tool.packages:
        TOOLS[id] = replace(tool, packages=("pycryptodome",) + tool.packages)
TOOLS["file-encoding-convert"] = replace(TOOLS["file-encoding-convert"], options=("source_encoding", "encoding"))
TOOLS["file-inspect"] = replace(TOOLS["file-inspect"], packages=("Pillow", "pycryptodome", "pypdf"))
TOOLS["pdf-edit"] = replace(
    TOOLS["pdf-edit"], options=("mode", "edits", "password", "text", "x", "y", "page"),
    note="Edit supported text boxes using the original font. Longer text is fitted to its original width. "
         "Scans, text inside reusable forms and unavailable font characters cannot be edited. "
         "This is not a redaction tool. The legacy text option adds an overlay.",
)
TOOLS["image-convert"] = replace(TOOLS["image-convert"], fidelity="compromise")
TOOLS["image-crop"] = replace(TOOLS["image-crop"], fidelity="compromise", options=("box", "format", "quality"))
TOOLS["pdf-compress"] = replace(TOOLS["pdf-compress"], options=("compression_level",), packages=(*TOOLS["pdf-compress"].packages, "Pillow"), note="Light preserves image quality. Balanced and Maximum may reduce image quality and resolution. The original is kept if no smaller output is found.")
for id in ("csv-to-json", "csv-to-xlsx"):
    TOOLS[id] = replace(TOOLS[id], options=("delimiter",))
for id in ("pdf-to-png", "pdf-to-jpeg", "pdf-to-webp", "pdf-to-tiff", "pdf-to-pptx"):
    TOOLS[id] = replace(TOOLS[id], options=("dpi",))
TOOLS["pdf-rotate"] = replace(TOOLS["pdf-rotate"], options=("angle", "pages"))
for id in ("md-to-docx",):
    TOOLS[id] = replace(TOOLS[id], packages=("markdown-it-py", "python-docx"))
TOOLS["md-to-docx"] = replace(TOOLS["md-to-docx"], note="CommonMark headings, lists, emphasis and code are exported. Images, advanced layouts and Markdown extensions may need adjustment.")
TOOLS["pdf-to-pdfa"] = replace(TOOLS["pdf-to-pdfa"], options=("icc_profile",))
TOOLS["ocr-to-pdf"] = replace(TOOLS["ocr-to-pdf"], packages=("pytesseract", "Pillow", "pypdfium2", "pypdf", "pycryptodome"))
TOOLS["docx-to-png"] = replace(TOOLS["docx-to-png"], packages=("pypdfium2", "Pillow"), options=("dpi",))
TOOLS["pptx-to-png"] = replace(TOOLS["pptx-to-png"], packages=("pypdfium2", "Pillow"), options=("dpi",))
TOOLS["security-decrypt"] = replace(TOOLS["security-decrypt"], options=("password", "restore"))


LANGUAGE_EXTENSIONS = {
    "javascript": ("js", "mjs", "cjs"), "typescript": ("ts", "mts", "cts"), "jsx": ("jsx",), "tsx": ("tsx",),
    "python": ("py", "pyi"), "java": ("java",), "c": ("c", "h"), "cpp": ("cpp", "cc", "cxx", "hpp", "h"),
    "csharp": ("cs",), "go": ("go",), "rust": ("rs",), "php": ("php",), "ruby": ("rb",), "kotlin": ("kt", "kts"),
    "swift": ("swift",), "dart": ("dart",), "scala": ("scala", "sc"), "lua": ("lua",), "bash": ("sh", "bash"),
    "shell": ("sh",), "powershell": ("ps1", "psm1", "psd1"), "sql": ("sql",), "html": ("html",), "css": ("css",),
    "scss": ("scss",), "less": ("less",), "xml": ("xml",), "xsd": ("xsd", "xml"), "svg": ("svg", "xml"),
    "json": ("json",), "json5": ("json5", "json"), "jsonc": ("jsonc", "json"), "json-schema": ("json",),
    "yaml": ("yaml",), "toml": ("toml",), "csv": ("csv",), "markdown": ("md",), "mdx": ("mdx",),
    "latex": ("latex",), "graphql": ("graphql", "gql"), "vue": ("vue",), "svelte": ("svelte",), "astro": ("astro",),
    "solidity": ("sol",), "hcl": ("hcl",), "terraform": ("tf", "tfvars"), "dockerfile": ("dockerfile",),
    "r": ("r",), "julia": ("jl",), "elixir": ("ex", "exs"), "haskell": ("hs", "lhs"),
    "openapi": ("json", "yaml"), "asyncapi": ("json", "yaml"),
}
for id, tool in list(TOOLS.items()):
    accepts, mode = tool.accepts, "typed"
    if tool.group == "developer":
        language = id.split("-", 2)[2]
        accepts = (*LANGUAGE_EXTENSIONS[language], "txt", *(("",) if language in ("dockerfile", "bash", "shell") else ()))
        mode = "text"
    elif tool.group == "diff":
        accepts = {"diff-pdf": ("pdf",), "diff-word": ("docx",), "diff-notebook": ("ipynb",), "diff-json": ("json", "txt"), "diff-latex": ("latex", "txt")}.get(id, ("*",))
        mode = "typed" if id in ("diff-pdf", "diff-word") else "text"
    elif id == "security-decrypt":
        accepts = ("zip",)
    elif id in ("file-count", "file-encoding-convert"):
        mode = "encoded-text" if id.endswith("encoding-convert") else "text"
    elif tool.accepts == ("*",):
        mode = "any"
    elif tool.group == "converters" and tool.accepts[0] in ("md", "latex", "html", "json", "csv", "base64"):
        mode = "text"
    elif tool.group in ("audio", "video"):
        mode = "typed"
    if id == "audio-convert":
        accepts = ("mp3", "wav", "flac", "ogg", "aac", "m4a", "mp4", "aif", "aiff", "opus", "wma")
        mode = "typed"
    elif id == "video-convert":
        accepts = ("mp4", "webm", "mkv", "mov", "avi", "gif", "mpeg", "mpg", "m4v", "ogv", "ts")
        mode = "typed"
    limit = 8 * 1024 * 1024 if mode in ("text", "encoded-text") else 16 * 1024 * 1024 if tool.group == "fonts" else 64 * 1024 * 1024 if tool.group == "images" or tool.accepts == IMAGE_TYPES else 128 * 1024 * 1024
    TOOLS[id] = replace(tool, accepts=accepts, input_mode=mode, min_files=2 if tool.group == "diff" or id == "pdf-merge" else 1, max_files=2 if tool.group == "diff" else 256 if tool.multiple else 1, max_file_bytes=limit)
TOOLS["image-to-base64"] = replace(TOOLS["image-to-base64"], packages=("Pillow",))
TOOLS["base64-to-image"] = replace(TOOLS["base64-to-image"], accepts=("base64", "txt"))
for id in ("dev-minify-typescript", "dev-minify-jsx", "dev-minify-tsx"):
    TOOLS[id] = replace(TOOLS[id], produces="js", note="Produces minified JavaScript (.js). TypeScript types are removed; JSX and TSX are compiled. Keep the original source.")
TOOLS["dev-validate-sql"] = replace(TOOLS["dev-validate-sql"], options=("dialect",))
# These converters already have pure-Python implementations; an unused native
# engine must not make doctor report them as unavailable.
for id, tool in list(TOOLS.items()):
    if tool.id in ('base64-to-image', 'csv-to-json', 'csv-to-xlsx', 'docx-to-md', 'html-to-json', 'html-to-md', 'image-to-base64', 'image-to-pdf', 'image-to-pptx', 'json-to-xlsx', 'md-to-docx', 'md-to-html', 'md-to-json', 'pdf-to-docx', 'pdf-to-html', 'pdf-to-jpeg', 'pdf-to-md', 'pdf-to-png', 'pdf-to-pptx', 'pdf-to-tiff', 'pdf-to-webp', 'qrcode-to-json', 'qrcode-to-text', 'qrcode-to-vcard', 'xlsx-to-csv', 'xlsx-to-json'):
        TOOLS[id] = replace(tool, engines=())
for id in ("video-convert", "audio-convert"):
    TOOLS[id] = replace(TOOLS[id], engines=("ffmpeg", "ffprobe"))


add("video-download", "Download video", "video", "video_download", ("txt",), "*",
    packages=("yt-dlp",), engines=("ffmpeg",), input_mode="text",
    note="Downloads from YouTube and other yt-dlp sites, up to 128 MiB. Site support varies; an internet connection is required.",
    max_file_bytes=16384, options=("quality", "cookies", "cookies_from_browser", "format_id", "referer", "list_formats"))

QR_GENERATORS = {
    "text-to-qrcode": ("Text to QR code", "qrcode", ("txt",)),
    "url-to-qrcode": ("URL to QR code", "qrcode", ("txt",)),
    "wifi-to-qrcode": ("Wi-Fi to QR code", "qrcode", ("json",)),
    "vcard-to-qrcode": ("vCard to QR code", "qrcode", ("json", "vcf")),
}
for id, (name, group, accepts) in QR_GENERATORS.items():
    add(id, name, group, "qrcode", accepts, "png", packages=("segno", "Pillow"),
        input_mode="text", max_file_bytes=16384, options=("format", "shape", "corner_style", "overlay_type", "overlay_text", "overlay_image_base64", "overlay_size", "error_correction", "scale", "border", "dark", "light", "transparent_background", "include_payload"),
        note="Creates a standard QR code locally. Capacity depends on the content and error correction. Keep the quiet zone and test the code before printing.")
for id, name, group, produces in (
    ("scan-qrcode", "Scan QR code", "qrcode", "json"),
    ("reverse-qrcode", "Reverse QR code", "qrcode", "json"),
    ("qrcode-to-text", "QR code to text", "converters", "txt"),
    ("qrcode-to-json", "QR code to JSON", "converters", "json"),
):
    add(id, name, group, "qrcode", ("png", "jpeg", "webp", "bmp", "gif"), produces,
        packages=("Pillow", "zxing-cpp"), max_file_bytes=16*1024*1024,
        note="Reads QR payloads locally from an image; Reverse reveals the stored content, not the original image or generator settings. No links are opened automatically.")


add("text-to-barcode", "Generate barcode", "qrcode", "barcode", ("txt",), "png",
    packages=("python-barcode", "Pillow"), input_mode="text",
    max_file_bytes=1024, options=("barcode_type", "format", "module_width", "height", "quiet_zone", "show_text", "font_size", "dpi"),
    note="Generates Code 128, Code 39, EAN-13, EAN-8, UPC-A, ITF and ISBN-13 locally. Retail check digits are validated or calculated; identifiers are not registered or assigned by OneKit.")
for id, name, produces in (("scan-barcode", "Scan barcode", "json"), ("barcode-to-text", "Barcode to text", "txt")):
    add(id, name, "qrcode", "barcode", ("png", "jpeg", "webp", "bmp", "gif"), produces,
        packages=("Pillow", "zxing-cpp"), max_file_bytes=16*1024*1024, note="Reads standard linear barcodes locally from an image; Use a sharp image with complete bars and clear side margins.")


add("dev-regex-test", "Regex tester", "developer", "regex_tester", ("txt",), "json",
    engines=("node",), input_mode="text", max_file_bytes=128*1024, options=("pattern", "flags", "max_matches", "enable_replacement", "replacement"),
    note="Tests JavaScript regular expressions locally with captures, named groups, UTF-16 positions and replacement. Up to 128 KiB of text, 1000 matches and 1 MiB of output. Execution is time limited; the CLI requires Node.js.")


add("pdf-redact", "Permanently redact PDF", "pdf", "redaction", ("pdf",), "pdf",
    packages=("pypdfium2", "Pillow", "reportlab", "pypdf"), options=("regions", "dpi"),
    fidelity="compromise", note="Permanently masks selected areas and rebuilds every page from raster pixels. Original text, attachments, comments, forms and metadata are not copied; selectable text and vector quality are lost. The original file is unchanged.")
add("image-redact", "Permanently redact image", "images", "redaction", IMAGE_TYPES, "png",
    packages=("Pillow",), options=("regions",),
    fidelity="compromise", note="Replaces selected pixels with solid black and exports a new opaque PNG without original metadata or hidden alpha pixels. Single-frame images only. The original file is unchanged.")


add("pdf-watermark", "Add watermark to PDF", "pdf", "pdf.watermark", ("pdf",), "pdf",
    packages=("pypdf", "reportlab", "Pillow"),
    options=("text", "pages", "font", "font_size", "color", "opacity", "angle", "position", "layout", "margin", "watermark_type", "image_base64", "image_width"),
    note="Adds a text or PNG/JPEG image watermark to all or selected pages, retaining source text and graphics. Supports Western European text, single or repeated layout, rotation and opacity. The original file is unchanged.")


add("image-effects", "Blur, pixelate & image effects", "images", "image_effects", IMAGE_TYPES, "png",
    packages=("Pillow",), options=("effect", "scope", "strength", "color", "regions"), fidelity="compromise",
    note="Blur, pixelate, box blur, solid cover or grayscale in one tool. Apply to the whole image or selected areas, with adjustable intensity and a fresh PNG export. Blur and pixelation do not guarantee permanent removal of sensitive details. Single-frame images only.")


add("vcard-generate", "Generate vCard", "qrcode", "contacts", ("json",), "vcf",
    input_mode="text", max_file_bytes=16384, note="Creates a vCard 3.0 or 4.0 contact file from the fields you provide. Empty fields are omitted. No QR capacity limit applies.")
add("qrcode-to-vcard", "QR code to vCard", "converters", "qrcode", ("png", "jpeg", "webp", "bmp", "gif"), "vcf",
    packages=("Pillow", "zxing-cpp"), max_file_bytes=16*1024*1024, note="Extracts vCard contacts stored directly in QR images. Other payloads, including contact download links, are rejected; no URLs are opened.")
add("image-upscale", "Upscale image", "images", "image_upscale", IMAGE_TYPES, "png",
    packages=("Pillow",), options=("scale",), fidelity="compromise",
    note="Enlarges a single-frame image 2×, 3× or 4× with Lanczos resampling. This is not AI detail reconstruction. Exports PNG, up to 40 million output pixels.")
add("image-remove-background", "Remove image background", "images", "background", IMAGE_TYPES, "png",
    packages=("onnxruntime", "numpy", "pooch", "Pillow"), fidelity="compromise",
    note="Removes the background locally and exports a transparent PNG. Uses U2Net. Fine edges may need review. The model downloads on first use.")
for id, name, produces, options in (
    ("video-compress", "Compress video", "mp4", ("compression_level",)),
    ("video-speed", "Change video speed", "mp4", ("speed",)),
    ("video-to-gif", "Video to GIF", "gif", ("start", "duration", "fps", "width")),
):
    add(id, name, "video", "video_edit", TOOLS["video-convert"].accepts, produces,
        engines=("ffmpeg", "ffprobe"), options=options, fidelity="compromise",
        note="Processes locally with FFmpeg. Re-encoding may lose quality. GIF output has no audio.")
add("audio-to-text", "Audio to text", "audio", "transcription", TOOLS["audio-convert"].accepts, "txt",
    packages=("faster-whisper",), options=("language",), fidelity="compromise",
    note="Transcribes locally with Whisper tiny (multilingual). The model downloads on first use; no audio is uploaded. Recognition can make mistakes.")


# All license checks report unverified declarations and heuristic indications, never permission.
LICENSE_TYPES = {
    "pdf": ("PDF", ("pdf",), ("pypdf", "pycryptodome")),
    "word": ("Word", ("docx", "docm", "doc"), ("olefile",)),
    "powerpoint": ("PowerPoint", ("pptx", "pptm", "ppt"), ("olefile",)),
    "excel": ("Excel", ("xlsx", "xlsm", "xls"), ("olefile",)),
    "video": ("Video", TOOLS["video-convert"].accepts, ()),
    "audio": ("Audio", TOOLS["audio-convert"].accepts, ()),
    "image": ("Image", IMAGE_TYPES + ("svg",), ("Pillow",)),
    "font": ("Font", ("ttf", "otf", "woff", "woff2"), ("fonttools", "brotli")),
    "epub": ("EPUB", ("epub",), ()),
    "code": ("Code and project", ("*",), ()),
    "dataset": ("Dataset", ("csv", "json", "jsonld", "txt", "md", "license", ""), ()),
}
for kind, (label, accepts, packages) in LICENSE_TYPES.items():
    add(f"license-{kind}", f"{label} license checker", "licenses", "license_check", accepts, "json",
        input_mode="any", packages=("license-expression", "defusedxml", *packages),
        engines=("ffprobe",) if kind in ("audio", "video") else (),
        multiple=kind in ("code", "dataset"), max_files=256 if kind in ("code", "dataset") else 1,
        options=("ref",), fidelity="compromise",
        note="An estimate based on declarations and metadata, not a rights certificate or legal clearance. "
             "Verify every finding with the original source and rights holder. Missing information never means free to use. "
             "Authors and copyright holders may differ. Files are analyzed locally; links are downloaded directly from their source. "
             "Archives are bounded and scans can be incomplete.")


add("audio-youtube-download", "YouTube audio downloader", "audio", "audio_youtube", ("txt",), "*",
    packages=("yt-dlp", "yt-dlp-ejs"), engines=("ffmpeg", "ffprobe", "node"), input_mode="text",
    max_file_bytes=16384, options=("format", "quality"), fidelity="compromise",
    note="CLI only: extract one completed YouTube video's audio as original audio or MP3 at 64–320 kbps, up to 128 MiB. "
         "Use only when the service and applicable rights permit downloading. YouTube's terms restrict downloads; ownership alone is not a blanket authorization. "
         "No DRM bypass. Site availability can change. A higher MP3 bitrate cannot improve the source quality.")
add("audio-download", "Download audio", "audio", "link_tools", ("txt",), "*", input_mode="text",
    engines=("ffmpeg", "ffprobe"), max_file_bytes=16384, options=("format", "quality"), fidelity="compromise",
    note="Download a direct audio file or an audio source exposed by an accessible page. Original mode preserves downloaded bytes; MP3 conversion is lossy. "
         "Up to 128 MiB. Login and protected streams may prevent downloads. Use only with permission.")
add("image-download", "Download image", "images", "link_tools", ("txt",), "*", input_mode="text",
    max_file_bytes=16384, note="Download original PNG, JPEG, WebP, GIF, TIFF, BMP, ICO or AVIF bytes from a direct URL or the first accessible image exposed by a page. "
         "Up to 128 MiB. Sites may block access. Downloading does not grant usage rights.")
add("image-rotate-flip", "Rotate and flip image", "images", "image_transform", IMAGE_TYPES, "png",
    packages=("Pillow",), options=("angle", "flip"),
    note="Apply EXIF orientation, rotate clockwise by 0, 90, 180 or 270 degrees, then reflect horizontally, vertically or both. "
         "Exports a PNG without metadata, preserving decoded pixels and transparency. Single-frame images only; up to 40 million pixels.")
add("url-inspect", "URL inspector", "inspector", "link_tools", ("txt",), "json", input_mode="text",
    max_file_bytes=16384, fidelity="compromise",
    note="Inspect URL components, HTTP status, final URL and available response headers directly from your device. "
         "Records up to 10 HTTP redirects. "
         "Network failures leave a partial report. This is not a phishing, malware, DNS or ownership check.")


add("text-strip-formatting", "Remove text formatting", "inspector", "plain_text", ("txt", "html", "md", "docx"), "txt",
    input_mode="any", packages=("markdown-it-py", "defusedxml"), options=("input_format",),
    max_file_bytes=8*1024*1024, fidelity="compromise",
    note="Turn pasted text, UTF-8/UTF-16 text files, HTML, Markdown or Word DOCX body text into a UTF-8 TXT file locally. "
         "Removes styles, links and markup while retaining readable text and basic paragraph/table breaks. "
         "Plain text preserves literal punctuation. No OCR; DOCX headers, footers, images and comments are omitted. Up to 8 MiB per input.")

def manifest():
    return [asdict(tool) for tool in TOOLS.values()]
