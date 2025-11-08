import os, re, json, binascii, math, sys
from collections import Counter

MAP_PATH = os.path.join("third_party","retroproto","mapping_overrides.json")
FLOWS_ROOTS = [
    os.path.join("examples","pcap","flows"),
    os.path.join("orchestrator","examples","pcap","flows"),
]

def load_prefixes():
    with open(MAP_PATH, "r", encoding="utf8") as f:
        m = json.load(f)
    pref = []
    for e in m.get("entries", []):
        p = e.get("prefix")
        if p: pref.append(p)
    pref = sorted(set(pref), key=lambda s: (-len(s), s))
    return pref

def ascii_ratio(b: bytes):
    if not b: return 0.0
    printable = sum((32 <= x <= 126) or x in (10,13,9) for x in b)
    return printable / len(b)

def shannon_entropy(b: bytes):
    if not b: return 0.0
    c = Counter(b)
    n = len(b)
    ent = 0.0
    for v in c.values():
        p = v / n
        ent -= p * math.log2(p)
    return ent

def count_prefix_hits(b: bytes, prefixes):
    s = b.decode("utf-8", errors="ignore")
    hits = 0
    for p in prefixes:
        pat = rf"(?m)(?<![A-Za-z0-9]){re.escape(p)}(?=(?:[0-9;\|\+\-\?]|$))"
        if re.search(pat, s):
            hits += 1
    return hits

def list_flows():
    files = []
    for root in FLOWS_ROOTS:
        if os.path.isdir(root):
            for dirpath, _, filenames in os.walk(root):
                for fn in filenames:
                    if fn.startswith("flow_") and fn.endswith(".bin"):
                        files.append(os.path.join(dirpath, fn))
    return sorted(files)

def score_file(path, prefixes, max_bytes=512*1024):
    try:
        with open(path, "rb") as f:
            data = f.read(max_bytes)
    except Exception as e:
        return None
    ar = ascii_ratio(data)
    ent = shannon_entropy(data)
    hits = count_prefix_hits(data, prefixes)
    score = (hits * 1000.0) + (ar * 100.0) - ent
    return {
        "path": path,
        "ascii_ratio": ar,
        "entropy": ent,
        "prefix_hits": hits,
        "score": score,
        "size": len(data),
        "head_hex": binascii.hexlify(data[:64]).decode("ascii"),
        "head_ascii": data[:64].decode("utf-8", errors="replace"),
    }

def main():
    prefixes = load_prefixes()
    if not prefixes:
        print("ERROR: No prefixes loaded", file=sys.stderr); sys.exit(2)
    flows = list_flows()
    if not flows:
        print("ERROR: No flow_*.bin files found", file=sys.stderr); sys.exit(3)
    rows = []
    for p in flows:
        r = score_file(p, prefixes)
        if r: rows.append(r)
    rows.sort(key=lambda r: r["score"], reverse=True)
    report = {"candidates": rows[:10], "chosen": rows[0] if rows else None}
    out = os.path.join("examples","pcap","decoded","_plaintext_flow_probe.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf8") as f:
        json.dump(report, f, indent=2)
    if not rows or rows[0]["prefix_hits"] == 0:
        print("NO_PLAINTEXT_FLOW_FOUND")
        print(out)
        sys.exit(4)
    print("PLAINTEXT_FLOW", rows[0]["path"])
    print(out)

if __name__ == "__main__":
    main()