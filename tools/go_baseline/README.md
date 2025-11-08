# Go Baseline Parser for Retroproto

This directory contains a Go-based reference decoder that can parse the same network protocol messages as the Rust parsers, allowing for comparison and validation of the parsing logic.

## Overview

The Go baseline parser consists of several components:

1. **gen_go_registry.py** - Scans the Go source files to build a registry of available parsers
2. **main.go** - CLI tool that reads NDJSON files and re-parses messages using the Go registry
3. **registry.go** - Generated Go file containing the parser registry
4. **go.mod** - Go module file with local dependency replacement

## Requirements

- **Go 1.19+** - The Go programming language and toolchain
- **Python 3.7+** - For running the registry generation script
- **Access to retroproto source** - Located in `../../third_party/retroproto`

### Installing Go

If Go is not installed on your system:

**Windows:**
1. Download from [golang.org/dl/](https://golang.org/dl/)
2. Run the installer
3. Add Go to your PATH if not done automatically

**macOS:**
```bash
# Using Homebrew
brew install go

# Or download from golang.org
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install golang-go

# Or download from golang.org
```

Verify installation:
```bash
go version
```

## Building and Running

### Quick Start

Run the provided scripts from the repository root:

**PowerShell (Windows):**
```powershell
.\scripts\run_go_baseline.ps1
```

**Bash (Linux/macOS):**
```bash
./scripts/run_go_baseline.sh
```

### Manual Build and Run

1. **Generate the parser registry:**
   ```bash
   cd tools/go_baseline
   python gen_go_registry.py --out registry.go
   ```

2. **Build the Go binary:**
   ```bash
   cd tools/go_baseline
   go build -o ../../bin/retroproto_go_baseline.exe
   ```

3. **Run the parser:**
   ```bash
   cd tools/go_baseline
   ../../bin/retroproto_go_baseline.exe \
     --in ../../examples/pcap/decoded/dummy_parsed_new.ndjson \
     --out-ndjson ../../examples/pcap/decoded/dummy_go.ndjson \
     --out-json ../../examples/pcap/decoded/dummy_go.json
   ```

## Usage

### Command Line Interface

```bash
retroproto_go_baseline --in <input.ndjson> --out-ndjson <output.ndjson> --out-json <output.json>
```

**Parameters:**
- `--in`: Input NDJSON file containing Rust-parsed messages
- `--out-ndjson`: Output NDJSON file for Go-parsed messages
- `--out-json`: Output JSON file for Go-parsed messages (pretty-printed array)

### Input Format

The input NDJSON should follow the format produced by the Rust parsers:

```json
{
  "frame_index": 0,
  "prefix": "GM",
  "message_name": "GameMovement",
  "parsed": {"sprites": "..."},
  "parse_error": null,
  "extra_preview": "..."
}
```

### Output Format

The Go parser outputs:

```json
{
  "frame_index": 0,
  "message_name": "GameMovement",
  "payload_raw": "...",
  "go_parsed": {...},
  "parse_error": null
}
```

**Fields:**
- `frame_index`: Frame number (0-based)
- `message_name`: Name of the message type
- `payload_raw`: Original raw payload string
- `go_parsed`: Parsed result from Go parser (if successful)
- `parse_error`: Error message if parsing failed (if any)

## Registry Generation

The `gen_go_registry.py` script automatically discovers parsers by:

1. Scanning `third_party/retroproto/msgsvr/` and `third_party/retroproto/msgcli/`
2. Looking for Go structs with `New<MessageName>` constructors
3. Detecting `Deserialize(extra string) error` methods
4. Building a registry map: `message_name → parse_function`

### Generation Options

```bash
python gen_go_registry.py --help
```

**Available options:**
- `--msgsvr`: Path to msgsvr directory (default: `../../third_party/retroproto/msgsvr`)
- `--msgcli`: Path to msgcli directory (default: `../../third_party/retroproto/msgcli`)
- `--out`: Output file for generated registry (default: `registry.go`)
- `--dry-run`: Show what would be found without generating files
- `--prefer-server`: Prefer server parsers over client for same message
- `--json-out`: Output debug info as JSON

## Architecture

### Registry Structure

The generated registry follows this pattern:

```go
var Registry = map[string]ParserFn{
    "MessageName": func(s string) (interface{}, error) {
        return msgsvr.NewMessageName(s)
    },
    // ... more parsers
}
```

### Parser Function Signature

```go
type ParserFn func(s string) (interface{}, error)
```

All parsers return `interface{}` to accommodate different message types, with JSON marshaling providing type-safe access.

## Differences from Rust Parser

The Go baseline is designed to be:
- **Conservative**: Only uses well-defined parsing patterns
- **Complete**: Covers all available Go parsers (504 total)
- **Transparent**: Clear error reporting for missing parsers
- **Repeatable**: Idempotent - can be run multiple times safely

## Error Handling

The Go baseline reports:
- **Missing parsers**: When no Go parser exists for a message type
- **Parse errors**: When the Go parser fails to parse a message
- **Marshaling errors**: When the parsed result can't be JSON-serialized

## Output Files

After running, you'll find:
- **dummy_go.ndjson**: One JSON object per line, aligned with input by frame_index
- **dummy_go.json**: Pretty-printed JSON array of all results
- **Processing summary**: Statistics on parsing success/failure rates

## Troubleshooting

### Go Not Found
If you get "go: command not found", install Go or add it to your PATH.

### Import Errors
The `go.mod` uses a local replace directive. Make sure the retroproto directory exists at the expected path.

### Parser Coverage
Some messages may show "no go parser registered" - this indicates the message type wasn't found in the Go source, which is expected for newer or uncommon message types.

### Build Errors
If the Go build fails, try:
```bash
cd tools/go_baseline
go mod tidy
go build -o ../../bin/retroproto_go_baseline.exe
```

## Integration with Diff Tool

The Go baseline output is designed to work with the diff tool:

```bash
python tools/diff_go_rust_parsed.py \
  --rust examples/pcap/decoded/dummy_parsed_new.ndjson \
  --go examples/pcap/decoded/dummy_go.ndjson
```

This compares the Rust-parsed results with Go-parsed results, identifying discrepancies that may indicate bugs in the Rust parser.