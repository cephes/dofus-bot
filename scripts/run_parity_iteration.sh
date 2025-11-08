#!/bin/bash
# Bash script to run parity iteration

set -e  # Exit on any error

# Parse arguments
MAX_ITERS=5
TARGET_MISMATCH_RATE=5
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --max-iters)
            MAX_ITERS="$2"
            shift 2
            ;;
        --target)
            TARGET_MISMATCH_RATE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Get timestamp for this iteration
ts=$(date +%Y%m%d_%H%M%S)
echo "=== PARITY ITERATION $ts ==="

# Setup directories
iteration_dir=".parity/iter_$ts"
backup_dir=".archive/PARITY_$ts"
mkdir -p "$iteration_dir"
mkdir -p ".archive"
mkdir -p ".parity"

# Check if we have initial data
has_initial_data=false
# DEMO_DISABLED: if [[ -f "examples/pcap/decoded/dummy_parsed_new.ndjson" && -f "examples/pcap/decoded/dummy_go.ndjson" ]]; then
    has_initial_data=true
fi

if [[ "$has_initial_data" == false ]]; then
    echo "Initial data not found. Running initial pipeline..."
    
    # Run initial pipeline
    echo "Running Rust pipeline..."
    python scripts/run_dummy_parsing.ps1 || { echo "ERROR: Rust pipeline failed"; exit 1; }
    
    echo "Running Go baseline..."
    bash scripts/run_go_baseline.sh || { echo "ERROR: Go baseline failed"; exit 1; }
    
    echo "Running initial diff..."
# DEMO_DISABLED:     python tools/diff_go_rust_parsed.py --rust examples/pcap/decoded/dummy_parsed_new.ndjson --go examples/pcap/decoded/dummy_go.ndjson --json-out go_rust_diff.json --md-out GO_RUST_DIFF.md || { echo "ERROR: Initial diff failed"; exit 1; }
fi

# Take before snapshot
echo "Taking before snapshot..."
cp "go_rust_diff.json" "$iteration_dir/before.json"

# Create backup
echo "Creating backup..."
if [[ -d "core/src/retroproto_parsers/generated" ]]; then
    if [[ -d "$backup_dir" ]]; then
        rm -rf "$backup_dir"
    fi
    cp -r "core/src/retroproto_parsers/generated" "$backup_dir"
fi

# Run auto-refinement
echo "Running auto-refinement..."
refine_args=(
# DEMO_DISABLED:     "--go" "examples/pcap/decoded/dummy_go.ndjson"
# DEMO_DISABLED:     "--rs" "examples/pcap/decoded/dummy_parsed_new.ndjson"
    "--diff" "go_rust_diff.json"
    "--core" "core"
    "--out" "$iteration_dir"
    "--max-files" "50"
)

if [[ "$DRY_RUN" == true ]]; then
    refine_args+=("--dry-run")
fi

python tools/parity/auto_refine_from_go.py "${refine_args[@]}" || echo "WARNING: Auto-refinement had issues but continuing..."

# Re-run full pipeline
echo "Re-running pipeline after refinement..."

echo "  Regenerating registry..."
python tools/gen_parser_registry.py || echo "WARNING: Registry regeneration failed"

echo "  Building core..."
cd core
cargo build --release || { echo "ERROR: Core build failed"; exit 1; }
cd ..

echo "  Running Rust pipeline..."
python scripts/run_dummy_parsing.ps1 || echo "WARNING: Rust pipeline failed"

echo "  Running Go baseline..."
bash scripts/run_go_baseline.sh || echo "WARNING: Go baseline failed"

echo "  Running diff..."
# DEMO_DISABLED: python tools/diff_go_rust_parsed.py --rust examples/pcap/decoded/dummy_parsed_new.ndjson --go examples/pcap/decoded/dummy_go.ndjson --json-out go_rust_diff.json --md-out GO_RUST_DIFF.md || { echo "ERROR: Diff failed"; exit 1; }

