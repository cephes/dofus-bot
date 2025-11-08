import os, sys, json, subprocess, shutil, glob, time
from pathlib import Path

def run(cmd, cwd=None, timeout=60):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, shell=True)
        return {"cmd": cmd, "code": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    except Exception as e:
        return {"cmd": cmd, "code": -1, "stdout": "", "stderr": f"{type(e).__name__}: {e}"}

def safe_read_text(p, max_bytes=200_000):
    try:
        data = Path(p).read_bytes()
        if len(data) > max_bytes:
            return data[:max_bytes].decode("utf-8", errors="replace") + f"\n[...truncated {len(data)-max_bytes} bytes]"
        return data.decode("utf-8", errors="replace")
    except Exception as e:
        return f"[error reading {p}: {e}]"

def dir_summary(root, subpaths, max_files=1000):
    out = {}
    rootp = Path(root)
    for sp in subpaths:
        p = rootp / sp
        info = {"exists": p.exists(), "files": 0, "dirs": 0, "total_bytes": 0, "sample": []}
        if p.exists():
            files = []
            for dp, dn, fn in os.walk(p):
                info["dirs"] += 1
                for f in fn:
                    files.append(os.path.join(dp, f))
                    if len(files) >= max_files:
                        break
                if len(files) >= max_files:
                    break
            info["files"] = len(files)
            total = 0
            sample = []
            for i, f in enumerate(sorted(files)[:20] + sorted(files)[-20:]):
                try:
                    total += Path(f).stat().st_size
                except Exception:
                    pass
                if len(sample) < 20:
                    sample.append(str(Path(f).relative_to(rootp)))
            info["total_bytes"] = total
            info["sample"] = sample
        out[sp] = info
    return out

def count_patterns(root, globs, pattern):
    import re
    rex = re.compile(pattern, re.M)
    total = 0
    matches = 0
    sample = []
    for g in globs:
        for f in glob.glob(str(Path(root)/g), recursive=True):
            total += 1
            try:
                s = Path(f).read_text(encoding="utf-8", errors="replace")
                mm = rex.findall(s)
                if mm:
                    matches += len(mm)
                    if len(sample) < 20:
                        sample.append(str(Path(f).relative_to(root)))
            except Exception:
                pass
    return {"files_scanned": total, "matches": matches, "sample_files": sample}

def main():
    CWD = Path.cwd()
    diag = {"when": time.strftime("%Y-%m-%d %H:%M:%S"), "cwd": str(CWD), "errors": []}

    # Detect repo root by finding core/Cargo.toml upwards
    repo = CWD
    for _ in range(5):
        if (repo / "core" / "Cargo.toml").exists():
            break
        repo = repo.parent
    diag["repo_root"] = str(repo)

    # Tool versions
    diag["versions"] = {
        "rustc": run("rustc -V") ,
        "cargo": run("cargo -V"),
        "python": run("python --version"),
        "go": run("go version"),
        "git": run("git --version"),
    }

    # Top-level and key subtree summaries
    diag["trees"] = dir_summary(
        repo,
        subpaths=[
            ".", "core", "core/src", "core/src/bin",
            "core/src/retroproto_parsers",
            "core/src/retroproto_parsers/generated",
            "core/src/retroproto_parsers/handwritten",
            "core/target/release",
            "tools", "tools/retroproto_porter_py",
            "tools/retroproto_porter",
            "scripts",
            "examples", "examples/pcap", "examples/pcap/flows", "examples/pcap/decoded",
            "third_party", "third_party/retroproto",
            "third_party/retroproto/msgsvr", "third_party/retroproto/msgcli"
        ],
        max_files=5000
    )

    # Key files presence
    def exists(rel): return (repo / rel).exists()
    keys = [
        "core/Cargo.toml",
        "core/src/retroproto_parsers/mod.rs",
        "tools/gen_parser_registry.py",
        "tools/retroproto_porter_py/porter.py",
        "tools/retroproto_porter/main.go",
        "third_party/retroproto/mapping_overrides.json",
        "third_party/retroproto/mappings_go.txt",
        "examples/pcap/dummy.pcap",
        "examples/pcap/decoded/dummy_reassembled.json",
    ]
    diag["key_files"] = {k: exists(k) for k in keys}

    # Generated parsers stats
    gen_dir = repo / "core/src/retroproto_parsers/generated"
    gen_files = []
    if gen_dir.exists():
        gen_files = sorted([str(p.relative_to(repo)) for p in gen_dir.glob("*.rs")])
    diag["generated_parsers"] = {
        "count_rs": len(gen_files),
        "sample_first_10": gen_files[:10],
        "sample_last_10": gen_files[-10:]
    }

    # Count pub struct & parse_ functions
    diag["counts"] = {
        "pub_structs": count_patterns(repo, ["core/src/retroproto_parsers/generated/*.rs"], r"(?m)^\s*pub\s+struct\s+\w+"),
        "parse_functions": count_patterns(repo, ["core/src/retroproto_parsers/generated/*.rs",
                                                 "core/src/retroproto_parsers/handwritten/*.rs"],
                                          r"(?m)^\s*pub\s+fn\s+parse_[A-Za-z0-9_]+"),
    }

    # Parser registry probe (search known markers)
    # Look for either once_cell::sync::Lazy<HashMap<..>> or lazy_static! macro usage
    diag["registry_probe"] = count_patterns(repo, ["core/src/**/*.rs"], r"(once_cell::sync::Lazy\s*<\s*std::collections::HashMap|lazy_static!\s*\()")

    # Cargo metadata (from core/)
    core = repo / "core"
    diag["cargo_metadata"] = run("cargo metadata --no-deps -q", cwd=str(core), timeout=120)

    # Binary help probes (ignore errors)
    bins = {
        "reassemble": "core/target/release/reassemble.exe",
        "parse_messages": "core/target/release/parse_messages.exe",
        "pcap2flow": "core/target/release/pcap2flow.exe",
    }
    diag["binaries"] = {}
    for name, rel in bins.items():
        p = repo / rel
        info = {"exists": p.exists()}
        if p.exists():
            info["help"] = run(f'"{p}" --help', cwd=str(repo))
        diag["binaries"][name] = info

    # Peek parsed NDJSON if present
    parsed_glob = list((repo / "examples/pcap/decoded").glob("*parsed*.*ndjson"))
    diag["parsed_ndjson_peek"] = []
    for p in parsed_glob[:2]:
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= 5: break
                    lines.append(line.strip())
            diag["parsed_ndjson_peek"].append({"path": str(p.relative_to(repo)), "first_lines": lines})
        except Exception as e:
            diag["errors"].append(f"peek {p}: {e}")

    # Peek reassembled json
    reasm = repo / "examples/pcap/decoded/dummy_reassembled.json"
    if reasm.exists():
        try:
            import json as _json
            arr = _json.loads(reasm.read_text(encoding="utf-8", errors="replace"))
            head_keys = list(arr[0].keys()) if arr else []
            diag["reassembled_info"] = {"path": str(reasm.relative_to(repo)), "len": len(arr), "first_entry_keys": head_keys}
        except Exception as e:
            diag["errors"].append(f"reassembled parse: {e}")

    # Save repo_diag.json
    out_json = repo / "repo_diag.json"
    out_json.write_text(json.dumps(diag, indent=2), encoding="utf-8")

    # Render REPO_DIAGNOSTIC.md
    md = []
    md.append(f"# Repo Diagnostic ({time.strftime('%Y-%m-%d %H:%M:%S')})")
    md.append(f"- Repo root: `{diag['repo_root']}`")
    md.append("## Toolchain Versions")
    for k,v in diag["versions"].items():
        md.append(f"- **{k}**: code={v['code']} stdout=`{(v['stdout'] or '').replace('`','\\`')}` stderr=`{(v['stderr'] or '').replace('`','\\`')}`")
    md.append("\n## Key Files Present")
    for k,ok in diag["key_files"].items():
        md.append(f"- {k}: {'✅' if ok else '❌'}")
    md.append("\n## Generated Parsers")
    gp = diag["generated_parsers"]
    md.append(f"- Count .rs: **{gp['count_rs']}**")
    md.append(f"- First 10: {gp['sample_first_10']}")
    md.append(f"- Last 10: {gp['sample_last_10']}")
    md.append("\n## Counts")
    md.append(f"- pub struct: matches={diag['counts']['pub_structs']['matches']} (files scanned {diag['counts']['pub_structs']['files_scanned']})")
    md.append(f"- parse_ functions: matches={diag['counts']['parse_functions']['matches']} (files scanned {diag['counts']['parse_functions']['files_scanned']})")
    md.append(f"- Registry markers: matches={diag['registry_probe']['matches']}")
    md.append("\n## Cargo Metadata (core/)")
    md.append(f"- code={diag['cargo_metadata']['code']}")
    if diag['cargo_metadata']['stdout']:
        md.append(f"<details><summary>stdout (truncated)</summary>\n\n```\n{diag['cargo_metadata']['stdout'][:1500]}\n```\n</details>")
    if diag['cargo_metadata']['stderr']:
        md.append(f"<details><summary>stderr</summary>\n\n```\n{diag['cargo_metadata']['stderr']}\n```\n</details>")

    md.append("\n## Binaries")
    for name,info in diag["binaries"].items():
        md.append(f"- {name}: {'✅' if info['exists'] else '❌'}")
        if info.get("help"):
            md.append(f"  - help.code={info['help']['code']}")
            if info['help']['stdout']:
                md.append(f"  <details><summary>stdout</summary>\n\n```\n{info['help']['stdout']}\n```\n</details>")
            if info['help']['stderr']:
                md.append(f"  <details><summary>stderr</summary>\n\n```\n{info['help']['stderr']}\n```\n</details>")

    md.append("\n## Parsed NDJSON Peek")
    for peek in diag["parsed_ndjson_peek"]:
        md.append(f"- {peek['path']}")
        md.append("```\n" + "\n".join(peek["first_lines"]) + "\n```")

    if "reassembled_info" in diag:
        r = diag["reassembled_info"]
        md.append("\n## Reassembled JSON")
        md.append(f"- {r['path']}: len={r['len']}, first_entry_keys={r['first_entry_keys']}")

    md.append("\n## Directory Snapshots (summaries)")
    for sp,info in diag["trees"].items():
        md.append(f"\n### {sp}\n- exists: {'✅' if info['exists'] else '❌'}\n- dirs: {info['dirs']} files: {info['files']} total_bytes: {info['total_bytes']}\n- sample files: {info['sample']}")

    if diag["errors"]:
        md.append("\n## Errors (non-fatal)\n```\n" + "\n".join(diag["errors"]) + "\n```")

    (repo / "REPO_DIAGNOSTIC.md").write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {out_json} and REPO_DIAGNOSTIC.md")

if __name__ == "__main__":
    main()