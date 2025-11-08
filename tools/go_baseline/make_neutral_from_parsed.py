#!/usr/bin/env python3
"""
Convert parsed Rust NDJSON back to neutral prefix+payload format for Go baseline testing.
This creates the input that Go can parse to compare against Rust results.
"""

import json
import sys
import os

def convert_parsed_to_neutral(rust_ndjson_path, output_path):
    """Convert Rust parsed NDJSON to neutral format for Go baseline."""
    
    print(f"Reading Rust parsed data from: {rust_ndjson_path}")
    
    neutral_lines = []
    with open(rust_ndjson_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                prefix = data.get('prefix', '')
                extra_preview = data.get('extra_preview', '')
                
                # Skip empty payloads or invalid data
                if not prefix or not extra_preview:
                    continue
                    
                # Create neutral format: prefix|extra_preview
                neutral_line = f"{prefix}|{extra_preview}"
                neutral_lines.append(neutral_line)
                
            except json.JSONDecodeError as e:
                print(f"Warning: Line {line_num} - JSON decode error: {e}")
                continue
            except Exception as e:
                print(f"Warning: Line {line_num} - Processing error: {e}")
                continue
    
    print(f"Converted {len(neutral_lines)} lines to neutral format")
    
    # Write neutral input
    print(f"Writing neutral input to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in neutral_lines:
            f.write(line + '\n')
    
    return len(neutral_lines)

def main():
    if len(sys.argv) != 3:
        print("Usage: python make_neutral_from_parsed.py <rust_ndjson_path> <output_path>")
        sys.exit(1)
        
    rust_ndjson_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(rust_ndjson_path):
        print(f"Error: Input file not found: {rust_ndjson_path}")
        sys.exit(1)
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Convert
    count = convert_parsed_to_neutral(rust_ndjson_path, output_path)
    print(f"Conversion complete: {count} neutral lines written")

if __name__ == '__main__':
    main()