import json, os, sys, re
s = r"""PLAINTEXT_FLOW examples\pcap\flows\flow_000_TCP_192.168.1.8_2485_52.214.173.25_443.bin
examples\pcap\decoded\_plaintext_flow_probe.json"""
# if NO_PLAINTEXT_FLOW_FOUND appeared, just print the probe file path and exit with code 11
if "NO_PLAINTEXT_FLOW_FOUND" in s:
    m = re.search(r'(\S+_plaintext_flow_probe\.json)', s)
    print("No plaintext flow detected. Probe report at:", m.group(1) if m else "(unknown)")
    sys.exit(11)
# otherwise extract the chosen path
m = re.search(r'PLAINTEXT_FLOW\s+(.+)', s)
if not m:
    print("Could not parse chosen plaintext flow from probe output.")
    sys.exit(12)
chosen = m.group(1).strip()
out = os.path.join("examples","pcap","decoded","flow_reassembled_decoded.json")
print("CHOSEN_FLOW", chosen)
print("OUTPUT_JSON", out)
with open("_chosen_flow.txt","w",encoding="utf8") as f:
    f.write(chosen)
with open("_output_json.txt","w",encoding="utf8") as f:
    f.write(out)