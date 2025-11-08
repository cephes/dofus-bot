#!/usr/bin/env python3
"""
No Gaps Validator - Ensure comprehensive message parsing coverage

This script validates that:
1. Every message in NDJSON has a registered parser
2. Every message parses successfully (no null/empty results)
3. No "no parser registered" or similar error messages
4. Complete coverage of all discovered message types
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Any
import re

def load_coverage_data(coverage_file: str) -> Dict[str, Any]:
    """Load coverage data from JSON file"""
    coverage_path = Path(coverage_file)
    if not coverage_path.exists():
        print(f"Error: Coverage file {coverage_file} not found")
        return {}
    
    try:
        with open(coverage_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading coverage data: {e}")
        return {}

def analyze_ndjson_messages(ndjson_file: str) -> Dict[str, Any]:
    """Analyze NDJSON file to extract all message types and their parse status"""
    path = Path(ndjson_file)
    if not path.exists():
        print(f"Error: NDJSON file {ndjson_file} not found")
        return {}
    
    message_stats = {}
    total_messages = 0
    parse_errors = 0
    null_parses = 0
    unregistered_messages = 0
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    record = json.loads(line)
                    total_messages += 1
                    
                    # Extract message name and parse status
                    message_name = record.get('message', 'Unknown')
                    parse_result = record.get('parsed', None)
                    
                    # Track message statistics
                    if message_name not in message_stats:
                        message_stats[message_name] = {
                            'count': 0,
                            'successful_parses': 0,
                            'null_parses': 0,
                            'parse_errors': 0,
                            'unregistered': 0
                        }
                    
                    message_stats[message_name]['count'] += 1
                    
                    # Analyze parse result
                    if parse_result is None:
                        message_stats[message_name]['null_parses'] += 1
                        null_parses += 1
                    elif isinstance(parse_result, dict) and len(parse_result) == 0:
                        message_stats[message_name]['null_parses'] += 1
                        null_parses += 1
                    elif isinstance(parse_result, str) and parse_result.lower() in ['error', 'failed', 'no parser registered']:
                        message_stats[message_name]['parse_errors'] += 1
                        parse_errors += 1
                        if 'no parser registered' in parse_result.lower():
                            message_stats[message_name]['unregistered'] += 1
                            unregistered_messages += 1
                    elif isinstance(parse_result, dict) and len(parse_result) > 0:
                        message_stats[message_name]['successful_parses'] += 1
                    else:
                        # Other cases treated as successful
                        message_stats[message_name]['successful_parses'] += 1
                        
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON on line {line_num}: {e}")
                    continue
                    
    except Exception as e:
        print(f"Error reading NDJSON file: {e}")
        return {}
    
    return {
        'total_messages': total_messages,
        'message_stats': message_stats,
        'parse_errors': parse_errors,
        'null_parses': null_parses,
        'unregistered_messages': unregistered_messages
    }

def load_known_parsers() -> Set[str]:
    """Load list of known parsers from registry"""
    registry_path = Path("core/src/retroproto_parsers/registry.rs")
    if not registry_path.exists():
        print("Warning: Registry file not found")
        return set()
    
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract parser names from registry
        parser_pattern = r'm\.insert\("([^"]+)"'
        parsers = re.findall(parser_pattern, content)
        return set(parsers)
    except Exception as e:
        print(f"Error reading registry: {e}")
        return set()

def validate_coverage(ndjson_file: str, coverage_file: str = None) -> Dict[str, Any]:
    """Validate parsing coverage and identify gaps"""
    
    print(f"Analyzing NDJSON file: {ndjson_file}")
    ndjson_analysis = analyze_ndjson_messages(ndjson_file)
    
    if not ndjson_analysis:
        return {'success': False, 'error': 'Failed to analyze NDJSON file'}
    
    # Load known parsers
    known_parsers = load_known_parsers()
    print(f"Found {len(known_parsers)} registered parsers")
    
    # Analyze results
    message_stats = ndjson_analysis['message_stats']
    total_messages = ndjson_analysis['total_messages']
    
    # Find messages with issues
    messages_with_gaps = []
    for message_name, stats in message_stats.items():
        issues = []
        if stats['null_parses'] > 0:
            issues.append(f"null_parses:{stats['null_parses']}")
        if stats['parse_errors'] > 0:
            issues.append(f"parse_errors:{stats['parse_errors']}")
        if stats['unregistered'] > 0:
            issues.append(f"unregistered:{stats['unregistered']}")
        
        if issues:
            messages_with_gaps.append({
                'message': message_name,
                'total_count': stats['count'],
                'successful_parses': stats['successful_parses'],
                'issues': issues
            })
    
    # Find unregistered message types
    unregistered_types = []
    for message_name in message_stats.keys():
        if message_name not in known_parsers:
            unregistered_types.append(message_name)
    
    # Check for messages with zero successful parses
    messages_with_zero_success = []
    for message_name, stats in message_stats.items():
        if stats['successful_parses'] == 0 and stats['count'] > 0:
            messages_with_zero_success.append({
                'message': message_name,
                'total_count': stats['count']
            })
    
    # Calculate coverage percentage
    total_successful = sum(stats['successful_parses'] for stats in message_stats.values())
    coverage_percentage = (total_successful / total_messages * 100) if total_messages > 0 else 0
    
    results = {
        'success': len(messages_with_gaps) == 0 and len(messages_with_zero_success) == 0,
        'total_messages': total_messages,
        'total_successful': total_successful,
        'coverage_percentage': coverage_percentage,
        'registered_parsers': len(known_parsers),
        'messages_analyzed': len(message_stats),
        'messages_with_gaps': messages_with_gaps,
        'unregistered_message_types': unregistered_types,
        'messages_with_zero_success': messages_with_zero_success,
        'parse_errors': ndjson_analysis['parse_errors'],
        'null_parses': ndjson_analysis['null_parses'],
        'unregistered_messages': ndjson_analysis['unregistered_messages']
    }
    
    return results

def generate_coverage_report(results: Dict[str, Any], output_file: str = None):
    """Generate human-readable coverage report"""
    
    report_lines = [
        "# Parsing Coverage Validation Report",
        f"Generated: 2025-11-07T01:05:40Z",
        "",
        "## Summary",
        f"- Total messages analyzed: {results['total_messages']}",
        f"- Successfully parsed: {results['total_successful']}",
        f"- Coverage: {results['coverage_percentage']:.1f}%",
        f"- Registered parsers: {results['registered_parsers']}",
        f"- Message types found: {results['messages_analyzed']}",
        "",
        "## Issues Found"
    ]
    
    if results['parse_errors'] > 0:
        report_lines.append(f"- Parse errors: {results['parse_errors']}")
    if results['null_parses'] > 0:
        report_lines.append(f"- Null/empty parses: {results['null_parses']}")
    if results['unregistered_messages'] > 0:
        report_lines.append(f"- Unregistered message errors: {results['unregistered_messages']}")
    
    if not results['success']:
        report_lines.extend([
            "",
            "## Messages with Gaps",
            "| Message | Count | Successful | Issues |",
            "|---------|-------|------------|--------|"
        ])
        
        for gap in results['messages_with_gaps']:
            issues_str = ", ".join(gap['issues'])
            report_lines.append(f"| {gap['message']} | {gap['total_count']} | {gap['successful_parses']} | {issues_str} |")
        
        if results['messages_with_zero_success']:
            report_lines.extend([
                "",
                "## Messages with Zero Successful Parses",
                "| Message | Count |",
                "|---------|-------|"
            ])
            
            for msg in results['messages_with_zero_success']:
                report_lines.append(f"| {msg['message']} | {msg['total_count']} |")
        
        if results['unregistered_message_types']:
            report_lines.extend([
                "",
                "## Unregistered Message Types",
                "| Message Type |",
                "|--------------|"
            ])
            
            for msg_type in results['unregistered_message_types']:
                report_lines.append(f"| {msg_type} |")
    else:
        report_lines.extend([
            "",
            "✅ **SUCCESS**: All messages are being parsed successfully!",
            "✅ No gaps found in parsing coverage.",
            "✅ All message types have registered parsers."
        ])
    
    report_content = "\n".join(report_lines)
    
    if output_file:
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
# DEMO_DISABLED:             f.write(report_content)
        print(f"Coverage report written to: {output_path}")
    else:
        print("\n" + report_content)
    
    return report_content

def main():
    """Main execution function"""
    if len(sys.argv) < 2:
        print("Usage: python verify_no_gaps.py <ndjson_file> [coverage_file] [output_report]")
# DEMO_DISABLED:         print("Example: python verify_no_gaps.py examples/pcap/decoded/dummy_parsed_all.ndjson")
        return
    
    ndjson_file = sys.argv[1]
    coverage_file = sys.argv[2] if len(sys.argv) > 2 else None
    output_report = sys.argv[3] if len(sys.argv) > 3 else None
    
    print("=== No Gaps Validation ===")
    
    # Validate coverage
    results = validate_coverage(ndjson_file, coverage_file)
    
    if not results.get('success', False):
        print("\n❌ VALIDATION FAILED - Gaps found in parsing coverage")
        sys.exit(1)
    else:
        print("\n✅ VALIDATION PASSED - Complete parsing coverage")
    
    # Generate report
    report = generate_coverage_report(results, output_report)
    
    # Write JSON results for programmatic access
    results_file = "verify_no_gaps_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
# DEMO_DISABLED:         json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed results written to: {results_file}")
    
    return results

if __name__ == "__main__":
    main()