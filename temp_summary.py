import json, os, collections, re, binascii
base = "examples/pcap/decoded"
path = os.path.join(base, "flow_reassembled_decoded.json")
data = json.load(open(path,'r',encoding='utf8'))
cnt = collections.Counter()
unknown = collections.Counter()
samples = {}
for d in data:
    p = d.get('message_prefix') or '<NONE>'
    n = d.get('message_name')
    cnt[p]+=1
    if not n:
        unknown[p]+=1
        if p not in samples:
            # keep a tiny payload ascii preview for troubleshooting
            h = re.sub(r'[^0-9a-fA-F]','', d.get('payload_hex') or '')
            try:
                b = binascii.unhexlify(h)
                s = b.decode('utf-8','replace')[:160]
            except Exception:
                s = ''
            samples[p] = {"count":0,"example":s}
        samples[p]["count"] = unknown[p]
summ = {
  "total": len(data),
  "top_prefixes": cnt.most_common(20),
  "unknown_counts": unknown.most_common(20),
}
out1 = os.path.join(base, "reassemble_quick_summary.json")
out2 = os.path.join(base, "unknown_prefix_examples.json")
json.dump(summ, open(out1,"w",encoding="utf8"), indent=2)
json.dump(samples, open(out2,"w",encoding="utf8"), indent=2, ensure_ascii=False)
print(json.dumps(summ, indent=2))
print("\nWrote unknown samples to", out2)