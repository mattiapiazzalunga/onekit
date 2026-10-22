# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Isolated external engine adapters. No shell, network access or bundled executables."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from ..models import Artifact, OneKitError, Result

COPYLEFT = {"pandoc", "soffice", "gs", "ffmpeg", "ffprobe", "verapdf", "exiftool", "7z", "terraform", "hclfmt", "latexindent", "hadolint"}


def executable(name):
    if name in COPYLEFT and os.environ.get("ONEKIT_ALLOW_COPYLEFT") == "0":
        raise OneKitError(f"'{name}' is outside the default permissive license policy. This optional adapter is disabled. Review docs/engines.md before explicitly enabling it.")
    if os.name == "nt" and name in ("bash", "sh"):
        return windows_shell(name, shutil.which(name))
    aliases = {"gs": ("gs", "gswin64c", "gswin32c"), "soffice": ("soffice", "libreoffice")}
    for candidate in aliases.get(name, (name,)):
        path = shutil.which(candidate)
        if path:
            return path
        local = Path(sys.executable).parent / (candidate + ".exe" if os.name == "nt" else candidate)
        if local.is_file():
            return str(local)
    raise OneKitError(f"Install '{name}' and add it to PATH. Run 'onekit doctor' for engine requirements.")


def windows_shell(name, path):
    # System32/bash.exe launches WSL; it is not a Windows-compatible file parser.
    system32 = Path(os.environ.get("SystemRoot", "C:/Windows")) / "System32"
    if path and Path(path).parent != system32:
        return path
    roots = [Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git"]
    if os.environ.get("LOCALAPPDATA"):
        roots.append(Path(os.environ["LOCALAPPDATA"]) / "Programs" / "Git")
    for root in roots:
        for directory in ("usr/bin", "bin"):
            candidate = root / directory / f"{name}.exe"
            if candidate.is_file():
                return str(candidate)
    raise OneKitError(f"Install '{name}' (for example Git for Windows) and add it to PATH. The Windows WSL launcher cannot be used as this engine.")


def command(engine, arguments, cwd, *, stdin=None, timeout=120):
    path = executable(engine)
    try:
        result = subprocess.run([path, *map(str, arguments)], cwd=cwd, input=stdin, capture_output=True, timeout=timeout, check=False, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise OneKitError(f"'{engine}' exceeded its {timeout}s time limit.") from exc
    if result.returncode:
        raise OneKitError(f"'{engine}' failed: {result.stderr.decode('utf-8', errors='replace')[-1500:]}")
    return result.stdout


def process_file(file, engine, arguments, *, in_place=False):
    with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
        source = Path(directory, Path(file.name).name)
        source.write_bytes(file.data)
        data = command(engine, [*arguments, "./" + source.name], directory)
        return Result([Artifact(source.name, source.read_bytes() if in_place else data)])


def convert_document(file, source, target, options):
    # Semantic conversion stays useful even without a full office suite.
    if source == "docx" and target == "md":
        import io

        from docx import Document

        from .converters import text_document
        document = Document(io.BytesIO(file.data))
        return Result([text_document("\n\n".join(p.text for p in document.paragraphs), file, "md")])
    if source == "md" and target == "docx":
        return markdown_word(file)
    with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
        work = Path(directory)
        suffix = "tex" if source == "latex" else source
        input_path = work / f"input.{suffix}"
        input_path.write_bytes(file.data)
        out = work / f"output.{ 'tex' if target == 'latex' else target}"
        if source in ("docx", "pptx", "xlsx"):
            command("soffice", [f"-env:UserInstallation={ (work / 'profile').as_uri() }", "--headless", "--convert-to", "pdf", "--outdir", directory, input_path.name], directory)
            pdf = Artifact(f"{file.stem}.pdf", (work / "input.pdf").read_bytes())
            if target == "png":
                from .converters import pdf_images
                return Result(pdf_images(pdf, dpi=int(options.get("dpi", 144))))
            return Result([Artifact(f"{file.stem}.pdf", pdf.data)])
        if source == "latex" and target == "pdf":
            command("pdflatex", ["-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", directory, input_path.name], directory)
            return Result([Artifact(f"{file.stem}.pdf", (work / "input.pdf").read_bytes())])
        args = [input_path.name, "--from", "markdown" if source == "md" else source, "--to", "latex" if target == "latex" else "markdown" if target == "md" else target, "--output", out.name, "--sandbox"]
        if target == "latex":
            args.append("--standalone")
        if target == "pdf":
            args = [input_path.name, "--output", out.name, "--pdf-engine=pdflatex"]
        command("pandoc", args, directory)
        return Result([Artifact(f"{file.stem}.{out.suffix.lstrip('.')}", out.read_bytes())])


def pdfa(file, options):
    from ..models import require
    # ICC profiles have independent copyright; the caller supplies a licensed profile.
    profile = Path(require(options, "icc_profile")).resolve()
    if not profile.is_file():
        raise OneKitError("icc_profile must point to an installed sRGB ICC profile.")
    with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
        work = Path(directory)
        (work / "input.pdf").write_bytes(file.data)
        shutil.copyfile(profile, work / "srgb.icc")
        (work / "pdfa.ps").write_text('%!\n/ICCProfile (srgb.icc) def\n[/_objdef {icc_PDFA} /type /stream /OBJ pdfmark\n[{icc_PDFA} << /N 3 >> /PUT pdfmark\n[{icc_PDFA} ICCProfile (r) file /PUT pdfmark\n[/_objdef {OutputIntent_PDFA} /type /dict /OBJ pdfmark\n[{OutputIntent_PDFA} << /Type /OutputIntent /S /GTS_PDFA1 /DestOutputProfile {icc_PDFA} /OutputConditionIdentifier (sRGB) >> /PUT pdfmark\n[{Catalog} << /OutputIntents [{OutputIntent_PDFA}] >> /PUT pdfmark\n', encoding="ascii")
        command("gs", ["-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=pdfwrite", "-dPDFA=2", "-dPDFACompatibilityPolicy=1", "-sColorConversionStrategy=RGB", "-sOutputFile=output.pdf", "pdfa.ps", "input.pdf"], directory)
        return Result([Artifact(f"{file.stem}.pdf", (work / "output.pdf").read_bytes())], ["Run a standards validator on the output before relying on PDF/A conformance."])


def run_verapdf(file):
    import json
    from xml.etree import ElementTree

    from ..models import output
    with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
        Path(directory, "input.pdf").write_bytes(file.data)
        report = command("verapdf", ["--format", "xml", "input.pdf"], directory)
        root = ElementTree.fromstring(report)
        validations = [element.attrib for element in root.iter() if element.tag.rsplit("}", 1)[-1] == "validationReport"]
        details = {"compliant": bool(validations) and all(item.get("isCompliant") == "true" for item in validations), "reports": validations}
        return Result([output(file, "validation.json", json.dumps(details, indent=2))], details=details)


def markdown_word(file):
    import io

    from docx import Document
    from docx.shared import Pt
    from markdown_it import MarkdownIt

    from ..models import output
    document = Document()
    tokens = MarkdownIt("commonmark", {"html": False}).parse(file.text())
    style, list_styles, paragraph = None, [], None
    for token in tokens:
        if token.type == "heading_open":
            style = "Heading " + token.tag[1:]
            paragraph = document.add_paragraph(style=style)
        elif token.type == "heading_close":
            style = None
        elif token.type in ("bullet_list_open", "ordered_list_open"):
            list_styles.append("List Bullet" if token.type == "bullet_list_open" else "List Number")
        elif token.type in ("bullet_list_close", "ordered_list_close"):
            list_styles.pop()
        elif token.type in ("paragraph_open", "heading_open"):
            paragraph = document.add_paragraph(style=style or (list_styles[-1] if list_styles else None))
        elif token.type in ("fence", "code_block"):
            paragraph = document.add_paragraph()
            run = paragraph.add_run(token.content.rstrip("\n"))
            run.font.name = "Courier New"
            run.font.size = Pt(10)
        elif token.type == "inline":
            paragraph = paragraph or document.add_paragraph(style=style or (list_styles[-1] if list_styles else None))
            bold, italic, link = False, False, None
            for child in token.children or []:
                if child.type == "strong_open":
                    bold = True
                elif child.type == "strong_close":
                    bold = False
                elif child.type == "em_open":
                    italic = True
                elif child.type == "em_close":
                    italic = False
                elif child.type == "link_open":
                    link = child.attrGet("href")
                elif child.type == "link_close" and link:
                    paragraph.add_run(f" ({link})")
                    link = None
                elif child.type in ("softbreak", "hardbreak"):
                    paragraph.add_run("\n")
                else:
                    run = paragraph.add_run(child.content)
                    run.bold, run.italic = bold, italic
                    if child.type == "code_inline":
                        run.font.name = "Courier New"
    stream = io.BytesIO()
    document.save(stream)
    return Result([output(file, "docx", stream.getvalue())])


def inspect_media(file):
    """Read container/stream metadata using the configured local engine service."""
    from ..execution import current_context
    reader = current_context().media_probe
    if reader is not None:
        metadata = reader(file)
    else:
        with tempfile.TemporaryDirectory(prefix="onekit-media-probe-") as directory:
            path = Path(directory, "input." + file.kind)
            path.write_bytes(file.data)
            metadata = json.loads(command("ffprobe", ["-v", "error", "-protocol_whitelist", "file,pipe", "-show_format", "-show_streams", "-of", "json", path], directory, timeout=30))
    if not isinstance(metadata, dict) or not isinstance(metadata.get("streams", []), list) or not isinstance(metadata.get("format", {}), dict):
        raise OneKitError("The media metadata reader returned an invalid report.")
    return metadata
