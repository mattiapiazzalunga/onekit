# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import ast
import csv
import io
import json
import os
import re
import tempfile
import tomllib
from pathlib import Path
from xml.dom import minidom
from xml.etree import ElementTree

from ...models import Artifact, OneKitError, Result, output, parse_json

PRETTIER = {"javascript": "babel", "typescript": "typescript", "jsx": "babel", "tsx": "typescript", "html": "html", "css": "css", "scss": "scss", "less": "less", "json5": "json5", "jsonc": "json", "yaml": "yaml", "markdown": "markdown", "mdx": "mdx", "graphql": "graphql", "vue": "vue", "svelte": "svelte", "astro": "astro", "solidity": "solidity", "php": "php"}
FORMATTERS = {"java": ("google-java-format", ["-"], "java"), "c": ("clang-format", [], "c"), "cpp": ("clang-format", [], "cpp"), "csharp": ("clang-format", [], "cs"), "go": ("gofmt", [], "go"), "rust": ("rustfmt", ["--emit", "stdout"], "rs"), "ruby": ("rufo", [], "rb"), "kotlin": ("ktfmt", ["--stdin-name=input.kt", "-"], "kt"), "swift": ("swift-format", ["format"], "swift"), "dart": ("dart", ["format", "--output=show"], "dart"), "scala": ("scalafmt", ["--stdin"], "scala"), "lua": ("lua-format", [], "lua"), "bash": ("shfmt", [], "sh"), "shell": ("shfmt", [], "sh"), "sql": ("sqlformat", ["--reindent", "-"], "sql"), "latex": ("latexindent", ["-"], "tex"), "hcl": ("hclfmt", [], "hcl"), "terraform": ("tofu", ["fmt", "-"], "tf"), "dockerfile": ("dockerfmt", [], "Dockerfile"), "r": ("Rscript", ["-e", 'cat(paste(styler::style_text(readLines(file("stdin"))), collapse="\\n"))'], "R"), "julia": ("julia", ["--startup-file=no", "-e", "using JuliaFormatter; print(format_text(read(stdin, String)))"], "jl"), "elixir": ("mix", ["format", "-"], "ex"), "haskell": ("ormolu", [], "hs"), "powershell": ("pwsh", ["-NoProfile", "-NonInteractive", "-Command", "if(-not (Get-Module -ListAvailable PSScriptAnalyzer)){[Console]::Error.Write('Install PSScriptAnalyzer with Install-Module PSScriptAnalyzer -Scope CurrentUser.');exit 1};$s=[Console]::In.ReadToEnd();Invoke-Formatter -ScriptDefinition $s"], "ps1")}
VALIDATORS = {"javascript": ("node", ["--check", "input.js"], "js"), "typescript": ("tsc", ["--noEmit", "--strict", "input.ts"], "ts"), "jsx": ("tsc", ["--noEmit", "--allowJs", "--jsx", "preserve", "input.jsx"], "jsx"), "tsx": ("tsc", ["--noEmit", "--jsx", "preserve", "input.tsx"], "tsx"), "java": ("javac", ["-proc:none", "input.java"], "java"), "c": ("clang", ["-fsyntax-only", "input.c"], "c"), "cpp": ("clang++", ["-fsyntax-only", "input.cpp"], "cpp"), "go": ("gofmt", ["-e", "input.go"], "go"), "rust": ("rustfmt", ["--check", "input.rs"], "rs"), "php": ("php", ["-l", "input.php"], "php"), "ruby": ("ruby", ["-c", "input.rb"], "rb"), "bash": ("bash", ["-n", "input.sh"], "sh"), "shell": ("sh", ["-n", "input.sh"], "sh"), "lua": ("luac", ["-p", "input.lua"], "lua"), "dart": ("dart", ["analyze", "input.dart"], "dart"), "dockerfile": ("hadolint", ["input.Dockerfile"], "Dockerfile"), "terraform": ("terraform", ["fmt", "-check", "input.tf"], "tf"), "hcl": ("hclfmt", ["input.hcl"], "hcl"), "haskell": ("ghc", ["-fno-code", "input.hs"], "hs"), "elixir": ("elixir", ["--no-halt", "-e", 'Code.string_to_quoted!(File.read!("input.ex")); System.halt(0)'], "ex")}


