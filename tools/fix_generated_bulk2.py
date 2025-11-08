from pathlib import Path
import re, json

ROOT = Path(__file__).resolve().parents[1]
GEN  = ROOT / "core" / "src" / "retroproto_parsers" / "generated"
ACTIONS = GEN / "actions"

STATS = {
  "files_examined":0, "files_changed":0,
  "serde_added":0, "derive_injected":0, "derive_dedup":0,
  "common_decode_added":0, "keyword_fixed":0,
  "default_sugar_added":0, "actions_mod_rebuilt":False
}

def dedup_derive_traits(line: str) -> str:
    m = re.match(r'(\s*#\s*\[\s*derive\s*\()\s*(.*?)\s*(\)\s*\]\s*)', line)
    if not m: return line
    head, inner, tail = m.groups()
    toks = [re.sub(r'\s+', '', t) for t in inner.split(',') if t.strip()]
    out, seen = [], set()
    for t in toks:
        t = t.replace('serde::','')
        if t not in seen:
            seen.add(t); out.append(t)
    return f"{head}{', '.join(out)}{tail}"

def ensure_single_serde_use(lines):
    has_short = any(re.match(r'\s*use\s+serde::\{\s*Serialize\s*,\s*Deserialize\s*\}\s*;', x) for x in lines)
    new=[]
    for ln in lines:
        if re.match(r'\s*use\s+serde\s*::\s*\{\s*Serialize\s*,\s*Deserialize\s*\}\s*;', ln): continue
        if re.match(r'\s*use\s+serde\s*::\s*Serialize\s*;', ln): continue
        if re.match(r'\s*use\s+serde\s*::\s*Deserialize\s*;', ln): continue
        new.append(ln)
    if not has_short:
        # insert after last "use " near top
        last_use = -1
        for i, ln in enumerate(new[:80]):
            if ln.strip().startswith("use "): last_use = i
        new.insert((last_use+1) if last_use>=0 else 0, "use serde::{Serialize, Deserialize};")
        STATS["serde_added"] += 1
    return new

def attach_or_fix_derive(lines):
    out=[]
    i=0
    while i < len(lines):
        ln = lines[i]
        if re.match(r'\s*#\s*\[\s*derive\b', ln):
            # keep only if next non-empty is type decl
            j=i+1
            while j<len(lines) and lines[j].strip()=="":
                j+=1
            if j>=len(lines) or not re.match(r'\s*(pub\s+)?(struct|enum|union)\b', lines[j]):
                # stray derive -> drop
                i+=1; continue
            out.append(dedup_derive_traits(ln)); STATS["derive_dedup"] += 1; i+=1; continue
        if re.match(r'\s*(pub\s+)?(struct|enum)\b', ln):
            if not out or not re.match(r'\s*#\s*\[\s*derive\b', out[-1]):
                out.append("#[derive(Debug, Clone, Default, Serialize, Deserialize)]")
                STATS["derive_injected"] += 1
            out.append(ln); i+=1; continue
        out.append(ln); i+=1
    return out

def ensure_common_decode_import(lines):
    needs = any("common_decode::" in ln for ln in lines)
    has   = any(re.search(r'\buse\s+crate::retroproto_parsers::parser::common_decode\s*;', ln) for ln in lines)
    if needs and not has:
        # after serde import
        insert_at = 0
        for i, ln in enumerate(lines[:80]):
            if re.match(r'\s*use\s+serde::\{.*\}\s*;', ln): insert_at = i+1
        lines.insert(insert_at, "use crate::retroproto_parsers::parser::common_decode;")
        STATS["common_decode_added"] += 1
    return lines

def fix_keyword_type(text):
    before = text
    text = text.replace("r#r#type", "r#type")
    text = re.sub(r'(\bpub\s+)type\s*:', r'\1r#type:', text)
    text = re.sub(r'(\.)type\b', r'\1r#type', text)
    # in struct literal blocks, normalize type entries
    def fix_block(m):
        blk = m.group(0)
        blk = re.sub(r'(?<!:)\br#?type\s*,', 'r#type: r#type,', blk)
        blk = re.sub(r'\btype\s*:', 'r#type:', blk)
        return blk
    text = re.sub(r'let\s+result\s*=\s*[A-Za-z0-9_]+\s*\{[^}]*\}', fix_block, text, flags=re.S)
    if text != before: STATS["keyword_fixed"] += 1
    return text

def add_default_sugar(text):
    # add `..Default::default()` to struct literals when missing
    before = text
    def repl(m):
        blk = m.group(0)
        if re.search(r'\.\.\s*Default::default\s*\(\s*\)', blk): return blk
        # ensure commas are okay
        blk = re.sub(r'\s*\}\s*$', ', ..Default::default()}', blk)
        return blk
    text = re.sub(r'let\s+result\s*=\s*[A-Za-z0-9_]+\s*\{[^}]*\}', repl, text, flags=re.S)
    if text != before: STATS["default_sugar_added"] += 1
    return text

def normalize_file(p: Path):
    STATS["files_examined"] += 1
    raw = p.read_text(encoding="utf-8")
    txt = raw

    txt = fix_keyword_type(txt)
    lines = txt.splitlines()

    lines = ensure_single_serde_use(lines)
    lines = ensure_common_decode_import(lines)
    lines = attach_or_fix_derive(lines)

    txt = "\n".join(lines) + "\n"
    txt = add_default_sugar(txt)

    txt = re.sub(r'\n{3,}', '\n\n', txt)

    if txt != raw:
        p.write_text(txt, encoding="utf-8")
        STATS["files_changed"] += 1

def rebuild_actions_mod():
    if not ACTIONS.exists(): return
    files = [f for f in ACTIONS.glob("*.rs") if f.name != "mod.rs"]
    order_first = {"shims.rs","GameActions.rs","GameActionsStart.rs","GameActionsFinish.rs","GameActionsSendActions.rs"}
    files.sort(key=lambda f: (0 if f.name in order_first else 1, f.name.lower()))
    lines = [
        "// AUTO-REBUILT actions/mod.rs",
        "#![allow(clippy::all, non_snake_case, non_camel_case_types, unused_imports)]",
        "use serde::{Serialize, Deserialize};",
        "",
    ]
    for f in files:
        lines.append(f"pub mod {f.stem};")
    lines.append("")
    for f in files:
        lines.append(f"pub use self::{f.stem}::*;")
    lines.append("")
    if (ACTIONS / "shims.rs").exists():
        lines.append("pub use self::shims::*;")
    (ACTIONS / "mod.rs").write_text("\n".join(lines) + "\n", encoding="utf-8")
    STATS["actions_mod_rebuilt"] = True

def main():
    rs_files = list(GEN.rglob("*.rs"))
    for p in rs_files:
        if p == GEN / "mod.rs":  # leave the root mod.rs alone
            continue
        normalize_file(p)
    rebuild_actions_mod()
    print(json.dumps(STATS, indent=2))

if __name__ == "__main__":
    main()
