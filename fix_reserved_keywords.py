#!/usr/bin/env python3
"""
Fix reserved keyword issues in generated Rust files
"""
import os
from pathlib import Path

def fix_file_keywords(file_path):
    """Fix reserved keyword issues in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix struct field declarations
        content = content.replace('pub type:', 'pub r#type:')
        
        # Fix let statements
        content = content.replace('let type =', 'let r#type =')
        content = content.replace('let type,', 'let r#type,')
        content = content.replace('let type', 'let r#type')
        
        # Fix struct field usage
        content = content.replace('type,', 'r#type,')
        content = content.replace('type}', 'r#type}')
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main execution function"""
    generated_dir = Path("core/src/retroproto_parsers/generated")
    
    if not generated_dir.exists():
        print("Generated directory not found")
        return
    
    fixed_count = 0
    for file_path in generated_dir.rglob("*.rs"):
        if file_path.name != "mod.rs":
            if fix_file_keywords(file_path):
                fixed_count += 1
    
    print(f"Fixed reserved keyword issues in {fixed_count} files")

if __name__ == "__main__":
    main()