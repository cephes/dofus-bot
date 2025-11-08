#!/usr/bin/env python3
"""
Repository Normalization Diagnostic Collector
Systematically gathers all data needed for the normalization plan.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any
import hashlib

def gather_cargo_metadata():
    """Gather and analyze cargo metadata from all Rust packages."""
    results = {
        'root_metadata': None,
        'core_metadata': None,
        'sub_core_metadata': None,
        'binary_timestamps': {}
    }
    
    # Read root metadata
    if os.path.exists('tmp.cargo-metadata.json') and os.path.getsize('tmp.cargo-metadata.json') > 0:
        try:
            with open('tmp.cargo-metadata.json', 'r', encoding='utf-8') as f:
                results['root_metadata'] = json.load(f)
        except (json.JSONDecodeError, Exception) as e:
            results['root_metadata'] = {'error': str(e)}
    
    # Read core metadata
    if os.path.exists('tmp.core-metadata.json') and os.path.getsize('tmp.core-metadata.json') > 0:
        try:
            with open('tmp.core-metadata.json', 'r', encoding='utf-8') as f:
                results['core_metadata'] = json.load(f)
        except (json.JSONDecodeError, Exception) as e:
            results['core_metadata'] = {'error': str(e)}
    
    # Read sub-core metadata
    if os.path.exists('tmp.sub-core-metadata.json') and os.path.getsize('tmp.sub-core-metadata.json') > 0:
        try:
            with open('tmp.sub-core-metadata.json', 'r', encoding='utf-8') as f:
                results['sub_core_metadata'] = json.load(f)
        except (json.JSONDecodeError, Exception) as e:
            results['sub_core_metadata'] = {'error': str(e)}
    
    # Binary timestamps
    core_binaries = [
        'core/target/release/parse_messages.exe',
        'core/target/release/reassemble.exe', 
        'core/target/release/pcap2flow.exe',
        'core/target/release/dofus-core.exe'
    ]
    
    for binary in core_binaries:
        if os.path.exists(binary):
            stat = os.stat(binary)
            results['binary_timestamps'][binary] = stat.st_mtime
    
    return results

def analyze_parser_topology():
    """Analyze the parser source topology (generated vs handwritten)."""
    results = {
        'generated_parsers': {},
        'handwritten_parsers': {},
        'mod_rs_analysis': {},
        'structure_mismatches': []
    }
    
    # Generated parsers analysis
    generated_dir = Path('core/src/retroproto_parsers/generated')
    if generated_dir.exists():
        for rs_file in generated_dir.glob('*.rs'):
            try:
                with open(rs_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                filename = rs_file.name
                has_struct = 'pub struct' in content and filename.replace('.rs', '') in content
                has_parse_fn = f"pub fn parse_{filename.replace('.rs', '')}" in content
                
                results['generated_parsers'][filename] = {
                    'has_struct': has_struct,
                    'has_parse_fn': has_parse_fn,
                    'size_bytes': len(content)
                }
            except Exception as e:
                results['generated_parsers'][filename] = {'error': str(e)}
    
    # Handwritten parsers analysis
    handwritten_dir = Path('core/src/retroproto_parsers/handwritten')
    if handwritten_dir.exists():
        for rs_file in handwritten_dir.glob('*.rs'):
            try:
                with open(rs_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                filename = rs_file.name
                parse_fns = [line.strip() for line in content.split('\n') if 'pub fn parse_' in line]
                
                results['handwritten_parsers'][filename] = {
                    'parse_functions': parse_fns,
                    'size_bytes': len(content)
                }
            except Exception as e:
                results['handwritten_parsers'][filename] = {'error': str(e)}
    
    # mod.rs analysis
    mod_files = [
        'core/src/retroproto_parsers/mod.rs',
        'core/src/retroproto_parsers/generated/mod.rs',
        'core/src/retroproto_parsers/handwritten/mod.rs'
    ]
    
    for mod_file in mod_files:
        if os.path.exists(mod_file):
            with open(mod_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            mod_name = os.path.basename(mod_file)
            declared_modules = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('pub mod ') or line.startswith('mod '):
                    module = line.replace('pub mod ', '').replace('mod ', '').rstrip(';')
                    declared_modules.append(module)
            
            results['mod_rs_analysis'][mod_name] = {
                'declared_modules': declared_modules,
                'line_count': len(content.split('\n'))
            }
    
    # Check for structure mismatches (files that exist but aren't declared)
    generated_files = set(os.listdir('core/src/retroproto_parsers/generated')) if os.path.exists('core/src/retroproto_parsers/generated') else set()
    handwritten_files = set(os.listdir('core/src/retroproto_parsers/handwritten')) if os.path.exists('core/src/retroproto_parsers/handwritten') else set()
    
    all_parser_files = generated_files | handwritten_files
    
    # Check main mod.rs for declarations
    main_mod_path = 'core/src/retroproto_parsers/mod.rs'
    if os.path.exists(main_mod_path):
        with open(main_mod_path, 'r', encoding='utf-8') as f:
            main_mod_content = f.read()
        
        declared_in_main = []
        for line in main_mod_content.split('\n'):
            line = line.strip()
            if 'mod generated' in line or 'mod handwritten' in line:
                declared_in_main.append(line)
        
        if 'generated' not in main_mod_content:
            results['structure_mismatches'].append('generated module not declared in main mod.rs')
        if 'handwritten' not in main_mod_content:
            results['structure_mismatches'].append('handwritten module not declared in main mod.rs')
    
    return results

def check_registry_and_dispatcher():
    """Check parser registry generation and GA dispatcher presence."""
    results = {
        'registry_tools': {},
        'game_actions_analysis': {},
        'static_registries': [],
        'registry_preview': {}
    }
    
    # Check for gen_parser_registry.py
    registry_tool = 'tools/gen_parser_registry.py'
    if os.path.exists(registry_tool):
        with open(registry_tool, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import_patterns = [line for line in content.split('\n') if 'crate::retroproto_parsers::generated' in line]
        ga_mentions = [line for line in content.split('\n') if 'GameActions' in line or 'game_actions' in line]
        
        results['registry_tools'] = {
            'found': True,
            'import_patterns': import_patterns,
            'ga_mentions': ga_mentions,
            'size_bytes': len(content)
        }
    else:
        results['registry_tools'] = {'found': False}
    
    # Check GameActions.rs
    game_actions_path = 'core/src/retroproto_parsers/handwritten/GameActions.rs'
    if os.path.exists(game_actions_path):
        with open(game_actions_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        parse_functions = [line.strip() for line in content.split('\n') if 'pub fn parse_GameActions' in line]
        schema_fields = [line.strip() for line in content.split('\n') if 'action_code' in line or 'rest' in line]
        
        results['game_actions_analysis'] = {
            'has_parse_GameActions': len(parse_functions) > 0,
            'parse_functions': parse_functions,
            'schema_fields': schema_fields,
            'size_bytes': len(content)
        }
    
    # Search for static registry patterns
    registry_patterns = [
        'once_cell::sync::Lazy',
        'static mut',
        'lazy_static',
        'std::sync::OnceLock'
    ]
    
    for root, dirs, files in os.walk('core/src'):
        for file in files:
            if file.endswith('.rs'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern in registry_patterns:
                        if pattern in content:
                            results['static_registries'].append({
                                'file': file_path,
                                'pattern': pattern,
                                'line_count': len(content.split('\n'))
                            })
                except:
                    pass
    
    # Count registered parsers (if registry.rs exists)
    registry_path = 'core/src/retroproto_parsers/registry.rs'
    if os.path.exists(registry_path):
        with open(registry_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to estimate registered count
        lines = content.split('\n')
        parse_calls = [line for line in lines if '.parse_' in line]
        
        results['registry_preview'] = {
            'total_registrations_estimated': len(parse_calls),
            'sample_entries': parse_calls[:20] if parse_calls else []
        }
    
    return results

def analyze_duplicate_trees():
    """Analyze duplicate directories and path drift."""
    results = {
        'retroproto_trees': {},
        'example_paths': {},
        'file_comparison': {}
    }
    
    # Retroproto trees
    retroproto_paths = [
        'third_party/retroproto',
        'dofus-retro-bot/third_party/retroproto'
    ]
    
    for path in retroproto_paths:
        if os.path.exists(path):
            file_count = sum([len(files) for r, d, files in os.walk(path)])
            results['retroproto_trees'][path] = {
                'exists': True,
                'file_count': file_count,
                'root_files': os.listdir(path)
            }
        else:
            results['retroproto_trees'][path] = {'exists': False}
    
    # Example paths
    example_paths = [
        'examples/pcap/flows',
        'examples/pcap/decoded', 
        'orchestrator/examples/pcap/flows',
        'dofus-retro-bot/examples/pcap/flows',
        'dofus-retro-bot/examples/pcap/decoded'
    ]
    
    for path in example_paths:
        if os.path.exists(path):
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            results['example_paths'][path] = {
                'exists': True,
                'file_count': len(files),
                'files': files
            }
        else:
            results['example_paths'][path] = {'exists': False}
    
    return results

def check_binary_cli_expectations():
    """Check binary CLI argument formats."""
    results = {
        'parse_messages_args': None,
        'reassemble_flags': None,
        'pcap2flow_flags': None,
        'pipeline_scripts': []
    }
    
    # Check parse_messages.rs source
    parse_source = 'core/src/bin/parse_messages.rs'
    if os.path.exists(parse_source):
        with open(parse_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for argument parsing patterns
        positional_args = 'arg(' in content and 'required(true)' in content
        flag_based = '--input' in content or '--output' in content
        
        results['parse_messages_args'] = {
            'uses_positional': positional_args,
            'uses_flags': flag_based,
            'arg_count': content.count('arg(')
        }
    
    # Check other binaries
    binary_sources = [
        'core/src/bin/reassemble.rs',
        'core/src/bin/pcap2flow.rs'
    ]
    
    for source in binary_sources:
        if os.path.exists(source):
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
            
            flag_usage = '--' in content
            results[os.path.basename(source).replace('.rs', '_flags')] = {
                'uses_flags': flag_usage,
                'flag_count': content.count('--')
            }
    
    # Check pipeline scripts
    pipeline_scripts = [
        'scripts/run_dummy_pipeline.py',
        'scripts/run_dummy_parsing.ps1'
    ]
    
    for script in pipeline_scripts:
        if os.path.exists(script):
            with open(script, 'r', encoding='utf-8') as f:
                content = f.read()
            
            results['pipeline_scripts'].append({
                'path': script,
                'mentions_parse_messages': 'parse_messages' in content,
                'mentions_reassemble': 'reassemble' in content,
                'mentions_pcap2flow': 'pcap2flow' in content
            })
    
    return results

def main():
    """Main diagnostic collection function."""
    print("Starting comprehensive repository diagnostic...")
    
    results = {
        'cargo_metadata': gather_cargo_metadata(),
        'parser_topology': analyze_parser_topology(),
        'registry_analysis': check_registry_and_dispatcher(),
        'duplicate_trees': analyze_duplicate_trees(),
        'cli_expectations': check_binary_cli_expectations(),
        'timestamp': subprocess.run(['python', '-c', 'from datetime import datetime; print(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"))'],
                                  capture_output=True, text=True).stdout.strip()
    }
    
    # Save results
    with open('repo_diagnostic_raw.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("Diagnostic data saved to repo_diagnostic_raw.json")
    return results

if __name__ == '__main__':
    main()