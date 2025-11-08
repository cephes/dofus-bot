# --- BEGIN FILE: tools/align_structs_only.py ---
import re, json, sys, os, pathlib
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
GO_ROOT = ROOT / "third_party" / "retroproto"
RUST_GEN = ROOT / "core" / "src" / "retroproto_parsers" / "generated"
CACHE = ROOT / "tools" / "_cache"
CACHE.mkdir(parents=True, exist_ok=True)
CACHE_FILE = CACHE / "go_structs.json"

STRUCT_RE = re.compile(r'(?ms)^\\s*type\\s+(?P<name>[A-Za-z0-9_]+)\\s+struct\\s*\\{(?P<body>.*?)\\}', re.M)
FIELD_RE = re.compile(r'(?m)^\\s*(?P<ident>[A-Za-z0-9_]+)\\s+(?P<typ>\\[\\][A-Za-z0-9_]+|[A-Za-z0-9_]+)')

def go2rust_ty(go):
    g = go.replace("[]", "slice:")
    if g in ("int","int32","int64"): return "i64"
    if g in ("string",): return "String"
    if g in ("bool",): return "bool"
    if g.startswith("slice:"):
        e = g.split("slice:",1)[1]
        if e in ("int","int32","int64"): return "Vec[i64]"
        if e=="string": return "Vec[String]"
        if e=="bool": return "Vec[bool]"
        return "Vec[String]"
    return "String"

def snake(s):
    out=[]
    for i,ch in enumerate(s):
        if ch.isupper() and i>0 and (not s[i-1].isupper()):
            out.append('_')
        out.append(ch.lower())
    return ''.join(out)

def scan_go_structs():
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf8"))
    structs={}
    for p in GO_ROOT.rglob("*.go"):
        txt=p.read_text(encoding="utf8", errors="ignore")
        for m in STRUCT_RE.finditer(txt):
            name=m.group("name")
            body=m.group("body")
            fields=[]
            for fm in FIELD_RE.finditer(body):
                ident=fm.group("ident")
                typ=fm.group("typ")
                fields.append({
                    "name": ident,
                    "rust_name": snake(ident),
                    "go_type": typ,
                    "rust_type": go2rust_ty(typ)
                })
            if fields:
                structs[name]=fields
    CACHE_FILE.write_text(json.dumps(structs, indent=2), encoding="utf8")
    return structs

RUST_STRUCT_RE = re.compile(r'(?ms)pub\\s+struct\\s+(?P<name>[A-Za-z0-9_]+)\\s*\\{(?P<body>.*?)\\}', re.M)

def parse_rust_struct(txt):
    m = RUST_STRUCT_RE.search(txt)
    if not m: return None
    name=m.group("name")
    body=m.group("body")
    # collect "pub foo: Type,"
    fields=[]
    for line in body.splitlines():
        line=line.strip().rstrip(',')
        if line.startswith("pub "):
            part=line[4:]
            if ":" in part:
                fname, fty = part.split(":",1)
                fields.append((fname.strip(), fty.strip()))
    return {"name":name, "fields":fields, "span":m.span(0), "body_span":m.span("body")}

def ensure_derives(txt):
    # Ensure we have #[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]
    if "#[derive(" in txt:
        return txt
    return '#[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]\n' + txt

def rustify_type(t):
    return t.replace("Vec[","Vec<").replace("]",">")

def merge_struct(txt, go_fields):
    rs = parse_rust_struct(txt)
    if not rs: return txt, 0, 0
    rust_names = [n for n,_ in rs["fields"]]
    added=0; changed=0
    # assemble new body lines preserving existing order + appending missing
    existing = {n:t for n,t in rs["fields"]}
    target_lines=[]
    present=set()
    for f in go_fields:
        rn = f["rust_name"]
        rt = rustify_type(f["rust_type"])
        if rn in existing:
            old = existing[rn]
            if old != rt:
                existing[rn] = rt
                changed += 1
        else:
            existing[rn] = rt
            added += 1
    # Build merged body sorted by appearance in original (keep stability), then remaining by Go order
    used=set()
    for n,_ in rs["fields"]:
        t=existing[n]
        target_lines.append(f"    pub {n}: {t},")
        used.add(n)
    for f in go_fields:
        rn=f["rust_name"]
        if rn not in used:
            target_lines.append(f"    pub {rn}: {rustify_type(f['rust_type'])},")
            used.add(rn)
    new_body = "\n".join(target_lines) + "\n"

    # Replace only the body span
    b0,b1 = rs["body_span"]
    out = txt[:b0] + new_body + txt[b1:]
    # Ensure derive exists somewhere above struct; if missing, add right before struct
    s0,_ = rs["span"]
    pre = out[:s0]
    if "#[derive(" not in pre.splitlines()[-5:]:
        out = out[:s0] + ensure_derives(out[s0:])
    return out, added, changed

def main():
    structs = scan_go_structs()
    files = list(RUST_GEN.rglob("*.rs"))
    changed_files=0; fields_added=0; types_changed=0
    for fp in files:
        txt = fp.read_text(encoding="utf8", errors="ignore")
        rs = parse_rust_struct(txt)
        if not rs: 
            continue
        name = rs["name"]
        go = structs.get(name)
        if not go:
            # Try action name variants like GameAction_123 -> GameAction123
            if name.startswith("GameAction_"):
                alt=name.replace("GameAction_","GameAction")
                go = structs.get(alt)
            if name.startswith("CliAction_"):
                alt=name.replace("CliAction_","CliAction")
                go = structs.get(alt)
        if not go:
            continue
        new_txt, add_cnt, chg_cnt = merge_struct(txt, go)
        if new_txt != txt:
            fp.write_text(new_txt, encoding="utf8")
            changed_files += 1
            fields_added += add_cnt
            types_changed += chg_cnt
    report = {
        "timestamp": datetime.utcnow().isoformat()+"Z",
        "changed_files": changed_files,
        "fields_added": fields_added,
        "types_changed": types_changed,
        "note": "STRUCTS-ONLY alignment; parse_* bodies untouched."
    }
    print(json.dumps(report))
if __name__=="__main__":
    main()
# --- END FILE ---