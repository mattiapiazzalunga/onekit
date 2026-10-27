"""Markdown boundaries used by documentation inventory and rendering."""
import re


def table_parts(line):
    parts, current, fence = [], [], 0
    index = 0
    while index < len(line):
        if line[index] == "`":
            end = index
            while end < len(line) and line[end] == "`":
                end += 1
            length = end - index
            fence = 0 if fence == length else length if not fence else fence
            current.append(line[index:end])
            index = end
            continue
        if line[index] == "|" and not fence and (index == 0 or line[index-1] != "\\"):
            parts.extend(["".join(current), "|"])
            current = []
        else:
            current.append(line[index])
        index += 1
    parts.append("".join(current))
    return parts


def blocks(content):
    lines = content.splitlines(keepends=True)
    index = 0
    special = re.compile(r"\s*(?:#{1,6}\s|[-+*]\s|\d+[.)]\s|>|\||<|```|~~~|[-*_]{3,}\s*$)")
    while index < len(lines):
        line = lines[index]
        if line.lstrip().startswith(("```", "~~~")):
            marker = line.lstrip()[:3]
            code = [line]
            index += 1
            while index < len(lines):
                code.append(lines[index])
                index += 1
                if code[-1].lstrip().startswith(marker):
                    break
            yield "code", "".join(code)
        elif line.startswith(("    ", "\t")):
            yield "code", line
            index += 1
        elif re.match(r"\s*(?:[-+*]|\d+[.)])\s+", line):
            paragraph = [line]
            index += 1
            while index < len(lines) and re.match(r"^ {1,3}\S", lines[index]) and not special.match(lines[index]):
                paragraph.append(lines[index])
                index += 1
            yield "line", paragraph[0].rstrip("\r\n") + (" " + " ".join(part.strip() for part in paragraph[1:]) if len(paragraph) > 1 else "") + ("\n" if paragraph[-1].endswith("\n") else "")
        elif not line.strip() or special.match(line):
            yield "line", line
            index += 1
        else:
            paragraph = [line]
            index += 1
            while index < len(lines) and lines[index].strip() and not special.match(lines[index]) and not lines[index].startswith(("    ", "\t")):
                paragraph.append(lines[index])
                index += 1
            indentation = paragraph[0][:len(paragraph[0])-len(paragraph[0].lstrip())]
            yield "prose", indentation + " ".join(part.strip() for part in paragraph) + ("\n" if paragraph[-1].endswith("\n") else "")
