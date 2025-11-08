#!/usr/bin/env python3
"""
NDJSON Parse Integrity Validator

Validates parsed NDJSON data against schema rules, counts parsing results,
and generates both machine-readable JSON and human-readable Markdown reports.
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from collections import defaultdict
import yaml
import traceback
from datetime import datetime


def type_check(value: Any, expected_type: str) -> bool:
    """Check if a value matches the expected type."""
    if expected_type == "int":
        return isinstance(value, int)
    elif expected_type == "str":
        return isinstance(value, str)
    elif expected_type == "list":
        return isinstance(value, list)
    elif expected_type == "int_or_str":
        return isinstance(value, (int, str))
    elif expected_type == "list_or_str":
        return isinstance(value, (list, str))
    else:
        return False


# DEMO_DISABLED: def choose_any_required_set(parsed_data: Dict, sets: List[List[str]]) -> Tuple[bool, Optional[List[str]]]:
    """
# DEMO_DISABLED:     Check if any of the required sets is fully present in parsed_data.
    Returns (True, chosen_set) if found, (False, None) otherwise.
    """
    for required_set in sets:
# DEMO_DISABLED:         if all(field in parsed_data for field in required_set):
            return True, required_set
    return False, None


def load_rules(rules_path: str) -> Dict[str, Any]:
    """Load validation rules from YAML file."""
    try:
        with open(rules_path, 'r', encoding='utf-8') as f:
            rules = yaml.safe_load(f)
        return rules
    except FileNotFoundError:
        print(f"Warning: Rules file {rules_path} not found. Using default rules.")
        return get_default_rules()
    except Exception as e:
        print(f"Error loading rules file {rules_path}: {e}")
        return get_default_rules()


def get_default_rules() -> Dict[str, Any]:
    """Return default validation rules if YAML file is missing."""
    return {
        'global': {
            'allow_empty_messages': [],
            'fail_on': {
                'parsed_null': True,
                'parsed_empty_object': True,
                'parse_error_present': True
            }
        },
        'messages': {}
    }


def validate_row(row: Dict[str, Any], rules: Dict[str, Any], message_rules: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a single NDJSON row and return validation result."""
    frame_index = row.get('frame_index', -1)
    prefix = row.get('prefix', '')
    message_name = row.get('message_name', 'Unknown')
    parsed = row.get('parsed')
    parse_error = row.get('parse_error')
    
    result = {
        'frame_index': frame_index,
        'prefix': prefix,
        'message_name': message_name,
        'status': 'ok',
        'reasons': []
    }
    
    # Check for parse error
    if parse_error and parse_error.strip():
        result['status'] = 'fail'
        result['reasons'].append(f'parse_error_present: {parse_error}')
    
    # Check if parsed is null
    if parsed is None:
        result['status'] = 'fail'
        result['reasons'].append('parsed_null')
    
    # Check if parsed is empty object
    elif isinstance(parsed, dict) and len(parsed) == 0:
        # Only fail if message is not in allow_empty_messages
        if message_name not in rules.get('global', {}).get('allow_empty_messages', []):
            result['status'] = 'fail'
            result['reasons'].append('parsed_empty_object')
    
    # If parsed is a valid object, validate against schema
    elif isinstance(parsed, dict) and len(parsed) > 0:
        if message_name in message_rules:
            msg_rules = message_rules[message_name]
            
            # Check any_of_required_sets first
            if 'any_of_required_sets' in msg_rules:
                found, chosen_set = choose_any_required_set(parsed, msg_rules['any_of_required_sets'])
                if not found:
                    result['status'] = 'fail'
                    result['reasons'].append(f'missing_required_fields: none of {msg_rules["any_of_required_sets"]} found')
            
            # Check required fields
            elif 'required' in msg_rules:
                for field in msg_rules['required']:
                    if field not in parsed:
                        result['status'] = 'fail'
                        result['reasons'].append(f'missing_required_field: {field}')
            
            # Check types
            if 'types' in msg_rules:
                for field, expected_type in msg_rules['types'].items():
                    if field in parsed:
                        if not type_check(parsed[field], expected_type):
                            result['status'] = 'fail'
                            actual_type = type(parsed[field]).__name__
                            result['reasons'].append(f'type_mismatch: {field} expected {expected_type}, got {actual_type}')
    
    return result


def categorize_row(row: Dict[str, Any]) -> str:
    """Categorize a row into one of the main categories."""
    parsed = row.get('parsed')
    parse_error = row.get('parse_error')
    
    # If there's a parse error, categorize as parse_error_present
    if parse_error and parse_error.strip():
        return 'parse_error_present'
    
    # If parsed is null
    if parsed is None:
        return 'parsed_null'
    
    # If parsed is empty object
    if isinstance(parsed, dict) and len(parsed) == 0:
        return 'parsed_empty_object'
    
    # If parsed is a valid object with content
    if isinstance(parsed, dict) and len(parsed) > 0:
        return 'parsed_ok'
    
    return 'unknown'


