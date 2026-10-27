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

for source,target in (('xml','xlsx'),('xlsx','xml'),('xml','csv'),('csv','xml'),('xml','json'),('json','csv'),('json','xml'),('yaml','json'),('json','yaml')):
    add(f'{source}-to-{target}', f'{LABELS.get(source,source.upper())} to {LABELS.get(target,target.upper())}',
        'converters','structured_data',(source,),target,
        input_mode='typed' if source=='xlsx' else 'text',
        packages=tuple(['defusedxml'] if source=='xml' else [])+tuple(['openpyxl'] if 'xlsx' in (source,target) else [])+tuple(['PyYAML'] if 'yaml' in (source,target) else []),
        options=('sheet',) if source=='xlsx' else ('delimiter',) if source=='csv' else (),
        max_file_bytes=8*1024*1024,
        note='XML tables use repeated flat records. JSON to XML preserves types using a typed root/item schema; XML attributes use @ and text uses #text in JSON. Spreadsheet formulas are not evaluated; the first sheet is used by default. Review schema and values after conversion.')
add('tiff-to-svg','TIFF to SVG','converters','vector_images',('tiff',),'svg',packages=('Pillow',),options=('colors','resolution'),fidelity='compromise',
    note='Vectorizes the first TIFF frame as palette-based vector tiles, without an embedded bitmap. Gradients and fine detail are approximated.')
add('svg-to-png','SVG to PNG','converters','vector_images',('svg',),'png',input_mode='text',packages=('Pillow','defusedxml','resvg-py'),options=('scale',),fidelity='compromise',max_file_bytes=8*1024*1024,
    note='Renders static, self-contained SVG to PNG. External resources, scripts, animation and embedded images are rejected. Fonts may render differently across devices.')
add('epub-to-pdf','EPUB to PDF','converters','epub_pdf',('epub',),'pdf',packages=('reportlab','Pillow','defusedxml'),fidelity='compromise',max_file_bytes=32*1024*1024,
    note='Exports basic text in EPUB reading order. CSS, images, fixed layouts and interactive content are omitted; encrypted or DRM-protected books are rejected.')
for target in ('xlsx','csv'):
    add(f'pdf-tables-to-{target}',f'PDF tables to {LABELS.get(target,target.upper())}','converters','pdf_tables',('pdf',),target,
        packages=('pypdf',)+(('openpyxl',) if target=='xlsx' else ()),options=('pages',),fidelity='compromise',
        note='Detects tables from aligned selectable text. Scans require OCR; complex layouts, merged cells and column alignment require review. Excel uses one sheet per table; CSV exports one file per table.')

