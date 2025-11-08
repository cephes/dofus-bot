#!/usr/bin/env python3
"""
Summarize diff results for progress tracking.
"""
import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# Add parent directory to path for utils import
sys.path.append(str(Path(__file__).parent.parent))
from parity.utils import read_json, write_json, write_text, ts


def summarize_diff(diff_path: str) -> dict:
    """Read and summarize diff data."""
    diff_data = read_json(diff_path)
    if not diff_data:
        return {
            'total': 0,
            'matches': 0,
            'mismatches': 0,
            'missing_in_go': 0,
            'missing_in_rust': 0,
            'mismatch_rate': 1.0,
            'top_mismatch_messages': [],
            'timestamp': ts()
        }
    
    # Extract results
    results = diff_data.get('results', [])
    
    # Count by verdict
    stats = Counter()
    message_counts = Counter()
    
    for result in results:
        verdict = result.get('verdict', 'unknown')
        message_name = result.get('message_name', 'unknown')
        stats[verdict] += 1
        if verdict == 'mismatch':
            message_counts[message_name] += 1
    
    # Create top mismatch messages list
    top_mismatches = [
        {'name': name, 'count': count} 
        for name, count in message_counts.most_common(10)
    ]
    
    total = len(results)
    mismatch_rate = stats['mismatch'] / total if total > 0 else 1.0
    
    return {
        'total': total,
        'matches': stats['match'],
        'mismatches': stats['mismatch'],
        'missing_in_go': stats['missing_go'],
        'missing_in_rust': stats['missing_rust'],
        'mismatch_rate': mismatch_rate,
        'top_mismatch_messages': top_mismatches,
        'timestamp': ts()
    }


def format_human_summary(summary: dict) -> str:
    """Format summary for human reading."""
    lines = []
    lines.append(f"DIFF SUMMARY - {summary['timestamp']}")
    lines.append("=" * 50)
    lines.append(f"Total messages: {summary['total']}")
    lines.append(f"✅ Matches: {summary['matches']} ({summary['matches']/summary['total']*100:.1f}%)")
    lines.append(f"❌ Mismatches: {summary['mismatches']} ({summary['mismatch_rate']*100:.1f}%)")
    lines.append(f"🔸 Missing in Go: {summary['missing_in_go']}")
    lines.append(f"🔹 Missing in Rust: {summary['missing_in_rust']}")
    lines.append("")
    
    if summary['top_mismatch_messages']:
        lines.append("Top mismatched message types:")
        for item in summary['top_mismatch_messages']:
            lines.append(f"  • {item['name']}: {item['count']} mismatches")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Summarize diff results")
    parser.add_argument('--diff', required=True, help='Path to diff JSON file')
    parser.add_argument('--out-json', help='Output path for JSON summary')
    parser.add_argument('--out-md', help='Output path for markdown summary')
    
    args = parser.parse_args()
    
    # Generate summary
    summary = summarize_diff(args.diff)
    
    # Output JSON summary
    if args.out_json:
        write_json(args.out_json, summary)
    
    # Output markdown summary
    if args.out_md:
        human_summary = format_human_summary(summary)
        write_text(args.out_md, human_summary)
    
    # Always print to stdout as well
    human_summary = format_human_summary(summary)
    print(human_summary)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())