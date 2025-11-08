import re, json, os, sys, argparse, pathlib
from collections import defaultdict, OrderedDict

# --- Helpers --------------------------------------------------------------

def slurp(p):
    try:
        return pathlib.Path(p).read_text(encoding="utf-8", errors="ignore")
    except:
        return ""

def load_json_safely(p):
    """Load JSON file safely, return empty dict if missing or invalid."""
    try:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}

def ensure_dir(p):
    pathlib.Path(p).mkdir(parents=True, exist_ok=True)

def guess_rust_type(go_hint):
    go_hint = (go_hint or "").lower()
    if go_hint in ("int","int32","int64","uint","uint32","uint64"):
        return "i64"
    if go_hint in ("bool",):
        return "bool"
    # default
    return "String"

def lower_first(s):
    return s[:1].lower() + s[1:] if s else s

def sanitize_ident(s):
    return s.replace("-", "_").replace("|", "_")

# --- GA Action Parser Generation -----------------------------------------

def gen_game_action_parser(action_code, action_type):
    """Generate a parser for a specific Game Action code"""
    struct_name = f"{action_type.capitalize()}Action_{action_code}"
    
    # Define fields based on action code
    if action_code == 0:  # Default
        fields = {}
    elif action_code == 1:  # Movement
        fields = {"dir_and_cells": "Vec<String>"}
    elif action_code == 2:  # LoadGameMap  
        fields = {"sprite_id": "i64", "cinematic": "String"}
    elif action_code == 900:  # Challenge
        fields = {"challenger_id": "i64", "challenged_id": "i64"}
    elif action_code == 901:  # ChallengeAccept
        fields = {"challenger_id": "i64", "challenged_id": "i64"}
    elif action_code == 902:  # ChallengeRefuse
        fields = {"challenger_id": "i64", "challenged_id": "i64"}
    elif action_code == 903:  # ChallengeJoin
        fields = {"challenger_id": "i64", "error_reason": "String"}
    else:
        fields = {"raw_data": "String"}
    
    lines = []
    lines.append(f"// AUTO-GENERATED Game Action Parser for code {action_code}")
    lines.append("use serde_json::Value;")
    lines.append("")
    lines.append(f"#[derive(Debug, Clone, serde::Serialize)]")
    lines.append(f"pub struct {struct_name} {{")
    for f, t in fields.items():
        lines.append(f"    pub {f}: {t},")
    lines.append("}")
    lines.append("")
    # Fix function name to use proper snake_case with game_action/cli_action naming
    if action_type and action_type.lower() == "game":
        fn_name = f"parse_game_action_{action_code}"
    elif action_type and action_type.lower() == "cli":
        fn_name = f"parse_cli_action_{action_code}"
    else:
        fn_name = f"parse_{sanitize_ident(struct_name).lower()}"
    lines.append(f"pub fn {fn_name}(extra: &str) -> Result<{struct_name}, String> {{")
    lines.append("    let payload = extra.trim();")
    
    if not fields:
        # Empty struct
        lines.append(f"    Ok({struct_name} {{")
        lines.append("    })")
    elif action_code == 1:  # Movement - special handling for dirAndCells
        lines.append("    let cells: Vec<String> = if payload.is_empty() {")
        lines.append("        vec![]")
        lines.append("    } else {")
        lines.append("        payload.chars()")
        lines.append("            .collect::<Vec<_>>()")
        lines.append("            .chunks(3)")
        lines.append("            .map(|chunk| chunk.iter().collect::<String>())")
        lines.append("            .collect()")
        lines.append("    };")
        lines.append(f"    Ok({struct_name} {{")
        lines.append("        dir_and_cells: cells,")
        lines.append("    })")
    elif action_code == 2:  # LoadGameMap
        lines.append("    let parts: Vec<&str> = if payload.is_empty() {")
        lines.append("        vec![]")
        lines.append("    } else {")
        lines.append("        payload.split(';').collect()")
        lines.append("    };")
        lines.append(f"    Ok({struct_name} {{")
        lines.append("        sprite_id: parts.get(0).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),")
        lines.append("        cinematic: parts.get(1).map(|s| s.to_string()).unwrap_or_default(),")
        lines.append("    })")
    else:
        # Generic split parsing
        lines.append("    let parts: Vec<&str> = if payload.is_empty() {")
        lines.append("        vec![]")
        lines.append("    } else {")
        lines.append("        payload.split(';').collect()")
        lines.append("    };")
        lines.append(f"    Ok({struct_name} {{")
        
        field_idx = 0
        for f, t in fields.items():
            if t == "i64":
                lines.append(f"        {f}: parts.get({field_idx}).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default(),")
            elif t == "Vec<String>":
                lines.append(f"        {f}: parts.get({field_idx}).map(|s| s.to_string()).unwrap_or_default(),")
            else:
                lines.append(f"        {f}: parts.get({field_idx}).map(|s| s.to_string()).unwrap_or_default(),")
            field_idx += 1
        lines.append("    })")
    
    lines.append("}")
    lines.append("")
    # Fix JSON function name to use proper snake_case with game_action/cli_action naming
    if action_type and action_type.lower() == "game":
        json_fn_name = f"game_action_{action_code}_to_json"
    elif action_type and action_type.lower() == "cli":
        json_fn_name = f"cli_action_{action_code}_to_json"
    else:
        json_fn_name = f"{sanitize_ident(struct_name).lower()}_to_json"
    lines.append(f"pub fn {json_fn_name}(m: &{struct_name}) -> Value {{")
    lines.append("    serde_json::json!({")
    
    for f, t in fields.items():
        if t == "Vec<String>":
            lines.append(f"        {f}: m.{f},")
        else:
            lines.append(f"        {f}: m.{f},")
    lines.append("    })")
    lines.append("}}")
    
    return "\n".join(lines)

