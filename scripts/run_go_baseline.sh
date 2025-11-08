#!/usr/bin/env bash
#
# SYNOPSIS
#     Run the Go baseline parser and diff tool pipeline
#
# DESCRIPTION
#     This script orchestrates the complete Go baseline pipeline:
#     1. Checks for Go installation
#     2. Generates the Go parser registry
#     3. Builds the Go binary
#     4. Runs the Go parser on sample data
#     5. Compares Go vs Rust outputs
#     6. Generates reports
#

set -e  # Exit on any error

# Get script directory and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Output directories
BIN_DIR="$REPO_ROOT/bin"
EXAMPLES_DIR="$REPO_ROOT/examples"
GO_BASELINE_DIR="$REPO_ROOT/tools/go_baseline"

# Input files
RUST_INPUT="$EXAMPLES_DIR/pcap/decoded/dummy_parsed_new.ndjson"
GO_OUTPUT_NDJSON="$EXAMPLES_DIR/pcap/decoded/dummy_go.ndjson"
GO_OUTPUT_JSON="$EXAMPLES_DIR/pcap/decoded/dummy_go.json"
DIFF_JSON_OUTPUT="$REPO_ROOT/go_rust_diff.json"
DIFF_MD_OUTPUT="$REPO_ROOT/GO_RUST_DIFF.md"

# Go binary path
GO_BINARY="$BIN_DIR/retroproto_go_baseline"

echo "========================================"
echo "Go Baseline Parser Pipeline"
echo "========================================"
echo

# Step 1: Check for Go installation
echo "Step 1: Checking Go installation..." >&2
if ! command -v go &> /dev/null; then
    echo "❌ Go not found or not in PATH" >&2
    echo
    echo "To install Go:" >&2
    echo "1. Download from https://golang.org/dl/" >&2
    echo "2. Install and add to PATH" >&2
    echo "3. Restart your terminal" >&2
    echo
    echo "The Go baseline tools have been created but cannot be run without Go." >&2
    echo "You can run the pipeline manually after installing Go." >&2
    exit 0
fi

GO_VERSION=$(go version)
echo "✅ Go found: $GO_VERSION" >&2

# Step 2: Ensure bin directory exists
if [ ! -d "$BIN_DIR" ]; then
    echo "Creating bin directory: $BIN_DIR" >&2
    mkdir -p "$BIN_DIR"
fi

# Step 3: Generate Go registry
echo
echo "Step 2: Generating Go parser registry..." >&2
cd "$GO_BASELINE_DIR"
if ! python gen_go_registry.py --out registry.go; then
    echo "❌ Registry generation failed" >&2
    exit 1
fi
echo "✅ Registry generated successfully" >&2

# Step 4: Build Go binary
echo
echo "Step 3: Building Go binary..." >&2
cd "$GO_BASELINE_DIR"
if ! go build -o "$GO_BINARY"; then
    echo "❌ Go build failed" >&2
    exit 1
fi
echo "✅ Go binary built successfully: $GO_BINARY" >&2

# Check if input file exists
if [ ! -f "$RUST_INPUT" ]; then
    echo "❌ Input file not found: $RUST_INPUT" >&2
    echo "Make sure you have run the Rust parser first to generate this file." >&2
    exit 1
fi

# Step 5: Run Go parser
echo
echo "Step 4: Running Go parser..." >&2
echo "Input: $RUST_INPUT" >&2
echo "Output NDJSON: $GO_OUTPUT_NDJSON" >&2
echo "Output JSON: $GO_OUTPUT_JSON" >&2
echo

if ! "$GO_BINARY" --in "$RUST_INPUT" --out-ndjson "$GO_OUTPUT_NDJSON" --out-json "$GO_OUTPUT_JSON"; then
    echo "❌ Go parser failed" >&2
    exit 1
fi
echo "✅ Go parsing completed" >&2

# Step 6: Run diff tool
echo
echo "Step 5: Running diff tool..." >&2
echo "Rust input: $RUST_INPUT" >&2
echo "Go input: $GO_OUTPUT_NDJSON" >&2
echo

if ! python tools/diff_go_rust_parsed.py --rust "$RUST_INPUT" --go "$GO_OUTPUT_NDJSON" --json-out "$DIFF_JSON_OUTPUT" --md-out "$DIFF_MD_OUTPUT"; then
    DIFF_EXIT_CODE=1
else
    DIFF_EXIT_CODE=0
fi

echo
echo "========================================"
echo "Pipeline Summary"
echo "========================================"

# Parse the diff results for summary
if [ -f "$DIFF_JSON_OUTPUT" ]; then
    if command -v jq &> /dev/null; then
        TOTAL=$(jq '.summary.total' "$DIFF_JSON_OUTPUT")
        MATCHES=$(jq '.summary.matches' "$DIFF_JSON_OUTPUT")
        MISMATCHES=$(jq '.summary.mismatches' "$DIFF_JSON_OUTPUT")
        MISSING_GO=$(jq '.summary.missing_go' "$DIFF_JSON_OUTPUT")
        MISSING_RUST=$(jq '.summary.missing_rust' "$DIFF_JSON_OUTPUT")
        
        # Calculate percentages
        MATCHES_PCT=$(awk "BEGIN {printf \"%.1f\", ($MATCHES/$TOTAL)*100}")
        MISMATCHES_PCT=$(awk "BEGIN {printf \"%.1f\", ($MISMATCHES/$TOTAL)*100}")
        MISSING_GO_PCT=$(awk "BEGIN {printf \"%.1f\", ($MISSING_GO/$TOTAL)*100}")
        MISSING_RUST_PCT=$(awk "BEGIN {printf \"%.1f\", ($MISSING_RUST/$TOTAL)*100}")
        
        echo "Total messages processed: $TOTAL"
        echo "✅ Matches: $MATCHES ($MATCHES_PCT%)"
        echo "❌ Mismatches: $MISMATCHES ($MISMATCHES_PCT%)"
        echo "🔸 Missing in Go: $MISSING_GO ($MISSING_GO_PCT%)"
        echo "🔹 Missing in Rust: $MISSING_RUST ($MISSING_RUST_PCT%)"
    else
        echo "Could not parse diff summary (jq not found)"
    fi
fi

echo
echo "Generated files:"
echo "  📄 Go output (NDJSON): $GO_OUTPUT_NDJSON"
echo "  📄 Go output (JSON): $GO_OUTPUT_JSON"
echo "  📊 Diff report (JSON): $DIFF_JSON_OUTPUT"
echo "  📋 Diff report (Markdown): $DIFF_MD_OUTPUT"

if [ -f "$DIFF_MD_OUTPUT" ]; then
    echo "  📖 Human-readable report: $DIFF_MD_OUTPUT"
fi

echo
if [ $DIFF_EXIT_CODE -eq 0 ]; then
    echo "🎉 Perfect match! All parsers agree."
else
    echo "⚠️  Differences found between Rust and Go parsers."
    echo "   See $DIFF_MD_OUTPUT for detailed analysis."
fi

echo
echo "========================================"

exit $DIFF_EXIT_CODE