import json, os, collections
base = "examples/pcap/decoded"
path = os.path.join(base, "flow_reassembled_decoded.json")
data = json.load(open(path,'r',encoding='utf8'))
cnt = collections.Counter()
unknown = collections.Counter()
for d in data:
    p = d.get('message_prefix') or '<NONE>'
    n = d.get('message_name')
    cnt[p]+=1
    if not n:
        unknown[p]+=1
summ = {"total": len(data), "unknown_counts": unknown.most_common(30)}
print(json.dumps(summ, indent=2))
out = os.path.join(base, "reassemble_quick_summary.json")
json.dump(summ, open(out,"w",encoding="utf8"), indent=2)