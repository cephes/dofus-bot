#!/usr/bin/env python3
"""
Go vs Rust Parsed Output Diff Tool

Compares parsed outputs from Rust and Go parsers to identify discrepancies.
Generates both machine-readable and human-readable reports.
"""

import argparse
import json
import sys
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import re
from datetime import datetime


class DiffResult:
    """Represents the result of comparing two parsed messages."""
    
    def __init__(self):
        self.frame_index: int = 0
        self.message_name: str = ""
        self.verdict: str = "unknown"  # match, mismatch, missing_go, missing_rust
        self.rust_parsed: Any = None
        self.go_parsed: Any = None
        self.rust_error: Optional[str] = None
        self.go_error: Optional[str] = None
        self.differences: List[str] = []
        self.similarity_score: float = 0.0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "frame_index": self.frame_index,
            "message_name": self.message_name,
            "verdict": self.verdict,
            "rust_parsed": self.rust_parsed,
            "go_parsed": self.go_parsed,
            "rust_error": self.rust_error,
            "go_error": self.go_error,
            "differences": self.differences,
            "similarity_score": self.similarity_score
        }


def normalize_value(value: Any) -> Any:
    """Normalize values for comparison (e.g., convert strings to ints when possible)."""
    if isinstance(value, str):
        # Try to convert strings that look like numbers
        if re.match(r'^-?\d+$', value):
            try:
                return int(value)
            except ValueError:
                pass
        elif re.match(r'^-?\d+\.\d+$', value):
            try:
                return float(value)
            except ValueError:
                pass
        # Convert empty strings to None for comparison
        if value == "":
            return None
    elif isinstance(value, dict):
        # Remove empty values from dictionaries for comparison
        return {k: normalize_value(v) for k, v in value.items() if v not in [None, "", 0, [], {}]}
    elif isinstance(value, list):
        # Normalize list elements
        return [normalize_value(item) for item in value]
    
    return value


def deep_compare(rust_val: Any, go_val: Any, path: str = "") -> Tuple[bool, List[str]]:
    """
    Deep comparison of two values, returning (is_equal, list_of_differences).
    """
    differences = []
    
    # Normalize both values
    rust_val = normalize_value(rust_val)
    go_val = normalize_value(go_val)
    
    # Handle None/empty cases
    if rust_val in [None, "", 0, [], {}] and go_val in [None, "", 0, [], {}]:
        return True, differences
    
    if rust_val is None and go_val is not None:
        differences.append(f"{path}: Rust has None/empty, Go has {go_val}")
        return False, differences
    
    if go_val is None and rust_val is not None:
        differences.append(f"{path}: Go has None/empty, Rust has {rust_val}")
        return False, differences
    
    # Type comparison
    if type(rust_val) != type(go_val):
        differences.append(f"{path}: Type mismatch - Rust: {type(rust_val).__name__}, Go: {type(go_val).__name__}")
        return False, differences
    
    # Handle different types
    if isinstance(rust_val, dict):
        # Compare dictionaries
        rust_keys = set(rust_val.keys())
        go_keys = set(go_val.keys())
        
        # Check for missing keys
        for key in rust_keys - go_keys:
            if rust_val[key] not in [None, "", 0, [], {}]:
                differences.append(f"{path}.{key}: Missing in Go (Rust value: {rust_val[key]})")
        
        for key in go_keys - rust_keys:
            if go_val[key] not in [None, "", 0, [], {}]:
                differences.append(f"{path}.{key}: Missing in Rust (Go value: {go_val[key]})")
        
        # Compare common keys
        for key in rust_keys & go_keys:
            equal, key_diff = deep_compare(rust_val[key], go_val[key], f"{path}.{key}")
            if not equal:
                differences.extend(key_diff)
        
        return len(differences) == 0, differences
    
    elif isinstance(rust_val, list):
        # Compare lists
        if len(rust_val) != len(go_val):
            differences.append(f"{path}: List length mismatch - Rust: {len(rust_val)}, Go: {len(go_val)}")
            return False, differences
        
        for i, (rust_item, go_item) in enumerate(zip(rust_val, go_val)):
            equal, item_diff = deep_compare(rust_item, go_item, f"{path}[{i}]")
            if not equal:
                differences.extend(item_diff)
        
        return len(differences) == 0, differences
    
    else:
        # Primitive type comparison
        if rust_val != go_val:
            differences.append(f"{path}: Value mismatch - Rust: {rust_val}, Go: {go_val}")
            return False, differences
        
        return True, differences


