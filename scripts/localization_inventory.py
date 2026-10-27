"""Extract independently maintained CLI messages and documentation prose."""
import ast
import argparse
import inspect
from html.parser import HTMLParser
import json
import re
import sys
from pathlib import Path
from localization_markdown import blocks, table_parts

ROOT = Path(__file__).resolve().parents[1]
texts = set()


def add(value):
    value = re.sub(r"\s+", " ", value).strip()
    if re.match(r"(?:import\s+\w|from\s+\S+\s+import\b|def\s+\w+\(|class\s+\w+[:(]|(?:const|let|var)\s+\w+\s*=|SELECT\s+.+\s+FROM|INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM|CREATE\s+TABLE|ALTER\s+TABLE|PRAGMA\s|<\/?[a-z][\w:-]*(?:\s|>|\/)|[\"']\s*[\w-]+=|\(\?)", value) or "sys.path.insert(" in value or "process.stdout.write(" in value:
        return
    if re.search(r"[A-Za-z]{2}", value) and (not re.fullmatch(r"[\w./:@#$%+*=-]+", value) or re.fullmatch(r"[A-Za-z]{2,}", value)):
        texts.add(value)


for source in (ROOT / "src/onekit").rglob("*.py"):
    for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            add(node.value)
        elif isinstance(node, ast.JoinedStr):
            parts = []
            number = 0
            for item in node.values:
                if isinstance(item, ast.Constant):
                    parts.append(item.value)
                else:
                    parts.append("{" + str(number) + "}")
                    number += 1
            add("".join(parts))

for node in ast.walk(ast.parse(inspect.getsource(argparse))):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "_" and node.args and isinstance(node.args[0], ast.Constant):
        add(node.args[0].value)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "ngettext":
        for argument in node.args[:2]:
            if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                add(argument.value)
for text in ("usage:", "options", "positional arguments", "Warning:", "ready", "Interface language"):
    texts.add(text)
texts.add("Languages:")

documents = [ROOT / name for name in ("README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "images/README.md")]
documents += [*sorted((ROOT / "docs").glob("*.md")), *sorted((ROOT / "tools").rglob("README.md"))]
manifest = {}
class DocumentationHTML(HTMLParser):
    def handle_data(self, value):
        add(value)

    def handle_starttag(self, tag, attributes):
        for name, value in attributes:
            if name in ("alt", "title", "aria-label") and value:
                add(value)

for source in documents:
    if not source.exists():
        continue
    content = source.read_text(encoding="utf-8")
    manifest[source.relative_to(ROOT).as_posix()] = content
    for kind, block in blocks(content):
        if block.startswith("Languages: [English]("):
            continue
        if kind == "prose" or (kind == "line" and re.match(r"\s*(?:[-+*]|\d+[.)])\s+", block)):
            add(block)
        elif kind != "code" and block.lstrip().startswith("|"):
            for cell in table_parts(block)[::2]:
                if not re.fullmatch(r"[\s:|-]*", cell):
                    add(cell)
    fenced = False
    for line in content.splitlines():
        if line.startswith("Languages: [English]("):
            continue
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced and line.strip() and not re.match(r"\s*(?:\|[\s:|-]+\||<!--|<img|<svg|<path|<a )", line):
            add(line)
            if "<" in line:
                DocumentationHTML().feed(line)

target = ROOT / "src/onekit/locales"
if "--check" in sys.argv:
    existing = json.loads((target / "en.json").read_text(encoding="utf-8"))
    missing, obsolete = sorted(texts - existing.keys()), sorted(existing.keys() - texts)
    print(f"CLI source alignment: {len(missing)} missing, {len(obsolete)} obsolete")
    if missing:
        print(f"First unregistered message: {missing[0]!a}")
    raise SystemExit(1 if missing or obsolete else 0)
target.mkdir(exist_ok=True)
(target / "en.json").write_text(json.dumps({key: key for key in sorted(texts)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "docs/localization-sources.json").write_text(json.dumps(list(manifest), indent=2) + "\n", encoding="utf-8")
print(f"CLI inventory: {len(texts)} texts, {len(manifest)} documents")
