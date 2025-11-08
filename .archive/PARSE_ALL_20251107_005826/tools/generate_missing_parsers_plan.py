#!/usr/bin/env python3
import json, re, sys, os
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[1]

COVERAGE_JSON = ROOT / "parser_coverage.json"
NDJSON = ROOT / "examples" / "pcap" / "decoded" / "dummy_parsed_new.ndjson"

GO_ROOTS = [
    ROOT / "third_party" / "retroproto" / "msgsvr",
    ROOT / "third_party" / "retroproto" / "msgcli",
]

RUST_DIRS = [
    ROOT / "core" / "src" / "retroproto_parsers" / "generated",
    ROOT / "core" / "src" / "retroproto_parsers" / "generated" / "actions",
    ROOT / "core" / "src" / "retroproto_parsers" / "handwritten",
]

REGISTRY_RS = ROOT / "core" / "src" / "retroproto_parsers" / "registry.rs"

OUT_JSON = ROOT / "missing_parsers_plan.json"
OUT_MD   = ROOT / "MISSING_PARSERS_PLAN.md"

# --- helpers --------------------------------------------------------------

def pascalize(name: str) -> str:
    # best-effort normalization (handles GameEffect, SpellsBoost, etc.)
    # leave as-is if already PascalCase
    if re.match(r'^[A-Z][A-Za-z0-9]*$', name):
        return name
    parts = re.split(r'[_\-\s]+', name)
    return ''.join(p[:1].upper() + p[1:] for p in parts if p)

