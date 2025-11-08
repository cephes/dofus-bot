#!/bin/bash
# Parse Integrity Check Shell Script
# Runs the NDJSON validator on the Dofus bot parsing output

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Default input file
INPUT_FILE="examples/pcap/decoded/dummy_parsed_all.ndjson"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -In|--in)
            INPUT_FILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--in <path>]"
            exit 1
            ;;
    esac
done

# Define paths
PYTHON_SCRIPT="tools/validate_parsed_integrity.py"
OUTPUT_JSON="PARSE_INTEGRITY.json"
OUTPUT_MD="PARSE_INTEGRITY.md"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file not found: $INPUT_FILE" >&2
    exit 1
fi

# Check if python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python script not found: $PYTHON_SCRIPT" >&2
    exit 1
fi

# Determine Python executable
PYTHON_EXE=""
if [ -f ".venv/bin/python" ]; then
    PYTHON_EXE=".venv/bin/python"
    echo "Using virtual environment Python: $PYTHON_EXE"
elif [ -f ".venv/Scripts/python.exe" ]; then
    PYTHON_EXE=".venv/Scripts/python.exe"
    echo "Using virtual environment Python: $PYTHON_EXE"
else
    # Try system python
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_EXE="python3"
        echo "Using system Python3: $PYTHON_EXE"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_EXE="python"
        echo "Using system Python: $PYTHON_EXE"
    else
        echo "Error: Python not found in PATH" >&2
        exit 1
    fi
fi

# Display what we're about to run
echo "=== Parse Integrity Check ===" >&2
echo "Input:    $INPUT_FILE" >&2
echo "Script:   $PYTHON_SCRIPT" >&2
echo "Output:   $OUTPUT_JSON, $OUTPUT_MD" >&2
echo "Python:   $PYTHON_EXE" >&2
echo "============================" >&2
echo "" >&2

# Run the validator
if $PYTHON_EXE "$PYTHON_SCRIPT" --in "$INPUT_FILE" --out-json "$OUTPUT_JSON" --out-md "$OUTPUT_MD"; then
    EXIT_CODE=0
else
    EXIT_CODE=$?
fi

echo "" >&2
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ PARSE INTEGRITY CHECK PASSED" >&2
else
    echo "❌ PARSE INTEGRITY CHECK FAILED (exit code: $EXIT_CODE)" >&2
fi

# Show output file locations
if [ -f "$OUTPUT_JSON" ]; then
    echo "📄 JSON report: $OUTPUT_JSON" >&2
fi
if [ -f "$OUTPUT_MD" ]; then
    echo "📄 Markdown report: $OUTPUT_MD" >&2
fi

exit $EXIT_CODE