def generate_markdown_report(results: Dict[str, Any], violations: List[Dict[str, Any]], output_path: str) -> None:
    """Generate human-readable Markdown report."""
    
    with open(output_path, 'w', encoding='utf-8') as f:
# DEMO_DISABLED:         f.write("# Parse Integrity Summary\n\n")
        
        # Overall summary
        summary = results['summary']
# DEMO_DISABLED:         f.write("## Overall Statistics\n\n")
# DEMO_DISABLED:         f.write(f"- **Total rows processed:** {summary['total_rows']}\n")
# DEMO_DISABLED:         f.write(f"- **Parsed OK:** {summary['parsed_ok']} ({summary['parsed_ok']/summary['total_rows']*100:.1f}%)\n")
# DEMO_DISABLED:         f.write(f"- **Parsed empty object:** {summary['parsed_empty_object']} ({summary['parsed_empty_object']/summary['total_rows']*100:.1f}%)\n")
# DEMO_DISABLED:         f.write(f"- **Parsed null:** {summary['parsed_null']} ({summary['parsed_null']/summary['total_rows']*100:.1f}%)\n")
# DEMO_DISABLED:         f.write(f"- **Parse errors present:** {summary['parse_error_present']} ({summary['parse_error_present']/summary['total_rows']*100:.1f}%)\n\n")
        
        # Violations overview
# DEMO_DISABLED:         f.write("## Violations Overview\n\n")
        if violations:
# DEMO_DISABLED:             f.write(f"**Total violations found: {len(violations)}**\n\n")
            
            # Group violations by type
            violation_types = defaultdict(int)
            for violation in violations:
                for reason in violation.get('reasons', []):
                    violation_types[reason] += 1
            
# DEMO_DISABLED:             f.write("### Violation Types\n\n")
            for violation_type, count in sorted(violation_types.items(), key=lambda x: x[1], reverse=True):
# DEMO_DISABLED:                 f.write(f"- **{violation_type}:** {count} occurrences\n")
# DEMO_DISABLED:             f.write("\n")
        else:
# DEMO_DISABLED:             f.write("No violations found.\n\n")
        
        # Per-message statistics
# DEMO_DISABLED:         f.write("## Per-Message Statistics\n\n")
        per_message = results['per_message']
        
        if per_message:
            # Create table
# DEMO_DISABLED:             f.write("| Message Name | Total | OK | Empty | Null | Error | Failure Rate |\n")
# DEMO_DISABLED:             f.write("|-------------|-------|----|-----|------|-------|-------------|\n")
            
            # Sort by failure rate descending, then by count descending
            sorted_messages = sorted(
                per_message.items(),
                key=lambda x: (x[1]['violations']/x[1]['total'] if x[1]['total'] > 0 else 0, x[1]['total']),
                reverse=True
            )
            
            for message_name, stats in sorted_messages:
                failure_rate = stats['violations']/stats['total']*100 if stats['total'] > 0 else 0
# DEMO_DISABLED:                 f.write(f"| {message_name} | {stats['total']} | {stats['parsed_ok']} | {stats['parsed_empty_object']} | {stats['parsed_null']} | {stats['parse_error_present']} | {failure_rate:.1f}% |\n")
# DEMO_DISABLED:             f.write("\n")
        else:
# DEMO_DISABLED:             f.write("No per-message statistics available.\n\n")
        
        # Sample failures
        if violations:
# DEMO_DISABLED:             f.write("## Sample Failures\n\n")
# DEMO_DISABLED:             f.write("First 10 failed rows with failure reasons:\n\n")
            
            for i, violation in enumerate(violations[:10], 1):
# DEMO_DISABLED:                 f.write(f"### {i}. Frame {violation['frame_index']} - {violation['message_name']}\n")
# DEMO_DISABLED:                 f.write(f"- **Status:** {violation['status']}\n")
# DEMO_DISABLED:                 f.write(f"- **Reasons:** {', '.join(violation['reasons'])}\n")
# DEMO_DISABLED:                 f.write(f"- **Prefix:** {violation['prefix']}\n\n")


