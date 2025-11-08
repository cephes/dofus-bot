import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "core" / "src" / "retroproto_parsers" / "registry.rs"
EXPORTS = ROOT / ".tmp_action_exports.json"

def load_exports():
    data = json.loads(EXPORTS.read_text(encoding="utf-8"))
    return data["alias_map"], data["module_path"]

def rewrite_registry(text, alias_map, module_path):
    # Patterns we may find in call sites or imports
    # We will convert ANY of these to fully-qualified module_path::<exported-fn>
    # ex: parse_GameAction_900(...)  or generated::actions::parse_GameAction_900(...)
    # Keep the function name, only normalize path + case.
    call_pat = re.compile(r'(?<![A-Za-z0-9_])(parse_[A-Za-z0-9_]+)\s*\(')

    def repl(m):
        name = m.group(1)
        canon = alias_map.get(name, alias_map.get(name.lower()))
        if not canon:
            # leave as-is if not an action parser
            return m.group(0)
        return f"{module_path}::{canon}("

    # Nuke stale 'use' imports to avoid shadowing or unresolved crates
    text = re.sub(r'^\s*use\s+crate::retroproto_parsers::generated::actions::[^\n;]+;\s*\n', '', text, flags=re.MULTILINE)

    text = call_pat.sub(repl, text)
    return text

def main():
    alias_map, module_path = load_exports()
    orig = REG.read_text(encoding="utf-8")
    new = rewrite_registry(orig, alias_map, module_path)
    if new != orig:
        REG.write_text(new, encoding="utf-8")
        print("registry.rs updated")
    else:
        print("registry.rs unchanged")

if __name__ == "__main__":
    main()