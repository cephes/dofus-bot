package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

type GenReport struct {
	Generated []string          `json:"generated"`
	Todos     map[string]string `json:"todos"`
	Errors    []string          `json:"errors"`
}

type MessageSpec struct {
	Name       string            `json:"name"`
	Prefix     string            `json:"prefix,omitempty"`
	Fields     map[string]string `json:"fields"` // field -> rust type (string,int,bool,hex,json)
	Assignments []string         `json:"assignments"` // simple steps detected in Deserialize
	Delims     []string          `json:"delims"` // detected delimiters order (e.g. ["|",";"," ,"])
	Notes      []string          `json:"notes"`
}

func main() {
	outDir := flag.String("out", "core/src/retroproto_parsers", "output dir for generated Rust parsers")
	tp := flag.String("tp", "third_party/retroproto", "path to retroproto checkout in repo")
	flag.Parse()

	report := GenReport{Generated: []string{}, Todos: map[string]string{}, Errors: []string{}}
	msgs := map[string]*MessageSpec{} // by message name

	// ensure outDir exists
	if err := os.MkdirAll(*outDir, 0o755); err != nil {
		log.Fatalf("mkdir out: %v", err)
	}

	collect := map[string]string{} // prefix -> message name
	for _, sub := range []string{"msgsvr", "msgcli"} {
		dir := filepath.Join(*tp, sub)
		if _, err := os.Stat(dir); err != nil {
			// not fatal: continue
			continue
		}
		err := filepath.Walk(dir, func(path string, fi os.FileInfo, err error) error {
			if err != nil { return err }
			if fi.IsDir() { return nil }
			if !strings.HasSuffix(path, ".go") { return nil }
			// parse file
			fset := token.NewFileSet()
			f, perr := parser.ParseFile(fset, path, nil, parser.ParseComments)
			if perr != nil {
				report.Errors = append(report.Errors, fmt.Sprintf("parse %s: %v", path, perr))
				return nil
			}
			// find const string assignments for MsgSvrId / MsgCliId IDs
			ast.Inspect(f, func(n ast.Node) bool {
				// look for ValueSpec with const string
				vs, ok := n.(*ast.ValueSpec)
				if !ok { return true }
				if vs.Type == nil && len(vs.Values) == 1 {
					if bl, ok := vs.Values[0].(*ast.BasicLit); ok && bl.Kind.String() == "STRING" {
						for _, name := range vs.Names {
							// Heuristics: names in retroproto use MsgSvrId = "XX"
							// Also search for patterns like: <MessageName> MsgSvrId = "RD"
							// We'll map string literal -> name token
							collect[strings.Trim(bl.Value, `"`)] = name.Name
						}
					}
				}
				return true
			})
			// Also scan file text for patterns: MsgSvrId = "GA" lines with message name before them
			text, _ := ioutil.ReadFile(path)
			r1 := regexp.MustCompile(`(?m)^\s*([A-Za-z0-9_?+\-]+)\s+MsgSvrId\s*=\s*"([^"]+)"`)
			r2 := regexp.MustCompile(`(?m)^\s*([A-Za-z0-9_?+\-]+)\s*=\s*MsgCliId\("([^"]+)"\)`)
			for _, m := range r1.FindAllStringSubmatch(string(text), -1) {
				if len(m) >= 3 {
					collect[m[2]] = m[1]
					ensureMsg(msgs, m[1]).Prefix = m[2]
				}
			}
			for _, m := range r2.FindAllStringSubmatch(string(text), -1) {
				if len(m) >= 3 {
					collect[m[2]] = m[1]
					ensureMsg(msgs, m[1]).Prefix = m[2]
				}
			}
			// AST: collect struct fields for type <Message> struct { ... }
			ast.Inspect(f, func(n ast.Node) bool {
				ts, ok := n.(*ast.TypeSpec)
				if !ok { return true }
				st, ok := ts.Type.(*ast.StructType)
				if !ok { return true }
				msg := ensureMsg(msgs, ts.Name.Name)
				if msg.Fields == nil { msg.Fields = map[string]string{} }
				for _, f := range st.Fields.List {
					ftype := "string"
					switch fmt.Sprintf("%T", f.Type) {
					case "*ast.Ident":
						id := f.Type.(*ast.Ident).Name
						if id == "int" || id == "int32" || id == "int64" { ftype = "int" }
						if id == "bool" { ftype = "bool" }
					}
					for _, name := range f.Names {
						msg.Fields[name.Name] = ftype
					}
				}
				return true
			})
			// AST: detect Deserialize(extra string) receiver *<Message>
			ast.Inspect(f, func(n ast.Node) bool {
				fd, ok := n.(*ast.FuncDecl)
				if !ok || fd.Recv == nil || fd.Name == nil { return true }
				if fd.Name.Name != "Deserialize" || fd.Type == nil || fd.Type.Params == nil { return true }
				// receiver type
				recv := ""
				if len(fd.Recv.List) > 0 {
					if se, ok := fd.Recv.List[0].Type.(*ast.StarExpr); ok {
						if id, ok := se.X.(*ast.Ident); ok { recv = id.Name }
					}
				}
				if recv == "" { return true }
				msg := ensureMsg(msgs, recv)
				if msg.Assignments == nil { msg.Assignments = []string{} }
				// naive scan body text for common patterns (m.Field = extra; parts := strings.Split(extra,"|"); ...)
				if fd.Body != nil {
					src := string(text[fd.Body.Pos()-1 : fd.Body.End()-1])
					// direct assignment m.Field = extra
					rAssign := regexp.MustCompile(`m\.(\w+)\s*=\s*extra`)
					for _, m := range rAssign.FindAllStringSubmatch(src, -1) {
						msg.Assignments = append(msg.Assignments, "assign:"+m[1]+"=extra")
					}
					// detect primary delimiter usage
					rSplit := regexp.MustCompile(`strings\.SplitN?\(\s*extra\s*,\s*"([^"]+)"`)
					for _, s := range rSplit.FindAllStringSubmatch(src, -1) {
						if !contains(msg.Delims, s[1]) { msg.Delims = append(msg.Delims, s[1]) }
					}
				}
				return true
			})
			return nil
		})
		if err != nil {
			report.Errors = append(report.Errors, fmt.Sprintf("walk %s: %v", dir, err))
		}
	}

	// Write mapping manifest (prefix -> message name)
	mappingFile := filepath.Join(*outDir, "mapping_manifest.json")
	mappingBytes, _ := json.MarshalIndent(collect, "", "  ")
	_ = ioutil.WriteFile(mappingFile, mappingBytes, 0o644)
	report.Generated = append(report.Generated, mappingFile)

	// Generate Rust files per message
	for name, spec := range msgs {
		if spec.Fields == nil || len(spec.Fields) == 0 {
			// no struct? still generate fallback parser for this file
			continue
		}
		rustFile := filepath.Join(*outDir, name+".rs")
		var buf bytes.Buffer
		buf.WriteString("// AUTO-GENERATED typed parser from retroproto: " + name + "\n")
		buf.WriteString("use serde::{Serialize, Deserialize};\nuse serde_json::{Value, json};\n\n")
		// struct
		buf.WriteString(fmt.Sprintf("#[derive(Debug, Clone, Serialize, Deserialize)]\npub struct %s {\n", name))
		for f, t := range spec.Fields {
			buf.WriteString(fmt.Sprintf("  pub %s: %s,\n", lowerFirst(f), rustType(t)))
		}
		buf.WriteString("}\n\n")
		// parser
		buf.WriteString(fmt.Sprintf("pub fn parse_%s(payload: &str) -> Result<%s, String> {\n", sanitizeIdent(name), name))
		buf.WriteString("  let p = payload.trim_end_matches('\\0');\n")
		// If Deserialize had "m.Field = extra", just assign
		if hasAssignExtra(spec.Assignments) && len(spec.Fields) == 1 {
			// pick the single field
			var single string
			for f := range spec.Fields { single = f; break }
			buf.WriteString(fmt.Sprintf("  Ok(%s { %s: p.to_string() })\n", name, lowerFirst(single)))
		} else {
			// generic split-aware parse skeleton
			buf.WriteString("  // TODO: verify field ordering against Go Deserialize; current impl is best-effort.\n")
			del := "|"
			if len(spec.Delims) > 0 { del = spec.Delims[0] }
			buf.WriteString(fmt.Sprintf("  let parts: Vec<&str> = if p.is_empty() { vec![] } else { p.split(%q).collect() };\n", del))
			buf.WriteString(fmt.Sprintf("  let mut out = %s{", name))
			i := 0
			for f, t := range spec.Fields {
				if i > 0 { buf.WriteString(",") }
				switch t {
				case "int":
					buf.WriteString(fmt.Sprintf(" %s: parts.get(%d).and_then(|s| s.trim().parse::<i64>().ok()).unwrap_or_default()", lowerFirst(f), i))
				case "bool":
					buf.WriteString(fmt.Sprintf(" %s: parts.get(%d).map(|s| *s == \"1\" || *s == \"true\").unwrap_or(false)", lowerFirst(f), i))
				default:
					buf.WriteString(fmt.Sprintf(" %s: parts.get(%d).map(|s| s.to_string()).unwrap_or_default()", lowerFirst(f), i))
				}
				i++
			}
			buf.WriteString(" };\n  Ok(out)\n")
		}
		buf.WriteString("}\n\n")
		// to_json helper
		buf.WriteString(fmt.Sprintf("pub fn %s_to_json(m: &%s) -> Value { json!(m) }\n", sanitizeIdent(name), name))
		if err := ioutil.WriteFile(rustFile, buf.Bytes(), 0o644); err == nil {
			report.Generated = append(report.Generated, rustFile)
		} else {
			report.Errors = append(report.Errors, fmt.Sprintf("write %s: %v", rustFile, err))
		}
	}

	// Generate mod.rs with `mod` lines and re-exports + registry
	genDir := *outDir
	files, _ := ioutil.ReadDir(genDir)
	var mods []string
	var exports []string
	for _, fi := range files {
		if !fi.IsDir() && strings.HasSuffix(fi.Name(), ".rs") && fi.Name() != "mod.rs" && fi.Name() != "generation_report.json" && fi.Name() != "mapping_manifest.json" {
			modName := strings.TrimSuffix(fi.Name(), ".rs")
			mods = append(mods, fmt.Sprintf("pub mod %s;", modName))
			exports = append(exports, fmt.Sprintf("pub use %s::*;", modName))
		}
	}
	var modBuf bytes.Buffer
	modBuf.WriteString("// AUTO-GENERATED registry\n")
	for _, m := range mods { modBuf.WriteString(m + "\n") }
	for _, e := range exports { modBuf.WriteString(e + "\n") }
	_ = ioutil.WriteFile(filepath.Join(genDir, "mod.rs"), modBuf.Bytes(), 0o644)

	// Write generation report
	repB, _ := json.MarshalIndent(report, "", "  ")
	_ = ioutil.WriteFile(filepath.Join(*outDir, "generation_report.json"), repB, 0o644)

	fmt.Println("Generation finished. Report:", filepath.Join(*outDir, "generation_report.json"))
}

// atoiSafe
func atoiSafe(s string) int {
	var v int
	fmt.Sscanf(s, "%d", &v)
	return v
}

func ensureMsg(m map[string]*MessageSpec, name string) *MessageSpec {
	if name == "" { return &MessageSpec{} }
	if m[name] == nil {
		m[name] = &MessageSpec{Name: name, Fields: map[string]string{}}
	}
	return m[name]
}

func sanitizeIdent(s string) string {
	return strings.ReplaceAll(strings.ReplaceAll(s, "-", "_"), "|", "_")
}
func lowerFirst(s string) string {
	if s == "" { return s }
	return strings.ToLower(s[:1]) + s[1:]
}
func rustType(goHint string) string {
	switch goHint {
	case "int": return "i64"
	case "bool": return "bool"
	default: return "String"
	}
}
func hasAssignExtra(ops []string) bool {
	for _, o := range ops {
		if strings.HasPrefix(o, "assign:") && strings.HasSuffix(o, "=extra") { return true }
	}
	return false
}
func contains(ss []string, s string) bool {
	for _, x := range ss { if x == s { return true } }
	return false
}