def calculate_similarity(rust_val: Any, go_val: Any) -> float:
    """Calculate similarity score between two values (0.0 to 1.0)."""
    try:
        equal, differences = deep_compare(rust_val, go_val)
        if equal:
            return 1.0
        
        # Simple heuristic: fewer differences = higher similarity
        # This is a basic implementation - could be improved
        if isinstance(rust_val, dict) and isinstance(go_val, dict):
            total_keys = len(set(rust_val.keys()) | set(go_val.keys()))
            if total_keys == 0:
                return 1.0
            return max(0.0, 1.0 - len(differences) / total_keys)
        elif isinstance(rust_val, list) and isinstance(go_val, list):
            total_items = max(len(rust_val), len(go_val))
            if total_items == 0:
                return 1.0
            return max(0.0, 1.0 - len(differences) / total_items)
        else:
            return 0.0 if differences else 1.0
    except Exception:
        return 0.0


def load_ndjson_file(file_path: str) -> List[Dict[str, Any]]:
    """Load NDJSON file and return list of parsed JSON objects."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [json.loads(line.strip()) for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []


def align_messages(rust_data: List[Dict[str, Any]], go_data: List[Dict[str, Any]]) -> List[DiffResult]:
    """Align messages by frame_index and message_name, then compare."""
    
    # Create lookup maps
    rust_map: Dict[Tuple[int, str], Dict[str, Any]] = {}
    go_map: Dict[Tuple[int, str], Dict[str, Any]] = {}
    
    for entry in rust_data:
        key = (entry.get('frame_index', 0), entry.get('message_name', ''))
        rust_map[key] = entry
    
    for entry in go_data:
        key = (entry.get('frame_index', 0), entry.get('message_name', ''))
        go_map[key] = entry
    
    # Get all unique keys
    all_keys = set(rust_map.keys()) | set(go_map.keys())
    
    results = []
    
    for frame_idx, message_name in sorted(all_keys):
        result = DiffResult()
        result.frame_index = frame_idx
        result.message_name = message_name
        
        rust_entry = rust_map.get((frame_idx, message_name))
        go_entry = go_map.get((frame_idx, message_name))
        
        if rust_entry and go_entry:
            # Both present - compare parsed content
            result.rust_parsed = rust_entry.get('parsed')
            result.go_parsed = go_entry.get('go_parsed')
            result.rust_error = rust_entry.get('parse_error')
            result.go_error = go_entry.get('parse_error')
            
            if result.rust_error and result.go_error:
                # Both have errors - consider as match
                result.verdict = "match"
            elif result.rust_error and not result.go_error:
                result.verdict = "mismatch"
                result.differences.append("Rust parse failed, Go parse succeeded")
            elif not result.rust_error and result.go_error:
                result.verdict = "mismatch"
                result.differences.append("Go parse failed, Rust parse succeeded")
            elif not result.rust_error and not result.go_error:
                # Both parsed successfully - deep compare
                equal, differences = deep_compare(result.rust_parsed, result.go_parsed)
                result.differences = differences
                result.verdict = "match" if equal else "mismatch"
                result.similarity_score = calculate_similarity(result.rust_parsed, result.go_parsed)
            else:
                result.verdict = "unknown"
        
        elif rust_entry and not go_entry:
            # Only in Rust
            result.rust_parsed = rust_entry.get('parsed')
            result.rust_error = rust_entry.get('parse_error')
            result.verdict = "missing_go"
            result.differences.append("Message present in Rust data but missing in Go data")
        
        elif go_entry and not rust_entry:
            # Only in Go
            result.go_parsed = go_entry.get('go_parsed')
            result.go_error = go_entry.get('parse_error')
            result.verdict = "missing_rust"
            result.differences.append("Message present in Go data but missing in Rust data")
        
        results.append(result)
    
    return results


def generate_machine_readable_report(results: List[DiffResult], output_file: str):
    """Generate machine-readable JSON report."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total": len(results),
            "matches": sum(1 for r in results if r.verdict == "match"),
            "mismatches": sum(1 for r in results if r.verdict == "mismatch"),
            "missing_go": sum(1 for r in results if r.verdict == "missing_go"),
            "missing_rust": sum(1 for r in results if r.verdict == "missing_rust"),
            "unknown": sum(1 for r in results if r.verdict == "unknown")
        },
        "results": [result.to_dict() for result in results]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
# DEMO_DISABLED:         json.dump(report, f, indent=2)
    
    print(f"Machine-readable report written to: {output_file}")


