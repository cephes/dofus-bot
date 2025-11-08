import os
import re
from pathlib import Path

# Fix all remaining files with the "struct{}" pattern issues
generated_dir = Path("core/src/retroproto_parsers/generated")
fixed_count = 0

for rust_file in generated_dir.rglob("*.rs"):
    try:
        with open(rust_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if this file has the same broken pattern
        if '// This Go message is struct{}\n' in content and '}; payload is expected to be empty.' in content:
            # Get the struct name
            struct_match = re.search(r'pub struct (\w+) \{\}', content)
            if struct_match:
                struct_name = struct_match.group(1)
                
                # Fix the file with proper structure
                fixed_content = f"""use serde{{Serialize, Deserialize}};
use serde_json{{Value, json}};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct {struct_name} {{}}

pub fn parse_{struct_name}(payload: &str) -> Result<{struct_name}, String> {{
    // This Go message is struct{{}}; payload is expected to be empty.
    let p = payload.trim_matches('\0').trim();
    if p.is_empty() {{
        Ok({struct_name} {{}})
    }} else {{
        // Some variants ignore payload in Go; we still succeed but you can switch to strict:
        // return Err(format!("expected empty payload for {struct_name}, got: {{}}", p));
        Ok({struct_name} {{}})
    }}
}}

pub fn {struct_name}_to_json(m: &{struct_name}) -> Value {{ json!(m) }}"""
                
                content = fixed_content
        
        if content != original_content:
            with open(rust_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {rust_file}")
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {rust_file}: {e}")

print(f"Fixed {fixed_count} files")