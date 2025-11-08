#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, json, shutil, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GO_DIRS = [ROOT / "third_party" / "retroproto" / "msgsvr",
           ROOT / "third_party" / "retroproto" / "msgcli"]
RUST_GEN_DIR = ROOT / "core" / "src" / "retroproto_parsers" / "generated"
ARCHIVE_BASE = ROOT / ".archive" / time.strftime("%Y%m%d_%H%M%S")

GO_STRUCT_RE = re.compile(r"type\s+(?P<name>[A-Za-z0-9_]+)\s+struct\s*{\s*(?P<body>.*?)\s*}", re.S)
GO_FIELD_RE  = re.compile(r"(?P<fname>[A-Za-z0-9_]+)\s+(?P<ftype>[\[\]A-Za-z0-9_*]+)")

def log(msg):
    print(msg, flush=True)

def archive_before_edit(p: Path):
    dst = ARCHIVE_BASE / p.relative_to(ROOT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        shutil.copy2(p, dst)

def find_go_file(msg_name: str):
    # heuristics: try <Name>.go, lowercase variations, and grep inside candidates
    candidates = []
    leafs = [f"{msg_name}.go", f"{msg_name.lower()}.go"]
    for gd in GO_DIRS:
        for leaf in leafs:
            p = gd / leaf
            if p.exists():
                return p
        # fallback: scan all .go files for "type <Name> struct"
        for p in gd.glob("*.go"):
            try:
                txt = p.read_text(encoding="utf-8", errors="replace")
            except:
                continue
            if re.search(rf"type\s+{re.escape(msg_name)}\s+struct", txt):
                candidates.append(p)
    return candidates[0] if candidates else None

def parse_go_struct(path: Path, msg_name: str):
    txt = path.read_text(encoding="utf-8", errors="replace")
    m = None
    for m0 in GO_STRUCT_RE.finditer(txt):
        if m0.group("name") == msg_name:
            m = m0
            break
    if not m:
        return []
    body = m.group("body")
    fields = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        m1 = GO_FIELD_RE.match(line)
        if not m1:
            continue
        fname = m1.group("fname")
        ftype = m1.group("ftype")
        fields.append((fname, ftype))
    return fields

def go_type_to_rust(go_t: str):
    go_t = go_t.strip()
    vec = False
    elem = None
    if go_t.startswith("[]"):
        vec = True
        elem = go_t[2:]
        rt, _ = go_type_to_rust(elem)
        return (f"Vec<{rt}>", rt)
    basemap = {
        "int":"i64","int32":"i64","int64":"i64",
        "uint":"i64","uint32":"i64","uint64":"i64",
        "string":"String","bool":"bool",
        "float32":"f64","float64":"f64",
    }
    # pointer types
    if go_t.startswith("*"):
        return ("String", None)
    # strip package prefixes if any (e.g., typ.Foo)
    if "." in go_t:
        t = go_t.split(".")[-1]
        return ("String", None) if t not in basemap else (basemap[t], None)
    return (basemap.get(go_t, "String"), None)

def rust_struct_fields(name: str, fields):
    lines = []
    lines.append("#[derive(Default, Debug, Clone, serde::Serialize, serde::Deserialize)]")
    lines.append(f"pub struct {name} {{")
    for (fname, go_t) in fields:
        rt, _ = go_type_to_rust(go_t)
        # keep original field casing to match existing generated style
        lines.append(f"    pub {fname}: {rt},")
    lines.append("}")
    return "\n".join(lines)

def helper_fns():
    return r'''
fn to_i64(s: &str) -> i64 {
    s.trim().parse::<i64>().unwrap_or_default()
}
fn to_f64(s: &str) -> f64 {
    s.trim().parse::<f64>().unwrap_or_default()
}
fn to_bool(s: &str) -> bool {
    match s.trim() {
        "1" | "true" | "True" | "TRUE" => true,
        _ => false,
    }
}
fn split_csv(s: &str) -> Vec<&str> {
    if s.trim().is_empty() { return vec![]; }
    s.split(',').collect()
}
'''

def rust_parse_body(name: str, fields):
    # map tokens in order; default delimiter ';'
    map_lines = []
    map_lines.append("    let parts: Vec<&str> = payload.split(';').collect();")
    map_lines.append(f"    let mut out = {name}::default();")
    map_lines.append("    let mut idx = 0usize;")
    for (fname, go_t) in fields:
        rt, vec_elem = go_type_to_rust(go_t)
        map_lines.append(f"    // field: {fname} : {go_t} -> {rt}")
        if rt == "i64":
            map_lines.append(f"    out.{fname} = parts.get(idx).map(|s| to_i64(s)).unwrap_or_default();")
            map_lines.append( "    idx += 1;")
        elif rt == "f64":
            map_lines.append(f"    out.{fname} = parts.get(idx).map(|s| to_f64(s)).unwrap_or_default();")
            map_lines.append( "    idx += 1;")
        elif rt == "bool":
            map_lines.append(f"    out.{fname} = parts.get(idx).map(|s| to_bool(s)).unwrap_or(false);")
            map_lines.append( "    idx += 1;")
        elif rt.startswith("Vec<"):
            if vec_elem == "i64":
                map_lines.append(f"    out.{fname} = parts.get(idx).map(|s| split_csv(s).into_iter().map(|x| to_i64(x)).collect()).unwrap_or_else(|| vec![]);")
            elif vec_elem == "f64":
                map_lines.append(f"    out.{fname} = parts.get(idx).map(|s| split_csv(s).into_iter().map(|x| to_f64(x)).collect()).unwrap_or_else(|| vec![]);")
            else:
                map_lines.append(f"    out.{fname} = parts.get(idx).map(|s| split_csv(s).into_iter().map(|x| x.trim().to_string()).collect()).unwrap_or_else(|| vec![]);")
            map_lines.append( "    idx += 1;")
        else:
            map_lines.append(f"    out.{fname} = parts.get(idx).map(|s| s.trim().to_string()).unwrap_or_default();")
            map_lines.append( "    idx += 1;")
    map_lines.append("    Ok(out)")
    return "\n".join(map_lines)

def render_rust_file(name: str, fields):
    header = "// AUTO-GENERATED/UPDATED by tools/port_missing_parsers_from_go.py\n#![allow(non_snake_case, non_camel_case_types, unused_imports)]\nuse serde_json::Value;\n"
    struct_def = rust_struct_fields(name, fields)
    helpers = helper_fns()
    parse_fn = f"pub fn parse_{name}(payload: &str) -> Result<{name}, String> {{\n{rust_parse_body(name, fields)}\n}}\n"
    to_json = f"pub fn {name}_to_json(m: &{name}) -> Value {{ serde_json::to_value(m).unwrap_or(Value::Null) }}\n"
    return "\n\n".join([header, struct_def, helpers, parse_fn, to_json]) + "\n"

def merge_into_existing(existing: str, name: str, fields):
    # replace content of parse_<Name> with generated body; if missing, append fn
    body = f"pub fn parse_{name}(payload: &str) -> Result<{name}, String> {{\n{rust_parse_body(name, fields)}\n}}\n"
    if f"pub fn parse_{name}(" in existing:
        new = re.sub(rf"pub fn parse_{name}\([^\{{]+\{{.*?^\}}\n", body, existing, flags=re.S|re.M)
        if new != existing:
            return new
    # else append body + ensure struct exists
    if f"pub struct {name}" not in existing:
        existing = render_rust_file(name, fields)
    else:
        existing += "\n" + body
    return existing

def main():
    (ARCHIVE_BASE).mkdir(parents=True, exist_ok=True)
    plan_path = ROOT / "missing_parsers_plan.json"
    if not plan_path.exists():
        print(json.dumps({"error":"missing missing_parsers_plan.json"}))
        return
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    entries = plan.get("entries", [])
    ported, filled, errors = [], [], []
    for e in entries:
        act = e.get("action")
        name = e.get("message_name") or e.get("name")
        if not name or act not in ("PORT_GO_TO_RUST","FILL_FIELDS_IN_RUST_PARSER"):
            continue
        gofile = find_go_file(name)
        if not gofile:
            errors.append({"name":name, "error":"go source not found"})
            continue
        fields = parse_go_struct(gofile, name)
        if not fields:
            errors.append({"name":name, "error":"go struct not found"})
            continue
        out_rs = RUST_GEN_DIR / f"{name}.rs"
        if out_rs.exists():
            # fill fields
            archive_before_edit(out_rs)
            txt = out_rs.read_text(encoding="utf-8", errors="replace")
            new_txt = merge_into_existing(txt, name, fields)
            out_rs.write_text(new_txt, encoding="utf-8")
            filled.append(name)
        else:
            out_rs.parent.mkdir(parents=True, exist_ok=True)
            archive_before_edit(out_rs)
            out_rs.write_text(render_rust_file(name, fields), encoding="utf-8")
            ported.append(name)
    print(json.dumps({"ported":ported, "filled":filled, "errors":errors}, indent=2))

if __name__ == "__main__":
    main()