TEXT_NAMES = {'md':'Markdown','html':'HTML','docx':'Word','pptx':'PowerPoint','xlsx':'Excel','csv':'CSV','json':'JSON','xml':'XML','yaml':'YAML','epub':'EPUB','txt':'TXT','pdf':'PDF'}
TEXT_EXPORTS = {
    'md': (('markdown-it-py',),(), 'Extracts readable Markdown text, removing markup. Headings, lists and tables lose formatting; images and scripts are not exported.'),
    'html': ((),(), 'Extracts readable HTML body text without running scripts or fetching resources. Formatting, images, hidden content and styles are omitted.'),
    'docx': (('defusedxml',),(), 'Extracts Word DOCX body paragraphs and tables to UTF-8. Images, headers, footers, comments and automatic numbering are not exported.'),
    'pptx': (('defusedxml',),(), 'Extracts PowerPoint slide text in presentation order. Images, speaker notes and visual layout are not exported; review text order within slides.'),
    'xlsx': (('openpyxl',),('sheet',), 'Exports one Excel worksheet as tab-separated UTF-8 text. Uses stored formula results without recalculation; formatting and other sheets are omitted.'),
    'csv': ((),('delimiter',), 'Converts CSV rows into quoted, tab-separated UTF-8 TXT. Select the input delimiter. Embedded tabs and newlines remain quoted.'),
    'json': ((),(), 'Validates and formats JSON as UTF-8 TXT, preserving its data structure rather than flattening values.'),
    'xml': (('defusedxml',),(), 'Validates XML and exports its markup as UTF-8 TXT. DTDs and entities are rejected; this does not flatten XML into prose.'),
    'yaml': (('PyYAML',),(), 'Validates YAML and exports its source, including comments, as UTF-8 TXT. Unsafe tags, cyclic aliases and duplicate mapping keys are rejected.'),
    'epub': (('defusedxml',),(), 'Extracts EPUB chapter text in reading order. Images, CSS and interactive content are omitted; encrypted or DRM-protected books are rejected.'),
}
TEXT_IMPORTS = {
    'pdf': (('reportlab','Pillow'),(), 'Creates a PDF with basic paragraph layout from plain text. Original TXT line breaks become paragraphs; unsupported characters or excessive page counts are reported.'),
    'docx': (('python-docx',),(), 'Creates a Word DOCX document from plain text, using one paragraph per line. No formatting or document structure is inferred.'),
    'html': ((),(), 'Creates a safe HTML document with escaped plain text and preserved whitespace. Source markup is displayed literally, never executed.'),
    'md': ((),(), 'Wraps plain TXT in a literal Markdown code block, preserving whitespace and syntax. Headings, lists and links are not inferred.'),
    'csv': ((),('delimiter',), 'Parses consistently delimited TXT rows and writes comma-separated CSV. Choose tabs, commas, semicolons, pipes or automatic detection. No column structure is guessed from prose.'),
    'xlsx': (('openpyxl',),('delimiter',), 'Parses delimited TXT into an Excel worksheet. Cells are stored as text, preserving leading zeros and preventing formula execution. Requires consistent column counts.'),
    'json': ((),(), 'Requires valid JSON already contained in the TXT file. Validates and formats the data; arbitrary prose is not converted into an invented JSON schema.'),
    'xml': (('defusedxml',),(), 'Requires valid XML already contained in the TXT file. Validates its markup and writes UTF-8 XML; DTDs and entities are rejected.'),
    'yaml': (('PyYAML',),(), 'Requires valid YAML contained in the TXT file. Validates and preserves its source and comments; unsupported values, duplicate keys and unsafe tags are rejected.'),
}
for source,(packages,options,note) in TEXT_EXPORTS.items():
    add(f'{source}-to-txt',f'{TEXT_NAMES[source]} to TXT','converters','text_converters',(source,),'txt',packages=packages,options=options,
        input_mode='typed' if source in ('docx','pptx','xlsx','epub') else 'text',
        fidelity='exact' if source in ('json','xml','yaml','csv') else 'compromise',note=note)
for target,(packages,options,note) in TEXT_IMPORTS.items():
    add(f'txt-to-{target}',f'TXT to {TEXT_NAMES[target]}','converters','text_converters',('txt',),target,packages=packages,
        options=(*options,'source_encoding'),input_mode='encoded-text',fidelity='compromise' if target in ('pdf','docx') else 'exact',note=note)

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
TOOLS["pdf-to-pdfa"] = replace(TOOLS["pdf-to-pdfa"], packages=("pdftopdfa", "pikepdf", "jsonschema", "fonttools", "pdfminer.six"), engines=(), options=("icc_profile", "profile"), note="Convert to PDF/A-2b or 3b locally with embedded fonts. The exact output is validated before download. Unsupported content can be removed or rejected; review the result.")
TOOLS["pdf-validate-pdfa"] = replace(TOOLS["pdf-validate-pdfa"], name="Validate PDF/A", packages=("pikepdf", "jsonschema", "fonttools"), engines=(), options=("profile",), note="Validate PDF/A-1b, 2b or 3b with pikepdf. Unsupported constructs are reported as not checked, never as compliant. Other conformance levels are not supported.")
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
    elif tool.handler == 'text_converters':
        mode = tool.input_mode
    elif tool.group == "converters" and tool.accepts[0] in ("md", "latex", "html", "json", "csv", "base64", "xml", "yaml", "svg"):
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


add("image-add-text", "Add text to image", "images", "image_text", IMAGE_TYPES, "png",
    packages=("Pillow",), options=("text", "font_size", "color", "position", "margin", "x", "y", "text_boxes"), fidelity="compromise",
    note="Adds Western European text to a new PNG with adjustable size, color and position. Animation and metadata are not retained.")
