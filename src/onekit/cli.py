# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
from __future__ import annotations

import argparse
import getpass
import gettext
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

from . import __version__
from .api import execute, pipeline
from .catalog import TOOLS, manifest
from .models import Artifact, OneKitError
from .validation import MAX_BYTES
from .workflows import WORKFLOW_FILENAME, dump_workflow, load_workflow

_ = gettext.translation("onekit", localedir=Path(__file__).parent / "locales", fallback=True).gettext
WEBSITE_MESSAGE = "Try the free OneKit web app at https://onekit.org"

CONTRIBUTING_MESSAGE = (
    "Help build OneKit's open revolution: make everyday and agentic tools more efficient and effective. "
    "Contribute: https://github.com/mattiapiazzalunga/onekit/blob/main/CONTRIBUTING.md"
)
HELP_EPILOG = f"{WEBSITE_MESSAGE} {CONTRIBUTING_MESSAGE}"


def welcome(stream):
    print(f"Welcome to OneKit {__version__}! Your files stay yours.", file=stream)
    print(WEBSITE_MESSAGE, file=stream)
    print(CONTRIBUTING_MESSAGE, file=stream)

PACKAGE_MODULES = {"PyYAML": "yaml", "Pillow": "PIL", "markdown-it-py": "markdown_it", "python-docx": "docx", "python-pptx": "pptx", "fonttools": "fontTools", "pycryptodome": "Crypto", "zxing-cpp": "zxingcpp", "python-barcode": "barcode"}


def doctor(tool_id=None):
    from .setup import activate
    activate()
    from .tools.native import COPYLEFT, command, executable
    report = []
    for tool in ([TOOLS[tool_id]] if tool_id else TOOLS.values()):
        packages = list(tool.packages)
        engines = list(tool.engines)
        if tool.group == "developer":
            from .tools.developer import engine_for
            engine = engine_for(tool)
            if engine:
                engines.append(engine)
        missing = [name for name in packages if importlib.util.find_spec(PACKAGE_MODULES.get(name, name.replace("-", "_"))) is None]
        blocked = [name for name in engines if name in COPYLEFT and os.environ.get("ONEKIT_ALLOW_COPYLEFT") == "0"]
        for name in engines:
            if name in blocked:
                continue
            try:
                executable(name)
            except OneKitError:
                missing.append(name)
        if "node" in engines and tool.id != "dev-regex-test" and not (Path(os.environ.get("ONEKIT_NODE_ENGINE_PATH", Path.home() / ".cache" / "onekit" / "node")) / "node_modules").is_dir():
            missing.append("OneKit Node engines (onekit engines install)")
        if tool.id == "dev-format-powershell" and "pwsh" not in missing:
            try:
                command("pwsh", ["-NoProfile", "-NonInteractive", "-Command", "if(-not (Get-Module -ListAvailable PSScriptAnalyzer)){exit 1}"], Path.cwd(), timeout=10)
            except (OneKitError, OSError):
                missing.append("PSScriptAnalyzer (Install-Module PSScriptAnalyzer -Scope CurrentUser)")
        report.append({"tool": tool.id, "ready": not missing and not blocked, "missing": missing, "policyBlocked": blocked})
    return report


def read_files(paths, folders=False, tool=None, mapped=False):
    if tool and not folders and not mapped and not tool.min_files <= len(paths) <= tool.max_files:
        raise OneKitError(f"{tool.name} requires {tool.min_files}–{tool.max_files} input file(s).")
    files = []
    total = 0

    def append(path, name):
        nonlocal total
        size = path.stat().st_size
        if size > (tool.max_file_bytes if tool else MAX_BYTES):
            raise OneKitError(f"'{path.name}' exceeds the tool's per-file size limit.")
        if tool and tool.accepts != ("*",) and Artifact(name, b"").kind not in tool.accepts:
            raise OneKitError(f"Expected file types: {', '.join(tool.accepts)}. Rejected '{path.name}'.")
        if len(files) >= (tool.max_files if tool and not mapped else 256) or total + size > min(MAX_BYTES, tool.max_total_bytes if tool else MAX_BYTES):
            raise OneKitError("Input exceeds the limit of 256 files or 128 MiB.")
        with path.open("rb") as stream:
            data = stream.read(min(MAX_BYTES - total, tool.max_file_bytes if tool else MAX_BYTES) + 1)
        if tool and len(data) > tool.max_file_bytes:
            raise OneKitError("File grew beyond the tool's per-file size limit while reading.")
        total += len(data)
        if total > MAX_BYTES:
            raise OneKitError("Input exceeds 128 MiB.")
        files.append(Artifact(name, data))

    for value in paths:
        path = Path(value)
        if path.is_symlink():
            raise OneKitError("Symlink inputs are not supported.")
        if path.is_dir() and folders:
            for child in sorted(path.rglob("*")):
                if child.is_symlink():
                    raise OneKitError("Folders containing symlinks are not supported.")
                if child.is_file():
                    append(child, (Path(path.name) / child.relative_to(path)).as_posix())
        elif path.is_file():
            append(path, path.name)
        else:
            raise OneKitError(f"Cannot read '{path}'.")
    return files


