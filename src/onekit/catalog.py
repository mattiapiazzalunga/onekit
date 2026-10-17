# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
"""Single source of truth for CLI discovery, web routes and runtime contracts."""
from dataclasses import asdict, dataclass, replace


@dataclass(frozen=True)
class Tool:
    id: str
    name: str
    group: str
    handler: str
    accepts: tuple[str, ...] = ("*",)
    produces: str = "*"
    browser: bool = False
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
    browser_max_total_bytes: int = 32 * 1024 * 1024
    browser_max_file_bytes: int = 32 * 1024 * 1024


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
        browser = pair in PURE or pair in {("md", "html"), ("html", "md"), ("image", "pdf"), ("xlsx", "csv"), ("xlsx", "json"), ("json", "xlsx"), ("csv", "xlsx")}
        packages = ("markdown-it-py",) if pair == ("md", "html") else ("markdownify",) if pair == ("html", "md") else ("Pillow",) if source == "image" and target != "base64" else ("openpyxl",) if "xlsx" in pair else ()
        native = not browser
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
        add(f"{source}-to-{target}", f"{LABELS.get(source, source.upper())} to {LABELS.get(target, target.upper())}", "converters", "converters", IMAGE_TYPES if source == "image" else (source,), target, browser=browser, packages=packages, engines=engine, fidelity="exact" if pair in PURE and source != "html" else "compromise", note="Formatting, fonts, layout, formulas or unsupported elements may change. Scanned PDFs require OCR first." if pair not in PURE else "Structured conversion; the output represents the source data.", options=("sheet",) if source == "xlsx" else ())

PDF_OPS = ["merge", "split", "remove-pages", "organize", "extract-pages", "compress", "repair", "edit", "rotate", "sign", "protect", "unlock", "validate-pdfa"]
for operation in PDF_OPS:
    native = operation in ("sign", "validate-pdfa")
    add(f"pdf-{operation}", f"{operation.replace('-', ' ').capitalize()} PDF", "pdf", "pdf", ("pdf",), "pdf" if operation != "validate-pdfa" else "json", browser=not native and operation not in ("protect", "unlock"), packages=("pypdf", "reportlab") if operation == "edit" else ("pypdf",) if not native else ("pyhanko",) if operation == "sign" else (), engines=("verapdf",) if operation == "validate-pdfa" else (), multiple=operation == "merge", fidelity="compromise" if operation in ("compress", "repair", "edit", "sign") else "exact", note="Repair is best effort. Editing adds text overlays. Signing requires a PKCS#12 certificate." if operation in ("repair", "edit", "sign") else "Compression is lossless and may not reduce already optimized files." if operation == "compress" else "Page operations preserve content. Encryption permissions are advisory.", options=("pages",) if operation in ("remove-pages", "organize", "extract-pages") else ("angle",) if operation == "rotate" else ("password",) if operation in ("protect", "unlock") else ("text", "x", "y", "page") if operation == "edit" else ("certificate", "password") if operation == "sign" else ())

for op in ("compress", "crop", "convert"):
    add(f"image-{op}", f"{op.capitalize()} image", "images", "images", IMAGE_TYPES, "image", browser=True, packages=("Pillow",), fidelity="compromise" if op == "compress" else "exact", note="Lossy formats discard detail. Animation and metadata can be removed; use a lossless format to preserve pixels.", options=("format", "quality") if op != "crop" else ("box",))
add("image-extract-pdf", "Extract images from PDF", "images", "images", ("pdf",), "image", browser=True, packages=("pypdf", "Pillow"))
for group, formats in (("video", ("mp4", "webm", "mkv", "mov", "avi", "gif")), ("audio", ("mp3", "wav", "flac", "ogg", "aac", "m4a", "mp4"))):
    add(f"{group}-convert", f"Convert {group}", group, "media", ("*",), "*", engines=("ffmpeg",), fidelity="compromise", note="Available codecs depend on your FFmpeg build; re-encoding can lose quality.", options=("format", "codec", "bitrate"))
add("archive-convert", "Convert archive", "archives", "archives", ("zip", "tar", "gz", "bz2", "xz"), "*", browser=True, note="ZIP and TAR variants are supported. Archive links and unsafe paths are rejected.", options=("format",))
add("font-convert", "Convert font", "fonts", "fonts", ("ttf", "otf", "woff", "woff2"), "*", packages=("fonttools",), note="Changes font containers; does not transform TrueType outlines into CFF outlines or vice versa.", options=("format",))
for op in ("inspect", "metadata-set", "metadata-remove", "count", "encoding-convert"):
    add(f"file-{op}", {"inspect": "Inspect file", "metadata-set": "Set metadata", "metadata-remove": "Remove metadata", "count": "Count text", "encoding-convert": "Convert text encoding"}[op], "inspector", "inspector", browser=op in ("inspect", "count", "encoding-convert"), produces="json" if op in ("inspect", "count") else "*", engines=("exiftool",) if op.startswith("metadata") else (), options=("metadata",) if op == "metadata-set" else ("encoding",) if op == "encoding-convert" else ())
for op in ("encrypt", "decrypt"):
    add(f"security-{op}", f"{op.capitalize()} files or folders", "security", "security", produces="onekit" if op == "encrypt" else "*", browser=True, packages=("pycryptodome",), options=("password",), multiple=op == "encrypt", note="Authenticated AES-256-GCM with scrypt. Losing the password makes recovery impossible.")

