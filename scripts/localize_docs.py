"""Generate translated Markdown without changing code blocks or canonical files."""
import json
import os
import re
from pathlib import Path
from localization_markdown import blocks, table_parts

ROOT = Path(__file__).resolve().parents[1]
sources = json.loads((ROOT / "docs/localization-sources.json").read_text(encoding="utf-8"))
english = json.loads((ROOT / "src/onekit/locales/en.json").read_text(encoding="utf-8"))
languages = [language for language in json.loads((ROOT / "src/onekit/locales/languages.json").read_text(encoding="utf-8")) if language != "en"]
catalogs = {language: json.loads((ROOT / f"src/onekit/locales/{language}.json").read_text(encoding="utf-8")) for language in languages}
for language, catalog in catalogs.items():
    if catalog.keys() != english.keys():
        raise SystemExit(f"Incomplete {language} catalog; finish all translations before generating documentation.")
for language in languages:
    catalog = catalogs[language]
    for name in sources:
        source = ROOT / name
        target = ROOT / "docs/locales" / language / name
        def local_link(link):
            if not link or link.startswith(("#", "/")) or re.match(r"[a-z]+:", link):
                return link
            path, separator, anchor = link.partition("#")
            resolved = (source.parent / path).resolve()
            if not resolved.is_relative_to(ROOT):
                return link
            relative = resolved.relative_to(ROOT).as_posix()
            if relative in sources and not (navigation and relative == "README.md"):
                resolved = ROOT / "docs/locales" / language / relative
            return Path(os.path.relpath(resolved, target.parent)).as_posix() + (separator + anchor if separator else "")
        def rewrite_links(text):
            text = re.sub(r"(\]\()([^)]*)(\))", lambda match: match[1] + local_link(match[2]) + match[3], text)
            return re.sub(r'(\b(?:src|href)=)(["\'])([^"\']+)\2', lambda match: match[1] + match[2] + local_link(match[3]) + match[2], text)
        output = []
        for kind, line in blocks(source.read_text(encoding="utf-8")):
            navigation = line.startswith("Languages: [English](")
            if kind == "code" or line.lstrip().startswith("<!--"):
                output.append(line)
                continue
            key = re.sub(r"\s+", " ", line).strip()
            translated = catalog.get(key)
            if navigation:
                line = line.replace("Languages:", catalog.get("Languages:", "Languages:"), 1)
                translated = None
            elif line.lstrip().startswith("|"):
                parts = table_parts(line)
                for index in range(0, len(parts), 2):
                    cell = parts[index]
                    key_cell = re.sub(r"\s+", " ", cell).strip()
                    if key_cell in catalog:
                        parts[index] = cell[:len(cell)-len(cell.lstrip())] + catalog[key_cell] + cell[len(cell.rstrip()):]
                line = "".join(parts)
                translated = None
            elif line.lstrip().startswith("<"):
                pieces = re.split(r"(<[^>]+>)", line)
                for index in range(0, len(pieces), 2):
                    segment = pieces[index]
                    normalized = re.sub(r"\s+", " ", segment).strip()
                    if normalized in catalog:
                        pieces[index] = segment[:len(segment)-len(segment.lstrip())] + catalog[normalized] + segment[len(segment.rstrip()):]
                for index in range(1, len(pieces), 2):
                    pieces[index] = re.sub(r'(\b(?:alt|title|aria-label)=)(["\'])([^"\']*)\2', lambda match: match[1] + match[2] + catalog.get(match[3], match[3]).replace('"', '&quot;').replace("'", '&#39;') + match[2], pieces[index])
                line = "".join(pieces)
                translated = None
            if translated:
                if line.lstrip().startswith("#"):
                    heading = re.sub(r"^#+\s*", "", line.strip()).rstrip("#").strip().lower()
                    anchor = re.sub(r"[^\w -]", "", heading).replace(" ", "-")
                    output.append(f'<a id="{anchor}"></a>\n')
                indentation = line[:len(line) - len(line.lstrip())]
                prefix = re.match(r"^\s*(?:#{1,6}|[-+*]|\d+[.)]|>)\s+", line)
                if prefix:
                    translated = prefix[0] + re.sub(r"^\s*(?:#{1,6}|[-+*]|\d+[.)]|>)\s+", "", translated, count=1)
                    indentation = ""
                line = indentation + translated + ("\n" if line.endswith("\n") else "")
            rewritten, offset = [], 0
            for code in re.finditer(r"(?P<tick>`+).*?(?P=tick)", line):
                rewritten.extend([rewrite_links(line[offset:code.start()]), code[0]])
                offset = code.end()
            rewritten.append(rewrite_links(line[offset:]))
            line = "".join(rewritten)
            output.append(line)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("".join(output), encoding="utf-8")