def write_files(result, destination, force=False):
    target = Path(destination)
    as_directory = len(result.files) > 1 or target.is_dir() or not target.suffix
    paths = [(target / file.name if as_directory else target, file) for file in result.files]
    if len({str(path.resolve()) for path, _ in paths}) != len(paths):
        raise OneKitError("Multiple outputs have the same file name; rename the inputs.")
    for path, _ in paths:
        for parent in (path, *path.parents):
            if parent.is_symlink():
                raise OneKitError("Output paths cannot contain symlinks.")
        if path.exists() and not force:
            raise OneKitError(f"'{path}' already exists. Choose another destination or pass --force.")
    for path, file in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(prefix=".1kit-", dir=path.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(file.data)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        print(path)
    for warning in result.warnings:
        print(f"Warning: {warning}", file=sys.stderr)


def parser():
    root = argparse.ArgumentParser(prog="onekit", description=_("One simple toolkit. Your files stay yours."), epilog=HELP_EPILOG)
    root.add_argument("--version", action="version", version=__version__)
    commands = root.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="Browse all tools and their fidelity notes")
    listing.add_argument("--json", action="store_true")
    listing.add_argument("--group")
    diagnosis = commands.add_parser("doctor", help="Check optional Python packages and system engines")
    diagnosis.add_argument("tool", nargs="?", choices=TOOLS, metavar="TOOL")
    diagnosis.add_argument("--json", action="store_true")
    engines = commands.add_parser("engines", help="Install the optional, version-locked Node developer engines")
    engines.add_argument("action", choices=["install"])
    engines.add_argument("--directory", type=Path)
    workflow = commands.add_parser("workflow", help="Import or export a portable .1kit workflow document")
    workflow.add_argument("action", choices=["import", "export"])
    workflow.add_argument("source", help="OneKit .1kit workflow document")
    workflow.add_argument("-o", "--output", required=True)
    workflow.add_argument("--force", action="store_true")
    download = commands.add_parser("download", help="Download one video from YouTube or another yt-dlp site (requires internet)")
    download.add_argument("url")
    download.add_argument("-o", "--output", required=True)
    download.add_argument("--quality", choices=("best", "360", "480", "720", "1080", "1440", "2160"), default="best")
    authentication = download.add_mutually_exclusive_group()
    authentication.add_argument("--cookies", help="Read a Netscape cookies file for a site you are signed into")
    authentication.add_argument("--cookies-from-browser", choices=("firefox", "chrome", "edge", "chromium", "brave", "opera", "vivaldi", "safari"), help="Explicitly read login cookies from this local browser")
    download.add_argument("--format-id", help="A site format ID, or VIDEO_ID+AUDIO_ID")
    download.add_argument("--list-formats", action="store_true", help="Save available stream IDs and codecs as JSON without downloading a video")
    download.add_argument("--referer", help="HTTP(S) source page required by some direct video links")
    download.add_argument("--force", action="store_true")
    for name in ("run", "pipeline"):
        command = commands.add_parser(name)
        if name == "run":
            command.add_argument("tool", choices=TOOLS, metavar="TOOL")
            command.add_argument("--options", default="{}", help="JSON object of tool options")
        else:
            command.add_argument("--steps", required=True, help="Portable .1kit workflow document")
        command.add_argument("files", nargs="*" if name == "run" else "+")
        if name == "run":
            command.add_argument("--url", help="Source URL for downloaders, URL inspector or license checkers; requests go directly from this device")
        command.add_argument("-o", "--output", required=True)
        command.add_argument("--force", action="store_true")
        command.add_argument("--ask-password", action="store_true", help="Read a password without exposing it in shell history")
    for command in commands.choices.values():
        command.epilog = HELP_EPILOG
    return root


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    root = parser()
    if not arguments:
        welcome(sys.stdout)
        root.print_help()
        return 0
    args = root.parse_args(arguments)
    if sys.stderr.isatty() and not getattr(args, "json", False):
        welcome(sys.stderr)
    try:
        from .setup import ensure_tool
        if args.command == "download":
            options = {key: value for key in ("quality", "cookies", "cookies_from_browser", "format_id", "referer", "list_formats") if (value := getattr(args, key))}
            ensure_tool(TOOLS["video-download"], options)
            result = execute("video-download", [Artifact("url.txt", args.url.encode())], options)
            write_files(result, args.output, args.force)
            return 0
        if args.command == "list":
            tools = [item for item in manifest() if not args.group or item["group"] == args.group]
            if args.json:
                print(json.dumps(tools, indent=2))
            else:
                for tool in tools:
                    print(f"{tool['id']:34} {'CLI':14} {tool['fidelity']}  {tool['name']}")
            return 0
        if args.command == "engines":
            install_node_engines(args.directory)
            return 0
        if args.command == "doctor":
            report = doctor(args.tool)
            if args.json:
                print(json.dumps(report, indent=2))
            else:
                for item in report:
                    print(f"{item['tool']:34} {'ready' if item['ready'] else 'needs setup'}  {', '.join(item['missing'] + item['policyBlocked'])}")
            return 0 if all(item["ready"] for item in report) else 1
        if args.command == "workflow":
            from .models import Result
            if Path(args.output).suffix and Path(args.output).suffix.lower() != ".1kit":
                raise OneKitError("Workflow output must use the .1kit extension.")
            document = load_workflow(args.source)
            write_files(Result([Artifact(WORKFLOW_FILENAME, dump_workflow(document))]), args.output, args.force)
            print("Workflow saved. Input files and passwords are not included.", file=sys.stderr)
            return 0
        if args.command == "run":
            options = json.loads(args.options)
            if not isinstance(options, dict):
                raise OneKitError("--options must contain a JSON object.")
            if args.ask_password:
                options["password"] = getpass.getpass("Password: ")
            if args.url:
                if args.files:
                    raise OneKitError("Choose a URL or local input files, not both.")
                if args.tool in ("audio-youtube-download", "audio-download", "image-download", "url-inspect"):
                    files = [Artifact("url.txt", args.url.encode("utf-8"))]
                elif args.tool.startswith("license-"):
                    from .license_sources import download_license_source
                    files, source = download_license_source(args.url, args.tool, ref=options.get("ref", ""))
                    options["_source"] = source
                else:
                    raise OneKitError("--url is supported by downloaders, URL inspector and license checkers.")
            else:
                if not args.files:
                    raise OneKitError("Choose local input files or use --url with a license checker.")
                files = read_files(args.files, args.tool in ("security-encrypt", "license-code"), TOOLS[args.tool])
            ensure_tool(TOOLS[args.tool], options)
            result = execute(args.tool, files, options)
        else:
            steps = load_workflow(args.steps)["steps"]
            if args.ask_password:
                password = getpass.getpass("Password: ")
                for step in steps:
                    step.setdefault("options", {})["password"] = password
            first = TOOLS[steps[0]["tool"]]
            files = read_files(args.files, tool=first, mapped=not first.multiple)
            for step in steps:
                ensure_tool(TOOLS[step["tool"]], step.get("options", {}))
            result = pipeline(steps, files)
        write_files(result, args.output, args.force)
        return 0
    except (OneKitError, OSError, ValueError) as exc:
        print(f"onekit: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("onekit: cancelled", file=sys.stderr)
        return 130


def install_node_engines(directory=None):
    from .setup import activate, native_engines
    activate()
    native_engines(["node", "npm"])
    from .tools.native import command
    target = directory or Path(os.environ.get("ONEKIT_NODE_ENGINE_PATH", Path.home() / ".cache" / "onekit" / "node"))
    target.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).parent / "tools" / "developer" / "node"
    if (target / "package.json").exists() and json.loads((target / "package.json").read_text())["name"] != "onekit-developer-engines":
        raise OneKitError("This directory contains a different Node project; choose another destination.")
    for name in ("package.json", "package-lock.json"):
        shutil.copyfile(source / name, target / name)
    command("npm", ["ci", "--ignore-scripts", "--no-fund", "--no-audit"], target, timeout=300)
    command("npm", ["audit", "--audit-level=low"], target)
    print(f"Developer engines installed in {target}.")


if __name__ == "__main__":
    sys.exit(main())
