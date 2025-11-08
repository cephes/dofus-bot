#!/usr/bin/env python3
"""
Auto-refine Rust parsers from Go baseline comparison.
"""
import argparse
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Add parent directory to path for utils import
sys.path.append(str(Path(__file__).parent.parent))
from parity.utils import (
    ts, ensure_dirs, read_jsonl, read_json, write_json, write_text,
    list_parser_file, snake_case, rust_type_for_json, 
    patch_struct_fields, patch_parse_body_csv, patch_parse_body_json_passthrough,
    rewrite_mod_rs_if_needed
)


def load_diff_data(diff_path: str) -> dict:
    """Load and process diff data."""
    diff_data = read_json(diff_path)
    if not diff_data or 'results' not in diff_data:
        return {'results': []}
    return diff_data


def compute_message_priorities(diff_data: dict) -> list:
    """Compute priority list of messages by mismatch count."""
    message_counts = Counter()
    
    for result in diff_data.get('results', []):
        if result.get('verdict') == 'mismatch':
            message_name = result.get('message_name')
            if message_name:
                message_counts[message_name] += 1
    
    # Return sorted by count (highest first)
    return message_counts.most_common()


def sample_message_data(go_data: list, rs_data: list, message_name: str, max_samples: int = 20) -> tuple:
    """Sample Go and Rust data for a specific message."""
    go_samples = []
    rs_samples = []
    
    # Sample Go data
    for item in go_data:
        if item.get('message_name') == message_name and item.get('go_parsed'):
            if isinstance(item['go_parsed'], dict):
                go_samples.append(item['go_parsed'])
                if len(go_samples) >= max_samples:
                    break
    
    # Sample Rust data
    for item in rs_data:
        if item.get('message_name') == message_name and item.get('parsed'):
            if isinstance(item['parsed'], dict):
                rs_samples.append(item['parsed'])
                if len(rs_samples) >= max_samples:
                    break
    
    return go_samples, rs_samples


def infer_field_schema(go_samples: list) -> list:
    """Infer field schema from Go samples."""
    if not go_samples:
        return []
    
    # Collect all field names and their types across samples
    field_types = defaultdict(list)
    
    for sample in go_samples:
        if isinstance(sample, dict):
            for key, value in sample.items():
                if not key.startswith('_'):  # Skip internal fields
                    field_types[key].append(value)
    
    # Determine most common field order and types
    field_order = []
    for field_name in go_samples[0].keys():
        if not field_name.startswith('_'):
            field_order.append(field_name)
    
    # Infer types (use widest safe type)
    field_schema = []
    for field_name in field_order:
        if field_name in field_types:
            values = field_types[field_name]
            # Use type of first non-null value
            non_null_values = [v for v in values if v is not None]
            if non_null_values:
                sample_value = non_null_values[0]
                rust_type = rust_type_for_json(sample_value)
                field_schema.append((field_name, rust_type))
    
    return field_schema


def detect_csv_parsing(rs_samples: list, message_name: str) -> bool:
    """Detect if message uses CSV-style parsing."""
    if not rs_samples:
        return False
    
    # Check if Rust data has 'extra_preview' with semicolons
    for sample in rs_samples:
        extra_preview = sample.get('extra_preview') or sample.get('payload')
        if extra_preview and isinstance(extra_preview, str):
            if ';' in extra_preview:
                return True
    
    return False


def patch_parser_file(file_path: str, field_schema: list, is_csv: bool, dry_run: bool = False) -> bool:
    """Patch a parser file with new field schema."""
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Extract field names for parsing
        field_names = [name for name, _ in field_schema]
        
        if is_csv:
            # Use CSV parsing
            content = patch_struct_fields(content, field_schema)
            content = patch_parse_body_csv(content, field_names)
        else:
            # Use JSON passthrough or conservative approach
            content = patch_struct_fields(content, field_schema)
            content = patch_parse_body_json_passthrough(content, dict(field_schema))
        
        if content != original_content:
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            return True
        
    except Exception as e:
        print(f"Error patching {file_path}: {e}")
    
    return False


