# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import difflib
import io
import json
import re

from ...models import OneKitError, Result, output, parse_json


def _unified_lines(matcher, fromfile, tofile):
    """Format the existing line matches with the standard three-line context."""
    def location(start, stop):
        length = stop-start
        return str(start+1) if length == 1 else f"{start if not length else start+1},{length}"

    started = False
    for group in matcher.get_grouped_opcodes(3):
        if not started:
            yield f"--- {fromfile}\n"
            yield f"+++ {tofile}\n"
            started = True
        first, last = group[0], group[-1]
        yield f"@@ -{location(first[1], last[2])} +{location(first[3], last[4])} @@\n"
        for kind, start, end, right_start, right_end in group:
            if kind == 'equal':
                for line in matcher.a[start:end]:
                    yield ' '+line
            else:
                if kind in ('delete', 'replace'):
                    for line in matcher.a[start:end]:
                        yield '-'+line
                if kind in ('insert', 'replace'):
                    for line in matcher.b[right_start:right_end]:
                        yield '+'+line


def extract(file, kind, options):
    if kind == "pdf":
        from pypdf import PdfReader
        return "\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(file.data)).pages)
    if kind == "word":
        from docx import Document
        doc = Document(io.BytesIO(file.data))
        return "\n".join([p.text for p in doc.paragraphs] + ["\t".join(cell.text for cell in row.cells) for table in doc.tables for row in table.rows])
    text = file.text()
    if kind == "json":
        return json.dumps(parse_json(text), indent=2, sort_keys=True, ensure_ascii=False)
    if kind == "notebook":
        mode = options.get("mode", "both")
        if mode not in ("both", "markdown", "code"):
            raise OneKitError("Notebook mode must be both, markdown or code.")
        cells = json.loads(text).get("cells", [])
        return "\n\n".join("".join(cell.get("source", [])) for cell in cells if cell.get("cell_type") in (("markdown", "code") if mode == "both" else (mode,)))
    if kind == "latex" and options.get("mode", "all") == "text":
        text = re.sub(r"(?m)(?<!\\)%.*$", "", text)
        text = re.sub(r"\\(?:begin|end|label|ref|cite|usepackage|documentclass)\*?(?:\[[^\]]*\])?\{[^}]*\}", "", text)
        text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", text)
        return text.replace("{", "").replace("}", "")
    return text


def run(tool, files, options):
    if len(files) != 2:
        raise OneKitError("Comparison requires exactly two files.")
    kind = tool.id.removeprefix("diff-")
    if kind == "notebook":
        return notebook_diff(files, options)
    left, right = [extract(file, kind, options) for file in files]
    a, b = left.splitlines(keepends=True), right.splitlines(keepends=True)
    # SequenceMatcher is quadratic on adversarial inputs. Bound comparison size.
    if max(len(a), len(b)) > 10000 or len(left) + len(right) > 2_000_000:
        raise OneKitError("Compare at most 10,000 lines and 2 million characters at a time.")
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=True)
    blocks = [{"kind": tag, "left": a[i:j], "right": b[k:l], "leftStart": i, "rightStart": k} for tag, i, j, k, l in matcher.get_opcodes()]
    patch = "".join(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n" for line in _unified_lines(matcher, files[0].name, files[1].name))
    details = {"left": left, "right": right, "equal": left == right, "blocks": blocks, "patch": patch}
    return Result([output(files[0], "diff.json", json.dumps(details, ensure_ascii=False, indent=2))], details=details)


def notebook_diff(files, options):
    import copy
    documents = [parse_json(file.text()) for file in files]
    mode = options.get("mode", "both")
    if mode not in ("both", "markdown", "code"):
        raise OneKitError("Notebook mode must be both, markdown or code.")
    kinds = ("markdown", "code") if mode == "both" else (mode,)

    def selected(document):
        cells = document.get("cells")
        if not isinstance(cells, list) or len(cells) > 10000:
            raise OneKitError("A notebook must contain a list of at most 10,000 cells.")
        indices = [i for i, cell in enumerate(cells) if cell.get("cell_type") in kinds]
        texts = ["".join(cells[i].get("source", [])) for i in indices]
        if sum(len(text) for text in texts) > 1_000_000:
            raise OneKitError("Compare at most one million source characters per notebook.")
        return indices, texts

    left_indices, a = selected(documents[0])
    right_indices, b = selected(documents[1])
    def operations_for():
        left_keys = [(documents[0]["cells"][i]["cell_type"], text) for i, text in zip(left_indices, a)]
        right_keys = [(documents[1]["cells"][i]["cell_type"], text) for i, text in zip(right_indices, b)]
        return difflib.SequenceMatcher(None, left_keys, right_keys, autojunk=True).get_opcodes()

    operations = operations_for()
    merge = options.get("merge")
    if merge:
        direction = merge.get("from")
        if direction not in ("left", "right"):
            raise OneKitError("Merge direction must be left or right.")
        changes = [op for op in operations if op[0] != "equal"]
        index = int(merge.get("block", -1))
        if not 0 <= index < len(changes):
            raise OneKitError("The selected change no longer exists; compare again.")
        _, i, j, k, l = changes[index]
        source_side, target_side = (0, 1) if direction == "left" else (1, 0)
        source_indices, target_indices = (left_indices, right_indices) if direction == "left" else (right_indices, left_indices)
        source_start, source_end, start, end = (i, j, k, l) if direction == "left" else (k, l, i, j)
        target_cells = documents[target_side]["cells"]
        insertion = target_indices[start] if start < len(target_indices) else target_indices[-1] + 1 if target_indices else len(target_cells)
        remove = set(target_indices[start:end])
        replacements = [copy.deepcopy(documents[source_side]["cells"][cell_index]) for cell_index in source_indices[source_start:source_end]]
        rebuilt = []
        for cell_index, cell in enumerate(target_cells):
            if cell_index == insertion:
                rebuilt.extend(replacements)
            if cell_index not in remove:
                rebuilt.append(cell)
        if insertion == len(target_cells):
            rebuilt.extend(replacements)
        documents[target_side]["cells"] = rebuilt
        left_indices, a = selected(documents[0])
        right_indices, b = selected(documents[1])
        operations = operations_for()
    left, right = "\n\n".join(a), "\n\n".join(b)
    blocks = [{"kind": tag, "left": a[i:j], "right": b[k:l], "leftStart": i, "rightStart": k} for tag, i, j, k, l in operations]
    details = {"left": left, "right": right, "equal": all(op[0] == "equal" for op in operations), "blocks": blocks, "unit": "cells", "sources": {side: json.dumps(document, ensure_ascii=False, indent=2) + "\n" for side, document in zip(("left", "right"), documents)}, "patch": "".join(difflib.unified_diff(left.splitlines(keepends=True), right.splitlines(keepends=True), fromfile=files[0].name, tofile=files[1].name))}
    if merge:
        side = "right" if merge["from"] == "left" else "left"
        return Result([type(files[0])(files[1 if side == "right" else 0].name, details["sources"][side].encode())], details=details)
    return Result([output(files[0], "diff.json", json.dumps(details, ensure_ascii=False, indent=2))], details=details)
