# Dofus Core

This crate provides the core functionality for the Dofus bot, including packet parsing and framing.

## Dofus Framing Module

The `dofus_framing` module implements a parser for Dofus Retro network protocol framing.

### Heuristics Used

Since automatic extraction from `third_party/retroproto` was not feasible (Go code, no direct framing spec), the parser uses conservative heuristics:

1. **u16 BE Length Prefix**: Assumes 2-byte big-endian length followed by payload.
2. **u32 BE Length Prefix**: Assumes 4-byte big-endian length followed by payload.
3. **Dofus Variable-Length Header**: Simplified heuristic parsing first byte for length type (1-4 bytes).
4. **StreamToEnd Fallback**: Single frame with remaining data if no header detected.

All heuristics enforce `MAX_FRAME_SIZE = 10 MB` to prevent abuse.

### Retroproto Mapping Integration

The `dofus_mapping` module loads message prefixes from `third_party/retroproto/mapping.json` at runtime. If the file is missing, it falls back to empty mappings.

To regenerate `mapping.json`, run the extraction script (see `third_party/retroproto/MAPPING_REPORT.md`).

The `dofus_proto` module uses `detect_prefix_from_text` to classify packets as Client/Server/Unknown, attaching provenance metadata.

Example CLI decode:
```bash
cargo run -- --mode dofus --input flow.bin --output decoded.json
```

Output includes `kind` (Client/Server/Unknown) and `header_meta` with source file/line info.

### Usage

```rust
use dofus_core::dofus_framing::read_dofus_frames;
use std::fs::File;

let file = File::open("data.bin")?;
let frames = read_dofus_frames(file)?;
for frame in frames {
    println!("Frame {}: {} bytes", frame.index, frame.payload.len());
}
```

### CLI Usage

Run with `--mode dofus` to use framing parser:

```bash
cargo run -- --input data.bin --mode dofus --output frames.json
```

Output: JSON array of frames with `index`, `length`, `payload_hex`, and `header_meta`.