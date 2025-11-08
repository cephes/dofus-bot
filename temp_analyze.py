import os, json, re, binascii, sys
from collections import Counter, defaultdict

root = os.getcwd()
summary_path = os.path.join(root, "examples", "pcap", "decoded", "flow_dummy_parsed_summary.json")
decoded_path = os.path.join(root, "examples", "pcap", "decoded", "flow_dummy_decoded.json")
analysis_out = os.path.join(root, "examples", "pcap", "decoded", "none_continuation_analysis.json")
examples_out = os.path.join(root, "examples", "pcap", "decoded", "none_continuation_examples.json")
mapping_path = os.path.join(root, "third_party", "retroproto", "mapping_overrides.json")

def hex_to_ascii(h):
    h = re.sub(r'[^0-9a-fA-F]', '', h or '')
    try:
        b = binascii.unhexlify(h)
    except Exception:
        return "", b""
    return b.decode("utf-8", errors="replace"), b

def extract_prefix(ascii_s):
    if not ascii_s: return None
    s = ascii_s.lstrip()
    if s.startswith("GM|-"): return "GM|-"
    if s.startswith("GM|"):  return "GM|"
    m = re.match(r'^([A-Za-z][A-Za-z\|\+\-\?]*)', s)
    return m.group(1) if m else None

# Load mapping for "is known?"
mapping = {}
if os.path.exists(mapping_path):
    mo = json.load(open(mapping_path, "r", encoding="utf8"))
    for e in mo.get("entries", []):
        mapping[e["prefix"]] = e.get("message_name")

# Load data
data = None
used_source = None
if os.path.exists(summary_path):
    data = json.load(open(summary_path, "r", encoding="utf8"))
    used_source = "summary"
elif os.path.exists(decoded_path):
    raw = json.load(open(decoded_path, "r", encoding="utf8"))
    # reconstruct minimal fields
    data = []
    for i, item in enumerate(raw):
        ph = item.get("payload_hex") or item.get("payload") or ""
        ascii_s, b = hex_to_ascii(ph)
        pref = extract_prefix(ascii_s)
        name = mapping.get(pref)
        data.append({
            "frame_index": item.get("index", i),
            "length": len(b),
            "message_prefix": pref or None,
            "message_name": name,
            "payload_hex": ph,
            "_ascii": ascii_s
        })
    used_source = "decoded"
else:
    print("ERROR: No decoded files found. Expected one of:")
    print(" -", summary_path)
    print(" -", decoded_path)
    sys.exit(2)

# Ensure ASCII exists in entries
for ent in data:
    if "_ascii" not in ent:
        asc, _ = hex_to_ascii(ent.get("payload_hex",""))
        ent["_ascii"] = asc

def looks_incomplete(prev_ascii):
    # Heuristic: does not end with a delimiter often present in text messages or segments
    # Many retro messages are line-like segments separated by ';' and sometimes end with ';' or '|' groups.
    s = prev_ascii.strip()
    if not s: return True
    # If ends with a clear terminator, probably complete
    if s.endswith(";") or s.endswith("|") or s.endswith(";;"): 
        return False
    # If it's very long and contains multiple segments but no end delim, likely incomplete
    if len(s) > 40 and ('|' in s or ';' in s) and not s.endswith((";", "|")):
        return True
    # Default neutral
    return False

# Prefix families that commonly produce multi-part payloads
SPAN_PRONE = {"GM|", "GM|-", "GA", "GAS", "GAF", "GDM", "GIE", "GTR", "GTS", "GTF", "GTM"}

total = len(data)
none_idx = [i for i, ent in enumerate(data) if (ent.get("message_prefix") in (None, "<NONE>"))]
none_total = len(none_idx)

likely_cont = []
chains = []
current_chain = []

def is_alpha_start(s):
    s = (s or "").lstrip()
    return bool(re.match(r'^[A-Za-z]', s))

# Determine likely continuation by heuristics
for i in none_idx:
    cur = data[i]
    cur_ascii = cur["_ascii"]
    prev = data[i-1] if i > 0 else None
    prev_known = bool(prev and prev.get("message_name"))
    prev_prefix = prev.get("message_prefix") if prev else None

    H1 = prev_known
    H2 = not is_alpha_start(cur_ascii)  # doesn't begin with a fresh protocol token
    H3 = prev_prefix in SPAN_PRONE or (prev and looks_incomplete(prev["_ascii"]))
    # Consider NONE-chain after known
    H4 = False
    if i>0 and (data[i-1].get("message_prefix") in (None, "<NONE>")):
        # if previous of the chain begins at a known prefix
        j = i-1
        chain_has_known_before = False
        while j >= 0 and data[j].get("message_prefix") in (None, "<NONE>"):
            j -= 1
        if j >= 0 and data[j].get("message_name"):
            chain_has_known_before = True
        H4 = chain_has_known_before

    if H1 and (H2 or H3 or H4):
        likely_cont.append(i)

    # build chains list for reporting (consecutive NONEs)
    if current_chain and i == current_chain[-1] + 1:
        current_chain.append(i)
    else:
        if len(current_chain) >= 2:
            chains.append(current_chain[:])
        current_chain = [i]
if len(current_chain) >= 2:
    chains.append(current_chain[:])

# Group likely continuations by their preceding known frame index
groups = defaultdict(list)
for i in likely_cont:
    # find nearest previous non-NONE as anchor
    j = i-1
    while j >= 0 and data[j].get("message_prefix") in (None, "<NONE>"):
        j -= 1
    if j >= 0 and data[j].get("message_name"):
        groups[j].append(i)

# Simulate a merge count: how many NONE would be "absorbed"
absorbed = len(set(likely_cont))

# Build examples
examples = []
for anchor, cont_list in list(groups.items())[:25]:  # limit
    prev = data[anchor]
    prev_ascii = prev["_ascii"][:160].replace("\n"," ")
    span_preview = []
    for k in cont_list[:5]:  # show first few per group
        ca = data[k]["_ascii"][:160].replace("\n"," ")
        span_preview.append({"idx": k, "start_ascii": ca})
    examples.append({
        "anchor_index": anchor,
        "anchor_prefix": prev.get("message_prefix"),
        "anchor_name": prev.get("message_name"),
        "anchor_ascii_head": prev_ascii,
        "continuations": span_preview
    })

# Stats
stats = {
    "total_packets": total,
    "none_packets": none_total,
    "likely_continuations": absorbed,
    "none_chains_count": len(chains),
    "none_chains_examples": [ {"len":len(ch), "start": ch[0], "end": ch[-1]} for ch in chains[:15] ],
    "span_prone_prefix_hits": sum(1 for i in range(1,total) if data[i-1].get("message_prefix") in SPAN_PRONE and (i in none_idx)),
    "heuristics_used": ["H1 prev_known", "H2 cur_not_alpha_start", "H3 prev_span_prone_or_incomplete", "H4 continuation_chain_after_known"],
    "source_used": used_source,
}

# Write outputs
os.makedirs(os.path.dirname(analysis_out), exist_ok=True)
with open(analysis_out, "w", encoding="utf8") as f:
    json.dump(stats, f, indent=2)

with open(examples_out, "w", encoding="utf8") as f:
    json.dump(examples, f, indent=2)

# Print concise report
print("Hypothesis test complete.")
print(f"Total: {total}  NONE: {none_total}  Likely continuations: {absorbed}")
print(f"NONE chains: {len(chains)}  (see {os.path.relpath(analysis_out, root)})")
print(f"Examples written to: {os.path.relpath(examples_out, root)}")