# --- Mapping loader -------------------------------------------------------

def load_mapping(mapping_json_path, mappings_txt_path):
    mapping = OrderedDict()
    if mapping_json_path and os.path.exists(mapping_json_path):
        data = json.loads(slurp(mapping_json_path) or "{}")
        for e in data.get("entries", []):
            pref = e.get("prefix")
            name = e.get("message_name")
            if pref and name:
                mapping[pref] = name
    if not mapping and mappings_txt_path and os.path.exists(mappings_txt_path):
        # parse lines like:   AksHelloConnect         MsgSvrId = "HC"
        txt = slurp(mappings_txt_path)
        r1 = re.compile(r'^\s*([A-Za-z0-9_?+\-]+)\s+MsgSvrId\s*=\s*"([^"]+)"', re.M)
        r2 = re.compile(r'^\s*([A-Za-z0-9_?+\-]+)\s*=\s*MsgCliId\("([^"]+)"\)', re.M)
        for m in r1.findall(txt):
            mapping[m[1]] = m[0]
        for m in r2.findall(txt):
            mapping[m[1]] = m[0]
    return mapping

# --- Go source scanning (heuristic, regex-based) --------------------------

import os as _os_porter_regex_fix
import re as _re_empty_struct_guard  # idempotent import across runs
# Permissive, *non*-anchored struct regex: scan whole file, allow comments/whitespace before/after.
# Matches both `struct{}` and `struct { ... }`. Use non-greedy body to the first matching '}'.
GO_STRUCT_RE = _re_empty_struct_guard.compile(
    r'''(?isx)                 # ignorecase off; dotall; verbose
        \btype \s+             # 'type' keyword
        (?P<name>[A-Za-z_][A-Za-z0-9_]*) \s+
        struct \s* \{          # 'struct {'
        (?P<body>.*?)          # body may be empty; non-greedy to first }
        \}                     # closing brace
    '''
)

def _normalize_newlines(text: str) -> str:
    # Normalize CRLF to LF and strip BOM if present.
    if text and text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    return text.replace("\r\n", "\n").replace("\r", "\n")

def _extract_go_struct(src_text, filepath=None):
    """
    Return (name, fields_text_or_empty) for the best `type Name struct{...}` in the file.
    Selection preference:
      1) Name equal to Go filename in PascalCase (e.g. mountcastrate.go -> MountCastrate)
      2) Presence of New<Name>/Deserialize methods
      3) First match in file
    """
    text = _normalize_newlines(src_text)
    cands = []  # (score, -pos, name, body)
    pascal_from_file = None
    if filepath:
        base = _os_porter_regex_fix.path.basename(filepath)
        if base.lower().endswith(".go"):
            stem = base[:-3]
            # snake/kebab/mixed -> PascalCase best-effort
            parts = _re_empty_struct_guard.split(r'[_\-\.]', stem)
            pascal_from_file = "".join(p[:1].upper()+p[1:] for p in parts if p)
    for m in GO_STRUCT_RE.finditer(text):
        name = m.group('name')
        pos = m.start()
        score = 0
        if pascal_from_file and name == pascal_from_file:
            score += 10  # strong filename bias
        if _re_empty_struct_guard.search(rf'func\s+New{name}\s*\(', text):
            score += 2
        if _re_empty_struct_guard.search(rf'func\s+\(\s*\*?{name}\s*\)\s*Deserialize\s*\(', text):
            score += 3
        cands.append((score, -pos, name, m.group('body')))
    if not cands:
        # Fallback: if we can prove message existence via methods, assume empty struct.
        # Try to infer <Name> from filename for zero-field types like MountCastrate.
        if pascal_from_file and (_re_empty_struct_guard.search(rf'func\s+New{pascal_from_file}\s*\(', text) or
                                 _re_empty_struct_guard.search(rf'func\s+\(\s*\*?{pascal_from_file}\s*\)\s*Deserialize\s*\(', text)):
            return (pascal_from_file, "")
        return None
    cands.sort(reverse=True)
    _, _, name, body = cands[0]
    return (name, body)