def regenerate_registry(core_path: str) -> bool:
    """Regenerate the parser registry."""
    try:
        result = subprocess.run([
            sys.executable, 'tools/gen_parser_registry.py'
        ], cwd=os.getcwd(), capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error regenerating registry: {e}")
        return False


def build_core(core_path: str) -> bool:
    """Build the core crate."""
    try:
        result = subprocess.run([
            'cargo', 'build', '--release'
        ], cwd=core_path, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error building core: {e}")
        return False


def run_pipeline() -> bool:
    """Run the Rust parsing pipeline."""
    try:
        result = subprocess.run([
            sys.executable, 'scripts/run_dummy_parsing.ps1'
        ], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running pipeline: {e}")
        return False


def run_go_baseline() -> bool:
    """Run the Go baseline."""
    try:
        result = subprocess.run([
            'powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', 
            '-File', 'scripts/run_go_baseline.ps1'
        ], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running Go baseline: {e}")
        return False


def run_diff(go_path: str, rs_path: str, diff_path: str) -> bool:
    """Run the diff comparison."""
    try:
        result = subprocess.run([
            sys.executable, 'tools/diff_go_rust_parsed.py',
            '--go', go_path,
            '--rs', rs_path,
            '--json-out', diff_path
        ], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running diff: {e}")
        return False


def write_iteration_summary(out_dir: str, patched_files: list, before_stats: dict, after_stats: dict) -> None:
    """Write iteration summary."""
    summary = {
        'timestamp': ts(),
        'patched_files': patched_files,
        'before': before_stats,
        'after': after_stats,
        'improvement': {
            'mismatch_count': before_stats.get('mismatches', 0) - after_stats.get('mismatches', 0),
            'mismatch_rate_change': before_stats.get('mismatch_rate', 1.0) - after_stats.get('mismatch_rate', 1.0)
        }
    }
    
    write_json(f"{out_dir}/summary.json", summary)
    write_text(f"{out_dir}/summary.txt", json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Auto-refine Rust parsers from Go baseline")
    parser.add_argument('--go', required=True, help='Path to Go NDJSON file')
    parser.add_argument('--rs', required=True, help='Path to Rust NDJSON file')
    parser.add_argument('--diff', required=True, help='Path to diff JSON file')
    parser.add_argument('--core', default='core', help='Path to core crate')
    parser.add_argument('--out', required=True, help='Output directory for iteration')
    parser.add_argument('--max-files', type=int, default=50, help='Max files to patch per run')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without modifying files')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    ensure_dirs([args.out])
    
    print(f"Auto-refine starting at {ts()}")
    print(f"Output directory: {args.out}")
    print(f"Dry run: {args.dry_run}")
    
    # Load data
    print("Loading diff data...")
    diff_data = load_diff_data(args.diff)
    go_data = read_jsonl(args.go)
    rs_data = read_jsonl(args.rs)
    
    print(f"Loaded {len(diff_data.get('results', []))} diff results")
    print(f"Loaded {len(go_data)} Go samples")
    print(f"Loaded {len(rs_data)} Rust samples")
    
    # Compute priorities
    priorities = compute_message_priorities(diff_data)
    print(f"Found {len(priorities)} messages with mismatches")
    
    # Process top priorities
    patched_files = []
    max_files = min(args.max_files, len(priorities))
    
    for i, (message_name, count) in enumerate(priorities[:max_files]):
        print(f"\nProcessing {message_name} (mismatches: {count}) [{i+1}/{max_files}]")
        
        # Get file path
        file_path = list_parser_file(message_name, args.core)
        if not os.path.exists(file_path):
            print(f"  Skipping: parser file not found at {file_path}")
            continue
        
        # Sample data
        go_samples, rs_samples = sample_message_data(go_data, rs_data, message_name)
        print(f"  Found {len(go_samples)} Go samples, {len(rs_samples)} Rust samples")
        
        if not go_samples:
            print(f"  Skipping: no Go samples found")
            continue
        
        # Infer schema
        field_schema = infer_field_schema(go_samples)
        print(f"  Inferred {len(field_schema)} fields: {[(n, t) for n, t in field_schema[:5]]}{'...' if len(field_schema) > 5 else ''}")
        
        # Detect parsing style
        is_csv = detect_csv_parsing(rs_samples, message_name)
        print(f"  Detected parsing style: {'CSV' if is_csv else 'JSON/Conservative'}")
        
        # Patch file
        if patch_parser_file(file_path, field_schema, is_csv, args.dry_run):
            patched_files.append(file_path)
            print(f"  {'[DRY RUN] ' if args.dry_run else ''}Patched {file_path}")
        else:
            print(f"  No changes needed for {file_path}")
    
    print(f"\nProcessed {len(patched_files)} files")
    
    # Calculate before stats
    before_stats = {
        'total': diff_data.get('total', 0),
        'matches': diff_data.get('matches', 0),
        'mismatches': diff_data.get('mismatches', 0),
        'missing_in_go': diff_data.get('missing_in_go', 0),
        'missing_in_rust': diff_data.get('missing_in_rust', 0),
        'mismatch_rate': diff_data.get('mismatch_rate', 1.0)
    }
    
    if args.dry_run:
        print("\n[Dry run] Skipping rebuild and re-diff")
        after_stats = before_stats
    else:
        print("\nRegenerating registry...")
        if not regenerate_registry(args.core):
            print("WARNING: Registry regeneration failed")
        
        print("Building core...")
        if not build_core(args.core):
            print("ERROR: Core build failed")
            return 1
        
        print("Running pipeline...")
        if not run_pipeline():
            print("WARNING: Pipeline execution failed")
        
        print("Running Go baseline...")
        if not run_go_baseline():
            print("WARNING: Go baseline execution failed")
        
        print("Running diff...")
        if not run_diff(args.go, args.rs, args.diff):
            print("ERROR: Diff execution failed")
            return 1
        
        # Load after stats
        after_diff_data = load_diff_data(args.diff)
        after_stats = {
            'total': after_diff_data.get('total', 0),
            'matches': after_diff_data.get('matches', 0),
            'mismatches': after_diff_data.get('mismatches', 0),
            'missing_in_go': after_diff_data.get('missing_in_go', 0),
            'missing_in_rust': after_diff_data.get('missing_in_rust', 0),
            'mismatch_rate': after_diff_data.get('mismatch_rate', 1.0)
        }
    
    # Write summary
    write_iteration_summary(args.out, patched_files, before_stats, after_stats)
    
    print(f"\nSummary:")
    print(f"  Before: {before_stats['mismatches']}/{before_stats['total']} mismatches ({before_stats['mismatch_rate']:.1%})")
    print(f"  After:  {after_stats['mismatches']}/{after_stats['total']} mismatches ({after_stats['mismatch_rate']:.1%})")
    print(f"  Improvement: {before_stats['mismatches'] - after_stats['mismatches']} mismatches")
    print(f"  Patched files: {len(patched_files)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())