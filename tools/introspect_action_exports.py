import re, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIONS_DIR = ROOT / "core" / "src" / "retroproto_parsers" / "generated" / "actions"

def collect_rs(paths):
    text = ""
    for p in paths:
        if p.exists():
            text += p.read_text(encoding="utf-8", errors="ignore") + "\n"
    return text

def main():
    mod = ACTIONS_DIR / "mod.rs"
    shims = ACTIONS_DIR / "shims.rs"

    exported = set()
    # Capture re-exports and function defs
    pat_pub_use = re.compile(r"pub\s+use\s+[^{;]+::(parse_[A-Za-z0-9_]+)\s*;")
    pat_pub_fn  = re.compile(r"pub\s+fn\s+(parse_[A-Za-z0-9_]+)\s*\(")

    text = collect_rs([mod, shims])

    for m in pat_pub_use.finditer(text):
        exported.add(m.group(1))
    for m in pat_pub_fn.finditer(text):
        exported.add(m.group(1))

    # Normalize to canonical names we expect to be called from registry:
    # Accept both parse_GameAction_123 and parse_CliAction_12, plus lowercase variants
    aliases = {}
    for fn in list(exported):
        aliases[fn] = fn
        aliases[fn.lower()] = fn

    print(json.dumps({
        "exports": sorted(exported),
        "alias_map": aliases,
        "module_path": "crate::retroproto_parsers::generated::actions"
    }, indent=2))

if __name__ == "__main__":
    main()