FIELD_RE = re.compile(
    r'(?P<fname>[A-Za-z0-9_]+)\s+(?P<ftype>[A-Za-z0-9_\*\[\]]+)\s*(?:`[^`]*`)?\s*$'
)

# Capture Deserialize(extra string) receiver *Type and body
DESER_RE = re.compile(
    r'func\s*\(\s*\*\s*(?P<recv>[A-Za-z0-9_]+)\s*\)\s*Deserialize\s*\(\s*extra\s+string\s*\)\s*error\s*\{(?P<body>.*?)\}',
    re.S
)

def parse_structs(go_text):
    msgs = {}
    # Use the new struct extraction for all structs in the file
    for m in GO_STRUCT_RE.finditer(go_text):
        name = m.group('name')
        body = (m.group('body') or '').strip()
        fields = OrderedDict()
        for line in body.splitlines():
            line = line.strip()
            if not line or line.startswith("//"): continue
            fm = FIELD_RE.match(line)
            if fm:
                fields[fm.group("fname")] = guess_rust_type(fm.group("ftype"))
        # Now, even if fields is empty, we consider it a valid struct
        msgs[name] = {"fields": fields, "assignments": [], "delims": []}
    # Deserialize captures
    for dm in DESER_RE.finditer(go_text):
        recv = dm.group("recv")
        body = dm.group("body")
        if recv not in msgs:
            msgs[recv] = {"fields": OrderedDict(), "assignments": [], "delims": []}
        # direct assignment m.Field = extra
        for am in re.finditer(r'm\.(?P<f>[A-Za-z0-9_]+)\s*=\s*extra', body):
            msgs[recv]["assignments"].append(f"assign:{am.group('f')}=extra")
        # detect splits on extra
        for sm in re.finditer(r'strings\.SplitN?\(\s*extra\s*,\s*"([^"]+)"', body):
            d = sm.group(1)
            if d not in msgs[recv]["delims"]:
                msgs[recv]["delims"].append(d)
        # map parts[...] to fields
        for pm in re.finditer(r'm\.(?P<f>[A-Za-z0-9_]+)\s*=\s*(?:strconv\.\w+\()?\s*parts\[(?P<i>\d+)\]', body):
            msgs[recv]["assignments"].append(f"parts:{pm.group('f')}={pm.group('i')}")
        # booleans like m.Flag = (parts[i] == "1")
        for bm in re.finditer(r'm\.(?P<f>[A-Za-z0-9_]+)\s*=\s*\(?\s*parts\[(?P<i>\d+)\]\s*==\s*"(?P<val>[^"]+)"\)?', body):
            msgs[recv]["assignments"].append(f"bool:{bm.group('f')}={bm.group('i')}=={bm.group('val')}")
    return msgs

# --- Rust code generation -------------------------------------------------

