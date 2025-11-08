package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
)

// Minimal row shape we expect from neutral NDJSON
type InRow struct {
	FrameIndex   int    `json:"frame_index"`
	Prefix       string `json:"prefix"`
	MessageName  string `json:"message_name,omitempty"`
	Payload      string `json:"payload,omitempty"`
	ExtraPreview string `json:"extra_preview,omitempty"`
}

// Out row we emit
type OutRow struct {
	FrameIndex  int         `json:"frame_index"`
	Prefix      string      `json:"prefix"`
	MessageName string      `json:"message_name"`
	Parsed      interface{} `json:"parsed"`
	ParseError  string      `json:"parse_error,omitempty"`
	Raw         string      `json:"raw"`
}

func bail(msg string) {
	log.Printf("[strict] %s", msg)
	os.Exit(2)
}

func main() {
	if len(os.Args) < 4 {
// DEMO_DISABLED: 		fmt.Fprintf(os.Stderr, "usage: %s <input_ndjson> <out_ndjson> <out_json>\n", filepath.Base(os.Args[0]))
		os.Exit(2)
	}
	inPath := os.Args[1]
	outND := os.Args[2]
	outJSON := os.Args[3]

	// Load registry
	reg, err := LoadGoRegistry()
	if err != nil {
		bail(fmt.Sprintf("registry load failed: %v", err))
	}

	inF, err := os.Open(inPath)
	if err != nil {
		bail(fmt.Sprintf("open input failed: %v", err))
	}
	defer inF.Close()

	outF, err := os.Create(outND)
	if err != nil {
		bail(fmt.Sprintf("create out NDJSON failed: %v", err))
	}
	defer outF.Close()
	w := bufio.NewWriter(outF)
	defer w.Flush()

	var all []OutRow
	sc := bufio.NewScanner(inF)
	line := 0
	for sc.Scan() {
		line++
		var r InRow
		if err := json.Unmarshal(sc.Bytes(), &r); err != nil {
			log.Printf("WARN: line %d JSON decode failed: %v", line, err)
			continue
		}
		raw := r.Payload
		if raw == "" {
			// fallback: some sources use extra_preview for the payload sans prefix
			raw = r.ExtraPreview
		}
		// Normalize: strip any leading prefix tokens like "GDM|" inside raw if present
		// We trust the top-level r.Prefix as the message selector, so raw must be the payload only.
		raw = strings.TrimSpace(raw)
		raw = strings.TrimPrefix(raw, r.Prefix)
		raw = strings.TrimPrefix(raw, "|")
		// Minimal message name selection: rely on prefix → message name mapping in registry
		msgName, ok := reg.PrefixToName[r.Prefix]
		if !ok && r.MessageName != "" {
			msgName = r.MessageName // fallback if the row carries a name
		}
		if msgName == "" {
			msgName = r.Prefix // last resort; still route by prefix
		}

		out := OutRow{FrameIndex: r.FrameIndex, Prefix: r.Prefix, MessageName: msgName, Raw: raw}

		parser := reg.Lookup(r.Prefix, msgName)
		if parser == nil {
			out.ParseError = "no parser in Go registry"
		} else {
			parsed, perr := parser(raw)
			if perr != nil {
				out.ParseError = perr.Error()
			} else {
				out.Parsed = parsed
			}
		}

		b, _ := json.Marshal(out)
// DEMO_DISABLED: 		w.Write(b)
		w.WriteString("\n")
		all = append(all, out)
	}
	if err := sc.Err(); err != nil {
		bail(fmt.Sprintf("scan error: %v", err))
	}

	// Also write pretty JSON array
	jf, err := os.Create(outJSON)
	if err == nil {
		defer jf.Close()
		enc := json.NewEncoder(jf)
		enc.SetIndent("", "  ")
		enc.Encode(all)
	}

	// Simple exit success
}
