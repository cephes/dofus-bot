# Repository Code Normalization Diagnostic Report

Generated: 2025-11-06 19:02:33 UTC

## Executive Summary

This report analyzes the Dofus retro bot repository structure to identify normalization opportunities and provide actionable steps for repository consolidation.

## Key Findings

### Core Package Analysis
- **Authoritative Core**: `core/`
- **Reasoning**: Core has more recent build: core/target/release/dofus-core.exe (timestamp: 1762389552.298707); dofus-retro-bot/core also contains Rust code but lacks recent builds

### Parser Topology
- **Total Parsers**: 440
- **Generated Parsers**: 437 
- **Handwritten Parsers**: 3
- **Structure Issues**: 0 issues found

### Duplicate Directory Analysis
- **Retroproto Trees**: 2 found
- **Canonical Path**: `third_party/retroproto`
- **Redundant Paths**: 1 paths identified

### Registry Status
- **Total Registered**: 0 parsers
- **Registry Gaps**: []

## Detailed Analysis

### Binary Build Status
The following binaries were found with their last build timestamps:
- `core/target/release/parse_messages.exe`: 2025-11-06 01:39:12
- `core/target/release/reassemble.exe`: 2025-11-06 01:39:12
- `core/target/release/pcap2flow.exe`: 2025-11-05 19:19:09
- `core/target/release/dofus-core.exe`: 2025-11-06 01:39:12

### Parser Structure Issues

### Mod.rs Analysis
**mod.rs**:
- Lines: 1
- Declared modules: GameActions


### Example Paths Analysis
- `examples/pcap/flows`: ✓ EXISTS (1 files)
- `examples/pcap/decoded`: ✓ EXISTS (21 files)
- `orchestrator/examples/pcap/flows`: ✓ EXISTS (1 files)
- `dofus-retro-bot/examples/pcap/flows`: ✗ MISSING (0 files)
- `dofus-retro-bot/examples/pcap/decoded`: ✗ MISSING (0 files)
