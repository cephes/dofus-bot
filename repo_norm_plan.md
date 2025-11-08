# Repository Normalization Plan

## Overview
This plan provides concrete, reversible steps to normalize the Dofus retro bot repository structure.

## Phase 1: Directory Structure Normalization

### 1.1 Consolidate Retroproto Trees
**Current State**: Duplicate `third_party/retroproto` directories exist
- `third_party/retroproto/` (canonical)
- `dofus-retro-bot/third_party/retroproto/` (redundant)

**Proposed Actions**:
1. Copy any unique files from `dofus-retro-bot/third_party/retroproto/` to `third_party/retroproto/`
2. Remove `dofus-retro-bot/third_party/retroproto/` directory
3. Update any references to the old path

### 1.2 Consolidate Example Paths
**Current State**: Examples exist in multiple locations
- `examples/pcap/flows/` (canonical)
- `examples/pcap/decoded/` (canonical)
- `dofus-retro-bot/examples/pcap/flows/` (redundant)
- `dofus-retro-bot/examples/pcap/decoded/` (redundant)

**Proposed Actions**:
1. Merge any unique files from dofus-retro-bot examples to main examples
2. Remove redundant example directories
3. Update pipeline scripts to use canonical paths

## Phase 2: Parser Module Structure Fixes

### 2.1 Fix mod.rs Declarations
**Current Issues**:

**Proposed Actions**:
1. Update `core/src/retroproto_parsers/mod.rs` to properly declare submodules
2. Ensure `generated` and `handwritten` modules are properly exposed
3. Verify all parser files are properly linked in the module tree

### 2.2 Actions Submodule Integration
**Current State**: Generated actions files may not be integrated
**Proposed Actions**:
1. Create `core/src/retroproto_parsers/generated/actions/` directory structure
2. Generate action-specific parser files (e.g., `ga_XXXX.rs`)
3. Update `generated/mod.rs` to include actions submodule
4. Integrate with GameActions dispatcher

## Phase 3: Registry Generation

### 3.1 Parser Registry Normalization
**Current State**: Registry may be incomplete or outdated
**Proposed Actions**:
1. Run `tools/gen_parser_registry.py` to regenerate registry
2. Verify all generated parsers are included
3. Update GameActions dispatcher registration
4. Generate comprehensive registry documentation

## Phase 4: Binary Consistency

### 4.1 Build System Alignment
**Current State**: Multiple core directories with different build states
**Proposed Actions**:
1. Ensure all builds use the authoritative core (`core/`)
2. Update Cargo.toml references to point to canonical paths
3. Verify binary CLI interfaces are consistent

## Phase 5: Documentation Updates

### 5.1 Path References
**Proposed Actions**:
1. Update all documentation to reflect new canonical paths
2. Update pipeline scripts and automation
3. Create migration guide for developers

## Success Criteria
- [ ] Single authoritative core directory
- [ ] Single retroproto tree location  
- [ ] All parsers properly declared in module tree
- [ ] Complete and accurate parser registry
- [ ] Consistent binary interfaces
- [ ] Updated documentation and scripts

## Rollback Plan
Each phase can be rolled back by:
1. Restoring directory copies from version control
2. Reverting mod.rs changes
3. Re-running registry generation if needed
4. Restoring original script references
