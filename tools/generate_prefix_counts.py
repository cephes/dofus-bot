#!/usr/bin/env python3
import json
import base64
from collections import Counter

def decode_hex_to_text(hex_str):
    """Decode hex string to text if possible."""
    try:
        bytes_data = bytes.fromhex(hex_str)
        return bytes_data.decode('utf-8', errors='ignore')
    except:
        return hex_str

def generate_prefix_counts(json_file, output_file):
    """Generate prefix counts from decoded JSON."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    prefixes = []
    for packet in data:
        payload_hex = packet.get('payload_hex', '')
        if payload_hex:
            text = decode_hex_to_text(payload_hex)
            if text and len(text) > 0:
                prefix = text[0]
                prefixes.append(prefix)

    counts = Counter(prefixes)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted_counts), f, indent=2, ensure_ascii=False)

    return len(data), sorted_counts[:30]

if __name__ == '__main__':
    num_messages, top_prefixes = generate_prefix_counts(
        'examples/pcap/decoded/flow_000_decoded.json',
        'examples/pcap/decoded/prefix_counts_after_overrides.json'
    )
    print(f"Generated prefix counts for {num_messages} messages")
    print("Top 30 prefixes:")
    for prefix, count in top_prefixes:
        print(f"  {prefix}: {count}")