from pathlib import Path
import re, sys, json

ROOT = Path(__file__).resolve().parents[1]
GEN  = ROOT / "core" / "src" / "retroproto_parsers" / "generated"
ACTIONS = GEN / "actions"

STATS = {"files_examined":0,"files_changed":0,"keyword_fixed":0,"serde_added":0,"derive_dedup":0,"derive_cleaned":0,"bare_init_fixed":0,"actions_mod_rebuilt":False}

def dedup_derive_traits(s: str) -> str:
    # #[derive(A, B, A , serde :: Serialize , Serialize)]
    m = re.match(r'(\s*#\s*\[\s*derive\s*\()\s*(.*?)\s*(\)\s*\]\s*)', s)
    if not m: return s
    head, inner, tail = m.groups()
    # strip spaces in trait tokens like "serde :: Serialize"
    traits = [re.sub(r'\s+', '', t) for t in inner.split(',') if t.strip()]
    # normalize serde:: paths to short names (we'll ensure use serde::{..})
    norm = []
    seen = set()
    for t in traits:
        t = t.replace('serde::','')
        if t not in seen:
            seen.add(t)
            norm.append(t)
    return f"{head}{', '.join(norm)}{tail}"

def ensure_serde_use(lines: list) -> list:
    # Keep a *single* `use serde::{Serialize, Deserialize};` after other uses.
    has_short = any(re.match(r'\s*use\s+serde::\{\s*Serialize\s*,\s*Deserialize\s*\}\s*;', ln) for ln in lines)
    # remove stray `use serde::{...}` duplicates and odd `use serde ::` variants
    new = []
    for ln in lines:
        if re.match(r'\s*use\s+serde\s*::\s*\{\s*Serialize\s*,\s*Deserialize\s*\}\s*;', ln):
            continue
        if re.match(r'\s*use\s+serde\s*::\s*Serialize\s*;', ln):  # kill single imports
            continue
        if re.match(r'\s*use\s+serde\s*::\s*Deserialize\s*;', ln):
            continue
        new.append(ln)
    if not has_short:
        # insert after last `use` block or after module header
        inserted = False
        for i in range(min(len(new), 20)):
            # find the last consecutive use; track last index
            pass
        last_use = -1
        for i, ln in enumerate(new[:80]):
            if ln.strip().startswith("use "):
                last_use = i
        insert_at = (last_use + 1) if last_use >= 0 else 0
        new.insert(insert_at, "use serde::{Serialize, Deserialize};")
        STATS["serde_added"] += 1
    return new

def attach_or_inject_derive(lines: list) -> list:
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        # remove stray derives not attached to the next non-empty item line
        if re.match(r'\s*#\s*\[\s*derive\b', ln):
            # lookahead for struct/enum/union
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j >= len(lines) or not re.match(r'\s*(pub\s+)?(struct|enum|union)\b', lines[j]):
                STATS["derive_cleaned"] += 1
                i += 1
                continue  # drop stray derive
            # dedup traits
            ln = dedup_derive_traits(ln)
            out.append(ln)
            i += 1
            continue
        # if we see a struct/enum without a derive right above, inject a sane derive
        if re.match(r'\s*(pub\s+)?(struct|enum)\b', ln):
            if not out or not re.match(r'\s*#\s*\[\s*derive\b', out[-1]):
                out.append("#[derive(Debug, Clone, Default, Serialize, Deserialize)]")
            out.append(ln)
            i += 1
            continue
        out.append(ln)
        i += 1
    return out

def fix_keyword_type(text: str) -> str:
    before = text
    # collapse accidental double raw-escape
    text = text.replace("r#r#type", "r#type")
    # struct field: "pub type:" -> "pub r#type:"
    text = re.sub(r'(\bpub\s+)type\s*:', r'\1r#type:', text)
    # access ".type" -> ".r#type"
    text = re.sub(r'(\.)type\b', r'\1r#type', text)
    # initializer entries inside { ... }: bare `type,` -> `r#type: r#type,`
    def repl_init(m):
        block = m.group(0)
        block = re.sub(r'(?<!:)\br#?type\s*,', 'r#type: r#type,', block)
        block = re.sub(r'\btype\s*:', 'r#type:', block)
        return block
    text = re.sub(r'let\s+result\s*=\s*[A-Za-z0-9_]+\s*\{[^}]*\};', repl_init, text, flags=re.S)
    if text != before:
        STATS["keyword_fixed"] += 1
    return text

def fix_bare_initializers(text: str) -> str:
    # Convert `{ foo, bar, baz }` -> `{ foo: foo, bar: bar, baz: baz }` within result inits.
    before = text
    def repl(m):
        blk = m.group(0)
        def f_field(nm):
            nm = nm.group(1)
            return f"{nm}: {nm},"
        blk = re.sub(r'(?m)^\s*([A-Za-z_][A-Za-z0-9_]*?)\s*,\s*$', lambda nm: f_field(nm), blk)
        return blk
    text = re.sub(r'let\s+result\s*=\s*[A-Za-z0-9_]+\s*\{[^}]*\};', repl, text, flags=re.S)
    if text != before:
        STATS["bare_init_fixed"] += 1
    return text

def normalize_file(p: Path):
    STATS["files_examined"] += 1
    raw = p.read_text(encoding="utf-8")
    txt = raw

    # 1) keyword/type fixes
    txt = fix_keyword_type(txt)

    # 2) line-based derive cleanup/inject + de-dup
    lines = txt.splitlines()
    lines = ensure_serde_use(lines)
    lines = attach_or_inject_derive(lines)

    # 3) final text + initializer cleanup
    txt = "\n".join(lines) + "\n"
    txt = fix_bare_initializers(txt)

    # small tidy: remove duplicate blank lines
    txt = re.sub(r'\n{3,}', '\n\n', txt)

    if txt != raw:
        p.write_text(txt, encoding="utf-8")
        STATS["files_changed"] += 1

def rebuild_actions_mod():
    if not ACTIONS.exists():
        return
    files = [f for f in ACTIONS.glob("*.rs") if f.name != "mod.rs"]
    # Order: core facades first
    order_first = {"shims.rs","GameActions.rs","GameActionsStart.rs","GameActionsFinish.rs","GameActionsSendActions.rs"}
    def key(f: Path):
        return (0 if f.name in order_first else 1, f.name.lower())
    files.sort(key=key)

    lines = [
        "// AUTO-REBUILT actions/mod.rs",
        "#![allow(clippy::all, non_snake_case, non_camel_case_types, unused_imports)]",
        "use serde::{Serialize, Deserialize};",
        "",
    ]
    for f in files:
        stem = f.stem
        lines.append(f"pub mod {stem};")
    lines.append("")
    # re-export all, harmless for generated modules
    for f in files:
        stem = f.stem
        lines.append(f"pub use self::{stem}::*;")
    lines.append("")
    # if shims present, make sure functions are visible
    if (ACTIONS / "shims.rs").exists():
        lines.append("pub use self::shims::*;")
    (ACTIONS / "mod.rs").write_text("\n".join(lines) + "\n", encoding="utf-8")
    STATS["actions_mod_rebuilt"] = True

def main():
    # Walk generated tree
    rs_files = list(GEN.rglob("*.rs"))
    for p in rs_files:
        # Skip root mod.rs (registry layout), but DO normalize content of others
        if p == GEN / "mod.rs":
            continue
        normalize_file(p)
    rebuild_actions_mod()
    print(json.dumps(STATS, indent=2))

if __name__ == "__main__":
    main()
