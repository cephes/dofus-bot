import json, sys, os, re
from collections import Counter

SRC_A = r"examples/pcap/flows/dummy_frames.ndjson"
# DEMO_DISABLED: SRC_B = r"examples/pcap/decoded/dummy_parsed_new.ndjson"
# DEMO_DISABLED: OUT_ND = r"examples/pcap/decoded/dummy_go_strict.ndjson"
# DEMO_DISABLED: OUT_JSON = r"examples/pcap/decoded/dummy_go_strict.json"
REPORT = r"GO_BASELINE_VALIDATION.md"

def pick_input():
    for p in (SRC_A, SRC_B):
        if os.path.exists(p): return p
    raise SystemExit("No neutral input found. Provide dummy_frames.ndjson or dummy_parsed_new.ndjson")

def read_nd(path, n=None):
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                out.append(json.loads(line))
            except Exception as e:
                out.append({"_decode_error": str(e), "_raw": line})
            if n and len(out) >= n: break
    return out

def shape_checks(rows):
    """Prefix-specific sanity/shape checks on the Go output rows."""
    errs = []
    def err(i, msg): errs.append((i, msg))

    for i, r in enumerate(rows):
        pfx = r.get("Prefix") or r.get("prefix")
        name = r.get("MessageName") or r.get("message_name")
        pe = r.get("ParseError") or r.get("parse_error")
        parsed = r.get("Parsed") or r.get("parsed") or {}
        raw = r.get("Raw") or r.get("raw") or ""

        # Generic: parser should either produce parsed or an explicit error.
        if not parsed and not pe:
            err(i, f"{pfx}/{name}: neither parsed nor parse_error")

        # fC (FightsCount) → scalar integer field 'value'
        if pfx == "fC" and parsed:
            if not isinstance(parsed, dict) or "value" not in parsed or not isinstance(parsed["value"], int):
                err(i, "fC: expected parsed.value:int")

        # GDM (GameMapData): should have id:int, name:str, key:hex-string
        if pfx == "GDM" and parsed:
            ok = isinstance(parsed, dict) and \
                 isinstance(parsed.get("id"), int) and \
                 isinstance(parsed.get("name"), str) and \
                 isinstance(parsed.get("key"), str) and re.fullmatch(r"[0-9a-fA-F]+", parsed["key"] or "") is not None
            if not ok:
                err(i, "GDM: expected fields id:int, name:str, key:hex")

        # BT (BasicsTime): often time fields or empty object allowed
        if pfx == "BT":
            # accept {} or {something}, but if parsed is str -> error
            if isinstance(parsed, str):
                err(i, "BT: parsed should be object or empty, not string")

        # GA (GameActions): must have action_code:int
        if pfx == "GA" and parsed:
            if not isinstance(parsed, dict) or "action_code" not in parsed or not isinstance(parsed["action_code"], int):
                err(i, "GA: missing action_code:int in parsed")

    return errs

def main():
    src = pick_input()
    # Build & run strict Go tool from correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    code = os.system(f'pushd tools\\go_baseline >NUL 2>&1 && go mod tidy && go run main_strict.go registry.go "../../{src}" "../../{OUT_ND}" "../../{OUT_JSON}" && popd >NUL 2>&1')
    if code != 0:
        print("Go strict run failed", file=sys.stderr)
        sys.exit(3)

    rows = read_nd(OUT_ND)
    total = len(rows)
    with_errors = sum(1 for r in rows if (r.get("ParseError") or r.get("parse_error")))
    by_prefix = Counter((r.get("Prefix") or r.get("prefix") or "??") for r in rows)

    errs = shape_checks(rows)

    # Write report
    with open(REPORT, "w", encoding="utf-8") as f:
# DEMO_DISABLED:         f.write("# Go Baseline Validation (Strict Mode)\n\n")
# DEMO_DISABLED:         f.write(f"- Input: `{src}`\n")
# DEMO_DISABLED:         f.write(f"- Output NDJSON: `{OUT_ND}`\n")
# DEMO_DISABLED:         f.write(f"- Output JSON: `{OUT_JSON}`\n\n")
# DEMO_DISABLED:         f.write(f"## Summary\n\n")
# DEMO_DISABLED:         f.write(f"- Total rows: **{total}**\n")
# DEMO_DISABLED:         f.write(f"- Rows with parse_error: **{with_errors}**\n")
# DEMO_DISABLED:         f.write(f"- Unique prefixes: **{len(by_prefix)}**\n\n")
# DEMO_DISABLED:         f.write("### By prefix (top 15)\n\n")
        for p, c in by_prefix.most_common(15):
# DEMO_DISABLED:             f.write(f"- `{p}`: {c}\n")
# DEMO_DISABLED:         f.write("\n## Shape Check Failures\n\n")
        if not errs:
# DEMO_DISABLED:             f.write("✅ No shape failures detected.\n")
        else:
# DEMO_DISABLED:             f.write(f"❌ {len(errs)} shape failures:\n")
            for i, msg in errs[:50]:
# DEMO_DISABLED:                 f.write(f"- Row {i}: {msg}\n")
            if len(errs) > 50:
# DEMO_DISABLED:                 f.write(f"- … (+{len(errs)-50} more)\n")

    # Exit status: fail if too many errors or any shape failures
    if errs or with_errors > total * 0.5:
        sys.exit(4)

if __name__ == "__main__":
    main()