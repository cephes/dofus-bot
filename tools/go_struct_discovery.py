# -*- coding: utf-8 -*-
"""
go_struct_discovery.py
Recursively scan third_party/retroproto for Go structs that define message payloads.

Outputs:
  tools/_cache/go_structs.json

Finds:
  - package, file, struct name, field list (name, type), tags (if present)
Notes:
  - Handles simple "type X struct { ... }" and "struct{...}" blocks
  - Designed for Dofus retro proto shapes; not a full Go parser, but robust enough
"""
import re, json, os, sys, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETRO = ROOT / "third_party" / "retroproto"
OUTDIR = ROOT / "tools" / "_cache"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTJSON = OUTDIR / "go_structs.json"

STRUCT_RE = re.compile(
    r'(?P<typedef>type\s+(?P<name>[A-Za-z0-9_]+)\s+struct\s*\{(?P<body>.*?)\})',
    re.DOTALL
)
FIELD_RE = re.compile(
    r'(?P<fname>[A-Za-z0-9_]+)\s+(?P<ftype>[\[\]\*\w\.]+)(?:\s+`(?P<tags>[^`]+)`)?\s*$'
)

def normalize_type(t):
    t = t.strip()
    # Basic mappings; extend as needed
    return t

def parse_structs(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    pkg = "unknown"
    m = re.search(r'^\s*package\s+([A-Za-z0-9_]+)', text, re.MULTILINE)
    if m:
        pkg = m.group(1)
    out = []
    for sm in STRUCT_RE.finditer(text):
        name = sm.group("name")
        body = sm.group("body")
        fields = []
        for line in body.splitlines():
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            fm = FIELD_RE.match(line)
            if fm:
                fields.append({
                    "name": fm.group("fname"),
                    "type": normalize_type(fm.group("ftype")),
                    "tags": fm.group("tags") or ""
                })
        out.append({
            "package": pkg,
            "file": str(path.relative_to(ROOT)),
            "name": name,
            "fields": fields
        })
    return out

def main():
    if not RETRO.exists():
# DEMO_DISABLED:         print(json.dumps({"error":"retroproto dir missing","path":str(RETRO)}))
        sys.exit(1)
    structs = []
    for p in RETRO.rglob("*.go"):
        structs.extend(parse_structs(p))
    # Add a quick index for lookups by struct name
    index = {}
    for s in structs:
        index.setdefault(s["name"], []).append(s)
# DEMO_DISABLED:     OUTJSON.write_text(json.dumps({
        "count": len(structs),
        "items": structs,
        "by_name": index,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
# DEMO_DISABLED:     print(json.dumps({"ok": True, "count": len(structs), "out": str(OUTJSON)}))

if __name__ == "__main__":
    main()