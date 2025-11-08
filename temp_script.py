import json, re, binascii, os, collections
p = os.path.join("examples","pcap","decoded","flow_reassembled_decoded.json")
if not os.path.exists(p):
    raise SystemExit(f"Decoder output not found at {p}")
data = json.load(open(p,"r",encoding="utf8"))

def hex_to_ascii(h):
    h = re.sub(r'[^0-9a-fA-F]','',h or '')
    try:
        b = binascii.unhexlify(h)
    except Exception:
        return "", b""
    return b.decode('utf-8','replace'), b

def pref(s):
    s=s.lstrip()
    if s.startswith("GM|-"): return "GM|-"
    if s.startswith("GM|"):  return "GM|"
    m=re.match(r'^([A-Za-z][A-Za-z\|\+\-\?]*)', s)
    return m.group(1) if m else None

cnt=collections.Counter(); none=0
for o in data:
    asc,_ = hex_to_ascii(o.get('payload_hex') or o.get('payload') or "")
    k = pref(asc)
    if not k:
        none += 1; cnt["<NONE>"] += 1
    else:
        cnt[k] += 1

summary = {
    "total": len(data),
    "none_after_reassembly": none,
    "top_prefixes": cnt.most_common(15),
}
out = os.path.join("examples","pcap","decoded","reassemble_quick_summary.json")
open(out,"w",encoding="utf8").write(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))