# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Automatic CLI-only setup in the user's private OneKit cache."""
from __future__ import annotations

from .i18n import gettext as tr

import importlib
import importlib.util
import io
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

from .models import OneKitError

REQUIREMENTS = {'pdfminer.six': 'pdfminer.six==20260107', 'pdftopdfa': 'pdftopdfa==0.9.24', 'pikepdf': 'pikepdf[pdfa]==10.17.0', 'yt-dlp-ejs': 'yt-dlp-ejs==0.8.0', 'license-expression': 'license-expression==30.4.4', 'olefile': 'olefile==0.47', 'brotli': "brotli>=1.2.1,<2; sys_platform != 'win32' or platform_machine != 'ARM64'",
 'defusedxml': 'defusedxml>=0.7.1,<0.8',
 'asn1crypto': 'asn1crypto==1.5.1',
 'faster-whisper': 'faster-whisper>=1.2.1,<2',
 'fonttools': 'fonttools>=4.67,<5',
 'json5': 'json5>=0.14,<1',
 'jsonschema': 'jsonschema>=4.26,<5',
 'markdown-it-py': 'markdown-it-py>=4.2,<5',
 'markdownify': 'markdownify>=1.2.3,<2',
 'numpy': 'numpy>=2.3,<3',
 'onnxruntime': 'onnxruntime>=1.23.2,<2',
 'openpyxl': 'openpyxl>=3.1.5,<4',
 'pillow': 'Pillow>=13,<14',
 'pooch': 'pooch>=1.8.2,<2',
 'pycryptodome': 'pycryptodome>=3.24.1,<4',
 'pyhanko': 'pyhanko>=0.34,<1',
 'pypdf': 'pypdf>=6.21.2,<7',
 'pypdfium2': 'pypdfium2>=5.14,<6',
 'pytesseract': 'pytesseract>=0.3.13,<0.4',
 'python-barcode': 'python-barcode==0.16.1',
 'python-docx': 'python-docx>=1.2,<2',
 'python-pptx': 'python-pptx>=1.0.2,<2',
 'pyyaml': 'PyYAML>=6.0.3,<7',
 'reportlab': 'reportlab>=4.4,<5',
 'resvg-py': 'resvg-py==0.5.0',
 'ruff': 'ruff>=0.17,<0.18',
 'segno': 'segno>=1.6.6,<2',
 'stream-inflate': 'stream-inflate==0.0.12',
 'stream-unzip': 'stream-unzip==0.0.91',
 'stream-zip': 'stream-zip==0.0.84',
 'tomli-w': 'tomli-w>=1.2,<2',
 'xmlschema': 'xmlschema>=4.2,<5',
 'yt-dlp': 'yt-dlp>=2026.8.19,<2027',
 'zxing-cpp': 'zxing-cpp>=3.1.1,<4'}
MODULES = {"pdfminer.six": "pdfminer", "PyYAML": "yaml", "Pillow": "PIL", "markdown-it-py": "markdown_it", "python-docx": "docx", "python-pptx": "pptx", "fonttools": "fontTools", "pycryptodome": "Crypto", "zxing-cpp": "zxingcpp", "python-barcode": "barcode"}
# conda-forge packages supply native engines without changing the system installation.
ENGINE_PACKAGES = {
    "ffmpeg": "ffmpeg", "ffprobe": "ffmpeg", "pandoc": "pandoc", "soffice": "libreoffice",
    "gs": "ghostscript", "tesseract": "tesseract", "exiftool": "exiftool", "7z": "7zip",
    "node": "nodejs>=24,<25", "npm": "nodejs>=24,<25", "pdflatex": "texlive-core",
    "verapdf": "verapdf", "clang": "clang", "clang++": "clangxx", "clang-format": "clang-format",
    "gofmt": "go", "rustfmt": "rust", "ruby": "ruby", "php": "php", "bash": "bash", "sh": "bash",
    "luac": "lua", "dart": "dart-sdk", "javac": "openjdk", "kotlinc": "kotlin", "scalac": "scala",
    "pwsh": "powershell", "Rscript": "r-base", "julia": "julia", "tofu": "opentofu",
    "terraform": "terraform", "hadolint": "hadolint", "ghc": "ghc", "ormolu": "ormolu",
    "mix": "elixir", "elixir": "elixir", "shfmt": "shfmt", "latexindent": "texlive-core",
    "google-java-format": "google-java-format", "ktfmt": "ktfmt", "scalafmt": "scalafmt",
    "lua-format": "luaformatter", "hclfmt": "hclfmt", "dockerfmt": "dockerfmt",
    "swiftc": "swift", "swift-format": "swift", "csc": "mono",
}
PYTHON_ENGINES = {"ruff": "ruff>=0.17,<0.18", "sqlformat": "sqlparse", "sqlfluff": "sqlfluff"}


