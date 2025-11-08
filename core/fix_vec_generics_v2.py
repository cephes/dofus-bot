#!/usr/bin/env python3
"""
Improved Vec generic parameter fixer with better type inference.
"""

import os
import re
import glob

def should_be_string_vec(field_name, content):
    """Determine if a field should be Vec<String> based on field name and usage."""
    # Fields that should be strings
    string_indicators = [
        'name', 'text', 'message', 'description', 'title', 'label', 'channel',
        'answer', 'emote', 'value'  # these can be strings
    ]
    
    # Fields that should be i64
    number_indicators = [
        'id', 'count', 'number', 'index', 'position', 'size', 'length', 
        'amount', 'level', 'timestamp', 'template', 'type', 'status'
    ]
    
    field_lower = field_name.lower()
    
    # Check for string indicators
    for indicator in string_indicators:
        if indicator in field_lower:
            return True
    
    # Check for number indicators
    for indicator in number_indicators:
        if indicator in field_lower:
            return False
    
    # Default to String for ambiguous cases
    return True

def fix_vec_generics_in_file(file_path):
    """Fix Vec generic parameters in a single Rust file with improved logic."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find all Vec field declarations
        vec_pattern = r'(\w+:\s+)Vec(\s*,|\s*;|\s*)$'
        
        def replace_vec(match):
            field_name = match.group(1).strip().split(':')[0].strip()
            suffix = match.group(2)
            
            if should_be_string_vec(field_name, content):
                return f"{match.group(1)}Vec<String>{suffix}"
            else:
                return f"{match.group(1)}Vec<i64>{suffix}"
        
        content = re.sub(vec_pattern, replace_vec, content, flags=re.MULTILINE)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed Vec generics in: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def fix_field_name_mismatches(file_path):
    """Fix field name mismatches in struct initialization."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Common field name fixes
        fixes = [
            # action_type -> action_r_type
            (r'\baction_type\b', 'action_r_type'),
            # action_challenge_refuse -> action_challenge_refr_use
            (r'\baction_challenge_refuse\b', 'action_challenge_refr_use'),
            # item_type -> item_r_type
            (r'\bitem_type\b', 'item_r_type'),
        ]
        
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed field names in: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix Vec generics and field names in all generated Rust files."""
    generated_dir = "src/retroproto_parsers/generated"
    
    if not os.path.exists(generated_dir):
        print(f"Directory {generated_dir} not found!")
        return
    
    # Get all .rs files in the generated directory
    rust_files = glob.glob(os.path.join(generated_dir, "*.rs"))
    
    print(f"Found {len(rust_files)} Rust files to check...")
    
    fixed_count = 0
    for file_path in rust_files:
        # First fix Vec generics
        if fix_vec_generics_in_file(file_path):
            fixed_count += 1
        
        # Then fix field name mismatches
        fix_field_name_mismatches(file_path)
    
    print(f"Fixed Vec generics in {fixed_count} files")

if __name__ == "__main__":
    main()