def gen_rust_for_message(name, spec):
    struct_name = name
    fields = spec.get("fields", {})
    assigns = spec.get("assignments", [])
    delims = spec.get("delims", []) or ["|"]  # default first-level delimiter

    lines = []
    lines.append(f"// AUTO-GENERATED from retroproto Go: {name}")
    lines.append("use serde::{Serialize, Deserialize};")
    lines.append("use serde_json::{Value, json};")
    lines.append("")
    lines.append(f"#[derive(Debug, Clone, Serialize, Deserialize)]")
    lines.append(f"pub struct {struct_name} {{")
    for f, t in fields.items():
        lines.append(f"  pub {lower_first(f)}: {t},")
    lines.append("}")
    lines.append("")
    fn_name = f"parse_{sanitize_ident(name)}"
    lines.append(f"pub fn {fn_name}(payload: &str) -> Result<{struct_name}, String> {{")
    lines.append("  let p = payload.trim_end_matches('\\0');")

    # If single-field and assign:extra, just assign
    single_field = list(fields.keys())[0] if len(fields)==1 else None
    if single_field and any(a.startswith("assign:"+single_field+"=extra") for a in assigns):
        lines.append(f"  Ok({struct_name} {{ {lower_first(single_field)}: p.to_string() }})")
        lines.append("}")
        lines.append("")
        lines.append(f"pub fn {sanitize_ident(name)}_to_json(m: &{struct_name}) -> Value {{ json!(m) }}")
        return "\n".join(lines)

    # Otherwise, split on primary delimiter and map by assignments if present
    primary = delims[0]
    lines.append(f"  let parts: Vec<&str> = if p.is_empty() {{ vec![] }} else {{ p.split({primary!r}).collect() }};")

    # Build field initializers
    init = []
    index_map = {}
    for a in assigns:
        if a.startswith("parts:"):
            f, i = a.split(":",1)[1].split("=")
            index_map[f] = int(i)
    # construct with best-effort by index order
    i = 0
    for f, t in fields.items():
        if f in index_map:
            idx = index_map[f]
        else:
            idx = i
        if t == "i64":
            init.append(f" {lower_first(f)}: parts.get({idx}).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default()")
        elif t == "bool":
            init.append(f" {lower_first(f)}: parts.get({idx}).map(|s| *s == \"1\" || *s == \"true\").unwrap_or(false)")
        else:
            init.append(f" {lower_first(f)}: parts.get({idx}).map(|s| s.to_string()).unwrap_or_default()")
        i += 1

    lines.append(f"  Ok({struct_name} {{" + ",".join(init) + " }})")
    lines.append("}")
    lines.append("")
    lines.append(f"pub fn {sanitize_ident(name)}_to_json(m: &{struct_name}) -> Value {{ json!(m) }}")
    return "\n".join(lines)

def emit_empty_struct_parser(msg_name, category, prefix):
    rust = f'''
use serde::{{Serialize, Deserialize}};
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct {msg_name} {{}}

pub fn parse_{sanitize_ident(msg_name)}(payload: &str) -> Result<{msg_name}, String> {{
    // This Go message is struct{{}}; payload is expected to be empty.
    let p = payload.trim_matches('\\0').trim();
    if p.is_empty() {{
        Ok({msg_name}{{}})
    }} else {{
        // Some variants ignore payload in Go; we still succeed but you can switch to strict:
        // return Err(format!("expected empty payload for {msg_name}, got: {{}}", p));
        Ok({msg_name}{{}})
    }}
}}
'''
    return rust

