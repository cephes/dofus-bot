import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GA = ROOT / "core" / "src" / "retroproto_parsers" / "handwritten" / "GameActions.rs"

def main():
    if not GA.exists():
        print("dispatcher not found, skipping")
        return
    t = GA.read_text(encoding="utf-8")

    # 1) Function name should be snake_case: parse_game_actions
    t = re.sub(r'\bparse\s*GameActions\b', 'parse_game_actions', t)
    t = re.sub(r'\bparse\s*GameAction\s*\(', 'parse_game_actions(', t)

    # 2) Normalize action subparser calls to the exported module path.
    # Replace any bare calls like parse_GameAction_900( with fully qualified path:
    t = re.sub(
        r'(?<![A-Za-z0-9_])(parse_GameAction_[0-9]+)\s*\(',
        r'crate::retroproto_parsers::generated::actions::\1(',
        t
    )
    t = re.sub(
        r'(?<![A-Za-z0-9_])(parse_CliAction_[0-9]+)\s*\(',
        r'crate::retroproto_parsers::generated::actions::\1(',
        t
    )

    # 3) Remove stale 'use generated::actions::...' imports to avoid path drift.
    t = re.sub(r'^\s*use\s+crate::retroproto_parsers::generated::actions::[^\n;]+;\s*\n', '', t, flags=re.MULTILINE)

    GA.write_text(t, encoding="utf-8")
    print("GameActions.rs normalized")

if __name__ == "__main__":
    main()