# tools/cleanup/disable_demo_outputs.py
import re
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]  # repo root
ARCHIVE = ROOT / ".archive" / f"PLACEHOLDER_CLEAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
REPORT_DIR = ROOT / ".reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

SKIP_DIRS = {
    ".git", ".venv", "target", "node_modules", ".parity", ".archive", "__pycache__",
    ".vscode", ".idea", ".pytest_cache", ".cargo"
}

TOUCHABLE_TOPS = {"scripts", "tools"}

SCAN_EXTS = {
    ".py", ".ps1", ".psm1", ".sh",
    ".go", ".js", ".mjs", ".cjs", ".ts", ".tsx",
    ".yml", ".yaml", ".bat", ".cmd"
}

PATTERNS = [
    r"\bparsed_data\b",
    r"\bsample_go\b",
    r"Hello world from Go",
    r'"account_id"\s*:\s*123\b',
    r'\bjohn_parsed_all\.ndjson\b',
    r'\bdummy_parsed_all\.ndjson\b',
    r"\bPLACEHOLDER\b",
    r"\bDEMO\b",
    r"\bSIMULAT(?:E|ION)\b",
    r'"ticket"\s*:\s*"sample"\b',
    r'"channel"\s*:\s*"general"\b',
    r"pretty json",
    r"Pretty JSON",
]

WRITE_HINTS = [
    r"json\.dump", r"json\.dumps", r"write\(", r"fprintf", r"fmt\.Fprint", r"fmt\.Fprintf",
    r"Write-Host", r"Out-File", r"Set-Content", r"Add-Content", r"ConvertTo-Json",
    r"decoded[\\/].*\.ndjson", r"decoded[\\/].*\.json",
    r"dummy_parsed_all\.ndjson", r"john_parsed_all\.ndjson",
    r"dummy_go.*\.ndjson", r"john_go.*\.ndjson"
]

COMMENT_PREFIX = {
    ".py": "# ",
    ".ps1": "# ",
    ".psm1": "# ",
    ".sh": "# ",
    ".go": "// ",
    ".js": "// ",
    ".mjs": "// ",
    ".cjs": "// ",
    ".ts": "// ",
    ".tsx": "// ",
    ".yml": "# ",
    ".yaml": "# ",
    ".bat": "REM ",
    ".cmd": "REM ",
}

def should_skip_dir(p: Path) -> bool:
    parts = {*p.parts}
    return any(name in SKIP_DIRS for name in parts)

def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)

def score_line(line: str) -> int:
    s = 0
    for pat in PATTERNS:
        if re.search(pat, line, flags=re.IGNORECASE):
            s += 2
    for pat in WRITE_HINTS:
        if re.search(pat, line, flags=re.IGNORECASE):
            s += 1
    return s

def is_touchable(file: Path) -> bool:
    try:
        top = file.relative_to(ROOT).parts[0]
    except Exception:
        return False
    return top in TOUCHABLE_TOPS

def comment_line(ext: str, line: str) -> str:
    prefix = COMMENT_PREFIX.get(ext.lower(), "# ")
    if line.lstrip().startswith(("//", "#", "REM ")):
        return line
    return prefix + "DEMO_DISABLED: " + line

def scan_file(file: Path):
    try:
        text = file.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True)
    except Exception:
        return {"matches": [], "score": 0}
    matches = []
    total_score = 0
    for idx, ln in enumerate(text, start=1):
        s = score_line(ln)
        if s > 0:
            matches.append({"line": idx, "content": ln.rstrip("\n"), "score": s})
            total_score += s
    return {"matches": matches, "score": total_score}

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Find and optionally disable placeholder/demo outputs across the repo.")
    ap.add_argument("--apply", action="store_true", help="Apply changes (comment out suspicious lines in tools/ and scripts/).")
    ap.add_argument("--limit", type=int, default=999999, help="Limit number of files to modify in a single run.")
    ap.add_argument("--dry", action="store_true", help="Alias for staying dry-run (default).")
    args = ap.parse_args()
    apply_changes = bool(args.apply) and not args.dry

    suspects = []
    for path in ROOT.rglob("*"):
        if path.is_dir():
            if should_skip_dir(path):
                for _ in path.iterdir():
                    pass
                continue
            continue
        if path.suffix.lower() not in SCAN_EXTS:
            continue
        if should_skip_dir(path.parent):
            continue

        res = scan_file(path)
        if res["score"] > 0:
            suspects.append({
                "file": rel(path),
                "score": res["score"],
                "matches": res["matches"],
                "touchable": is_touchable(path),
            })

    suspects.sort(key=lambda x: (-(x["touchable"]), -x["score"], x["file"]))

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_json = REPORT_DIR / "placeholder_suspects.json"
    report_md = REPORT_DIR / "placeholder_suspects.md"
    with report_json.open("w", encoding="utf-8") as f:
        json.dump({"root": str(ROOT), "suspects": suspects}, f, ensure_ascii=False, indent=2)

    with report_md.open("w", encoding="utf-8") as f:
        f.write("# Placeholder / Demo Writers — Suspect Report\n\n")
        f.write(f"- Repo root: `{ROOT}`\n")
        f.write(f"- Total suspects: **{len(suspects)}**\n")
        f.write(f"- Auto-touchable (in tools/ or scripts/): **{sum(1 for s in suspects if s['touchable'])}**\n\n")
        for s in suspects[:2000]:
            f.write(f"## {s['file']}  (score: {s['score']}, touchable: {s['touchable']})\n\n")
            for m in s["matches"][:30]:
                f.write(f"- L{m['line']}: `{m['content']}` (score {m['score']})\n")
            if len(s["matches"]) > 30:
                f.write(f"- … plus {len(s['matches']) - 30} more lines\n")
            f.write("\n")

    print(f"[OK] Wrote report:\n  {report_json}\n  {report_md}")
    print(f"[INFO] Total suspects: {len(suspects)} (touchable={sum(1 for s in suspects if s['touchable'])})")

    if not apply_changes:
        print("[DRY-RUN] No changes applied. Re-run with --apply to comment out demo writers in tools/ and scripts/.")
        return

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    modified = 0
    for s in suspects:
        if modified >= args.limit:
            break
        file = ROOT / s["file"]
        if not s["touchable"]:
            continue
        try:
            original = file.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True)
        except Exception:
            continue

        ext = file.suffix.lower()
        changed = False
        out_lines = []
        demo_line_nums = {m["line"] for m in s["matches"]}

        for idx, ln in enumerate(original, start=1):
            if idx in demo_line_nums:
                out_lines.append(comment_line(ext, ln))
                changed = True
            else:
                out_lines.append(ln)

        if changed:
            bak_path = ARCHIVE / s["file"]
            bak_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, bak_path)
            file.write_text("".join(out_lines), encoding="utf-8")
            modified += 1
            print(f"[PATCHED] {s['file']} (score={s['score']}, lines={len(demo_line_nums)})")

    print(f"[DONE] Modified files: {modified}, backup: {ARCHIVE}")

if __name__ == "__main__":
    sys.exit(main())