LANGUAGES = "JavaScript TypeScript JSX TSX Python Java C C++ C# Go Rust PHP Ruby Kotlin Swift Dart Scala Lua Bash Shell PowerShell SQL HTML CSS SCSS Less XML SVG JSON JSON5 JSONC YAML TOML Markdown MDX LaTeX GraphQL Vue Svelte Astro Solidity HCL Terraform Dockerfile R Julia Elixir Haskell".split()
VALIDATORS = LANGUAGES + ["XSD", "JSON-Schema", "CSV", "OpenAPI", "AsyncAPI"]
MINIFIERS = "JavaScript TypeScript JSX TSX HTML CSS JSON SVG GraphQL".split()
for operation, languages in (("format", LANGUAGES), ("validate", VALIDATORS), ("minify", MINIFIERS)):
    for language in languages:
        slug = language.lower().replace("++", "pp").replace("#", "sharp")
        built_in = language == "JSON" or operation == "validate" and language in ("Python", "XML", "SVG", "TOML", "CSV")
        add(f"dev-{operation}-{slug}", f"{operation.capitalize()} {language.replace('-', ' ')}", "developer", "developer", produces="json" if operation == "validate" else "*", browser=built_in, fidelity="compromise" if operation == "minify" else "exact", note="Validation checks the configured parser or compiler; project-wide types, imports and dependencies may require a local project.", options=())
for target in ("pdf", "docx", "md", "latex", "html", "json"):
    add(f"ocr-to-{target}", f"OCR to {LABELS.get(target, target.upper())}", "ocr", "ocr", ("pdf",) + IMAGE_TYPES, target, packages=("pytesseract", "Pillow", "pypdfium2", "python-docx"), engines=("tesseract",), fidelity="compromise", note="Recognition depends on scan quality and installed language packs. Equations and layout may need manual correction.", options=("language", "dpi"))
for kind in ("text", "json", "notebook", "latex", "pdf", "word", "code"):
    add(f"diff-{kind}", f"Compare {LABELS.get(kind, kind).replace('word', 'Word')} files", "diff", "diff", produces="json", browser=kind not in ("pdf", "word"), packages=("pypdf",) if kind == "pdf" else ("python-docx",) if kind == "word" else (), multiple=True, fidelity="compromise" if kind in ("pdf", "word", "latex") else "exact", note="Compares extracted text, not visual layout." if kind in ("pdf", "word") else "Notebook comparison can include Markdown, code or both. LaTeX text mode omits commands.", options=("mode",) if kind in ("notebook", "latex") else ())


for id in ("docx-to-md", "md-to-docx", "image-to-pptx", "pdf-to-md", "pdf-to-html", "pdf-to-docx", "pdf-protect", "pdf-unlock", "diff-pdf", "diff-word", "font-convert", "dev-format-xml", "dev-format-svg", "dev-format-toml", "dev-validate-json5", "dev-validate-jsonc", "dev-validate-yaml", "dev-validate-json-schema", "dev-validate-xsd"):
    TOOLS[id] = replace(TOOLS[id], browser=True, engines=())
for id, packages in {"docx-to-md": ("python-docx",), "md-to-docx": ("python-docx",), "font-convert": ("fonttools", "brotli"), "dev-format-toml": ("tomli-w",), "dev-validate-json5": ("json5",), "dev-validate-jsonc": ("json5",), "dev-validate-yaml": ("PyYAML",), "dev-validate-json-schema": ("jsonschema",), "dev-validate-xsd": ("xmlschema",)}.items():
    TOOLS[id] = replace(TOOLS[id], packages=packages)
for id, tool in list(TOOLS.items()):
    if "pypdf" in tool.packages:
        TOOLS[id] = replace(tool, packages=("pycryptodome",) + tool.packages)
TOOLS["file-encoding-convert"] = replace(TOOLS["file-encoding-convert"], options=("source_encoding", "encoding"))
TOOLS["file-inspect"] = replace(TOOLS["file-inspect"], packages=("Pillow", "pycryptodome", "pypdf"))
TOOLS["image-convert"] = replace(TOOLS["image-convert"], fidelity="compromise")
TOOLS["image-crop"] = replace(TOOLS["image-crop"], fidelity="compromise", options=("box", "format", "quality"))
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
        accepts = ("onekit",)
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
    TOOLS[id] = replace(tool, accepts=accepts, input_mode=mode, min_files=2 if tool.group == "diff" or id == "pdf-merge" else 1, max_files=2 if tool.group == "diff" else 256 if tool.multiple else 1, max_file_bytes=limit, browser_max_file_bytes=min(limit, 2_000_000 if tool.group == "diff" else 32 * 1024 * 1024))
TOOLS["image-to-base64"] = replace(TOOLS["image-to-base64"], packages=("Pillow",))
# Large-file support is opt-in: rendering, text extraction, compression and
# encryption have different expansion costs and retain their existing limits.
LARGE_BROWSER_PDF_TOOLS = frozenset({
    "pdf-merge", "pdf-split", "pdf-remove-pages", "pdf-organize",
    "pdf-extract-pages", "pdf-repair", "pdf-rotate", "pdf-unlock",
})
for id in LARGE_BROWSER_PDF_TOOLS:
    TOOLS[id] = replace(TOOLS[id], browser_max_file_bytes=100 * 1024 * 1024,
                        browser_max_total_bytes=100 * 1024 * 1024)
TOOLS["base64-to-image"] = replace(TOOLS["base64-to-image"], accepts=("base64", "txt"))
for id in ("video-convert", "audio-convert"):
    TOOLS[id] = replace(TOOLS[id], engines=("ffmpeg", "ffprobe"))


def manifest():
    return [asdict(tool) for tool in TOOLS.values()]