# --- Main -----------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tp", default="third_party/retroproto")
    ap.add_argument("--out", default="core/src/retroproto_parsers/generated")
    ap.add_argument("--actions_out", default="core/src/retroproto_parsers/generated/actions")
    ap.add_argument("--mapping", default="third_party/retroproto/mapping_overrides.json")
    ap.add_argument("--mappings_txt", default="third_party/retroproto/mappings_go.txt")
    ap.add_argument("--go-struct-hits", default="tools/out/go_struct_hits.json",
                   help="JSON file with Go struct discovery results for targeted generation")
    ap.add_argument("--targeted-only", action="store_true",
                   help="Only process messages found in go-struct-hits file")
    args = ap.parse_args()

    ensure_dir(args.out)
    ensure_dir(args.actions_out)

    # Load Go struct discovery results for targeted mode
    go_struct_hits = load_json_safely(args.go_struct_hits)
    target_messages = set()
    if args.targeted_only and go_struct_hits:
        target_messages = set(go_struct_hits.keys())
        print(f"Targeted mode: will process {len(target_messages)} messages from go-struct-hits")
        for msg in sorted(target_messages):
            print(f"  - {msg}")

    mapping = load_mapping(args.mapping, args.mappings_txt)
    
    # Collect sources
    sources = []
    for sub in ("msgsvr", "msgcli"):
        d = os.path.join(args.tp, sub)
        if os.path.isdir(d):
            for root, _, files in os.walk(d):
                for fn in files:
                    if fn.endswith(".go"):
                        sources.append(os.path.join(root, fn))

    report = {
        "generated": [],
        "todos": {},
        "errors": [],
        "mapping_count": len(mapping),
        "source_files": len(sources),
        "action_parsers_generated": 0,
        "action_parsers_todo": 0,
        "action_codes_detected": []
    }

    # Generate GA action parsers
    action_codes = [0, 1, 2, 900, 901, 902, 903]  # Based on GameActionType enum
    action_parsers_generated = 0
    action_parsers_todo = 0
    action_codes_detected = []

    for code in action_codes:
        # Generate server action parser
        action_name = f"GameAction_{code}"
        action_file = os.path.join(args.actions_out, f"{action_name}.rs")
        action_code = gen_game_action_parser(code, "game")
        pathlib.Path(action_file).write_text(action_code, encoding="utf-8")
        report["generated"].append(action_file)
        
        # Generate client action parser  
        client_action_name = f"CliAction_{code}"
        cli_action_file = os.path.join(args.actions_out, f"{client_action_name}.rs")
        cli_action_code = gen_game_action_parser(code, "cli")
        pathlib.Path(cli_action_file).write_text(cli_action_code, encoding="utf-8")
        report["generated"].append(cli_action_file)
        
        action_parsers_generated += 2
        action_codes_detected.append(code)

    # Write actions module
    actions_mod_path = os.path.join(args.actions_out, "mod.rs")
    actions_mod_lines = ["// AUTO-GENERATED GameAction parsers"]
    for code in action_codes:
        actions_mod_lines.append(f"pub mod GameAction_{code};")
        actions_mod_lines.append(f"pub mod CliAction_{code};")
        actions_mod_lines.append(f"pub use GameAction_{code}::*;")
        actions_mod_lines.append(f"pub use CliAction_{code}::*;")
    pathlib.Path(actions_mod_path).write_text("\n".join(actions_mod_lines) + "\n", encoding="utf-8")

    report["action_parsers_generated"] = action_parsers_generated
    report["action_parsers_todo"] = action_parsers_todo
    report["action_codes_detected"] = action_codes_detected

    # Parse all Go files for structs + Deserialize hints
    merged_specs = {}
    for p in sources:
        txt = slurp(p)
        specs = parse_structs(txt)
        for name, spec in specs.items():
            if name not in merged_specs:
                merged_specs[name] = spec
            else:
                # merge fields/assigns/delims
                merged_specs[name]["fields"].update(spec.get("fields", {}))
                merged_specs[name]["assignments"] += spec.get("assignments", [])
                for d in spec.get("delims", []):
                    if d not in merged_specs[name]["delims"]:
                        merged_specs[name]["delims"].append(d)

    # Generate Rust per message that appears in mapping (ensures we only emit what decoder may call)
    mod_lines = ["// AUTO-GENERATED registry",]
    export_lines = []
    processed_count = 0
    
    for pref, msg_name in mapping.items():
        # Skip if in targeted mode and not in target list
        if args.targeted_only and target_messages and msg_name not in target_messages:
            continue
            
        spec = merged_specs.get(msg_name)
        out_path = os.path.join(args.out, f"{msg_name}.rs")
        
        if not spec:
            # generate minimal stub to unblock build
            code = f"""// AUTO-GENERATED STUB (no struct found) for {msg_name}
use serde_json::{{Value, json}};
pub fn parse_{sanitize_ident(msg_name)}(payload: &str) -> Result<Value, String> {{
  let p = payload.trim_end_matches('\\0');
  Ok(json!({{ "message":"{msg_name}", "payload": p }}))
}}
"""
            pathlib.Path(out_path).write_text(code, encoding="utf-8")
            report["todos"][msg_name] = "No struct found in Go; emitted JSON stub parser."
        else:
            fields = spec.get("fields", {})
            if not fields:
                # Zero-field struct: generate a typed empty parser.
                code = emit_empty_struct_parser(msg_name, pref, pref)
                pathlib.Path(out_path).write_text(code, encoding="utf-8")
                note = "Struct has 0 fields; emitted empty typed parser."
                report.setdefault('notes', {})[msg_name] = note
            else:
                code = gen_rust_for_message(msg_name, spec)
                pathlib.Path(out_path).write_text(code, encoding="utf-8")
        report["generated"].append(out_path)
        mod_lines.append(f"pub mod {msg_name};")
        export_lines.append(f"pub use {msg_name}::*;")
        processed_count += 1

    # Write mod.rs
    pathlib.Path(os.path.join(args.out,"mod.rs")).write_text(
        "\n".join(mod_lines + export_lines) + "\n", encoding="utf-8"
    )

    # Write manifests
    pathlib.Path(os.path.join(args.out,"mapping_manifest.json")).write_text(
        json.dumps(mapping, indent=2), encoding="utf-8"
    )
    pathlib.Path(os.path.join(args.out,"generation_report.json")).write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    print("Generation finished.")
    print(json.dumps({
        "generated_count": len(report["generated"]),
        "processed_count": processed_count,
        "stubs": len(report["todos"]),
        "mapping_count": len(mapping),
        "targeted_mode": args.targeted_only,
        "action_parsers_generated": report["action_parsers_generated"],
        "action_parsers_todo": report["action_parsers_todo"]
    }, indent=2))

if __name__ == "__main__":
    main()