def cache():
    return Path(os.environ.get("ONEKIT_CACHE", Path.home() / ".cache" / "onekit"))


def activate():
    root = cache()
    packages = root / f"python-{sys.version_info.major}.{sys.version_info.minor}"
    if str(packages) not in sys.path:
        sys.path.insert(0, str(packages))
    prefix = root / "engines"
    paths = [root / "bin", root / "npm", root / "npm" / "bin", packages / ("Scripts" if os.name == "nt" else "bin"), prefix / "bin", prefix,
             prefix / "Scripts", prefix / "Library" / "bin"]
    os.environ["PATH"] = os.pathsep.join(dict.fromkeys([*map(str, paths), *os.environ.get("PATH", "").split(os.pathsep)]))
    current = os.environ.get("PYTHONPATH", "").split(os.pathsep)
    if str(packages) not in current:
        os.environ["PYTHONPATH"] = os.pathsep.join([str(packages), *filter(None, current)])
    importlib.invalidate_caches()
    return packages


def run(arguments):
    print(tr("OneKit setup:") + " " + " ".join(map(str, arguments)), file=sys.stderr)
    try:
        subprocess.run(list(map(str, arguments)), check=True, stdout=sys.stderr, stderr=sys.stderr, timeout=1800)
    except (subprocess.SubprocessError, OSError) as exc:
        raise OneKitError(f"Automatic setup failed: {exc}. Check your connection, disk space and platform support, then retry.") from exc