def read_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_read(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def scan_go_structs():
    """Return map: StructName -> list[files] where 'type StructName struct {' appears."""
    m = defaultdict(list)
    for root in GO_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.go"):
            text = safe_read(p)
            # capture public struct names
            for match in re.finditer(r'\btype\s+([A-Z][A-Za-z0-9_]*)\s+struct\s*\{', text):
                name = match.group(1)
                m[name].append(str(p.relative_to(ROOT)))
    return m

def scan_rust_generated():
    """Return:
       - rust_structs: set of 'Name' seen in 'pub struct Name {'
       - rust_parse_fns: set of 'Name' seen in 'pub fn parse_Name('
       - rust_files_for: Name -> list[file paths]
    """
    rust_structs, rust_parse_fns = set(), set()
    rust_files_for = defaultdict(list)

    def visit_dir(d: Path):
        if not d.exists():
            return
        for p in d.rglob("*.rs"):
            text = safe_read(p)
            rel = str(p.relative_to(ROOT))
            for ms in re.finditer(r'\bpub\s+struct\s+([A-Z][A-Za-z0-9_]*)\b', text):
                name = ms.group(1)
                rust_structs.add(name)
                rust_files_for[name].append(rel)
            # parse functions typically: pub fn parse_Name(
            for mf in re.finditer(r'\bpub\s+fn\s+parse_([A-Z][A-Za-z0-9_]*)\s*\(', text):
                name = mf.group(1)
                rust_parse_fns.add(name)
                rust_files_for[name].append(rel)

    for d in RUST_DIRS:
        visit_dir(d)

    return rust_structs, rust_parse_fns, rust_files_for

def scan_registry_names():
    """Attempt to extract registered message names from registry.rs."""
    names = set()
    text = safe_read(REGISTRY_RS)
    # handle patterns like: map.insert("GameMovement", parse_GameMovement as ParserFn);
    for m in re.finditer(r'insert\(\s*"([A-Z][A-Za-z0-9_]*)"\s*,', text):
        names.add(m.group(1))
    # also handle potentially static arrays like: ("GameMovement", parse_GameMovement)
    for m in re.finditer(r'"\s*([A-Z][A-Za-z0-9_]*)\s*"\s*,\s*parse_', text):
        names.add(m.group(1))
    return names

def load_coverage():
    """Return per-message coverage stats.
       If parser_coverage.json exists, use it.
       Otherwise, build minimal stats from NDJSON lines.
    """
    if COVERAGE_JSON.exists():
        data = read_json(COVERAGE_JSON)
        # Handle the actual structure: by_message is a list of message objects
        if isinstance(data, dict) and "by_message" in data:
            by_message = data["by_message"]
            if isinstance(by_message, list):
                # Convert list to dict keyed by message_name
                coverage_dict = {}
                for msg in by_message:
                    if isinstance(msg, dict) and "message_name" in msg:
                        name = msg["message_name"]
                        # Extract stats from the message object
                        counts = msg.get("ndjson_counts", {})
                        examples_seen = msg.get("examples_seen", 0)
                        
                        # Convert ndjson_counts to our expected format
                        structured = counts.get("structured", 0)
                        empty = counts.get("empty", 0)
                        null = counts.get("null", 0)
                        parse_error = 0  # Not directly available in this format
                        
                        coverage_dict[name] = {
                            "count": examples_seen,
                            "parsed_nonempty": structured,
                            "parsed_empty": empty,
                            "parse_errors": parse_error,
                        }
                return coverage_dict
            else:
                return by_message
        # try raw dict pass-through
        if isinstance(data, dict):
            return data
    # Fallback: derive from NDJSON
    stats = {}
    if NDJSON.exists():
        counts = Counter()
        nonempty = Counter()
        emptyobj = Counter()
        errors = Counter()
        with open(NDJSON, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                name = o.get("message_name") or o.get("message") or "Unknown"
                counts[name] += 1
                parsed = o.get("parsed")
                if isinstance(parsed, dict) and parsed:
                    nonempty[name] += 1
                elif isinstance(parsed, dict) and not parsed:
                    emptyobj[name] += 1
                elif parsed is None:
                    if o.get("parse_error"):
                        errors[name] += 1
        for k in counts:
            stats[k] = {
                "count": counts[k],
                "parsed_nonempty": nonempty[k],
                "parsed_empty": emptyobj[k],
                "parse_errors": errors[k],
            }
    return stats

# --- main ---------------------------------------------------------------

def main():
    coverage = load_coverage()
    go_index = scan_go_structs()
    rust_structs, rust_parse_fns, rust_files_for = scan_rust_generated()
    registry_names = scan_registry_names()

    plan = []
    for msg_name in sorted(coverage.keys()):
        pascal = pascalize(msg_name)
        cov = coverage[msg_name]
        count = cov["count"] if isinstance(cov, dict) and "count" in cov else 0
        parsed_nonempty = cov.get("parsed_nonempty", 0) if isinstance(cov, dict) else 0
        parsed_empty    = cov.get("parsed_empty", 0) if isinstance(cov, dict) else 0
        parse_errors    = cov.get("parse_errors", 0) if isinstance(cov, dict) else 0

        info = {
            "message_name": msg_name,
            "normalized": pascal,
            "observed_count": count,
            "parsed_nonempty": parsed_nonempty,
            "parsed_empty": parsed_empty,
            "parse_errors": parse_errors,

            "has_go_def": pascal in go_index,
            "go_files": go_index.get(pascal, []),

            "has_rust_struct": pascal in rust_structs,
            "has_rust_parse_fn": pascal in rust_parse_fns,
            "rust_files": rust_files_for.get(pascal, []),

            "registered_in_registry": pascal in registry_names,
        }

        # classify need
        if info["has_go_def"] and not info["has_rust_parse_fn"]:
            need = "PORT_GO_TO_RUST"
        elif info["has_rust_parse_fn"] and not info["registered_in_registry"]:
            need = "REGISTER_IN_REGISTRY"
        elif info["has_rust_parse_fn"] and info["registered_in_registry"] and parsed_empty > 0 and parsed_nonempty == 0:
            need = "FILL_FIELDS_IN_RUST_PARSER"
        elif info["observed_count"] > 0 and not info["has_rust_parse_fn"]:
            need = "RUST_PARSER_MISSING"
        else:
            need = "OK_OR_NOT_IN_TRAFFIC"

        info["action"] = need
        plan.append(info)

    # Sort by priority: traffic-heavy & missing first
    def priority(row):
        pri = 0
        if row["action"] in ("PORT_GO_TO_RUST", "RUST_PARSER_MISSING"):
            pri -= 1000
        if row["observed_count"]:
            pri -= min(999, row["observed_count"])
        if row["message_name"] in ("GameActions", "GameEffect"):
            pri -= 500  # known multiplexed, higher priority
        return (pri, row["message_name"])

    plan.sort(key=priority)

    OUT_JSON.write_text(json.dumps({
        "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "root": str(ROOT),
        "summary": {
            "total_messages_in_coverage": len(coverage),
            "go_defs": sum(1 for r in plan if r["has_go_def"]),
            "rust_parse_fns": sum(1 for r in plan if r["has_rust_parse_fn"]),
            "registered": sum(1 for r in plan if r["registered_in_registry"]),
            "needs_porting": sum(1 for r in plan if r["action"] == "PORT_GO_TO_RUST"),
            "needs_registration": sum(1 for r in plan if r["action"] == "REGISTER_IN_REGISTRY"),
            "needs_field_filling": sum(1 for r in plan if r["action"] == "FILL_FIELDS_IN_RUST_PARSER"),
            "missing_rust": sum(1 for r in plan if r["action"] == "RUST_PARSER_MISSING"),
        },
        "entries": plan
    }, indent=2), encoding="utf-8")

    # Markdown
    lines = []
    lines.append("# Missing/Partial Parser Synthesis Plan")
    lines.append("")
    lines.append("- Generated by `tools/generate_missing_parsers_plan.py`")
    lines.append(f"- Coverage source: `{COVERAGE_JSON.name if COVERAGE_JSON.exists() else NDJSON.name}`")
    lines.append("")
    # quick summary
    with open(OUT_JSON, "r", encoding="utf-8") as f:
        summary = json.load(f)["summary"]
    lines.append("## Summary")
    for k, v in summary.items():
        lines.append(f"- **{k.replace('_',' ').title()}**: {v}")
    lines.append("")
    lines.append("## Top Priority (by traffic & missing)")
    lines.append("")
    lines.append("| Message | Count | In Go | Rust Struct | Rust parse_* | In Registry | Next Action | Go Files | Rust Files |")
    lines.append("|---|---:|:---:|:---:|:---:|:---:|---|---|---|")

    for row in plan[:50]:
        lines.append("| {name} | {cnt} | {go} | {rs} | {pf} | {reg} | {act} | {gof} | {rsf} |".format(
            name=row["message_name"],
            cnt=row["observed_count"],
            go="✅" if row["has_go_def"] else "❌",
            rs="✅" if row["has_rust_struct"] else "❌",
            pf="✅" if row["has_rust_parse_fn"] else "❌",
            reg="✅" if row["registered_in_registry"] else "❌",
            act=row["action"],
            gof=", ".join(row["go_files"][:2]) + (" …" if len(row["go_files"])>2 else ""),
            rsf=", ".join(row["rust_files"][:2]) + (" …" if len(row["rust_files"])>2 else ""),
        ))

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "out_json": str(OUT_JSON.relative_to(ROOT)),
        "out_md": str(OUT_MD.relative_to(ROOT)),
        "messages_scanned": len(coverage),
        "go_defs_found": len(scan_go_structs()),
    }))
    return 0

if __name__ == "__main__":
    sys.exit(main())