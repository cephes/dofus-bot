import re, sys, pathlib

mod = pathlib.Path("core/src/retroproto_parsers/generated/mod.rs")
txt = mod.read_text(encoding="utf-8")

# Ensure the actions module is declared once
if "pub mod actions;" not in txt:
    # put the declaration near the top-level mods (safe insert before first 'pub mod ')
    txt = re.sub(r'(^\s*pub\s+mod\s+)', "pub mod actions;\n\\1", txt, count=1, flags=re.M)

# Drop unresolved per-action imports like `use actions::GameAction_900;`
txt = re.sub(r'^\s*use\s+actions::GameAction_\d+;\s*$', "", txt, flags=re.M)

# Also drop any old `pub use actions::GameAction_*;` lines that expect submodules
txt = re.sub(r'^\s*pub\s+use\s+actions::GameAction_\d+::\*;\s*$', "", txt, flags=re.M)

# Prefer shim exports if present (idempotent: only add once)
if "pub use actions::shims::*;" not in txt:
    # place it after `pub mod actions;`
    txt = txt.replace("pub mod actions;", "pub mod actions;\npub use actions::shims::*;")

mod.write_text(txt, encoding="utf-8")
print("patched:", mod)