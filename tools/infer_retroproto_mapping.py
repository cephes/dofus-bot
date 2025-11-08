#!/usr/bin/env python3
import json
import re
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

def download_file(url):
    """Download file from URL, return content or raise error."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            return response.read().decode('utf-8')
    except HTTPError as e:
        raise Exception(f"HTTP {e.code}: {e.reason}\n{str(e.read()[:400])}")
    except URLError as e:
        raise Exception(f"URL Error: {e.reason}")

def extract_prefixes(content, category):
    """Extract protocol IDs from Go file content."""
    prefixes = set()
    lines = content.split('\n')
    tokens = ["ProtocolId", "MsgCliIdByPkt", "MsgSvrIdByPkt", "case", "switch", "Protocol", "ProtocolId()"]

    for i, line in enumerate(lines):
        # Find string literals matching the pattern
        matches = re.findall(r'"([A-Za-z0-9\-\_]{1,12})"', line)
        for match in matches:
            # Check if within ±6 lines of a token
            start = max(0, i - 6)
            end = min(len(lines), i + 7)
            window = '\n'.join(lines[start:end])
            if any(token in window for token in tokens):
                # Normalize: trim trailing separators
                normalized = re.sub(r'[|;]$', '', match)
                prefixes.add(normalized)

    return sorted(list(prefixes))

def main():
    urls = {
        'client': 'https://raw.githubusercontent.com/kralamoure/retroproto/main/msgcli.go',
        'server': 'https://raw.githubusercontent.com/kralamoure/retroproto/main/msgsvr.go'
    }

    contents = {}
    for category, url in urls.items():
        try:
            contents[category] = download_file(url)
        except Exception as e:
            print(f"Failed to download {category} file: {e}", file=sys.stderr)
            sys.exit(1)

    all_prefixes = {}
    for category, content in contents.items():
        prefixes = extract_prefixes(content, category)
        if not prefixes:
            print(f"No prefixes found for {category}. First 30 lines:", file=sys.stderr)
            lines = content.split('\n')[:30]
            for line in lines:
                print(line, file=sys.stderr)
            sys.exit(1)
        all_prefixes[category] = prefixes

    # Generate JSON
    entries = []
    for category, prefixes in all_prefixes.items():
        for prefix in prefixes:
            entries.append({
                "prefix": prefix,
                "detection_type": "literal",
                "pattern": None,
                "category": category,
                "example_payload": "",
                "notes": f"from retroproto msg{category}.go"
            })

    data = {
        "generated_by": "kilocode-infer-retroproto",
        "source_commit": str(int(time.time())),
        "entries": entries
    }

    with open('third_party/retroproto/mapping_overrides.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Validate and print
    print("Prefixes discovered:")
    for category, prefixes in all_prefixes.items():
        print(f"{category.capitalize()}: {len(prefixes)} prefixes - {', '.join(prefixes)}")

if __name__ == '__main__':
    main()