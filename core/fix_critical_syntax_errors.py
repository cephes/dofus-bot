#!/usr/bin/env python3
"""
Critical syntax error fix for dofus-core compilation
Addresses the main issues preventing build success
"""

import os
import re
import glob
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix invalid import statements"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix r#crate imports
        content = re.sub(r'use r#crate::', 'use crate::', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed imports in {file_path}")
        return True
    except Exception as e:
        print(f"Error fixing imports in {file_path}: {e}")
        return False

def fix_field_names_in_file(file_path):
    """Fix malformed field names with # symbols"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix field names with # symbols
        content = re.sub(r'(\w+)#(\w+):', r'\1_\2:', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed field names in {file_path}")
        return True
    except Exception as e:
        print(f"Error fixing field names in {file_path}: {e}")
        return False

def add_serialize_derive(file_path):
    """Add missing serde Serialize derive"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find derive attributes and ensure serde::Serialize is included
        derive_pattern = r'#\[derive\(([^)]+)\)\]'
        
        def add_serialize_derive(match):
            derives = match.group(1)
            if 'serde::Serialize' not in derives:
                # Check if any serde derive exists
                if any(serde in derives for serde in ['serde::', 'Serialize', 'Deserialize']):
                    # Add Serialize to existing serde derives
                    if 'serde::Deserialize' in derives:
                        new_derives = derives.replace('serde::Deserialize', 'serde::Serialize, serde::Deserialize')
                    else:
                        new_derives = derives + ', serde::Serialize'
                else:
                    new_derives = derives + ', serde::Serialize'
                return f"#[derive({new_derives})]"
            return match.group(0)
        
        content = re.sub(derive_pattern, add_serialize_derive, content)
        
        # If no derive found, add one (this shouldn't happen but just in case)
        if '#[derive(' not in content and 'pub struct ' in content:
            # Find the struct definition and add derive
            struct_pattern = r'(pub struct \w+ \{)'
            content = re.sub(struct_pattern, r'#[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]\n\1', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Added Serialize derive to {file_path}")
        return True
    except Exception as e:
        print(f"Error adding Serialize derive to {file_path}: {e}")
        return False

def main():
    print("Starting critical syntax error fixes...")
    
    # Get all generated parser files
    generated_dir = Path("src/retroproto_parsers/generated")
    if not generated_dir.exists():
        print("Generated directory not found, trying current directory")
        generated_dir = Path(".")
    
    all_files = []
    for root, dirs, files in os.walk(generated_dir):
        for file in files:
            if file.endswith('.rs'):
                all_files.append(os.path.join(root, file))
    
    print(f"Found {len(all_files)} Rust files to process")
    
    success_count = 0
    for file_path in all_files:
        if fix_imports_in_file(file_path):
            if fix_field_names_in_file(file_path):
                if add_serialize_derive(file_path):
                    success_count += 1
    
    print(f"Successfully processed {success_count}/{len(all_files)} files")
    
    # Fix the registry.rs file specifically
    registry_path = Path("src/retroproto_parsers/registry.rs")
    if registry_path.exists():
        print("Fixing registry.rs file...")
        fix_imports_in_file(str(registry_path))
        fix_field_names_in_file(str(registry_path))
    
    print("Critical syntax fixes completed!")

if __name__ == "__main__":
    main()