def generate_human_readable_report(results: List[DiffResult], output_file: str):
    """Generate human-readable Markdown report."""
    
    # Calculate statistics
    total = len(results)
    matches = sum(1 for r in results if r.verdict == "match")
    mismatches = sum(1 for r in results if r.verdict == "mismatch")
    missing_go = sum(1 for r in results if r.verdict == "missing_go")
    missing_rust = sum(1 for r in results if r.verdict == "missing_rust")
    
    # Group mismatches by message type for analysis
    mismatches_by_message: Dict[str, List[DiffResult]] = {}
    for result in results:
        if result.verdict == "mismatch":
            if result.message_name not in mismatches_by_message:
                mismatches_by_message[result.message_name] = []
            mismatches_by_message[result.message_name].append(result)
    
    # Field-level statistics
    field_stats: Dict[str, Dict[str, int]] = {}
    for result in results:
        if result.verdict == "mismatch" and result.differences:
            for diff in result.differences:
                # Extract field name from difference message
                field_match = re.search(r'\.([a-zA-Z_][a-zA-Z0-9_]*)(?::|\[)', diff)
                if field_match:
                    field_name = field_match.group(1)
                    if field_name not in field_stats:
                        field_stats[field_name] = {"total": 0, "missing_rust": 0, "missing_go": 0, "type_mismatch": 0, "value_mismatch": 0}
                    
                    field_stats[field_name]["total"] += 1
                    if "Missing in Go" in diff:
                        field_stats[field_name]["missing_go"] += 1
                    elif "Missing in Rust" in diff:
                        field_stats[field_name]["missing_rust"] += 1
                    elif "Type mismatch" in diff:
                        field_stats[field_name]["type_mismatch"] += 1
                    else:
                        field_stats[field_name]["value_mismatch"] += 1
    
    # Start writing the report
    lines = [
        "# Go vs Rust Parsed Output Comparison Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total Messages:** {total}",
        "",
        "## Summary",
        "",
        "| Verdict | Count | Percentage |",
        "|---------|-------|------------|",
        f"| ✅ Match | {matches} | {matches/total*100:.1f}% |",
        f"| ❌ Mismatch | {mismatches} | {mismatches/total*100:.1f}% |",
        f"| 🔸 Missing in Go | {missing_go} | {missing_go/total*100:.1f}% |",
        f"| 🔹 Missing in Rust | {missing_rust} | {missing_rust/total*100:.1f}% |",
        "",
    ]
    
    if mismatches_by_message:
        lines.extend([
            "## Mismatches by Message Type",
            "",
            "| Message Type | Count | Examples |",
            "|--------------|-------|----------|",
        ])
        
        # Sort by count descending
        sorted_messages = sorted(mismatches_by_message.items(), key=lambda x: len(x[1]), reverse=True)
        
        for message_name, message_results in sorted_messages[:20]:  # Top 20
            count = len(message_results)
            examples = []
            for result in message_results[:3]:  # First 3 examples
                if result.differences:
                    examples.append(f"Frame {result.frame_index}: {result.differences[0]}")
            
            examples_str = "<br>".join(examples) if examples else "No differences shown"
            lines.append(f"| {message_name} | {count} | {examples_str} |")
        
        if len(sorted_messages) > 20:
            lines.append(f"| ... | ... | ... |")
        
        lines.append("")
    
    if field_stats:
        lines.extend([
            "## Field-Level Analysis",
            "",
            "| Field | Total Issues | Missing in Go | Missing in Rust | Type Mismatch | Value Mismatch |",
            "|-------|--------------|---------------|-----------------|---------------|----------------|",
        ])
        
        # Sort by total issues descending
        sorted_fields = sorted(field_stats.items(), key=lambda x: x[1]["total"], reverse=True)
        
        for field_name, stats in sorted_fields[:20]:  # Top 20 fields
            lines.append(f"| {field_name} | {stats['total']} | {stats['missing_go']} | {stats['missing_rust']} | {stats['type_mismatch']} | {stats['value_mismatch']} |")
        
        if len(sorted_fields) > 20:
            lines.append("| ... | ... | ... | ... | ... | ... |")
        
        lines.append("")
    
    # Top mismatches with examples
    mismatch_examples = [r for r in results if r.verdict == "mismatch"][:50]  # Top 50 mismatches
    
    if mismatch_examples:
        lines.extend([
            "## Top Mismatch Examples",
            "",
            "### Detailed Comparison",
            "",
        ])
        
        for i, result in enumerate(mismatch_examples, 1):
            lines.extend([
                f"#### {i}. {result.message_name} (Frame {result.frame_index})",
                "",
                f"**Verdict:** {result.verdict}",
                f"**Similarity Score:** {result.similarity_score:.2f}",
                "",
                "**Rust Parsed:**",
                "```json",
# DEMO_DISABLED:                 json.dumps(result.rust_parsed, indent=2) if result.rust_parsed else "null",
                "```",
                "",
                "**Go Parsed:**",
                "```json",
# DEMO_DISABLED:                 json.dumps(result.go_parsed, indent=2) if result.go_parsed else "null",
                "```",
                "",
                "**Differences:**",
            ])
            
            if result.differences:
                for diff in result.differences:
                    lines.append(f"- {diff}")
            else:
                lines.append("- No specific differences detailed")
            
            lines.append("")
    
    # Summary recommendations
    if mismatches > 0:
        lines.extend([
            "## Recommendations",
            "",
            "### Focus Areas for Rust Parser Improvements",
            "",
        ])
        
        if field_stats:
            # Top problematic fields
            top_fields = sorted(field_stats.items(), key=lambda x: x[1]["total"], reverse=True)[:5]
            lines.append("**Most Problematic Fields:**")
            for field_name, stats in top_fields:
                lines.append(f"- `{field_name}`: {stats['total']} issues ({stats['value_mismatch']} value mismatches, {stats['type_mismatch']} type mismatches)")
            lines.append("")
        
        if mismatches_by_message:
            # Top problematic message types
            top_messages = sorted(mismatches_by_message.items(), key=lambda x: len(x[1]), reverse=True)[:5]
            lines.append("**Most Problematic Message Types:**")
            for message_name, message_results in top_messages:
                lines.append(f"- `{message_name}`: {len(message_results)} mismatches")
            lines.append("")
        
        lines.extend([
            "### Action Items",
            "",
            "1. **Field-level analysis**: Focus on the most frequently problematic fields",
            "2. **Message-type specific fixes**: Address message types with highest mismatch rates",
            "3. **Type consistency**: Ensure Rust types match Go types for the same fields",
            "4. **Validation rules**: Review parsing logic for fields with frequent mismatches",
            "",
        ])
    else:
        lines.extend([
            "## ✅ Perfect Match!",
            "",
            "All parsed messages match between Rust and Go implementations. No issues found.",
            "",
        ])
    
    # Write the report
    with open(output_file, 'w', encoding='utf-8') as f:
