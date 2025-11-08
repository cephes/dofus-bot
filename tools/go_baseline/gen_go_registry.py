#!/usr/bin/env python3
"""
Go Registry Generator

Scans third_party/retroproto/msgsvr and msgcli to build a registry of message parsers.
Generates a Go file that maps message names to parse functions.
"""

import os
import re
import argparse
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json

# Compute paths relative to this script's location
SCRIPT_DIR = Path(__file__).resolve().parent
# From tools/go_baseline, go up to project root (dofus-bot directory)
REPO_ROOT = SCRIPT_DIR.parent.parent
RETROPROTO = REPO_ROOT / "third_party" / "retroproto"
MSGSVR = RETROPROTO / "msgsvr"
MSGCLI = RETROPROTO / "msgcli"

class GoMessageParser:
    """Represents a parsed Go message and its parsing method."""
    
    def __init__(self, name: str, package: str, file_path: str, parse_method: str, import_path: str):
        self.name = name
        self.package = package  # msgcli or msgsvr
        self.file_path = file_path
        self.parse_method = parse_method  # "func", "method", or "package"
        self.import_path = import_path  # for go import statement
        self.function_call = self._build_function_call()
    
    def _build_function_call(self) -> str:
        """Build the Go function call string for the registry."""
        if self.parse_method == "constructor":
            return f"New{self.name}(s)"
        elif self.parse_method == "func":
            return f"Parse{self.name}(s)"
        elif self.parse_method == "method":
            return f"parseWithMethod{self.name}(s)"
        else:  # package
            return f"Parse{self.name}(s)"
    
    def __repr__(self):
        return f"GoMessageParser({self.name}, {self.package}, {self.parse_method})"


def find_go_files(directory: str) -> List[str]:
    """Find all .go files in the given directory recursively."""
    go_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.go') and not file.endswith('_test.go'):
                go_files.append(os.path.join(root, file))
    return go_files


def extract_message_info(file_path: str) -> Optional[Tuple[str, str]]:
    """
    Extract message name and package from a Go file.
    Returns (message_name, package_name) or None if not a message file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return None
    
    # Look for type declaration
    type_match = re.search(r'type\s+(\w+)\s+struct\s*{', content)
    if not type_match:
        return None
    
    message_name = type_match.group(1)
    
    # Check if this looks like a message file (has Deserialize method or New* function)
    has_new = 'New' + message_name in content
    has_deserialize = 'Deserialize' in content
    
    if has_new and has_deserialize:
        # Extract package name
        package_match = re.search(r'package\s+(\w+)', content)
        if package_match:
            return (message_name, package_match.group(1))
    
    return None


def find_parse_methods(file_path: str, message_name: str, package: str) -> List[Tuple[str, str]]:
    """
    Find parse methods for a message.
    Returns list of (method_type, function_signature) tuples.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return []
    
    methods = []
    
    # Pattern 1: func New<MessageName>(extra string) (MessageName, error)
    new_pattern = rf'func\s+New{message_name}\s*\(\s*extra\s+string\s*\)\s*\(\s*{message_name}\s*,\s*error\s*\)'
    if re.search(new_pattern, content):
        methods.append(("constructor", f"New{message_name}(extra string) ({message_name}, error)"))
    
    # Pattern 2: func (<Type>) Deserialize(extra string) error
    method_pattern = rf'func\s*\(\s*\w+\s+{message_name}\s*\)\s+Deserialize\s*\(\s*extra\s+string\s*\)\s+error'
    if re.search(method_pattern, content):
        methods.append(("deserialize", f"({message_name}) Deserialize(extra string) error"))
    
    # Pattern 3: Look for existing Parse functions (fallback)
    parse_pattern = rf'func\s+Parse{message_name}\s*\('
    if re.search(parse_pattern, content):
        methods.append(("parsefunc", f"Parse{message_name}(s string) (...)"))
    
    return methods


def build_registry(msgsvr_dir: str, msgcli_dir: str, dry_run: bool = False, prefer_server: bool = True) -> Dict[str, GoMessageParser]:
    """
    Build the message parser registry by scanning both directories.
    """
    registry = {}
    
    # Scan msgsvr first if prefer_server
    if prefer_server:
        dirs = [(msgsvr_dir, "msgsvr"), (msgcli_dir, "msgcli")]
    else:
        dirs = [(msgcli_dir, "msgcli"), (msgsvr_dir, "msgsvr")]
    
    for directory, package_prefix in dirs:
        if not os.path.exists(directory):
            if not dry_run:
                print(f"Warning: Directory {directory} not found")
            continue
            
        go_files = find_go_files(directory)
        print(f"Scanning {directory} - found {len(go_files)} .go files")
        
        for file_path in go_files:
            file_rel_path = os.path.relpath(file_path, directory)
            package_name = os.path.dirname(file_rel_path).replace(os.sep, '/')
            
            if package_name and package_name != '.':
                import_path = f"{package_prefix}/{package_name}"
            else:
                import_path = package_prefix
            
            message_info = extract_message_info(file_path)
            if not message_info:
                continue
            
            message_name, package = message_info
            
            # Skip if we already have this message and prefer_server
            if message_name in registry and prefer_server:
                continue
            
            parse_methods = find_parse_methods(file_path, message_name, package)
            
            if parse_methods:
                # Use the first (preferred) method
                method_type, method_sig = parse_methods[0]
                parser = GoMessageParser(
                    name=message_name,
                    package=package,
                    file_path=file_path,
                    parse_method=method_type,
                    import_path=import_path
                )
                registry[message_name] = parser
                if dry_run:
                    print(f"  Found: {message_name} ({method_type}) in {file_rel_path}")
    
    return registry