# Take after snapshot
echo "Taking after snapshot..."
cp "go_rust_diff.json" "$iteration_dir/after.json"

# Generate summary
echo "Generating summary..."
python tools/parity/summarize_diff.py --diff "go_rust_diff.json" --out-json "$iteration_dir/summary.json" --out-md "$iteration_dir/summary.txt"

# Load before/after for comparison using Python
before_data=$(python3 -c "
import json
with open('$iteration_dir/before.json', 'r') as f:
    data = json.load(f)
print(f\"{data['total']},{data['mismatches']}\")
")

after_data=$(python3 -c "
import json
with open('$iteration_dir/after.json', 'r') as f:
    data = json.load(f)
print(f\"{data['total']},{data['mismatches']}\")
")

IFS=',' read -r before_total before_mismatches <<< "$before_data"
IFS=',' read -r after_total after_mismatches <<< "$after_data"

before_mismatch_rate=$(python3 -c "print(f'{( $before_mismatches / $before_total * 100 ):.2f}')")
after_mismatch_rate=$(python3 -c "print(f'{( $after_mismatches / $after_total * 100 ):.2f}')")
improvement=$((before_mismatches - after_mismatches))

# Append to progress log
cat >> PARITY_PROGRESS.md << EOF

### Iteration $ts
- **Before:** ${before_mismatch_rate}% mismatches ($before_mismatches/$before_total)
- **After:** ${after_mismatch_rate}% mismatches ($after_mismatches/$after_total)  
- **Improvement:** $improvement mismatches
- **Patched files:** See iteration summary
- **Top issues:** See iteration details

EOF

# Write detailed summary to iteration directory
python3 << EOF
import json

iteration_summary = {
    "timestamp": "$ts",
    "before": {
        "total": $before_total,
        "mismatches": $before_mismatches,
        "mismatch_rate": float($before_mismatch_rate)
    },
    "after": {
        "total": $after_total,
        "mismatches": $after_mismatches,
        "mismatch_rate": float($after_mismatch_rate)
    },
    "improvement": {
        "mismatch_count": $improvement,
        "mismatch_rate_change": float($before_mismatch_rate) - float($after_mismatch_rate)
    }
}

with open("$iteration_dir/summary.json", "w") as f:
# DEMO_DISABLED:     json.dump(iteration_summary, f, indent=2)
EOF

# Check stop conditions
converged=false
no_improvement=false
max_iters_reached=false

if (( $(echo "$after_mismatch_rate <= $TARGET_MISMATCH_RATE" | bc -l) )); then
    converged=true
    echo "**STATUS: CONVERGED** - Mismatch rate ($after_mismatch_rate%) ≤ target ($TARGET_MISMATCH_RATE%)" >> PARITY_PROGRESS.md
elif [[ $improvement -le 0 ]]; then
    no_improvement=true  
    echo "**STATUS: NO IMPROVEMENT** - No net gain in mismatches" >> PARITY_PROGRESS.md
elif [[ $MAX_ITERS -eq 1 ]]; then
    max_iters_reached=true
    echo "**STATUS: MAX ITERS REACHED** - Completed $MAX_ITERS iterations" >> PARITY_PROGRESS.md
fi

# Final output
echo
echo "=== ITERATION COMPLETE ==="
echo "Before: ${before_mismatch_rate}% mismatches ($before_mismatches/$before_total)"
echo "After:  ${after_mismatch_rate}% mismatches ($after_mismatches/$after_total)"
echo "Improvement: $improvement mismatches"

if [[ "$converged" == true ]]; then
    echo
    echo "🎉 CONVERGED! Target mismatch rate achieved."
    exit 0
elif [[ "$no_improvement" == true ]]; then
    echo
    echo "⚠️  NO IMPROVEMENT - Stopping iteration."
    exit 0
elif [[ "$max_iters_reached" == true ]]; then
    echo
    echo "⏹️  MAX ITERS REACHED - Stopping iteration."
    exit 0
else
    echo
    echo "➡️  Continue to next iteration."
    exit 0
fi