# DEMO_DISABLED:         f.write('\n'.join(lines))
    
    print(f"Human-readable report written to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Compare Rust and Go parsed message outputs")
    parser.add_argument("--rust", required=True, help="Rust parsed NDJSON file")
    parser.add_argument("--go", required=True, help="Go parsed NDJSON file")
    parser.add_argument("--json-out", default="go_rust_diff.json", help="Output JSON report file")
    parser.add_argument("--md-out", default="GO_RUST_DIFF.md", help="Output Markdown report file")
    
    args = parser.parse_args()
    
    print("Loading files...")
    rust_data = load_ndjson_file(args.rust)
    go_data = load_ndjson_file(args.go)
    
    print(f"Loaded {len(rust_data)} Rust messages and {len(go_data)} Go messages")
    
    if not rust_data or not go_data:
        print("Error: Could not load input files")
        sys.exit(1)
    
    print("Aligning and comparing messages...")
    results = align_messages(rust_data, go_data)
    
    print(f"Generated {len(results)} comparison results")
    
    # Generate reports
    print("Generating reports...")
    generate_machine_readable_report(results, args.json_out)
    generate_human_readable_report(results, args.md_out)
    
    # Print summary
    total = len(results)
    matches = sum(1 for r in results if r.verdict == "match")
    mismatches = sum(1 for r in results if r.verdict == "mismatch")
    missing_go = sum(1 for r in results if r.verdict == "missing_go")
    missing_rust = sum(1 for r in results if r.verdict == "missing_rust")
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Total messages: {total}")
    print(f"[OK] Matches: {matches} ({matches/total*100:.1f}%)")
    print(f"[ERROR] Mismatches: {mismatches} ({mismatches/total*100:.1f}%)")
    print(f"[WARNING] Missing in Go: {missing_go} ({missing_go/total*100:.1f}%)")
    print(f"[WARNING] Missing in Rust: {missing_rust} ({missing_rust/total*100:.1f}%)")
    print("="*50)
    
    if mismatches > 0:
        print(f"\n[WARNING] Found {mismatches} mismatches - see {args.md_out} for details")
        sys.exit(1)
    else:
        print(f"\n[OK] All messages match! Perfect parity achieved.")
        sys.exit(0)


if __name__ == "__main__":
    main()