def python_packages(specs, *, no_deps=False):
    # Only the non-OCR API is used. Install its reviewed dependency set explicitly;
    # upstream currently declares the optional PaddleOCR stack as mandatory.
    if any(spec in specs for spec in ("pdftopdfa==0.9.24", "pdfminer.six==20260107")) and not no_deps:
        if sys.version_info < (3, 12):
            raise OneKitError("PDF/A conversion requires Python 3.12 or newer.")
        python_packages(["pikepdf[pdfa]==10.17.0", "lxml>=6.1.1", "click>=8.4.2", "colorama>=0.4.6", "tqdm==4.70.1", "fonttools>=4.67,<5", "charset-normalizer>=3.5.2", "numpy>=2.3,<2.4"])
        python_packages(["pdfminer.six==20260107", "pdftopdfa==0.9.24"], no_deps=True)
        specs = [spec for spec in specs if spec not in ("pdftopdfa==0.9.24", "pdfminer.six==20260107")]
    if not specs:
        return
    target = activate()
    target.mkdir(parents=True, exist_ok=True)
    run([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--target", target, *(["--no-deps"] if no_deps else []), *specs])
    importlib.invalidate_caches()


def micromamba():
    root = cache()
    binary = root / ("micromamba.exe" if os.name == "nt" else "micromamba")
    if binary.is_file():
        return binary
    machine = platform.machine().lower()
    system = platform.system()
    target = {("Windows", "amd64"): "win-64", ("Windows", "x86_64"): "win-64", ("Windows", "arm64"): "win-64",
              ("Linux", "x86_64"): "linux-64", ("Linux", "aarch64"): "linux-aarch64",
              ("Darwin", "x86_64"): "osx-64", ("Darwin", "arm64"): "osx-arm64"}.get((system, machine))
    if not target:
        raise OneKitError(f"Automatic native engine setup is unavailable for {system}/{machine}.")
    print(tr("OneKit setup: downloading the private native-engine installerâ€¦"), file=sys.stderr)
    try:
        with urllib.request.urlopen(f"https://micro.mamba.pm/api/micromamba/{target}/latest", timeout=120) as response:
            data = response.read(32 * 1024 * 1024 + 1)
        if len(data) > 32 * 1024 * 1024:
            raise ValueError("Installer exceeds size limit")
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:bz2") as archive:
            member = archive.getmember("Library/bin/micromamba.exe" if os.name == "nt" else "bin/micromamba")
            if not member.isfile() or member.size > 64 * 1024 * 1024:
                raise ValueError("Invalid installer archive")
            root.mkdir(parents=True, exist_ok=True)
            temporary = binary.with_suffix(".download")
            with archive.extractfile(member) as source:
                temporary.write_bytes(source.read())
            temporary.chmod(0o755)
            temporary.replace(binary)
    except (OSError, ValueError, KeyError, tarfile.TarError) as exc:
        raise OneKitError(f"Cannot download the automatic engine installer: {exc}") from exc
    return binary


SYSTEM_PACKAGES = {
    "soffice": ("TheDocumentFoundation.LibreOffice", "libreoffice", "libreoffice"),
    "hadolint": ("hadolint.hadolint", "hadolint", "hadolint"),
    "swiftc": ("Swift.Toolchain", "swift", "swift"),
    "swift-format": ("Swift.Toolchain", "swift-format", "swift-format"),
    "scalac": ("Lightbend.Scala", "scala", "scala"),
    "scalafmt": ("scalameta.scalafmt", "scalafmt", "scalafmt"),
    "ormolu": (None, "ormolu", "ormolu"),
    "lua-format": (None, "luaformatter", "lua-format"),
}
GO_ENGINES = {"shfmt": "mvdan.cc/sh/v3/cmd/shfmt@latest", "dockerfmt": "github.com/reteps/dockerfmt@latest"}
NPM_ENGINES = {"redocly": "@redocly/cli", "asyncapi": "@asyncapi/cli"}


def system_engine(name):
    windows, macos, linux = SYSTEM_PACKAGES[name]
    if os.name == "nt" and windows and shutil.which("winget"):
        run(["winget", "install", "--exact", "--id", windows, "--silent",
             "--accept-package-agreements", "--accept-source-agreements", "--disable-interactivity"])
        # Newly installed application paths are not inherited by this process.
        import winreg
        for hive, key in [(winreg.HKEY_CURRENT_USER, "Environment"),
                          (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")]:
            with winreg.OpenKey(hive, key) as handle:
                value, _ = winreg.QueryValueEx(handle, "Path")
                os.environ["PATH"] += os.pathsep + os.path.expandvars(value)
        for directory in [Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "LibreOffice" / "program"]:
            os.environ["PATH"] += os.pathsep + str(directory)
    elif platform.system() == "Darwin" and shutil.which("brew"):
        run(["brew", "install", macos])
    elif platform.system() == "Linux" and shutil.which("apt-get"):
        prefix = [] if os.geteuid() == 0 else ["sudo", "-n"]
        run([*prefix, "apt-get", "update"])
        run([*prefix, "apt-get", "install", "--yes", linux])
    else:
        raise OneKitError(f"Automatic installation of {name} requires a supported system package manager (winget, Homebrew or apt).")


def native_engines(names):
    from .tools.native import executable
    missing = []
    for name in dict.fromkeys(names):
        try:
            executable(name)
        except OneKitError:
            missing.append(name)
    python_packages([PYTHON_ENGINES[name] for name in missing if name in PYTHON_ENGINES])
    missing = [name for name in missing if name not in PYTHON_ENGINES]
    if not missing:
        return
    for name in list(missing):
        if os.name == "nt" and name in ("bash", "sh", "pdflatex", "latexindent"):
            SYSTEM_PACKAGES.setdefault(name, ("Git.Git" if name in ("bash", "sh") else "MiKTeX.MiKTeX", None, None))
        if name in SYSTEM_PACKAGES:
            system_engine(name)
            executable(name)
            missing.remove(name)
        elif name in GO_ENGINES:
            native_engines(["gofmt"])
            bindir = cache() / "bin"
            bindir.mkdir(parents=True, exist_ok=True)
            previous = os.environ.get("GOBIN")
            os.environ["GOBIN"] = str(bindir)
            try:
                run(["go", "install", GO_ENGINES[name]])
            finally:
                if previous is None:
                    os.environ.pop("GOBIN", None)
                else:
                    os.environ["GOBIN"] = previous
            executable(name)
            missing.remove(name)
        elif name in NPM_ENGINES:
            native_engines(["node", "npm"])
            run(["npm", "install", "--prefix", cache() / "npm", "--global", NPM_ENGINES[name]])
            executable(name)
            missing.remove(name)
    if not missing:
        return
    unknown = [name for name in missing if name not in ENGINE_PACKAGES]
    if unknown:
        raise OneKitError("No automatic installer is configured for: " + ", ".join(unknown))
    prefix = cache() / "engines"
    action = "install" if (prefix / "conda-meta").is_dir() else "create"
    run([micromamba(), action, "--yes", "--no-rc", "--root-prefix", cache() / "mamba",
         "--prefix", prefix, "--override-channels", "--channel", "conda-forge",
         *dict.fromkeys(ENGINE_PACKAGES[name] for name in missing)])
    activate()
    for name in missing:
        executable(name)


def ensure_tool(tool, options=None):
    from .tools.native import COPYLEFT
    options = options or {}
    activate()
    engines = list(tool.engines)
    if tool.id == "audio-download" and options.get("format", "original") == "original":
        engines = []
    if tool.group == "developer":
        from .tools.developer import engine_for
        engine = engine_for(tool)
        if engine:
            engines.append(engine)
    if os.environ.get("ONEKIT_ALLOW_COPYLEFT") == "0" and set(engines) & COPYLEFT:
        raise OneKitError("A required engine is disabled by ONEKIT_ALLOW_COPYLEFT=0.")
    missing = [name for name in tool.packages
               if MODULES.get(name, name.replace("-", "_")) not in sys.modules
               and importlib.util.find_spec(MODULES.get(name, name.replace("-", "_"))) is None]
    python_packages([REQUIREMENTS.get(name.lower(), name) for name in missing])
    if tool.id == "license-font" and not any(importlib.util.find_spec(name) for name in ("brotli", "brotlicffi")):
        # Windows ARM has no prebuilt Python Brotli wheel; Node ships a decoder.
        engines.append("node")
    if "rufo" in engines:
        native_engines(["ruby"])
        if not shutil.which("rufo"):
            run(["gem", "install", "rufo", "--no-document"])
        engines.remove("rufo")
    if tool.id == "video-download" and options.get("list_formats"):
        engines = []
    native_engines(engines)
    if "node" in engines and tool.id not in ("dev-regex-test", "license-font"):
        from .cli import install_node_engines
        target = Path(os.environ.get("ONEKIT_NODE_ENGINE_PATH", Path.home() / ".cache" / "onekit" / "node"))
        if not (target / "node_modules").is_dir():
            install_node_engines(target)
    if tool.id == "dev-format-powershell":
        from .tools.native import command
        command("pwsh", ["-NoProfile", "-NonInteractive", "-Command",
                "if(-not(Get-Module -ListAvailable PSScriptAnalyzer)){Install-Module PSScriptAnalyzer -Scope CurrentUser -Force -ErrorAction Stop}"], Path.cwd(), timeout=300)
    if tool.id == "dev-format-r":
        from .tools.native import command
        command("Rscript", ["--vanilla", "-e", 'if (!requireNamespace("styler", quietly=TRUE)) install.packages("styler", repos="https://cloud.r-project.org")'], Path.cwd(), timeout=600)
    if tool.id == "dev-format-julia":
        from .tools.native import command
        command("julia", ["--startup-file=no", "-e", 'using Pkg; if Base.find_package("JuliaFormatter") === nothing; Pkg.add("JuliaFormatter"); end'], Path.cwd(), timeout=600)
    if tool.group == "ocr":
        language = options.get("language", "eng")
        if not isinstance(language, str) or not re.fullmatch(r"[a-zA-Z_]+(?:\+[a-zA-Z_]+)*", language):
            raise OneKitError("Use Tesseract language codes such as eng or eng+ita.")
        data = cache() / "tessdata"
        data.mkdir(parents=True, exist_ok=True)
        for code in language.split("+"):
            target = data / f"{code}.traineddata"
            if not target.is_file():
                print(tr(f"OneKit setup: downloading OCR language {code}â€¦"), file=sys.stderr)
                try:
                    with urllib.request.urlopen(f"https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/{code}.traineddata", timeout=120) as response:
                        content = response.read(64 * 1024 * 1024 + 1)
                    if not content or len(content) > 64 * 1024 * 1024:
                        raise ValueError("Invalid OCR language data")
                    temporary = target.with_suffix(".download")
                    temporary.write_bytes(content)
                    temporary.replace(target)
                except (OSError, ValueError) as exc:
                    raise OneKitError(f"Cannot install OCR language {code}: {exc}") from exc
        os.environ["TESSDATA_PREFIX"] = str(data)
    # Whisper and U2Net already download and cache their models automatically in their handlers.
