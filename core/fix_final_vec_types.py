#!/usr/bin/env python3
"""
Final fix for specific Vec type mismatches.
"""

import os
import re
import glob

def fix_specific_vec_types(file_path):
    """Fix specific Vec type mismatches based on error analysis."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Field-specific fixes based on compilation errors
        fixes = [
            # position fields should be Vec<i64>
            (r'pub position: Vec<String>', 'pub position: Vec<i64>'),
            # answers should be Vec<i64> (these are likely numeric IDs)
            (r'pub answers: Vec<String>', 'pub answers: Vec<i64>'),
            # emotes should be Vec<i64> (emote IDs)
            (r'pub emotes: Vec<String>', 'pub emotes: Vec<i64>'),
            # item_template_ids should be Vec<i64>
            (r'pub item_template_ids: Vec<String>', 'pub item_template_ids: Vec<i64>'),
            # items_templates_ids should be Vec<i64>
            (r'pub items_templates_ids: Vec<String>', 'pub items_templates_ids: Vec<i64>'),
        ]
        
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed Vec types in: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix specific Vec type mismatches in files with errors."""
    # Files that have Vec type errors based on the compilation output
    error_files = [
        "src/retroproto_parsers/generated/AccountNewQueue.rs",
        "src/retroproto_parsers/generated/AccountQueue.rs",
        "src/retroproto_parsers/generated/DialogQuestion.rs",
        "src/retroproto_parsers/generated/EmotesList.rs",
        "src/retroproto_parsers/generated/ExchangeBigStoreTypeItemsList.rs",
        "src/retroproto_parsers/generated/ItemsItemSetAdd.rs",
        "src/retroproto_parsers/generated/ItemsMovement.rs",
        "src/retroproto_parsers/generated/ItemsRequestMovement.rs",
        "src/retroproto_parsers/generated/SpellsMoveToUsed.rs",
    ]
    
    fixed_count = 0
    for file_path in error_files:
        if os.path.exists(file_path):
            if fix_specific_vec_types(file_path):
                fixed_count += 1
        else:
            print(f"File not found: {file_path}")
    
    print(f"Fixed Vec types in {fixed_count} files")

if __name__ == "__main__":
    main()