def generate_go_registry(registry: Dict[str, GoMessageParser], output_file: str):
    """Generate the Go registry file."""
    
    # Organize imports by package
    imports = {}
    for parser in registry.values():
        if parser.import_path not in imports:
            imports[parser.import_path] = []
        imports[parser.import_path].append(parser)
    
    # Start building the Go file
    lines = [
        "package main",
        ""
    ]
    
    # Add imports for each package
    if imports:
        lines.append("import (")
        for import_path in sorted(imports.keys()):
            lines.append(f'	"github.com/kralamoure/retroproto/{import_path}"')
        lines.append(")")
        lines.append("")
    
    # Add type definitions and wrapper functions
    lines.append("// ParserFn is the signature for message parser functions")
    lines.append("type ParserFn func(s string) (interface{}, error)")
    lines.append("")
    
    # Add wrapper functions for method-based parsers
    method_parsers = [p for p in registry.values() if p.parse_method == "method"]
    if method_parsers:
        lines.append("// Wrapper functions for method-based parsers")
        for parser in method_parsers:
            lines.append(f"func parseWithMethod{parser.name}(s string) (interface{{}}, error) {{")
            lines.append(f"	var msg {parser.import_path}.{parser.name}")
            lines.append(f"	if err := msg.FromString(s); err != nil {{")
            lines.append(f"		return nil, err")
            lines.append(f"	}}")
            lines.append(f"	return &msg, nil")
            lines.append("}")
            lines.append("")
    
    # Build the registry map
    lines.append("// Registry contains all message parsers")
    lines.append("var Registry = map[string]ParserFn{")
    
    for message_name in sorted(registry.keys()):
        parser = registry[message_name]
        
        # Add comment with file info
        rel_path = os.path.relpath(parser.file_path, str(RETROPROTO))
        lines.append(f"	// {message_name} - {rel_path}")
        
        if parser.parse_method == "method":
            lines.append(f"	\"{message_name}\": parseWithMethod{message_name},")
        else:
            lines.append(f"	\"{message_name}\": func(s string) (interface{{}}, error) {{")
            lines.append(f"		return {parser.import_path}.{parser.function_call}")
            lines.append(f"	}},")
        
        lines.append("")
    
    lines.append("}")
    lines.append("")
    
    # Add utility function to get all message names
    lines.append("// GetMessageNames returns all registered message names")
    lines.append("func GetMessageNames() []string {")
    lines.append("	names := make([]string, 0, len(Registry))")
    lines.append("	for name := range Registry {")
    lines.append("		names = append(names, name)")
    lines.append("	}")
    lines.append("	return names")
    lines.append("}")
    lines.append("")
    
    # Write the file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Generated registry file: {output_file}")
    print(f"Total parsers registered: {len(registry)}")


def main():
    parser = argparse.ArgumentParser(description="Generate Go message parser registry")
    parser.add_argument("--msgsvr", default="../../third_party/retroproto/msgsvr",
                       help="Path to msgsvr directory")
    parser.add_argument("--msgcli", default="../../third_party/retroproto/msgcli",
                       help="Path to msgcli directory")
    parser.add_argument("--out", default="registry.go",
                       help="Output file for generated registry")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be found without generating files")
    parser.add_argument("--prefer-server", action="store_true", default=True,
                       help="Prefer server (msgsvr) parsers over client (msgcli) for same message")
    parser.add_argument("--json-out", 
                       help="Output registry info as JSON for debugging")
    
    args = parser.parse_args()
    
    # Assert that the required directories exist, using script-relative paths
    if not MSGSVR.exists():
        print(f"ERROR: MSGSVR directory not found: {MSGSVR}")
        return 1
    if not MSGCLI.exists():
        print(f"ERROR: MSGCLI directory not found: {MSGCLI}")
        return 1
    
    # Use script-relative paths if no explicit paths provided
    msgsvr_dir = args.msgsvr if args.msgsvr != "../../third_party/retroproto/msgsvr" else str(MSGSVR)
    msgcli_dir = args.msgcli if args.msgcli != "../../third_party/retroproto/msgcli" else str(MSGCLI)
    
    # Build the registry
    registry = build_registry(msgsvr_dir, msgcli_dir, args.dry_run, args.prefer_server)
    
    if args.json_out:
        # Output debug info as JSON
        debug_info = {}
        for name, parser in registry.items():
            debug_info[name] = {
                "package": parser.package,
                "file_path": parser.file_path,
                "parse_method": parser.parse_method,
                "import_path": parser.import_path,
                "function_call": parser.function_call
            }
        
        with open(args.json_out, 'w', encoding='utf-8') as f:
            json.dump(debug_info, f, indent=2)
        print(f"Debug info written to: {args.json_out}")
    
    if not args.dry_run:
        # Generate the Go registry file
        generate_go_registry(registry, args.out)
    else:
        print(f"Dry run complete. Would register {len(registry)} message parsers.")


if __name__ == "__main__":
    main()