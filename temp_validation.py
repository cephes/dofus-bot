import json, os
from collections import Counter

parsed = json.load(open('examples/pcap/decoded/dummy_parsed.json','r',encoding='utf8'))
prefix_ctr = Counter()
name_ctr = Counter()
known = 0
for it in parsed:
    px = it.get('message_prefix','')
    nm = it.get('message_name') or ''
    prefix_ctr[px]+=1
    if nm and nm.lower() != 'unknown':
        known+=1
        name_ctr[nm]+=1
report = {
    "total": len(parsed),
    "known": known,
    "unknown": len(parsed)-known,
    "top_prefixes": prefix_ctr.most_common(10),
    "top_names": name_ctr.most_common(10)
}
print(json.dumps(report,indent=2))
assert report["total"]>100,"unexpectedly few parsed messages"
assert report["unknown"]<50,"too many unknowns"