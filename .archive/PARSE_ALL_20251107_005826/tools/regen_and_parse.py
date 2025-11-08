#!/usr/bin/env python3
import argparse, os, re, sys, json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root (…/dofus-bot)
CORE = ROOT / "core"
GEN_DIR = CORE / "src" / "retroproto_parsers" / "generated"
DECODED = ROOT / "examples" / "pcap" / "decoded"
FLOWS = ROOT / "examples" / "pcap" / "flows"
PROBE = ROOT / "probe_report.json"  # optional, if present

def info(msg): print(f"[+] {msg}")
def warn(msg): print(f"[!] {msg}", file=sys.stderr)
def die(msg, code=1): warn(msg); sys.exit(code)

def add_derives_to_generated():
    if not GEN_DIR.exists():
        warn(f"Generated dir missing: {GEN_DIR}")
        return 0,0
    rs_files = list(GEN_DIR.rglob("*.rs"))
    changed = 0
    scanned = 0
    pat = re.compile(r"(^\s*)(pub\s+struct\s+\w+\s*(?:;|\{))", re.M|re.S)
    already = re.compile(r"#\s*\[\s*derive[^\]]*Serialize", re.S)
    for p in rs_files:
        txt = p.read_text(encoding="utf-8", errors="ignore")
        scanned += 1
        if already.search(txt):
            continue
        # insert derive above first struct occurrence
        new_txt, n = pat.subn(r"\1#[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]\n\1\2", txt, count=1)
        if n > 0 and new_txt != txt:
            p.write_text(new_txt, encoding="utf-8", newline="\n")
            changed += 1
    return scanned, changed

def ensure_serde_deps():
    cargo = CORE / "Cargo.toml"
    if not cargo.exists():
        die(f"Cargo.toml not found at {cargo}")
    txt = cargo.read_text(encoding="utf-8")
    if "[dependencies]" not in txt:
        txt += "\n[dependencies]\n"
    if "serde_json" not in txt or "serde" not in txt:
        # very light-touch insertion inside [dependencies]
        def inject(dep_line, key):
            nonlocal_txt = txt  # shadow outer
            return nonlocal_txt if key in nonlocal_txt else nonlocal_txt.replace("[dependencies]", "[dependencies]\n" + dep_line)
        txt = inject('serde = { version = "1", features = ["derive"] }\n', "serde =")
        txt = inject('serde_json = "1"\n', "serde_json")
        cargo.write_text(txt, encoding="utf-8", newline="\n")
        return True
    return False

def cargo_build_release():
    info("Building core (release)…")
    subprocess.run(["cargo","build","--release"], cwd=str(CORE), check=True)

def exe(path_no_ext: Path) -> Path:
    return path_no_ext.with_suffix(".exe") if os.name == "nt" else path_no_ext

def choose_flow(arg_flow: Path|None):
    if arg_flow:
        return arg_flow
    # 1) probe_report.json if present
    if PROBE.exists():
        try:
            pr = json.loads(PROBE.read_text(encoding="utf-8"))
            cand = pr.get("chosen", {}).get("path")
            if cand:
                p = ROOT / cand
                if p.exists(): return p
        except Exception:
            pass
    # 2) fallback: first *.bin in examples/pcap/flows
    bins = sorted(FLOWS.glob("*.bin"))
    if not bins:
        die(f"No .bin flows found in {FLOWS}. Generate flows first.")
    return bins[0]

def run_reassemble(flow_path: Path) -> Path:
    out = DECODED / "dummy_reassembled.json"
    DECODED.mkdir(parents=True, exist_ok=True)
    binpath = exe(CORE / "target" / "release" / "reassemble")
    if not binpath.exists():
        die(f"reassemble binary not found at {binpath}")
    cmd = [str(binpath), "--input", str(flow_path), "--output", str(out)]
    info(" ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT), check=True)
    return out

def run_parse_messages(reass_json: Path) -> tuple[Path, Path]:
    out_json = DECODED / "dummy_parsed.json"
    out_ndjson = DECODED / "dummy_parsed.ndjson"
    binpath = exe(CORE / "target" / "release" / "parse_messages")
    if not binpath.exists():
        die(f"parse_messages binary not found at {binpath}")
    cmd = [str(binpath), "--in", str(reass_json), "--out", str(out_json), "--ndjson", str(out_ndjson)]
    info(" ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT), check=True)
    return out_json, out_ndjson

def summarize_ndjson(ndjson: Path):
    if not ndjson.exists():
        die(f"NDJSON not found: {ndjson}")
    total = 0
    ok = 0
    by_prefix = {}
    examples = []
    with ndjson.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            obj = json.loads(line)
            total += 1
            if obj.get("parsed_ok"):
                ok += 1
                if len(examples) < 8:
                    examples.append(obj)
            pref = obj.get("message_prefix") or "<NONE>"
            by_prefix[pref] = by_prefix.get(pref, 0) + 1
    print(json.dumps({
        "total_messages": total,
        "parsed_ok": ok,
        "unknown": total - ok,
        "top_prefixes": sorted(by_prefix.items(), key=lambda kv: kv[1], reverse=True)[:12],
        "first_ok_examples": examples
    }, indent=2, ensure_ascii=False))

def main():
    ap = argparse.ArgumentParser(description="Regenerate derives, build, and run dummy parsing (Python, fast).")
    ap.add_argument("--flow", type=str, help="Path to a specific .bin flow (default: auto)")
    args = ap.parse_args()
    flow = Path(args.flow).resolve() if args.flow else None

    info(f"Repo root: {ROOT}")
    scanned, changed = add_derives_to_generated()
    info(f"Scanned generated *.rs: {scanned}, added derives to: {changed}")

    if ensure_serde_deps():
        info("Updated serde deps in Cargo.toml")

    cargo_build_release()

    flow_path = choose_flow(flow)
    info(f"Using flow: {flow_path}")

    reass_json = run_reassemble(flow_path)
    info(f"Reassembled → {reass_json}")

    parsed_json, parsed_ndjson = run_parse_messages(reass_json)
    info(f"Parsed JSON  → {parsed_json}")
    info(f"Parsed NDJSON → {parsed_ndjson}")

    summarize_ndjson(parsed_ndjson)

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        die(f"Command failed ({e.returncode}): {' '.join(e.cmd)}")
