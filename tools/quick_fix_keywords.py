# tools/quick_fix_keywords.py
from pathlib import Path
import re, sys

root = Path(__file__).resolve().parents[1]  # repo root
gen = root / "core" / "src" / "retroproto_parsers" / "generated"

targets = [
    gen / "ExchangeCreateSuccess.rs",
    gen / "ExchangeRequest.rs",
    gen / "GameCreate.rs",
    gen / "GameCreateSuccess.rs",
]

def fix_keywords(p: Path):
    text = p.read_text(encoding="utf-8")

    # 1) de-double-escape: r#r#type -> r#type
    text = text.replace("r#r#type", "r#type")

    # 2) in the initializer block "let result = Struct { ... }"
    #    convert bare field entries `r#type,` into `r#type: r#type,`
    def repl_init(m):
        block = m.group(0)
        # replace any line/entry that is exactly r#type, possibly with spaces
        block = re.sub(r'(?<!:)\br#type\s*,', 'r#type: r#type,', block)
        return block

    text = re.sub(
        r'let\s+result\s*=\s*[A-Za-z0-9_]+\s*\{[^}]*\};',
        repl_init,
        text,
        flags=re.S
    )

    p.write_text(text, encoding="utf-8")
    print(f"fixed: {p.relative_to(root)}")

def fix_gameactions_derives():
    ga = gen / "actions" / "GameActions.rs"
    if not ga.exists():
        return
    lines = ga.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        # drop stray derives that are not attached to a type
        if re.match(r'^\s*#\s*\[\s*derive\b', line):
            continue
        out.append(line)
    ga.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"cleaned derives: {ga.relative_to(root)}")

if __name__ == "__main__":
    for p in targets:
        if p.exists():
            fix_keywords(p)
    fix_gameactions_derives()
    print("done.")
