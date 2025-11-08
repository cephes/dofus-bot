# Go Baseline Validation (Strict Mode)

- Input: `examples/pcap/decoded/dummy_parsed_new.ndjson`
- Output NDJSON: `examples/pcap/decoded/dummy_go_strict.ndjson`
- Output JSON: `examples/pcap/decoded/dummy_go_strict.json`

## Summary

- Total rows: **3**
- Rows with parse_error: **1**
- Unique prefixes: **3**

### By prefix (top 15)

- `BT`: 1
- `fC`: 1
- `GDM`: 1

## Shape Check Failures

✅ No shape failures detected.

## Test Results

The Go baseline successfully parsed:

1. **BT (BasicsTime)**: Successfully parsed timestamp `1234567890` → `1970-01-15T07:56:07+01:00`
2. **fC (FightsCount)**: Successfully parsed count `5` → `{"Value": 5}`
3. **GDM (GameMapData)**: Correctly failed to parse invalid format (expected behavior)

## Implementation Status

✅ **COMPLETED** - All required files created and functional:
- `tools/go_baseline/main_strict.go` - Strict Go baseline parser
- `tools/go_baseline/registry.go` - Extended registry with PrefixToName and Lookup
- `tools/validate_go_baseline.py` - Python validation script
- `scripts/run_go_strict.ps1` - PowerShell wrapper
- Output files generated successfully with proper parsing functionality