add("pdf-page-numbers", "Add page numbers to PDF", "pdf", "pdf.page_numbers", ("pdf",), "pdf",
    packages=("pypdf", "reportlab"), options=("pages", "start_number", "number_style", "font_size", "position", "margin", "color"),
    note="Adds sequential numbers to all or selected pages, retaining source text and graphics. Existing digital signatures are invalidated.")

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
    ("video-extract-audio", "Extract audio from video", "mp3", ()),
    ("video-mute", "Remove audio from video", "mp4", ()),
    ("video-trim", "Trim video", "mp4", ("start", "end")),
    ("video-to-frames", "Video to frames", "png", ("start", "duration", "fps", "width", "all_frames")),
    ("video-compress", "Compress video", "mp4", ("compression_level",)),
    ("video-speed", "Change video speed", "mp4", ("speed",)),
    ("video-to-gif", "Video to GIF", "gif", ("start", "duration", "fps", "width")),
):
    add(id, name, "video", "video_edit", TOOLS["video-convert"].accepts, produces,
        packages=("Pillow",) if id == 'video-to-frames' else (),
        engines=("ffmpeg", "ffprobe"), options=options, fidelity="compromise",
        note={
            "video-extract-audio": "Extracts the first audio track as MP3 at 192 kbps using FFmpeg. Requires a video containing audio; re-encoding may lose quality.",
            "video-mute": "Exports MP4 without any audio tracks using FFmpeg. Video is re-encoded and may lose quality.",
            "video-to-frames": "Extracts PNG frames from a video using FFmpeg. Choose start, duration and width. Up to 120 frames: original-frame mode preserves each frame in the interval; otherwise timestamps are sampled at the requested frame rate.",
            "video-trim": "Keeps the selected start-to-end range in seconds and exports MP4 with audio when present. Re-encoding may lose quality.",
        }.get(id, "Processes locally with FFmpeg. Re-encoding may lose quality. GIF output has no audio."))
add("audio-to-text", "Audio to text", "audio", "transcription", TOOLS["audio-convert"].accepts, "txt",
    packages=("faster-whisper",), options=("language",), fidelity="compromise",
    note="Transcribes locally with Whisper tiny (multilingual). The model downloads on first use; no audio is uploaded. Recognition can make mistakes.")


add('file-checksum','Calculate checksum','inspector','file_checksum',('*',),'json',input_mode='any',multiple=True,min_files=1,max_files=20,
    options=('algorithm','expected'),note='Calculates SHA-256, SHA-512, SHA-1 or MD5 locally. An optional expected checksum can be compared against one file. A checksum does not verify a digital signature or establish file safety.')
add('signature-verify','Verify digital signature','security','signatures',('*',),'json',input_mode='any',multiple=True,min_files=1,max_files=2,
    packages=('pypdf','asn1crypto','pycryptodome'),
    note='Offline cryptographic verification of PDF and CMS/P7M/P7S signatures using embedded certificates. Detached signatures require the original file. Trust chains, revocation, qualified-signature status and trusted timestamps are not checked.')
add('pdf-to-text','PDF to text','converters','pdf_text',('pdf',),'txt',packages=('pypdf',),options=('pages','layout'),fidelity='compromise',
    note='Extracts selectable text to UTF-8, optionally retaining approximate layout. Scans require OCR; reading order, tables and columns need review.')
add('gif-to-images','GIF to images','converters','image_frames',('gif',),'png',packages=('Pillow',),fidelity='compromise',
    note='Exports each GIF frame as a composed PNG, respecting disposal and transparency. Up to 120 frames and 40 million total pixels. Timing is included in the result details.')
add('png-to-svg','PNG to SVG','converters','vector_images',('png',),'svg',packages=('Pillow',),options=('colors','resolution'),fidelity='compromise',
    note='Vectorizes a PNG as palette-based vector tiles, without embedding a bitmap. Gradients and fine detail are approximated; transparent pixels are composited on white.')
