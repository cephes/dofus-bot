#!/usr/bin/env python3
import re, json, sys, unicodedata
from pathlib import Path

RAW_DIR = Path("third_party/identifiants/raw")
OUT_JSON_DIR = Path("third_party/identifiants/json")
OUT_ASSETS_DIR = Path("core/assets/ids")
OUT_JSON_DIR.mkdir(parents=True, exist_ok=True)
OUT_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "monsters": "Monstres.txt",
    "spells": "Sorts.txt",
    "items": "Objets.txt",
    "jobs": "Metiers.txt",
    "interactives": "Interactives.txt",
}

LINE_RX = re.compile(r"^\s*(\d+)\s*[-:]\s*(.+?)\s*$")

def norm_name(s: str) -> str:
    # Keep accents, trim, collapse spaces, standardize apostrophes
    s = s.replace("\u2019", "'").replace("’", "'")
    s = " ".join(s.split())
    # NFC for consistent accents
    return unicodedata.normalize("NFC", s)

def load_map(txt_path: Path) -> dict[int, str]:
    result = {}
    if not txt_path.exists():
        return result
    with txt_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = LINE_RX.match(line)
            if not m:
                # tolerate "123 - Name (extra)" and trailing comments
                # try split on first "-"/":" if regex failed
                for sep in (" - ", ":", " -", "- ", "–", "—"):
                    if sep in line:
                        left, right = line.split(sep, 1)
                        if left.strip().isdigit():
                            result[int(left.strip())] = norm_name(right)
                            break
                else:
                    continue
            else:
                idv, name = m.groups()
                result[int(idv)] = norm_name(name)
    return result

def dump_json(basename: str, data: dict[int, str]):
    # Stable, string keys for JSON to avoid JS/Rust int parsing surprises
    s = json.dumps({str(k): v for k, v in sorted(data.items())}, ensure_ascii=False, indent=2)
    (OUT_JSON_DIR / f"{basename}.json").write_text(s, encoding="utf-8")
    # Mirror into core/assets/ids for include_str!()
    (OUT_ASSETS_DIR / f"{basename}.json").write_text(s, encoding="utf-8")

def main():
    totals = {}
    for key, fname in FILES.items():
        mp = load_map(RAW_DIR / fname)
        dump_json(key, mp)
        totals[key] = len(mp)
    meta = {
        "totals": totals,
        "sources": FILES,
        "raw_dir": str(RAW_DIR),
        "out_json_dir": str(OUT_JSON_DIR),
        "out_assets_dir": str(OUT_ASSETS_DIR),
    }
    print(json.dumps(meta, ensure_ascii=False))

if __name__ == "__main__":
    sys.exit(main())