#!/usr/bin/env python3
"""
Repository Normalization Report Generator
Generates all required output files from the diagnostic data.
"""

import json
import os
from datetime import datetime, UTC
from pathlib import Path
import re

def load_diagnostic_data():
    """Load the diagnostic data from JSON file."""
    with open('repo_diagnostic_raw.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_authoritative_core(data):
    """Determine which core is authoritative based on cargo metadata and build times."""
    analysis = {
        'core_metadata': data['cargo_metadata']['core_metadata'],
        'binary_timestamps': data['cargo_metadata']['binary_timestamps'],
        'authoritative_core': None,
        'reasoning': []
    }
    
    # Check binary timestamps to determine which core is more recently built
    core_binaries = data['cargo_metadata']['binary_timestamps']
    if core_binaries:
        latest_binary = max(core_binaries.items(), key=lambda x: x[1])
        if 'core/target/release' in latest_binary[0]:
            analysis['authoritative_core'] = 'core/'
            analysis['reasoning'].append(f"Core has more recent build: {latest_binary[0]} (timestamp: {latest_binary[1]})")
    
    # Check dofus-retro-bot core
    sub_core_metadata = data['cargo_metadata']['sub_core_metadata']
    if sub_core_metadata and 'error' not in sub_core_metadata:
        analysis['reasoning'].append("dofus-retro-bot/core also contains Rust code but lacks recent builds")
    
    if not analysis['authoritative_core']:
        analysis['authoritative_core'] = 'core/'
        analysis['reasoning'].append("Defaulting to core/ as authoritative based on presence of recent builds")
    
    return analysis

def generate_parser_inventory(data):
    """Generate parser inventory analysis."""
    topology = data['parser_topology']
    
    # Count parsers
    generated_count = len(topology['generated_parsers'])
    handwritten_count = len(topology['handwritten_parsers'])
    
    # Analyze mod.rs declarations
    mod_analysis = topology['mod_rs_analysis']
    main_mod = mod_analysis.get('mod.rs', {})
    generated_mod = mod_analysis.get('mod.rs', {})
    
    inventory = {
        'total_parsers': generated_count + handwritten_count,
        'generated_parsers': generated_count,
        'handwritten_parsers': handwritten_count,
        'missing_declarations': topology['structure_mismatches'],
        'mod_declarations': mod_analysis
    }
    
    return inventory

def check_duplicate_trees(data):
    """Check for duplicate directories."""
    duplicates = data['duplicate_trees']
    
    retroproto_analysis = {
        'trees_found': [],
        'canonical_path': None,
        'redundant_paths': []
    }
    
    for path, info in duplicates['retroproto_trees'].items():
        if info['exists']:
            retroproto_analysis['trees_found'].append({
                'path': path,
                'file_count': info['file_count'],
                'files': info['root_files']
            })
    
    # Determine canonical path
    if 'third_party/retroproto' in duplicates['retroproto_trees'] and duplicates['retroproto_trees']['third_party/retroproto']['exists']:
        retroproto_analysis['canonical_path'] = 'third_party/retroproto'
        if 'dofus-retro-bot/third_party/retroproto' in duplicates['retroproto_trees'] and duplicates['retroproto_trees']['dofus-retro-bot/third_party/retroproto']['exists']:
            retroproto_analysis['redundant_paths'].append('dofus-retro-bot/third_party/retroproto')
    
    return retroproto_analysis

def generate_registry_preview(data):
    """Generate registry preview."""
    registry = data['registry_analysis']
    
    preview = {
        'total_registered': 0,
        'sample_entries': [],
        'missing_from_registry': [],
        'registry_gaps': []
    }
    
    if 'registry_preview' in registry and registry['registry_preview']:
        preview['total_registered'] = registry['registry_preview'].get('total_registrations_estimated', 0)
        preview['sample_entries'] = registry['registry_preview'].get('sample_entries', [])
    
    # Compare generated parsers with registry
    generated_parsers = list(data['parser_topology']['generated_parsers'].keys())
    if registry.get('registry_preview', {}).get('sample_entries'):
        # This is a simplified check - in reality would need more sophisticated parsing
        preview['registry_gaps'] = f"Estimated {len(generated_parsers)} generated files vs {preview['total_registered']} registry entries"
    
    return preview

def create_human_readable_report(data, analysis):
    """Create the human-readable diagnostic report."""
    content = f"""# Repository Code Normalization Diagnostic Report

Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC

## Executive Summary

This report analyzes the Dofus retro bot repository structure to identify normalization opportunities and provide actionable steps for repository consolidation.

## Key Findings

### Core Package Analysis
- **Authoritative Core**: `{analysis['authoritative_core']['authoritative_core']}`
- **Reasoning**: {'; '.join(analysis['authoritative_core']['reasoning'])}

### Parser Topology
- **Total Parsers**: {analysis['parser_inventory']['total_parsers']}
- **Generated Parsers**: {analysis['parser_inventory']['generated_parsers']} 
- **Handwritten Parsers**: {analysis['parser_inventory']['handwritten_parsers']}
- **Structure Issues**: {len(analysis['parser_inventory']['missing_declarations'])} issues found

### Duplicate Directory Analysis
- **Retroproto Trees**: {len(analysis['retroproto_trees']['trees_found'])} found
- **Canonical Path**: `{analysis['retroproto_trees']['canonical_path'] or 'Not determined'}`
- **Redundant Paths**: {len(analysis['retroproto_trees']['redundant_paths'])} paths identified

### Registry Status
- **Total Registered**: {analysis['registry_preview']['total_registered']} parsers
- **Registry Gaps**: {analysis['registry_preview']['registry_gaps']}

## Detailed Analysis

### Binary Build Status
The following binaries were found with their last build timestamps:
"""
    
    for binary, timestamp in data['cargo_metadata']['binary_timestamps'].items():
        build_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        content += f"- `{binary}`: {build_time}\n"
    
    content += f"""
### Parser Structure Issues
"""
    for issue in analysis['parser_inventory']['missing_declarations']:
        content += f"- {issue}\n"
    
    content += f"""
### Mod.rs Analysis
"""
    for mod_file, info in analysis['parser_inventory']['mod_declarations'].items():
        content += f"**{mod_file}**:\n"
        content += f"- Lines: {info['line_count']}\n"
        content += f"- Declared modules: {', '.join(info['declared_modules']) if info['declared_modules'] else 'None'}\n\n"
    
    content += f"""
### Example Paths Analysis
"""
    for path, info in data['duplicate_trees']['example_paths'].items():
        status = "✓ EXISTS" if info['exists'] else "✗ MISSING"
        content += f"- `{path}`: {status} ({info.get('file_count', 0)} files)\n"
    
    return content

def create_normalization_plan(analysis):
    """Create the normalization plan with concrete steps."""
    plan = """# Repository Normalization Plan

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
"""
    for issue in analysis['parser_inventory']['missing_declarations']:
        plan += f"- {issue}\n"
    
    plan += """
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
"""
    
    return plan

def create_dry_run_scripts(plan_content):
    """Create dry-run shell and PowerShell scripts."""
    
    # Extract actions from plan for shell script
    shell_script = """#!/bin/bash
# Repository Normalization Dry-Run Script (Bash)
# This script only echoes the actions that would be performed

echo "=== Repository Normalization Dry Run (Bash) ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%S)Z"
echo ""

# Phase 1: Directory Structure Normalization
echo "Phase 1: Directory Structure Normalization"
echo "==========================================="

echo "1.1 Consolidating Retroproto Trees..."
echo "  - Would copy unique files from dofus-retro-bot/third_party/retroproto/ to third_party/retroproto/"
echo "  - Would remove dofus-retro-bot/third_party/retroproto/ directory"
echo "  - Would update references to old path"

echo ""
echo "1.2 Consolidating Example Paths..."
echo "  - Would merge unique files from dofus-retro-bot/examples/ to examples/"
echo "  - Would remove redundant example directories"
echo "  - Would update pipeline scripts to use canonical paths"

# Phase 2: Parser Module Structure Fixes
echo ""
echo "Phase 2: Parser Module Structure Fixes"
echo "======================================="

echo "2.1 Fixing mod.rs Declarations..."
echo "  - Would update core/src/retroproto_parsers/mod.rs"
echo "  - Would ensure generated and handwritten modules are properly exposed"
echo "  - Would verify all parser files are linked in module tree"

echo ""
echo "2.2 Actions Submodule Integration..."
echo "  - Would create core/src/retroproto_parsers/generated/actions/ directory"
echo "  - Would generate action-specific parser files"
echo "  - Would update generated/mod.rs to include actions submodule"

# Phase 3: Registry Generation
echo ""
echo "Phase 3: Registry Generation"
echo "==========================="

echo "3.1 Parser Registry Normalization..."
echo "  - Would run tools/gen_parser_registry.py"
echo "  - Would verify all generated parsers are included"
echo "  - Would update GameActions dispatcher registration"
echo "  - Would generate comprehensive registry documentation"

# Phase 4: Binary Consistency
echo ""
echo "Phase 4: Binary Consistency"
echo "==========================="

echo "4.1 Build System Alignment..."
echo "  - Would ensure all builds use authoritative core (core/)"
echo "  - Would update Cargo.toml references"
echo "  - Would verify binary CLI interfaces are consistent"

# Phase 5: Documentation Updates
echo ""
echo "Phase 5: Documentation Updates"
echo "=============================="

echo "5.1 Path References..."
echo "  - Would update all documentation to reflect new canonical paths"
echo "  - Would update pipeline scripts and automation"
echo "  - Would create migration guide for developers"

echo ""
echo "=== Dry Run Complete ==="
echo "To execute these changes, run the actual normalization script."
"""
    
    # PowerShell script
    powershell_script = """# Repository Normalization Dry-Run Script (PowerShell)
# This script only Write-Hosts the actions that would be performed

Write-Host "=== Repository Normalization Dry Run (PowerShell) ===" -ForegroundColor Green
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')" -ForegroundColor Gray
Write-Host ""

# Phase 1: Directory Structure Normalization
Write-Host "Phase 1: Directory Structure Normalization" -ForegroundColor Yellow
Write-Host "===========================================" -ForegroundColor Yellow

Write-Host "1.1 Consolidating Retroproto Trees..." -ForegroundColor Cyan
Write-Host "  - Would copy unique files from dofus-retro-bot/third_party/retroproto/ to third_party/retroproto/" -ForegroundColor White
Write-Host "  - Would remove dofus-retro-bot/third_party/retroproto/ directory" -ForegroundColor White
Write-Host "  - Would update references to old path" -ForegroundColor White

Write-Host ""
Write-Host "1.2 Consolidating Example Paths..." -ForegroundColor Cyan
Write-Host "  - Would merge unique files from dofus-retro-bot/examples/ to examples/" -ForegroundColor White
Write-Host "  - Would remove redundant example directories" -ForegroundColor White
Write-Host "  - Would update pipeline scripts to use canonical paths" -ForegroundColor White

# Phase 2: Parser Module Structure Fixes
Write-Host ""
Write-Host "Phase 2: Parser Module Structure Fixes" -ForegroundColor Yellow
Write-Host "=======================================" -ForegroundColor Yellow

Write-Host "2.1 Fixing mod.rs Declarations..." -ForegroundColor Cyan
Write-Host "  - Would update core/src/retroproto_parsers/mod.rs" -ForegroundColor White
Write-Host "  - Would ensure generated and handwritten modules are properly exposed" -ForegroundColor White
Write-Host "  - Would verify all parser files are linked in module tree" -ForegroundColor White

Write-Host ""
Write-Host "2.2 Actions Submodule Integration..." -ForegroundColor Cyan
Write-Host "  - Would create core/src/retroproto_parsers/generated/actions/ directory" -ForegroundColor White
Write-Host "  - Would generate action-specific parser files" -ForegroundColor White
Write-Host "  - Would update generated/mod.rs to include actions submodule" -ForegroundColor White

# Phase 3: Registry Generation
Write-Host ""
Write-Host "Phase 3: Registry Generation" -ForegroundColor Yellow
Write-Host "===========================" -ForegroundColor Yellow

Write-Host "3.1 Parser Registry Normalization..." -ForegroundColor Cyan
Write-Host "  - Would run tools/gen_parser_registry.py" -ForegroundColor White
Write-Host "  - Would verify all generated parsers are included" -ForegroundColor White
Write-Host "  - Would update GameActions dispatcher registration" -ForegroundColor White
Write-Host "  - Would generate comprehensive registry documentation" -ForegroundColor White

# Phase 4: Binary Consistency
Write-Host ""
Write-Host "Phase 4: Binary Consistency" -ForegroundColor Yellow
Write-Host "===========================" -ForegroundColor Yellow

Write-Host "4.1 Build System Alignment..." -ForegroundColor Cyan
Write-Host "  - Would ensure all builds use authoritative core (core/)" -ForegroundColor White
Write-Host "  - Would update Cargo.toml references" -ForegroundColor White
Write-Host "  - Would verify binary CLI interfaces are consistent" -ForegroundColor White

# Phase 5: Documentation Updates
Write-Host ""
Write-Host "Phase 5: Documentation Updates" -ForegroundColor Yellow
Write-Host "==============================" -ForegroundColor Yellow

Write-Host "5.1 Path References..." -ForegroundColor Cyan
Write-Host "  - Would update all documentation to reflect new canonical paths" -ForegroundColor White
Write-Host "  - Would update pipeline scripts and automation" -ForegroundColor White
Write-Host "  - Would create migration guide for developers" -ForegroundColor White

Write-Host ""
Write-Host "=== Dry Run Complete ===" -ForegroundColor Green
Write-Host "To execute these changes, run the actual normalization script." -ForegroundColor Gray
"""
    
    return shell_script, powershell_script

def main():
    """Main report generation function."""
    print("Loading diagnostic data...")
    data = load_diagnostic_data()
    
    print("Analyzing diagnostic data...")
    analysis = {
        'authoritative_core': analyze_authoritative_core(data),
        'parser_inventory': generate_parser_inventory(data),
        'retroproto_trees': check_duplicate_trees(data),
        'registry_preview': generate_registry_preview(data)
    }
    
    print("Generating output files...")
    
    # 1. Human-readable report
    print("Creating REPO_CODE_NORM_DIAG.md...")
    with open('REPO_CODE_NORM_DIAG.md', 'w', encoding='utf-8') as f:
        f.write(create_human_readable_report(data, analysis))
    
    # 2. Machine-readable JSON
    print("Creating repo_code_norm.json...")
    with open('repo_code_norm.json', 'w', encoding='utf-8') as f:
        json.dump({
            'analysis': analysis,
            'raw_data': data,
            'generated_at': datetime.now(UTC).isoformat() + 'Z'
        }, f, indent=2, ensure_ascii=False)
    
    # 3. Normalization plan
    print("Creating repo_norm_plan.md...")
    with open('repo_norm_plan.md', 'w', encoding='utf-8') as f:
        f.write(create_normalization_plan(analysis))
    
    # 4. Dry-run scripts
    print("Creating repo_norm_actions.sh and repo_norm_actions.ps1...")
    shell_script, powershell_script = create_dry_run_scripts(analysis)
    
    with open('repo_norm_actions.sh', 'w', encoding='utf-8') as f:
        f.write(shell_script)
    
    with open('repo_norm_actions.ps1', 'w', encoding='utf-8') as f:
        f.write(powershell_script)
    
    # 5. Registry preview
    print("Creating registry_preview.txt...")
    with open('registry_preview.txt', 'w', encoding='utf-8') as f:
        f.write(f"""Parser Registry Preview
Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} UTC

Total Registered Parsers: {analysis['registry_preview']['total_registered']}

Sample Registry Entries:
""")
        for entry in analysis['registry_preview']['sample_entries']:
            f.write(f"  {entry}\n")
        
        f.write(f"""
Registry Analysis:
{analysis['registry_preview']['registry_gaps']}

Generated Parser Files: {analysis['parser_inventory']['generated_parsers']}
Handwritten Parser Files: {analysis['parser_inventory']['handwritten_parsers']}
""")
    
    print("All output files generated successfully!")
    print("\nGenerated files:")
    print("- REPO_CODE_NORM_DIAG.md (human-readable report)")
    print("- repo_code_norm.json (machine-readable data)")
    print("- repo_norm_plan.md (normalization plan)")
    print("- repo_norm_actions.sh (dry-run script)")
    print("- repo_norm_actions.ps1 (dry-run script)")
    print("- registry_preview.txt (parser registry summary)")

if __name__ == '__main__':
    main()