add('mp4-to-mp3','MP4 to MP3','video','video_edit',('mp4',),'mp3',engines=('ffmpeg','ffprobe'),fidelity='compromise',
    note='Extracts the first audio track of an MP4 as MP3 at 192 kbps. Requires an audio track; re-encoding may lose quality.')
add('video-to-text','Video to text','video','transcription',TOOLS['video-convert'].accepts,'txt',packages=('faster-whisper',),options=('language',),fidelity='compromise',
    note='Transcribes the audio of a video locally with multilingual Whisper tiny. Exports UTF-8 text and timestamped segments. Recognition can make mistakes; this does not read subtitles or text visible in frames.')

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


add("color-palette", "Color Palette Generator", "design", "design", ("txt",), "json",
    input_mode="text", max_file_bytes=128, max_total_bytes=1024*1024,
    options=("harmony", "lightness", "chroma", "hue", "format"),
    note="Five-color OKLCH palettes with sRGB chroma reduction and WCAG text contrast. Harmony rules are design heuristics, not accessibility guarantees.")


add("color-picker", "Color Picker", "design", "photo_tools", (*IMAGE_TYPES, "txt"), "json",
    packages=("Pillow",), options=("x", "y"),
    note="Read a six-digit HEX color from TXT or sample an EXIF-oriented image pixel. Reports visible sRGB, original RGBA, OKLCH and text contrast. Transparent pixels are composited on white.")
add("image-extract-colors", "Extract Image Colors", "design", "photo_tools", IMAGE_TYPES, "json",
    packages=("Pillow",), options=("colors",),
    note="Median-cut dominant colors from a bounded image sample. Excludes fully transparent pixels; partial transparency is composited on white. Color fractions describe the sample, not semantic objects.")
add("jpg-to-svg", "JPG to SVG", "images", "photo_tools", ("jpeg",), "svg",
    packages=("Pillow",), options=("colors", "resolution"), fidelity="compromise",
    note="Creates real palette-based vector paths by merging color tiles, without embedding a bitmap. Photographs become posterized; curved outlines and fine gradients are approximated. Best for simple flat artwork.")
add("image-repair", "Repair Photo Defects", "images", "photo_tools", IMAGE_TYPES, "png",
    packages=("Pillow", "numpy"), options=("regions", "iterations", "size"), fidelity="compromise",
    note="Clean small speckles with a median filter or reconstruct selected areas by harmonic diffusion. Estimates surrounding colors; cannot recover hidden originals or repair every photographic defect. Saves a new PNG.")
add("image-remove-watermark", "Remove Image Watermark", "images", "photo_tools", IMAGE_TYPES, "png",
    packages=("Pillow", "numpy"), options=("regions", "iterations"), fidelity="compromise",
    note="Reconstruct manually selected watermark areas from surrounding pixels using harmonic diffusion. Estimates missing content; large marks, textures and faces may not reconstruct convincingly. No automatic mark detection.")
add("image-sharpen", "Sharpen and Deblur Image", "images", "photo_tools", IMAGE_TYPES, "png",
    packages=("Pillow", "numpy"), options=("method", "radius", "amount", "iterations"), fidelity="compromise",
    note="Unsharp masking or bounded Gaussian Richardson-Lucy deconvolution. Deblurring assumes a blur model and may amplify noise or halos; missing detail cannot be guaranteed. Deconvolution is limited to one million pixels.")
add("pdf-remove-watermark", "Remove PDF Watermark", "pdf", "pdf_design", ("pdf",), "pdf",
    packages=("pypdf",), options=("text", "mode", "objects"), fidelity="compromise",
    note="Inspect and remove selected text, images and form invocations, including nested forms and font-encoded text. Removes tagged watermark artifacts and watermark annotations automatically. Untagged objects require selection or exact text; flattened marks cannot be separated from their image. Review every page.")
add("pdf-make-fillable", "Make PDF Fillable", "pdf", "pdf_design", ("pdf",), "pdf",
    packages=("pypdf",), options=("fields",),
    note="Add named AcroForm text fields, checkboxes and dropdown choices using normalized top-left rectangles. Keeps existing fields and page contents. No automatic blank detection or XFA conversion; verify reader compatibility.")