VALIDATORS.update({
    "csharp": ("csc", ["/nologo", "/target:library", "input.cs"], "cs"),
    "kotlin": ("kotlinc", ["input.kt", "-d", "output.jar"], "kt"),
    "swift": ("swiftc", ["-frontend", "-parse", "input.swift"], "swift"),
    "scala": ("scalac", ["-Ystop-after:parser", "input.scala"], "scala"),
    "powershell": ("pwsh", ["-NoProfile", "-NonInteractive", "-Command", "$t=$null;$e=$null;[System.Management.Automation.Language.Parser]::ParseFile('input.ps1',[ref]$t,[ref]$e)|Out-Null;if($e.Count){$e|Out-String|Write-Error;exit 1}"], "ps1"),
    "sql": ("sqlfluff", ["parse", "--dialect", "ansi", "input.sql"], "sql"),
    "latex": ("pdflatex", ["-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "input.tex"], "tex"),
    "r": ("Rscript", ["--vanilla", "-e", "parse(file='input.R')"], "R"),
    "julia": ("julia", ["--startup-file=no", "-e", 'function validate(x); x isa Expr || return; x.head in (:error,:incomplete) && error("Invalid Julia syntax"); foreach(validate,x.args); end; validate(Meta.parseall(read("input.jl",String)))'], "jl"),
    "rust": ("rustfmt", ["--emit", "stdout", "input.rs"], "rs"),
    "terraform": ("tofu", ["fmt", "-write=false", "input.tf"], "tf"),
})


def engine_for(tool):
    # These operations are handled in-process and require no external executable.
    _, operation, language = tool.id.split("-", 2)
    if (language == "json" or
        operation == "format" and language in ("xml", "svg", "toml") or
        operation == "validate" and language in ("python", "xml", "svg", "json5", "jsonc", "yaml", "toml", "xsd", "json-schema", "csv")):
        return None
    if language in ("openapi", "asyncapi"):
        return "redocly" if language == "openapi" else "asyncapi"
    if operation == "minify" and language != "json":
        return "node"
    if language == "python" and operation == "format":
        return "ruff"
    if language in PRETTIER:
        return "node"
    if operation == "format" and language in FORMATTERS:
        return FORMATTERS[language][0]
    if operation == "validate" and language in VALIDATORS:
        return VALIDATORS[language][0]
    return {"javascript": "esbuild", "typescript": "esbuild", "jsx": "esbuild", "tsx": "esbuild", "css": "esbuild", "html": "html-minifier-terser", "svg": "svgo", "graphql": "prettier"}.get(language)


def run(tool, files, options):
    file = files[0]
    _, operation, language = tool.id.split("-", 2)
    text = file.text()
    if operation == "validate":
        try:
            validate(language, text, options, filename=file.name)
            report = {"valid": True, "language": language, "scope": "parser or configured project checks"}
        except (ValueError, SyntaxError, ElementTree.ParseError, OneKitError) as exc:
            if isinstance(exc, OneKitError) and ("Install " in str(exc) or "policy" in str(exc) or "No validator" in str(exc)):
                raise
            report = {"valid": False, "language": language, "errors": [str(exc)[:2000]]}
        return Result([output(file, "validation.json", json.dumps(report, indent=2))], details=report)
    if language == "json":
        value = parse_json(text)
        result = json.dumps(value, ensure_ascii=False, indent=2 if operation == "format" else None, separators=None if operation == "format" else (",", ":")) + ("\n" if operation == "format" else "")
    elif operation == "format" and language == "python":
        from ..native import command
        with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
            result = command("ruff", ["format", "--stdin-filename", "input.py", "-"], directory, stdin=text.encode()).decode()
    elif operation == "format" and language in ("xml", "svg"):
        if "<!DOCTYPE" in text.upper() or "<!ENTITY" in text.upper():
            raise OneKitError("XML declarations with DTDs or entities are not supported.")
        result = minidom.parseString(text).toprettyxml(indent="  ")
    elif operation == "format" and language == "toml":
        import tomli_w
        result = tomli_w.dumps(tomllib.loads(text))
    else:
        result = external(operation, language, text)
    compiled = operation == "minify" and language in ("typescript", "jsx", "tsx")
    return Result([output(file, "js", result) if compiled else Artifact(file.name, result.encode("utf-8"))])


def validate(language, text, options, *, filename=None):
    if language == "json":
        parse_json(text)
    elif language == "python":
        ast.parse(text)
    elif language == "toml":
        tomllib.loads(text)
    elif language in ("xml", "svg"):
        if "<!DOCTYPE" in text.upper() or "<!ENTITY" in text.upper():
            raise ValueError("DTD and entity declarations are disabled.")
        ElementTree.fromstring(text)
    elif language == "csv":
        rows = list(csv.reader(io.StringIO(text), strict=True))
        if rows and any(len(row) != len(rows[0]) for row in rows):
            raise ValueError("CSV rows have inconsistent field counts.")
    elif language == "json5":
        import json5
        json5.loads(text)
    elif language == "jsonc":
        string = r'"(?:\\.|[^"\\])*"'
        # Keep string contents intact while removing comments and trailing commas.
        cleaned = re.sub(string + r'|//[^\r\n]*|/\*[\s\S]*?\*/', lambda m: m[0] if m[0].startswith('"') else re.sub(r'[^\r\n]', ' ', m[0]), text)
        cleaned = re.sub(string + r'|,\s*(?=[}\]])', lambda m: m[0] if m[0].startswith('"') else '', cleaned)
        parse_json(cleaned)
    elif language == "yaml":
        import yaml
        try:
            yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ValueError(str(exc)) from exc
    elif language == "json-schema":
        import jsonschema
        schema = parse_json(text)
        try:
            jsonschema.validators.validator_for(schema).check_schema(schema)
        except jsonschema.exceptions.SchemaError as exc:
            raise ValueError(exc.message) from exc
    elif language in ("openapi", "asyncapi"):
        from ..native import command
        with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
            Path(directory, "spec.json").write_text(text, encoding="utf-8")
            command("redocly" if language == "openapi" else "asyncapi", ["lint", "spec.json"] if language == "openapi" else ["validate", "spec.json"], directory)
    elif language == "xsd":
        import xmlschema
        xmlschema.XMLSchema(text, allow="none", defuse="always")
    elif language in PRETTIER:
        external("format", language, text)
    elif language in VALIDATORS:
        from ..native import command
        engine, args, suffix = VALIDATORS[language]
        if language == "sql":
            dialect = options.get("dialect", "ansi")
            if not isinstance(dialect, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,39}", dialect):
                raise OneKitError("Use a SQL dialect name such as ansi or postgres.")
            args = [dialect if arg == "ansi" else arg for arg in args]
        with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
            name = Path(filename).name if language == "java" and filename and filename.endswith(".java") else f"input.{suffix}"
            args = [name if arg == f"input.{suffix}" else arg for arg in args]
            Path(directory, name).write_text(text, encoding="utf-8")
            command(engine, args, directory)
    else:
        # The same parser used to format rejects syntactically invalid inputs.
        external("format", language, text)


def external(operation, language, text):
    from ..native import command
    if language in PRETTIER or operation == "minify":
        directory = Path(os.environ.get("ONEKIT_NODE_ENGINE_PATH", Path.home() / ".cache" / "onekit" / "node"))
        if not (directory / "node_modules").is_dir():
            raise OneKitError("Install the optional Node engines with 'onekit engines install' (requires Node.js 24+).")
        script = Path(__file__).with_name("node-engine.mjs")
        payload = json.dumps({"operation": operation, "language": language, "text": text}).encode()
        return command("node", [str(script), str(directory.resolve())], directory, stdin=payload).decode()
    with tempfile.TemporaryDirectory(prefix="onekit-") as directory:
        if language in FORMATTERS:
            engine, arguments, suffix = FORMATTERS[language]
            if engine == "clang-format":
                arguments = [*arguments, f"--assume-filename=input.{suffix}"]
            return command(engine, arguments, directory, stdin=text.encode()).decode()
    raise OneKitError(f"No validator or formatter adapter is configured for {language}.")