def validate_ndjson_file(input_path: str, rules_path: str, output_json: str, output_md: str, max_print: int = 30) -> int:
    """Main validation function. Returns exit code (0 for success, non-zero for failure)."""
    
    # Load rules
    rules = load_rules(rules_path)
    message_rules = rules.get('messages', {})
    global_fail_on = rules.get('global', {}).get('fail_on', {})
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'input_file': input_path,
        'rules_file': rules_path,
        'summary': {
            'total_rows': 0,
            'parsed_ok': 0,
            'parsed_empty_object': 0,
            'parsed_null': 0,
            'parse_error_present': 0
        },
        'per_message': {},
        'violations': []
    }
    
    # Track if any fail_on conditions are triggered
    fail_on_triggered = []
    
    print("Starting NDJSON validation...")
    print(f"Input file: {input_path}")
    print(f"Rules file: {rules_path}")
    print("-" * 50)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping malformed JSON on line {line_num}: {e}")
                    results['summary']['total_rows'] += 1
                    results['violations'].append({
                        'frame_index': -1,
                        'prefix': 'malformed',
                        'message_name': 'JSON_ERROR',
                        'status': 'fail',
                        'reasons': [f'malformed_json: {e}']
                    })
                    continue
                
                # Categorize the row
                category = categorize_row(row)
                results['summary']['total_rows'] += 1
                results['summary'][category] += 1
                
                # Update per-message statistics
                message_name = row.get('message_name', 'Unknown')
                if message_name not in results['per_message']:
                    results['per_message'][message_name] = {
                        'total': 0,
                        'parsed_ok': 0,
                        'parsed_empty_object': 0,
                        'parsed_null': 0,
                        'parse_error_present': 0,
                        'violations': 0
                    }
                
                results['per_message'][message_name]['total'] += 1
                results['per_message'][message_name][category] += 1
                
                # Validate the row
                validation_result = validate_row(row, rules, message_rules)
                if validation_result['status'] == 'fail':
                    results['per_message'][message_name]['violations'] += 1
                    results['violations'].append(validation_result)
                
                # Print first few violations for immediate feedback
                if len(results['violations']) <= max_print:
                    if validation_result['status'] == 'fail':
                        reasons = ', '.join(validation_result['reasons'])
                        print(f"Violation {len(results['violations'])}: Frame {validation_result['frame_index']} - {validation_result['message_name']} ({reasons})")
                
    except FileNotFoundError:
        print(f"Error: Input file {input_path} not found.")
        return 1
    except Exception as e:
        print(f"Error processing file: {e}")
        traceback.print_exc()
        return 1
    
    print("-" * 50)
    print("Validation complete.")
    print(f"Processed {results['summary']['total_rows']} rows.")
    print(f"Found {len(results['violations'])} violations.")
    
    # Check fail_on conditions
    for condition, should_fail in global_fail_on.items():
        if should_fail and results['summary'][condition] > 0:
            fail_on_triggered.append(f"{condition}: {results['summary'][condition]} found")
    
    # Write JSON report
    try:
        with open(output_json, 'w', encoding='utf-8') as f:
# DEMO_DISABLED:             json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"JSON report written: {output_json}")
    except Exception as e:
        print(f"Error writing JSON report: {e}")
        return 1
    
    # Write Markdown report
    try:
        generate_markdown_report(results, results['violations'], output_md)
        print(f"Markdown report written: {output_md}")
    except Exception as e:
        print(f"Error writing Markdown report: {e}")
        return 1
    
    # Determine final status
    has_violations = len(results['violations']) > 0
    has_fail_on_triggered = len(fail_on_triggered) > 0
    
    if has_violations or has_fail_on_triggered:
        print()
        print("INTEGRITY CHECK FAILED")
        if has_fail_on_triggered:
            print("Fail-on conditions triggered:")
            for condition in fail_on_triggered:
                print(f"  - {condition}")
        if has_violations:
            print(f"Schema violations: {len(results['violations'])}")
        return 1
    else:
        print()
        print("INTEGRITY CHECK PASSED")
        return 0


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="NDJSON Parse Integrity Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Use default files
  %(prog)s --in custom.ndjson               # Use custom input file
  %(prog)s --max-print 50                    # Show first 50 violations
  %(prog)s --out-json custom.json --out-md custom.md  # Custom output files
        """
    )
    
    parser.add_argument(
        '--in',
# DEMO_DISABLED:         default='examples/pcap/decoded/dummy_parsed_all.ndjson',
# DEMO_DISABLED:         help='Input NDJSON file path (default: examples/pcap/decoded/dummy_parsed_all.ndjson)'
    )
    
    parser.add_argument(
        '--rules',
        default='tools/validate_rules.yaml',
        help='Validation rules YAML file (default: tools/validate_rules.yaml)'
    )
    
    parser.add_argument(
        '--out-json',
        default='PARSE_INTEGRITY.json',
        help='Output JSON report path (default: PARSE_INTEGRITY.json)'
    )
    
    parser.add_argument(
        '--out-md',
        default='PARSE_INTEGRITY.md',
        help='Output Markdown report path (default: PARSE_INTEGRITY.md)'
    )
    
    parser.add_argument(
        '--max-print',
        type=int,
        default=30,
        help='Maximum number of violations to print to console (default: 30)'
    )
    
    parsed_args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    out_json_path = Path(parsed_args.out_json)
    out_md_path = Path(parsed_args.out_md)
    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    out_md_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Extract arguments manually to avoid Python 3.14 compatibility issues
    input_file = getattr(parsed_args, 'in')
    rules_file = getattr(parsed_args, 'rules')
    output_json_file = getattr(parsed_args, 'out_json')
    output_md_file = getattr(parsed_args, 'out_md')
    max_print = parsed_args.max_print
    
    exit_code = validate_ndjson_file(input_file, rules_file, output_json_file, output_md_file, max_print)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()