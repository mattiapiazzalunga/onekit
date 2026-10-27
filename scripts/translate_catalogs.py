"""Populate local catalogs. Network is used only by this explicit authoring command.

Only messages are submitted, never files, user content, or source implementations.
Existing translations are retained. Review the generated text before release.
"""
import concurrent.futures
import json
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

DIRECTORY = Path(sys.argv[1])
SOURCE = json.loads((DIRECTORY / "en.json").read_text(encoding="utf-8"))
LANGUAGES = tuple(sorted(path.stem for path in DIRECTORY.glob("*.json") if path.stem not in {"en", "languages"}))
LOCK = threading.Lock()
PROTECT = re.compile(r"`[^`\n]+`|https?://[^\s<>\])]+|[\w.+-]+@[\w.-]+\.[A-Za-z]+|\{\d+\}|\bOneKit\b|\bonekit(?:[.-][a-z0-9]+)*\b|--[a-z][a-z0-9-]*|\b[A-Z][A-Z0-9/+.-]{1,}\b")


def translate(batch, language):
    protected = []
    def protect(match):
        protected.append(match.group())
        return f"__OKP{len(protected)-1}__"
    payload = "\n".join(f"[[{index:04}]] " + PROTECT.sub(protect, key) for index, key in enumerate(batch))
    query = urllib.parse.urlencode({"client": "gtx", "sl": "en", "tl": "zh-CN" if language == "zh" else language, "dt": "t", "q": payload})
    for attempt in range(5):
        try:
            request = urllib.request.Request("https://translate.googleapis.com/translate_a/single?" + query, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=45) as response:
                data = json.load(response)
            translated = "".join(item[0] or "" for item in data[0])
            sections = re.split(r"\[\[\s*(\d{4})\s*\]\]\s*", translated)
            result = {}
            for offset in range(1, len(sections), 2):
                index = int(sections[offset])
                value = sections[offset + 1].strip()
                value = re.sub(r"__\s*OKP\s*(\d+)\s*__", lambda match: protected[int(match[1])], value, flags=re.I)
                if "__OKP" in value or index >= len(batch):
                    raise ValueError("Unrestored protected text")
                key = batch[index]
                if sorted(re.findall(r"\{\d+\}", key)) != sorted(re.findall(r"\{\d+\}", value)):
                    raise ValueError("Changed placeholders")
                for token in PROTECT.findall(key):
                    if token not in value:
                        raise ValueError("Changed protected text: " + token)
                result[key] = value
            if len(result) != len(batch):
                raise ValueError("Incomplete translation batch")
            return result
        except Exception:
            if attempt == 4:
                if len(batch) > 1:
                    middle = len(batch) // 2
                    return {**translate(batch[:middle], language), **translate(batch[middle:], language)}
                raise
            time.sleep(1 + attempt * 2)


def run_language(language):
    destination = DIRECTORY / f"{language}.json"
    existing = json.loads(destination.read_text(encoding="utf-8")) if destination.exists() else {}
    pending = [key for key in SOURCE if key not in existing]
    batches = []
    batch = []
    size = 0
    for key in pending:
        if batch and size + len(key) > 3000:
            batches.append(batch)
            batch, size = [], 0
        batch.append(key)
        size += len(key) + 20
    if batch:
        batches.append(batch)
    print(f"{language}: {len(pending)} messages, {len(batches)} batches", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for count, result in enumerate(pool.map(lambda items: translate(items, language), batches), 1):
            existing.update(result)
            temporary = destination.with_suffix(".json.tmp")
            temporary.write_text(json.dumps({key: existing[key] for key in SOURCE if key in existing}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            temporary.replace(destination)
            if count % 20 == 0:
                print(f"{language}: {count}/{len(batches)} batches", flush=True)
    print(f"{language}: complete ({len(existing)} messages)", flush=True)


with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    list(executor.map(run_language, LANGUAGES))
