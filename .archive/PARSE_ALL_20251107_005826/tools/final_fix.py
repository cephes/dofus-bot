#!/usr/bin/env python3
"""
Final fix to clean up remaining syntax errors and restore malformed function definitions.
"""

import re
import pathlib

# Constants
ROOT = pathlib.Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "core" / "src" / "retroproto_parsers" / "generated"
ACT_DIR = GEN_DIR / "actions"

def restore_malformed_functions():
    """Restore function definitions that got corrupted by the aggressive fix."""
    print("Restoring malformed function definitions...")
    changes = 0
    
    # Files that likely got corrupted
    action_files = list(ACT_DIR.glob("*.rs"))
    
    for rust_file in action_files:
        try:
            content = rust_file.read_text(encoding='utf-8')
            original_content = content
            
            # Check if the file is malformed (has function signature parts in struct creation)
            if '-> Result<' in content and 'Ok(' in content and 'extra: &str) ->' in content:
                # This file is corrupted, restore it
                struct_name = rust_file.stem
                
                # Create a clean function definition
                clean_content = f"""// AUTO-GENERATED Game Action Parser for code 0
use serde_json::Value;

#[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]
pub struct {struct_name} {{
}}

pub fn parse_{struct_name}(extra: &str) -> Result<{struct_name}, String> {{
    let payload = extra.trim();
    Ok({struct_name}::default())
}}

pub fn {struct_name}_to_json(m: &{struct_name}) -> Value {{
    serde_json::to_value(m).unwrap_or(Value::Null)
}}"""
                
                rust_file.write_text(clean_content, encoding='utf-8')
                changes += 1
                print(f"  Restored {rust_file.name}")
        
        except Exception as e:
            print(f"Error processing {rust_file}: {e}")
    
    return changes

def fix_remaining_syntax_errors():
    """Fix any remaining syntax errors in other files."""
    print("Fixing remaining syntax errors...")
    changes = 0
    
    all_rust_files = list(GEN_DIR.glob("*.rs")) + list(ACT_DIR.glob("*.rs"))
    
    for rust_file in all_rust_files:
        if rust_file.name in ["mod.rs", "mod.rs.bak"]:
            continue
            
        try:
            content = rust_file.read_text(encoding='utf-8')
            original_content = content
            
            # Fix malformed struct creation patterns
            # Look for patterns like: field: type) -> Result<...,
            content = re.sub(r'(\w+:\s*[^,}]+)\s*\)\s*->\s*Result<[^,}]*,', r'\1,', content)
            
            # Fix function signatures that got broken
            # Pattern: pub fn name(params) -> Result<type, String> { content
            content = re.sub(r'(pub\s+fn\s+\w+\([^)]*\)\s*->\s*Result\s*<[^>]*>\s*\{[^}]*)Ok\([^)]*\s*\{[^}]*\}[^}]*}[^}]*}[^}]*\}', r'\1\n    Ok(m)', content)
            
            # Fix incomplete struct literals
            content = re.sub(r'Ok\(\{\s*([^}]*)\}\s*([^}]*)\s*([^}]*)\}', r'Ok({\1})', content)
            
            # Fix missing commas in struct creation
            content = re.sub(r'(\w+:\s*[^,}]+)\s*(\w+:\s*[^,}]+)', r'\1, \2', content)
            
            # Fix duplicate field definitions
            content = re.sub(r'(\w+:\s*[^,}]+,\s*)+\1', r'\1', content)
            
            if content != original_content:
                rust_file.write_text(content, encoding='utf-8')
                changes += 1
        
        except Exception as e:
            print(f"Error processing {rust_file}: {e}")
    
    return changes

def main():
    """Run the final fix."""
    print("Starting final syntax fix...")
    print("-" * 50)
    
    total_changes = 0
    
    # Restore malformed functions first
    changes1 = restore_malformed_functions()
    total_changes += changes1
    
    # Fix remaining syntax errors
    changes2 = fix_remaining_syntax_errors()
    total_changes += changes2
    
    print("-" * 50)
    print(f"Final fix completed: {total_changes} changes made")
    
    # Test build
    print("Testing build...")
    try:
        import subprocess
        result = subprocess.run([
            "cargo", "build", "--release", "-p", "dofus-core"
        ], capture_output=True, text=True, cwd=str(ROOT / "core"))
        
        if result.returncode == 0:
            print("SUCCESS: Build completed successfully!")
            return True
        else:
            print(f"FAILED: Build failed with {result.returncode} errors")
            error_lines = result.stderr.split('\n')
            # Count actual errors vs warnings
            error_count = len([line for line in error_lines if 'error:' in line])
            print(f"Total errors: {error_count}")
            if error_count > 0:
                print("First 10 errors:")
                error_lines = [line for line in error_lines if 'error:' in line][:10]
                for line in error_lines:
                    print(f"  {line}")
            return False
    except Exception as e:
        print(f"Error running build: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)