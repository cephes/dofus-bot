#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

REPO = Path(__file__).resolve().parents[1]
NDJSON_DEFAULT = REPO / "examples" / "pcap" / "decoded" / "dummy_parsed_new.ndjson"
CORE = REPO / "core"
GEN_DIR = CORE / "src" / "retroproto_parsers" / "generated"
GEN_ACT = GEN_DIR / "actions"
HAND_DIR = CORE / "src" / "retroproto_parsers" / "handwritten"
REGISTRY_RS = CORE / "src" / "retroproto_parsers" / "registry.rs"

def read_ndjson(path: Path):
    items = []
    if not path.exists():
        return items
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                items.append(obj)
            except Exception as e:
                items.append({"_parse_error_line": ln, "_line": line, "_err": str(e)})
    return items

def slurp(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def list_rs(dirpath: Path):
    if not dirpath.exists():
        return []
    return [p for p in dirpath.rglob("*.rs") if p.is_file()]

def infer_name_from_filename(p: Path):
    # Filename like GameMovement.rs -> GameMovement
    return p.stem

def has_parse_fn(source: str, msg_name: str) -> bool:
    # Look for pub fn parse_MessageName(
    pat = rf"\bpub\s+fn\s+parse_{re.escape(msg_name)}\s*\("
    return re.search(pat, source) is not None

def registry_entries(text: str):
    # Heuristic: capture message names referenced in registry (strings) or in m.insert calls
    names = set()
    # m.insert("GameMovement", Box::new(parse_GameMovement));
    for m in re.finditer(r'insert\(\s*"([^"]+)"\s*,', text):
        names.add(m.group(1))
    # Also catch explicit string arrays/maps: "GameMovement" =>
    for m in re.finditer(r'"([A-Za-z0-9_]+)"\s*=>', text):
        names.add(m.group(1))
    # Fallback: catch parse_* mentions and derive name
    for m in re.finditer(r'\bparse_([A-Za-z0-9_]+)\b', text):
        names.add(m.group(1))
    return names

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="ndjson", default=str(NDJSON_DEFAULT))
    ap.add_argument("--out-md", dest="out_md", default=str(REPO / "PARSER_COVERAGE.md"))
    ap.add_argument("--out-json", dest="out_json", default=str(REPO / "parser_coverage.json"))
    args = ap.parse_args()

    ndjson_path = Path(args.ndjson)
    items = read_ndjson(ndjson_path)

    # Aggregate NDJSON parse outcomes
    by_msg = defaultdict(list)
    by_prefix = defaultdict(list)
    totals = {"total_rows": 0, "parsed_structured": 0, "parsed_empty": 0, "parsed_null": 0, "parse_error": 0}
    for obj in items:
        totals["total_rows"] += 1
        msg = obj.get("message_name")
        prefix = obj.get("prefix")
        parsed = obj.get("parsed")
        perr = obj.get("parse_error")

        if perr:
            totals["parse_error"] += 1
        if parsed is None:
            totals["parsed_null"] += 1
            outcome = "null"
        elif isinstance(parsed, dict) and len(parsed) == 0:
            totals["parsed_empty"] += 1
            outcome = "empty"
        else:
            totals["parsed_structured"] += 1
            outcome = "structured"

        rec = {
            "frame_index": obj.get("frame_index"),
            "prefix": prefix,
            "message_name": msg,
            "outcome": outcome,
            "fields": list(parsed.keys()) if isinstance(parsed, dict) else [],
        }
        if msg: by_msg[msg].append(rec)
        if prefix: by_prefix[prefix].append(rec)

    # Scan Rust sources
    rust_index = {}
    for d in [GEN_DIR, GEN_ACT, HAND_DIR]:
        for p in list_rs(d):
            name = infer_name_from_filename(p)
            src = slurp(p)
            rust_index[name] = {
                "path": str(p.relative_to(REPO)),
                "has_parse_fn": has_parse_fn(src, name),
            }

    # Registry
    reg_text = slurp(REGISTRY_RS)
    reg_names = registry_entries(reg_text) if reg_text else set()

    # Build per-message report (union of NDJSON names and Rust file names)
    all_msg_names = set(by_msg.keys()) | set(rust_index.keys())
    report = []
    for name in sorted(all_msg_names):
        sample_prefixes = sorted({r["prefix"] for r in by_msg.get(name, []) if r.get("prefix")})[:3]
        outcomes = Counter(r["outcome"] for r in by_msg.get(name, []))
        rust = rust_index.get(name, None)
        entry = {
            "message_name": name,
            "prefixes_sample": sample_prefixes,
            "ndjson_counts": dict(outcomes),
            "rust_file": rust["path"] if rust else None,
            "has_parse_fn": bool(rust and rust["has_parse_fn"]),
            "registered_in_registry": (name in reg_names),
            "examples_seen": len(by_msg.get(name, [])),
            "example_fields_sample": next((r["fields"] for r in by_msg.get(name, []) if r["outcome"]=="structured"), []),
        }
        report.append(entry)

    # Coverage summaries
    pct = lambda num, den: (100.0 * num / den) if den else 0.0
    structured_msgs = {n for n, v in by_msg.items() if any(r["outcome"]=="structured" for r in v)}
    empty_msgs = {n for n, v in by_msg.items() if any(r["outcome"]=="empty" for r in v)}
    null_msgs = {n for n, v in by_msg.items() if all(r["outcome"]=="null" for r in v)}  # if seen, all null

    # Calculate relative path safely
    try:
        ndjson_rel = str(ndjson_path.relative_to(REPO)) if ndjson_path.exists() else str(ndjson_path)
    except ValueError:
        # If relative_to fails, just use the absolute path
        ndjson_rel = str(ndjson_path)
    
    summary = {
        "generated_at": datetime.utcnow().isoformat()+"Z",
        "ndjson_path": ndjson_rel,
        "totals": totals,
        "message_names_seen": len(by_msg),
        "messages_with_structured_output": sorted(structured_msgs),
        "messages_with_empty_object_output": sorted(empty_msgs),
        "messages_with_null_output_only": sorted(null_msgs),
        "rust_messages_indexed": len(rust_index),
        "registry_names_count": len(reg_names),
    }

    # Write JSON
    out_json = Path(args.out_json)
    out_json.write_text(json.dumps({
        "summary": summary,
        "by_message": report,
        "by_prefix": {k: Counter(r["outcome"] for r in v) for k, v in by_prefix.items()},
        "registry_names": sorted(reg_names),
    }, indent=2), encoding="utf-8")

    # Write Markdown
    out_md = Path(args.out_md)
    lines = []
    lines.append(f"# Parser Coverage Report\n")
    lines.append(f"- Generated: {summary['generated_at']}")
    lines.append(f"- NDJSON: `{summary['ndjson_path']}`")
    lines.append("")
    lines.append("## Totals")
    lines.append(f"- Rows: {totals['total_rows']}")
    lines.append(f"- Structured rows: {totals['parsed_structured']}")
    lines.append(f"- Empty-object rows: {totals['parsed_empty']}")
    lines.append(f"- Null rows: {totals['parsed_null']}")
    lines.append(f"- Rows with parse_error set: {totals['parse_error']}")
    lines.append("")
    lines.append("## Registry / Rust Sources")
    lines.append(f"- Rust message files found: {len(rust_index)} (generated + handwritten)")
    lines.append(f"- Registry names detected: {summary['registry_names_count']}")
    lines.append("")
    lines.append("## Top Missing (seen in NDJSON but no Rust parse fn or not registered)")
    missing = [e for e in report if (e["examples_seen"]>0 and (not e["has_parse_fn"] or not e["registered_in_registry"]))]
    missing_sorted = sorted(missing, key=lambda e: (-e["examples_seen"], e["message_name"]))[:50]
    for e in missing_sorted:
        lines.append(f"- **{e['message_name']}** — seen {e['examples_seen']}×, parse_fn={e['has_parse_fn']}, registered={e['registered_in_registry']} (file={e['rust_file']})")
    lines.append("")
    lines.append("## Messages With Null Output Only")
    for name in summary["messages_with_null_output_only"][:100]:
        lines.append(f"- {name}")
    lines.append("")
    lines.append("## Sample of Structured Messages (fields)")
    for e in [x for x in report if x["example_fields_sample"]][:30]:
        fields = ", ".join(e["example_fields_sample"][:10])
        lines.append(f"- **{e['message_name']}** — fields: {fields or '(many)'}")
    lines.append("")
    lines.append("## By Prefix Outcome Counts")
    # Load from the JSON we just built to avoid recomputing
    with out_json.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for pfx, cnts in sorted(data["by_prefix"].items()):
        pretty = ", ".join(f"{k}:{v}" for k,v in sorted(cnts.items()))
        lines.append(f"- **{pfx}** — {pretty}")
    out_md.write_text("\n".join(lines)+"\n", encoding="utf-8")

    # Console summary
    try:
        md_rel = str(out_md.relative_to(REPO)) if out_md.exists() else str(out_md)
    except ValueError:
        md_rel = str(out_md)
    
    try:
        json_rel = str(out_json.relative_to(REPO)) if out_json.exists() else str(out_json)
    except ValueError:
        json_rel = str(out_json)
    
    print(json.dumps({
        "wrote": {
            "markdown": md_rel,
            "json": json_rel,
        },
        "totals": totals,
        "messages_seen": len(by_msg),
        "rust_files_indexed": len(rust_index),
        "registry_names_detected": len(reg_names),
    }, indent=2))

if __name__ == "__main__":
    sys.exit(main())