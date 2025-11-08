#!/usr/bin/env python3
"""
Compare Rust vs Go parsing on the same dataset by using the existing Rust NDJSON.
This script extracts the target messages and compares the parsing results.
"""

import json
import subprocess
import os
import tempfile

def extract_target_messages(rust_ndjson_path, target_messages):
    """Extract only the target message types from Rust NDJSON."""
    
    print(f"Reading Rust NDJSON from: {rust_ndjson_path}")
    
    extracted_lines = []
    with open(rust_ndjson_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                message_name = data.get('message_name', '')
                
                if message_name in target_messages:
                    extracted_lines.append(line)
                    
            except json.JSONDecodeError as e:
                print(f"Warning: Line {line_num} - JSON decode error: {e}")
                continue
    
    print(f"Extracted {len(extracted_lines)} target messages")
    return extracted_lines

def create_neutral_input(rust_lines):
    """Create neutral input from Rust NDJSON for Go baseline."""
    
    neutral_lines = []
    for line in rust_lines:
        try:
            data = json.loads(line)
            prefix = data.get('prefix', '')
            extra_preview = data.get('extra_preview', '')
            
            if prefix and extra_preview:
                # Create format: prefix|extra_preview
                neutral_line = f"{prefix}|{extra_preview}"
                neutral_lines.append(neutral_line)
                
        except json.JSONDecodeError as e:
            print(f"Warning: Skipping invalid line: {e}")
            continue
    
    return neutral_lines

def run_go_baseline(neutral_lines, go_output_path):
    """Run Go baseline parser on the neutral input."""
    
    # Create temporary input file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ndjson', delete=False) as f:
        for line in neutral_lines:
            f.write(line + '\n')
        temp_input_path = f.name
    
    try:
        # Run Go baseline
        cmd = [
            'bin/retroproto_go_baseline.exe',
            '-in', temp_input_path,
            '-out-ndjson', go_output_path,
            '-out-json', go_output_path + '.json'
        ]
        
        print(f"Running Go baseline: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Go baseline failed with code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
        else:
            print("Go baseline completed successfully")
            print(f"Output: {result.stdout}")
            return True
            
    finally:
        # Clean up temp file
        if os.path.exists(temp_input_path):
            os.unlink(temp_input_path)

def compare_parsers(rust_ndjson_path, go_ndjson_path, target_messages):
    """Compare Rust vs Go parsing results."""
    
    print(f"Comparing parsers for {len(target_messages)} target message types...")
    
    # Load Rust results
    rust_results = {}
    with open(rust_ndjson_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                message_name = data.get('message_name', '')
                if message_name in target_messages:
                    rust_results[f"{message_name}_{len(rust_results)}"] = data
            except json.JSONDecodeError:
                continue
    
    # Load Go results
    go_results = {}
    if os.path.exists(go_ndjson_path):
        with open(go_ndjson_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    message_name = data.get('message_name', '')
                    if message_name in target_messages:
                        go_results[f"{message_name}_{len(go_results)}"] = data
                except json.JSONDecodeError:
                    continue
    
    # Compare results
    comparison_results = {
        'total_rust_messages': len(rust_results),
        'total_go_messages': len(go_results),
        'parsing_comparisons': [],
        'summary': {
            'exact_matches': 0,
            'field_differences': 0,
            'go_failed_rust_succeeded': 0,
            'rust_failed_go_succeeded': 0
        }
    }
    
    for key, rust_data in rust_results.items():
        message_name = rust_data.get('message_name', 'Unknown')
        go_key = key.replace(f"{message_name}_", f"{message_name}_")
        
        comparison = {
            'message_name': message_name,
            'rust_parsed': rust_data.get('parsed'),
            'rust_parse_error': rust_data.get('parse_error'),
            'go_parsed': None,
            'go_parse_error': None,
            'match': False,
            'differences': []
        }
        
        if go_key in go_results:
            go_data = go_results[go_key]
            comparison['go_parsed'] = go_data.get('parsed')
            comparison['go_parse_error'] = go_data.get('parse_error')
            
            # Check for exact match
            if (comparison['rust_parse_error'] == comparison['go_parse_error'] and
                comparison['rust_parsed'] == comparison['go_parsed']):
                comparison['match'] = True
                comparison_results['summary']['exact_matches'] += 1
            else:
                comparison_results['summary']['field_differences'] += 1
        else:
            comparison_results['summary']['go_failed_rust_succeeded'] += 1
        
        comparison_results['parsing_comparisons'].append(comparison)
    
    return comparison_results

def main():
    # Target messages we fixed
    target_messages = [
        'AksServerMessage',
        'BasicsDate', 
        'BasicsTime',
        'GameMapData',
        'GameMovement',
        'GameMovementRemove',
        'InfosLifeRestoreTimerStart',
        'InfosMessage',
        'ItemsQuantity',
        'ItemsWeight'
    ]
    
    rust_ndjson_path = 'examples/pcap/decoded/dummy_parsed_all.ndjson'
    go_output_path = 'examples/pcap/decoded/dummy_go_comprehensive.ndjson'
    
    print(f"Extracting {len(target_messages)} target message types from Rust dataset...")
    rust_lines = extract_target_messages(rust_ndjson_path, target_messages)
    
    if not rust_lines:
        print("No target messages found in Rust dataset!")
        return
    
    print("Creating neutral input for Go baseline...")
    neutral_lines = create_neutral_input(rust_lines)
    
    if not neutral_lines:
        print("Failed to create neutral input!")
        return
    
    # Write neutral input
    neutral_path = 'examples/pcap/decoded/dummy_neutral_comprehensive.ndjson'
    with open(neutral_path, 'w', encoding='utf-8') as f:
        for line in neutral_lines:
            f.write(line + '\n')
    
    print(f"Created neutral input: {neutral_path} ({len(neutral_lines)} lines)")
    
    # Try to run Go baseline
    print("Running Go baseline parser...")
    success = run_go_baseline(neutral_lines, go_output_path)
    
    if success:
        # Compare results
        print("Comparing parser results...")
        comparison_results = compare_parsers(rust_ndjson_path, go_output_path, target_messages)
        
        # Save comparison results
        with open('examples/pcap/decoded/comparison_comprehensive.json', 'w') as f:
            json.dump(comparison_results, f, indent=2)
        
        print("\nComparison Summary:")
        print(f"Rust messages: {comparison_results['total_rust_messages']}")
        print(f"Go messages: {comparison_results['total_go_messages']}")
        print(f"Exact matches: {comparison_results['summary']['exact_matches']}")
        print(f"Field differences: {comparison_results['summary']['field_differences']}")
        print(f"Go failed, Rust succeeded: {comparison_results['summary']['go_failed_rust_succeeded']}")
        print(f"Rust failed, Go succeeded: {comparison_results['summary']['rust_failed_go_succeeded']}")
        
        # Calculate parsing parity percentage
        if comparison_results['total_rust_messages'] > 0:
            exact_matches = comparison_results['summary']['exact_matches']
            parity_percent = (exact_matches / comparison_results['total_rust_messages']) * 100
            print(f"Parsing parity: {parity_percent:.1f}%")
    else:
        print("Go baseline failed. Generating summary with Rust results only...")
        
        # Generate summary with Rust results
        summary = {
            'note': 'Go baseline failed to run',
            'total_rust_messages': len(rust_lines),
            'target_messages': target_messages,
            'parsing_sample': rust_lines[:10]  # First 10 for inspection
        }
        
        with open('examples/pcap/decoded/comparison_comprehensive.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Generated summary with {len(rust_lines)} Rust target messages")

if __name__ == '__main__':
    main()