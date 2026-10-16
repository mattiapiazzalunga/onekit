# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: Apache-2.0
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
from .workflows import dump_workflow, load_workflow

_ = gettext.translation("onekit", localedir=Path(__file__).parent / "locales", fallback=True).gettext

PACKAGE_MODULES = {"PyYAML": "yaml", "Pillow": "PIL", "markdown-it-py": "markdown_it", "python-docx": "docx", "python-pptx": "pptx", "fonttools": "fontTools", "pycryptodome": "Crypto"}


def doctor(tool_id=None):
    from .tools.native import COPYLEFT, command, executable
    report = []
    for tool in ([TOOLS[tool_id]] if tool_id else TOOLS.values()):
        packages = list(tool.packages)
        engines = list(tool.engines)
        if tool.group == "developer" and not tool.browser:
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
        if "node" in engines and not (Path(os.environ.get("ONEKIT_NODE_ENGINE_PATH", Path.home() / ".cache" / "onekit" / "node")) / "node_modules").is_dir():
            missing.append("OneKit Node engines (onekit engines install)")
        if tool.id == "dev-format-powershell" and "pwsh" not in missing:
            try:
                command("pwsh", ["-NoProfile", "-NonInteractive", "-Command", "if(-not (Get-Module -ListAvailable PSScriptAnalyzer)){exit 1}"], Path.cwd(), timeout=10)
            except (OneKitError, OSError):
                missing.append("PSScriptAnalyzer (Install-Module PSScriptAnalyzer -Scope CurrentUser)")
        report.append({"tool": tool.id, "ready": not missing and not blocked, "missing": missing, "policyBlocked": blocked, "browser": tool.browser})
    return report


def read_files(paths, folders=False, tool=None, mapped=False):
    if tool and not folders and not mapped and not tool.min_files <= len(paths) <= tool.max_files:
        raise OneKitError(f"{tool.name} requires {tool.min_files}â€“{tool.max_files} input file(s).")
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
        descriptor, temporary = tempfile.mkstemp(prefix=".onekit-", dir=path.parent)
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
    root = argparse.ArgumentParser(prog="onekit", description=_("One simple toolkit. Your files stay yours."))
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
    workflow = commands.add_parser("workflow", help="Import or export a portable workflow JSON document")
    workflow.add_argument("action", choices=["import", "export"])
    workflow.add_argument("source", help="Workflow document or legacy steps JSON file")
    workflow.add_argument("-o", "--output", required=True)
    workflow.add_argument("--force", action="store_true")
    for name in ("run", "pipeline"):
        command = commands.add_parser(name)
        if name == "run":
            command.add_argument("tool", choices=TOOLS, metavar="TOOL")
            command.add_argument("--options", default="{}", help="JSON object of tool options")
        else:
            command.add_argument("--steps", required=True, help="Portable workflow JSON or legacy list of {tool, options} objects")
        command.add_argument("files", nargs="+")
        command.add_argument("-o", "--output", required=True)
        command.add_argument("--force", action="store_true")
        command.add_argument("--ask-password", action="store_true", help="Read a password without exposing it in shell history")
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "list":
            tools = [item for item in manifest() if not args.group or item["group"] == args.group]
            if args.json:
                print(json.dumps(tools, indent=2))
            else:
                for tool in tools:
                    print(f"{tool['id']:34} {'browser + CLI' if tool['browser'] else 'CLI':14} {tool['fidelity']}  {tool['name']}")
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
            document = load_workflow(args.source)
            write_files(Result([Artifact("workflow.onekit.json", dump_workflow(document))]), args.output, args.force)
            print("Workflow saved. Input files and passwords are not included.", file=sys.stderr)
            return 0
        if args.command == "run":
            options = json.loads(args.options)
            if not isinstance(options, dict):
                raise OneKitError("--options must contain a JSON object.")
            if args.ask_password:
                options["password"] = getpass.getpass("Password: ")
            result = execute(args.tool, read_files(args.files, args.tool == "security-encrypt", TOOLS[args.tool]), options)
        else:
            steps = load_workflow(args.steps)["steps"]
            if args.ask_password:
                password = getpass.getpass("Password: ")
                for step in steps:
                    step.setdefault("options", {})["password"] = password
            first = TOOLS[steps[0]["tool"]]
            result = pipeline(steps, read_files(args.files, tool=first, mapped=not first.multiple))
        write_files(result, args.output, args.force)
        return 0
    except (OneKitError, OSError, ValueError) as exc:
        print(f"onekit: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("onekit: cancelled", file=sys.stderr)
        return 130


def install_node_engines(directory=None):
    from .tools.native import command
    target = directory or Path(os.environ.get("ONEKIT_NODE_ENGINE_PATH", Path.home() / ".cache" / "onekit" / "node"))
    target.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).parent / "tools" / "developer" / "node"
    if (target / "package.json").exists() and json.loads((target / "package.json").read_text())["name"] != "onekit-developer-engines":
        raise OneKitError("This directory contains a different Node project; choose another destination.")
    for name in ("package.json", "package-lock.json"):
        shutil.copyfile(source / name, target / name)
    command("npm", ["ci", "--ignore-scripts", "--no-fund"], target, timeout=300)
    command("npm", ["audit", "--audit-level=low"], target)
    print(f"Developer engines installed in {target}.")


if __name__ == "__main__":
    sys.exit(main())
