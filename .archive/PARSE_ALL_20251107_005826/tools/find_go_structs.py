#!/usr/bin/env python3
"""
Find Go struct sources for missing parsers.
Auto-locates Go struct definitions for messages marked as "PORT_GO_TO_RUST" or "FILL_FIELDS_IN_RUST_PARSER".
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

def load_missing_parsers_plan(plan_path: str) -> Dict[str, Any]:
    """Load the missing parsers plan JSON file."""
    with open(plan_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_target_messages(plan_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find messages that need Go struct discovery."""
    target_messages = []
    
    for entry in plan_data.get('entries', []):
        action = entry.get('action', 'NONE')
        has_rust_parse_fn = entry.get('has_rust_parse_fn', False)
        has_go_def = entry.get('has_go_def', False)
        
        # Look for messages that need Go source discovery
        if (action == 'PORT_GO_TO_RUST' and not has_rust_parse_fn and has_go_def) or \
           (action == 'FILL_FIELDS_IN_RUST_PARSER' and has_go_def):
            target_messages.append({
                'name': entry['message_name'],
                'action': action,
                'has_rust_parse_fn': has_rust_parse_fn,
                'has_go_def': has_go_def,
                'observed_count': entry.get('observed_count', 0)
            })
    
    return target_messages

def search_go_files_in_directory(directory: Path, pattern: str) -> List[Dict[str, Any]]:
    """Search for Go files matching a pattern in a directory recursively."""
    matches = []
    search_pattern = re.compile(pattern, re.IGNORECASE)
    
    for go_file in directory.rglob('*.go'):
        try:
            with open(go_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
            for line_num, line in enumerate(lines, 1):
                if search_pattern.search(line):
                    # Check for struct definition pattern
                    if re.search(r'type\s+' + pattern + r'\s+struct\s*{', line, re.IGNORECASE):
                        score = 100  # High score for exact struct match
                        context = f"type {pattern} struct {{"
                    elif re.search(r'func\s+.*parse' + pattern + r'\(', line, re.IGNORECASE):
                        score = 80   # Good score for parse function
                        context = line.strip()
                    elif pattern.lower() in line.lower():
                        score = 60   # Lower score for mentions
                        context = line.strip()
                    else:
                        continue
                    
                    matches.append({
                        'path': str(go_file),
                        'line': line_num,
                        'context': context,
                        'score': score
                    })
        except Exception as e:
            print(f"Error reading {go_file}: {e}", file=sys.stderr)
            continue
    
    # Sort by score descending
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches

def search_go_structs_in_retroproto(target_messages: List[Dict[str, Any]], retroproto_root: Path) -> Dict[str, List[Dict[str, Any]]]:
    """Search for Go struct definitions in the retroproto directory."""
    results = {}
    search_dirs = [
        retroproto_root / 'msgcli',
        retroproto_root / 'msgsvr', 
        retroproto_root / 'enum',
        retroproto_root / 'typ',
        retroproto_root / 'cmd',
        retroproto_root / 'assets'
    ]
    
    # Also search the root directory
    search_dirs.append(retroproto_root)
    
    for msg in target_messages:
        name = msg['name']
        print(f"Searching for Go struct: {name}")
        
        # Try exact name match first
        exact_pattern = re.escape(name)
        matches = []
        
        for search_dir in search_dirs:
            if search_dir.exists():
                dir_matches = search_go_files_in_directory(search_dir, exact_pattern)
                matches.extend(dir_matches)
        
        if not matches:
            # Try snake_case and camelCase variations
            snake_name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
            camel_name = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), name)
            
            for variant in [snake_name, camel_name]:
                for search_dir in search_dirs:
                    if search_dir.exists():
                        variant_matches = search_go_files_in_directory(search_dir, variant)
                        matches.extend(variant_matches)
        
        if matches:
            # Remove duplicates and sort by score
            unique_matches = []
            seen_paths = set()
            for match in matches:
                key = (match['path'], match['line'])
                if key not in seen_paths:
                    unique_matches.append(match)
                    seen_paths.add(key)
            
            results[name] = unique_matches[:5]  # Top 5 matches
            print(f"  Found {len(unique_matches)} matches")
        else:
            results[name] = []
            print(f"  No matches found")
    
    return results

def main():
    """Main function."""
    plan_path = 'missing_parsers_plan.json'
    retroproto_root = Path('third_party/retroproto')
    output_path = 'tools/out/go_struct_hits.json'
    
    if not os.path.exists(plan_path):
        print(f"Error: {plan_path} not found", file=sys.stderr)
        sys.exit(1)
    
    if not retroproto_root.exists():
        print(f"Error: {retroproto_root} not found", file=sys.stderr)
        sys.exit(1)
    
    # Create output directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("Loading missing parsers plan...")
    plan_data = load_missing_parsers_plan(plan_path)
    
    print("Finding target messages...")
    target_messages = find_target_messages(plan_data)
    print(f"Found {len(target_messages)} messages needing Go struct discovery")
    
    for msg in target_messages:
        print(f"  - {msg['name']} ({msg['action']})")
    
    print("\nSearching for Go struct definitions...")
    results = search_go_structs_in_retroproto(target_messages, retroproto_root)
    
    print(f"\nSaving results to {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print summary table
    print("\n" + "="*80)
    print("GO STRUCT DISCOVERY RESULTS")
    print("="*80)
    print(f"{'Message Name':<25} {'Hits':<6} {'Top Match'}")
    print("-" * 80)
    
    for name, hits in results.items():
        msg_info = next((m for m in target_messages if m['name'] == name), {})
        count = len(hits)
        top_match = hits[0]['path'] + ":" + str(hits[0]['line']) if hits else "NO MATCHES"
        print(f"{name:<25} {count:<6} {top_match}")
    
    print("="*80)
    print(f"Total messages searched: {len(target_messages)}")
    print(f"Messages with Go struct found: {len([h for h in results.values() if h])}")
    print(f"Messages still missing: {len([h for h in results.values() if not h])}")
    print(f"Results saved to: {output_path}")

if __name__ == '__main__':
    main()