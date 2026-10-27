"""Apply reviewed terminology and remove tokenizer artifacts from draft catalogs."""
import json
import re
import sys
from pathlib import Path

directory = Path(sys.argv[1])
review = json.loads((Path(__file__).parent / "localization-reviewed.json").read_text(encoding="utf-8"))
source = json.loads((directory / "en.json").read_text(encoding="utf-8"))
for language, overrides in review.items():
    path = directory / f"{language}.json"
    catalog = json.loads(path.read_text(encoding="utf-8"))
    for key, value in catalog.items():
        value = re.sub(" +", " ", value.replace("▁", " ")).strip()
        if re.search(r"\]\([^)]*\)", key):
            value = re.sub(r"(?<=\])\s+(?=\()", "", value)
        if "Mattia Piazzalunga" in key:
            value = re.sub(r"\[[^\]]+\]\(mailto:hello@mattiapiazzalunga\.com\)", "[Mattia Piazzalunga](mailto:hello@mattiapiazzalunga.com)", value)
        if language == "zh":
            value = value.replace("发动机", "引擎")
            if "Simplified Chinese" not in key:
                value = re.sub(r"\s*\(中文\(简体\)\s*\)\.?", "", value).strip()
        elif language == "de":
            value = re.sub(r"\bMotor(en|s)?\b", lambda match: "Engines" if match[1] else "Engine", value)
        elif language == "ru":
            for original, translated in [("двигателями","движками"),("двигателей","движков"),("двигателях","движках"),("двигателем","движком"),("двигателю","движку"),("двигателя","движка"),("двигатели","движки"),("двигателе","движке"),("двигатель","движок")]:
                value = value.replace(original, translated)
        if key.startswith("OneKit. ") or key.endswith(". OneKit"):
            base = key.removeprefix("OneKit. ").removesuffix(". OneKit")
            translated = catalog.get(base, value.replace("OneKit", "")).strip(" .-–—|·")
            value = ("OneKit. " if key.startswith("OneKit. ") else "") + translated + (". OneKit" if key.endswith(". OneKit") else "")
        catalog[key] = value
    catalog.update({key: value for key, value in overrides.items() if key in source})
    path.write_text(json.dumps({key: catalog[key] for key in source if key in catalog}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
