# Placeholder / Demo Writers — Suspect Report

- Repo root: `D:\WorkDir\dofus-bot`
- Total suspects: **142**
- Auto-touchable (in tools/ or scripts/): **61**

## scripts\run_pcap_final.ps1  (score: 72, touchable: True)

- L5: `Write-Host "================= JOHN.PCAP ANALYSIS =================" -ForegroundColor Green` (score 1)
- L6: `Write-Host "Input PCAP: $PcapPath"` (score 1)
- L12: `Write-Host "Base name: $base"` (score 1)
- L13: `Write-Host "Output directory: $decDir"` (score 1)
- L14: `Write-Host ""` (score 1)
- L16: `# 1) Simulate Rust pipeline` (score 2)
- L17: `Write-Host "[1/5] SIMULATING: Rust decode pipeline" -ForegroundColor Cyan` (score 1)
- L24: `{`"frame_index`":1,`"message_name`":`"AccountLoginSuccess`",`"parsed_data`":{`"ticket`":`"sample`",`"account_id`":123}}` (score 2)
- L25: `{`"frame_index`":2,`"message_name`":`"GameCreateSuccess`",`"parsed_data`":{`"type`":`"character`",`"id`":456}}` (score 2)
- L26: `{`"frame_index`":3,`"message_name`":`"ChatMessageSuccess`",`"parsed_data`":{`"channel`":`"general`",`"message`":`"Hello world`"}}` (score 2)
- L27: `"@ | Out-File -FilePath $rustNdjson -Encoding UTF8` (score 1)
- L31: `  {`"frame_index`":1,`"message_name`":`"AccountLoginSuccess`",`"parsed_data`":{`"ticket`":`"sample`",`"account_id`":123}},` (score 2)
- L32: `  {`"frame_index`":2,`"message_name`":`"GameCreateSuccess`",`"parsed_data`":{`"type`":`"character`",`"id`":456}},` (score 2)
- L33: `  {`"frame_index`":3,`"message_name`":`"ChatMessageSuccess`",`"parsed_data`":{`"channel`":`"general`",`"message`":`"Hello world`"}}` (score 2)
- L35: `"@ | Out-File -FilePath $rustJson -Encoding UTF8` (score 1)
- L37: `Write-Host "  Created sample Rust NDJSON: $rustNdjson"` (score 1)
- L38: `Write-Host "  Created sample Rust JSON: $rustJson"` (score 1)
- L40: `# 2) Go baseline simulation` (score 2)
- L41: `Write-Host "[2/5] GOING: Go baseline analysis" -ForegroundColor Cyan` (score 1)
- L47: `{`"frame_index`":1,`"message_name`":`"AccountLoginSuccess`",`"parsed_data`":{`"ticket`":`"sample_go`",`"account_id`":123}}` (score 4)
- L48: `{`"frame_index`":2,`"message_name`":`"GameCreateSuccess`",`"parsed_data`":{`"type`":`"character_go`",`"id`":456}}` (score 2)
- L49: `{`"frame_index`":3,`"message_name`":`"ChatMessageSuccess`",`"parsed_data`":{`"channel`":`"general`",`"message`":`"Hello world from Go`"}}` (score 4)
- L50: `"@ | Out-File -FilePath $goNdjson -Encoding UTF8` (score 1)
- L52: `Write-Host "  Created sample Go NDJSON: $goNdjson"` (score 1)
- L54: `# 3) Deep diff simulation` (score 2)
- L55: `Write-Host "[3/5] ANALYZING: Go-Rust deep diff" -ForegroundColor Cyan` (score 1)
- L65: `$diffJson | Out-File -FilePath "go_rust_diff.json" -Encoding UTF8` (score 1)
- L78: `$diffMd | Out-File -FilePath "GO_RUST_DIFF.md" -Encoding UTF8` (score 1)
- L79: `Write-Host "  Created sample diff: go_rust_diff.json / GO_RUST_DIFF.md"` (score 1)
- L81: `# 4) Parse integrity validator simulation` (score 2)
- … plus 25 more lines

## scripts\run_pcap_simplified.ps1  (score: 66, touchable: True)

- L9: `  Write-Host "> $cmd" -ForegroundColor Cyan` (score 1)
- L12: `    Write-Host "Warning: Command failed but continuing... $cmd" -ForegroundColor Yellow` (score 1)
- L20: `Write-Host "================= JOHN.PCAP ANALYSIS =================" -ForegroundColor Green` (score 1)
- L21: `Write-Host "Input PCAP: $PcapPath"` (score 1)
- L22: `Write-Host "Base name: $base"` (score 1)
- L23: `Write-Host "Output directory: $decDir"` (score 1)
- L24: `Write-Host ""` (score 1)
- L26: `# 1) Simulate Rust pipeline (since build is broken, create sample data)` (score 2)
- L28: `  Write-Host "[1/5] SIMULATING: Rust decode pipeline" -ForegroundColor Cyan` (score 1)
- L32: `    @{ frame_index=1; message_name="AccountLoginSuccess"; parsed_data=@{ticket="sample"; account_id=123} },` (score 2)
- L33: `    @{ frame_index=2; message_name="GameCreateSuccess"; parsed_data=@{type="character"; id=456} },` (score 2)
- L34: `    @{ frame_index=3; message_name="ChatMessageSuccess"; parsed_data=@{channel="general"; message="Hello world"} }` (score 2)
- L38: `  $sampleData | ConvertTo-Json -Compress | Out-File -FilePath $rustNdjson -Encoding UTF8` (score 2)
- L39: `  Write-Host "  Created sample Rust NDJSON: $rustNdjson"` (score 1)
- L42: `  $sampleData | ConvertTo-Json | Out-File -FilePath $rustJson -Encoding UTF8` (score 2)
- L43: `  Write-Host "  Created sample Rust JSON: $rustJson"` (score 1)
- L48: `  Write-Host "[2/5] GOING: Go baseline analysis" -ForegroundColor Cyan` (score 1)
- L55: `    Write-Host "  Go baseline NDJSON: $goNdjson"` (score 1)
- L59: `      @{ frame_index=1; message_name="AccountLoginSuccess"; parsed_data=@{ticket="sample_go"; account_id=123} },` (score 4)
- L60: `      @{ frame_index=2; message_name="GameCreateSuccess"; parsed_data=@{type="character_go"; id=456} },` (score 2)
- L61: `      @{ frame_index=3; message_name="ChatMessageSuccess"; parsed_data=@{channel="general"; message="Hello world from Go"} }` (score 4)
- L63: `    $goSampleData | ConvertTo-Json -Compress | Out-File -FilePath $goNdjson -Encoding UTF8` (score 2)
- L64: `    Write-Host "  Created sample Go NDJSON: $goNdjson (using sample data)"` (score 1)
- L69: `Write-Host "[3/5] ANALYZING: Go↔Rust deep diff" -ForegroundColor Cyan` (score 1)
- L85: `  $diffData | ConvertTo-Json | Out-File -FilePath "go_rust_diff.json" -Encoding UTF8` (score 2)
- L94: `" | Out-File -FilePath "GO_RUST_DIFF.md" -Encoding UTF8` (score 1)
- L95: `  Write-Host "  Created sample diff: go_rust_diff.json / GO_RUST_DIFF.md"` (score 1)
- L99: `Write-Host "[4/5] VALIDATING: Parse integrity check" -ForegroundColor Cyan` (score 1)
- L118: `  $intgData | ConvertTo-Json | Out-File -FilePath "PARSE_INTEGRITY.json" -Encoding UTF8` (score 2)
- L130: `" | Out-File -FilePath "PARSE_INTEGRITY.md" -Encoding UTF8` (score 1)
- … plus 20 more lines

## scripts\run_go_baseline.ps1  (score: 64, touchable: True)

- L28: `$RustInput = Join-Path $ExamplesDir "pcap\decoded\dummy_parsed_new.ndjson"` (score 1)
- L29: `$GoOutputNdjson = Join-Path $ExamplesDir "pcap\decoded\dummy_go.ndjson"` (score 2)
- L30: `$GoOutputJson = Join-Path $ExamplesDir "pcap\decoded\dummy_go.json"` (score 1)
- L37: `Write-Host "========================================" -ForegroundColor Cyan` (score 1)
- L38: `Write-Host "Go Baseline Parser Pipeline" -ForegroundColor Cyan` (score 1)
- L39: `Write-Host "========================================" -ForegroundColor Cyan` (score 1)
- L40: `Write-Host ""` (score 1)
- L43: `Write-Host "Step 1: Checking Go installation..." -ForegroundColor Yellow` (score 1)
- L47: `        Write-Host "✅ Go found: $goVersion" -ForegroundColor Green` (score 1)
- L52: `    Write-Host "❌ Go not found or not in PATH" -ForegroundColor Red` (score 1)
- L53: `    Write-Host ""` (score 1)
- L54: `    Write-Host "To install Go:" -ForegroundColor Yellow` (score 1)
- L55: `    Write-Host "1. Download from https://golang.org/dl/" -ForegroundColor White` (score 1)
- L56: `    Write-Host "2. Install and add to PATH" -ForegroundColor White` (score 1)
- L57: `    Write-Host "3. Restart your terminal" -ForegroundColor White` (score 1)
- L58: `    Write-Host ""` (score 1)
- L59: `    Write-Host "The Go baseline tools have been created but cannot be run without Go." -ForegroundColor Yellow` (score 1)
- L60: `    Write-Host "You can run the pipeline manually after installing Go." -ForegroundColor Yellow` (score 1)
- L66: `    Write-Host "Creating bin directory: $BinDir" -ForegroundColor Yellow` (score 1)
- L71: `Write-Host ""` (score 1)
- L72: `Write-Host "Step 2: Generating Go parser registry..." -ForegroundColor Yellow` (score 1)
- L79: `    Write-Host "✅ Registry generated successfully" -ForegroundColor Green` (score 1)
- L85: `Write-Host ""` (score 1)
- L86: `Write-Host "Step 3: Building Go binary..." -ForegroundColor Yellow` (score 1)
- L93: `    Write-Host "✅ Go binary built successfully: $GoBinary" -ForegroundColor Green` (score 1)
- L100: `    Write-Host "❌ Input file not found: $RustInput" -ForegroundColor Red` (score 1)
- L101: `    Write-Host "Make sure you have run the Rust parser first to generate this file." -ForegroundColor Yellow` (score 1)
- L106: `Write-Host ""` (score 1)
- L107: `Write-Host "Step 4: Running Go parser..." -ForegroundColor Yellow` (score 1)
- L108: `Write-Host "Input: $RustInput" -ForegroundColor Gray` (score 1)
- … plus 33 more lines

## scripts\run_parity_iteration.ps1  (score: 41, touchable: True)

- L12: `Write-Host "=== PARITY ITERATION $ts ===" -ForegroundColor Cyan` (score 1)
- L22: `$hasInitialData = (Test-Path "examples\pcap\decoded\dummy_parsed_new.ndjson") -and (Test-Path "examples\pcap\decoded\dummy_go.ndjson")` (score 2)
- L25: `    Write-Host "Initial data not found. Running initial pipeline..." -ForegroundColor Yellow` (score 1)
- L28: `    Write-Host "Running Rust pipeline..." -ForegroundColor Green` (score 1)
- L32: `    Write-Host "Running Go baseline..." -ForegroundColor Green` (score 1)
- L36: `    Write-Host "Running initial diff..." -ForegroundColor Green` (score 1)
- L37: `    & python tools\diff_go_rust_parsed.py --rust examples\pcap\decoded\dummy_parsed_new.ndjson --go examples\pcap\decoded\dummy_go.ndjson --json-out go_rust_diff.json --md-out GO_RUST_DIFF.md` (score 3)
- L42: `Write-Host "Taking before snapshot..." -ForegroundColor Blue` (score 1)
- L46: `Write-Host "Creating backup..." -ForegroundColor Blue` (score 1)
- L53: `Write-Host "Running auto-refinement..." -ForegroundColor Green` (score 1)
- L55: `    "--go", "examples\pcap\decoded\dummy_go.ndjson",` (score 2)
- L56: `    "--rs", "examples\pcap\decoded\dummy_parsed_new.ndjson", ` (score 1)
- L68: `Write-Host "Re-running pipeline after refinement..." -ForegroundColor Green` (score 1)
- L70: `Write-Host "  Regenerating registry..." -ForegroundColor Gray` (score 1)
- L74: `Write-Host "  Building core..." -ForegroundColor Gray` (score 1)
- L80: `Write-Host "  Running Rust pipeline..." -ForegroundColor Gray` (score 1)
- L84: `Write-Host "  Running Go baseline..." -ForegroundColor Gray` (score 1)
- L88: `Write-Host "  Running diff..." -ForegroundColor Gray` (score 1)
- L89: `& python tools\diff_go_rust_parsed.py --rust examples\pcap\decoded\dummy_parsed_new.ndjson --go examples\pcap\decoded\dummy_go.ndjson --json-out go_rust_diff.json --md-out GO_RUST_DIFF.md` (score 3)
- L93: `Write-Host "Taking after snapshot..." -ForegroundColor Blue` (score 1)
- L97: `Write-Host "Generating summary..." -ForegroundColor Green` (score 1)
- L120: `Add-Content -Path "PARITY_PROGRESS.md" -Value $progressEntry` (score 1)
- L141: `$iterationSummary | ConvertTo-Json -Depth 3 | Set-Content "$iterationDir\summary.json"` (score 2)
- L150: `    Add-Content -Path "PARITY_PROGRESS.md" -Value "**STATUS: CONVERGED** - Mismatch rate ($afterMismatchRate%) ≤ target ($TargetMismatchRate%)"` (score 1)
- L153: `    Add-Content -Path "PARITY_PROGRESS.md" -Value "**STATUS: NO IMPROVEMENT** - No net gain in mismatches"` (score 1)
- L156: `    Add-Content -Path "PARITY_PROGRESS.md" -Value "**STATUS: MAX ITERS REACHED** - Completed $MaxIters iterations"` (score 1)
- L160: `Write-Host "`n=== ITERATION COMPLETE ===" -ForegroundColor Cyan` (score 1)
- L161: `Write-Host "Before: $beforeMismatchRate% mismatches ($($beforeData.mismatches)/$($beforeData.total))" -ForegroundColor Yellow` (score 1)
- L162: `Write-Host "After:  $afterMismatchRate% mismatches ($($afterData.mismatches)/$($afterData.total))" -ForegroundColor Green` (score 1)
- L163: `Write-Host "Improvement: $improvement mismatches" -ForegroundColor $(if ($improvement -gt 0) { "Green" } else { "Red" })` (score 1)
- … plus 4 more lines

## tools\validate_parsed_integrity.py  (score: 40, touchable: True)

- L37: `def choose_any_required_set(parsed_data: Dict, sets: List[List[str]]) -> Tuple[bool, Optional[List[str]]]:` (score 2)
- L39: `    Check if any of the required sets is fully present in parsed_data.` (score 2)
- L43: `        if all(field in parsed_data for field in required_set):` (score 2)
- L169: `        f.write("# Parse Integrity Summary\n\n")` (score 1)
- L173: `        f.write("## Overall Statistics\n\n")` (score 1)
- L174: `        f.write(f"- **Total rows processed:** {summary['total_rows']}\n")` (score 1)
- L175: `        f.write(f"- **Parsed OK:** {summary['parsed_ok']} ({summary['parsed_ok']/summary['total_rows']*100:.1f}%)\n")` (score 1)
- L176: `        f.write(f"- **Parsed empty object:** {summary['parsed_empty_object']} ({summary['parsed_empty_object']/summary['total_rows']*100:.1f}%)\n")` (score 1)
- L177: `        f.write(f"- **Parsed null:** {summary['parsed_null']} ({summary['parsed_null']/summary['total_rows']*100:.1f}%)\n")` (score 1)
- L178: `        f.write(f"- **Parse errors present:** {summary['parse_error_present']} ({summary['parse_error_present']/summary['total_rows']*100:.1f}%)\n\n")` (score 1)
- L181: `        f.write("## Violations Overview\n\n")` (score 1)
- L183: `            f.write(f"**Total violations found: {len(violations)}**\n\n")` (score 1)
- L191: `            f.write("### Violation Types\n\n")` (score 1)
- L193: `                f.write(f"- **{violation_type}:** {count} occurrences\n")` (score 1)
- L194: `            f.write("\n")` (score 1)
- L196: `            f.write("No violations found.\n\n")` (score 1)
- L199: `        f.write("## Per-Message Statistics\n\n")` (score 1)
- L204: `            f.write("| Message Name | Total | OK | Empty | Null | Error | Failure Rate |\n")` (score 1)
- L205: `            f.write("|-------------|-------|----|-----|------|-------|-------------|\n")` (score 1)
- L216: `                f.write(f"| {message_name} | {stats['total']} | {stats['parsed_ok']} | {stats['parsed_empty_object']} | {stats['parsed_null']} | {stats['parse_error_present']} | {failure_rate:.1f}% |\n")` (score 1)
- L217: `            f.write("\n")` (score 1)
- L219: `            f.write("No per-message statistics available.\n\n")` (score 1)
- L223: `            f.write("## Sample Failures\n\n")` (score 1)
- L224: `            f.write("First 10 failed rows with failure reasons:\n\n")` (score 1)
- L227: `                f.write(f"### {i}. Frame {violation['frame_index']} - {violation['message_name']}\n")` (score 1)
- L228: `                f.write(f"- **Status:** {violation['status']}\n")` (score 1)
- L229: `                f.write(f"- **Reasons:** {', '.join(violation['reasons'])}\n")` (score 1)
- L230: `                f.write(f"- **Prefix:** {violation['prefix']}\n\n")` (score 1)
- L338: `            json.dump(results, f, indent=2, ensure_ascii=False)` (score 1)
- L388: `        default='examples/pcap/decoded/dummy_parsed_all.ndjson',` (score 4)
- … plus 1 more lines

## tools\cleanup\disable_demo_outputs.py  (score: 37, touchable: True)

- L30: `    r"Hello world from Go",` (score 2)
- L39: `    r"pretty json",` (score 4)
- L40: `    r"Pretty JSON",` (score 4)
- L44: `    r"json\.dump", r"json\.dumps", r"write\(", r"fprintf", r"fmt\.Fprint", r"fmt\.Fprintf",` (score 1)
- L45: `    r"Write-Host", r"Out-File", r"Set-Content", r"Add-Content", r"ConvertTo-Json",` (score 5)
- L48: `    r"dummy_go.*\.ndjson", r"john_go.*\.ndjson"` (score 2)
- L117: `    ap = argparse.ArgumentParser(description="Find and optionally disable placeholder/demo outputs across the repo.")` (score 4)
- L152: `        json.dump({"root": str(ROOT), "suspects": suspects}, f, ensure_ascii=False, indent=2)` (score 1)
- L155: `        f.write("# Placeholder / Demo Writers — Suspect Report\n\n")` (score 5)
- L156: `        f.write(f"- Repo root: `{ROOT}`\n")` (score 1)
- L157: `        f.write(f"- Total suspects: **{len(suspects)}**\n")` (score 1)
- L158: `        f.write(f"- Auto-touchable (in tools/ or scripts/): **{sum(1 for s in suspects if s['touchable'])}**\n\n")` (score 1)
- L160: `            f.write(f"## {s['file']}  (score: {s['score']}, touchable: {s['touchable']})\n\n")` (score 1)
- L162: `                f.write(f"- L{m['line']}: `{m['content']}` (score {m['score']})\n")` (score 1)
- L164: `                f.write(f"- … plus {len(s['matches']) - 30} more lines\n")` (score 1)
- L165: `            f.write("\n")` (score 1)
- L171: `        print("[DRY-RUN] No changes applied. Re-run with --apply to comment out demo writers in tools/ and scripts/.")` (score 2)

## scripts\run_integrity_check.ps1  (score: 20, touchable: True)

- L6: `    [string]$In = "examples\pcap\decoded\dummy_parsed_all.ndjson"` (score 4)
- L35: `    Write-Host "Using virtual environment Python: $pythonExe"` (score 1)
- L38: `    Write-Host "Using virtual environment Python: $pythonExe"` (score 1)
- L44: `            Write-Host "Using system Python: $pythonExe"` (score 1)
- L49: `                Write-Host "Using system Python3: $pythonExe"` (score 1)
- L62: `Write-Host "=== Parse Integrity Check ===" -ForegroundColor Cyan` (score 1)
- L63: `Write-Host "Input:    $inputPath"` (score 1)
- L64: `Write-Host "Script:   $pythonScript"` (score 1)
- L65: `Write-Host "Output:   $outputJson, $outputMd"` (score 1)
- L66: `Write-Host "Python:   $pythonExe"` (score 1)
- L67: `Write-Host "============================" -ForegroundColor Cyan` (score 1)
- L68: `Write-Host ""` (score 1)
- L75: `    Write-Host ""` (score 1)
- L77: `        Write-Host "✅ PARSE INTEGRITY CHECK PASSED" -ForegroundColor Green` (score 1)
- L79: `        Write-Host "❌ PARSE INTEGRITY CHECK FAILED (exit code: $exitCode)" -ForegroundColor Red` (score 1)
- L84: `        Write-Host "📄 JSON report: $outputJson" -ForegroundColor Blue` (score 1)
- L87: `        Write-Host "📄 Markdown report: $outputMd" -ForegroundColor Blue` (score 1)

## tools\validate_go_baseline.py  (score: 19, touchable: True)

- L5: `SRC_B = r"examples/pcap/decoded/dummy_parsed_new.ndjson"` (score 1)
- L6: `OUT_ND = r"examples/pcap/decoded/dummy_go_strict.ndjson"` (score 2)
- L7: `OUT_JSON = r"examples/pcap/decoded/dummy_go_strict.json"` (score 1)
- L87: `        f.write("# Go Baseline Validation (Strict Mode)\n\n")` (score 1)
- L88: `        f.write(f"- Input: `{src}`\n")` (score 1)
- L89: `        f.write(f"- Output NDJSON: `{OUT_ND}`\n")` (score 1)
- L90: `        f.write(f"- Output JSON: `{OUT_JSON}`\n\n")` (score 1)
- L91: `        f.write(f"## Summary\n\n")` (score 1)
- L92: `        f.write(f"- Total rows: **{total}**\n")` (score 1)
- L93: `        f.write(f"- Rows with parse_error: **{with_errors}**\n")` (score 1)
- L94: `        f.write(f"- Unique prefixes: **{len(by_prefix)}**\n\n")` (score 1)
- L95: `        f.write("### By prefix (top 15)\n\n")` (score 1)
- L97: `            f.write(f"- `{p}`: {c}\n")` (score 1)
- L98: `        f.write("\n## Shape Check Failures\n\n")` (score 1)
- L100: `            f.write("✅ No shape failures detected.\n")` (score 1)
- L102: `            f.write(f"❌ {len(errs)} shape failures:\n")` (score 1)
- L104: `                f.write(f"- Row {i}: {msg}\n")` (score 1)
- L106: `                f.write(f"- … (+{len(errs)-50} more)\n")` (score 1)

## scripts\run_pcap_full.ps1  (score: 17, touchable: True)

- L9: `  Write-Host "> $cmd" -ForegroundColor Cyan` (score 1)
- L25: `# Expect your existing pipeline to write to examples/pcap/decoded/<name>_parsed_all.ndjson` (score 1)
- L59: `Write-Host ""` (score 1)
- L60: `Write-Host "================= JOHN.PCAP REPORT =================" -ForegroundColor Green` (score 1)
- L61: `Write-Host "Input frames        : $($diff.total_rows)"` (score 1)
- L62: `Write-Host "Go-Rust matches     : $($diff.matches)  ($matchPercent%)"` (score 1)
- L63: `Write-Host "Go-Rust mismatches  : $($diff.mismatches)"` (score 1)
- L64: `Write-Host "Integrity violations: $($intg.violations_total)"` (score 1)
- L65: `Write-Host " - empty objects    : $($intg.categories.parsed_empty_object)"` (score 1)
- L66: `Write-Host " - parse errors     : $($intg.categories.parse_error_present)"` (score 1)
- L67: `Write-Host " - missing fields   : $($intg.categories.missing_required_field)"` (score 1)
- L68: `Write-Host " - type mismatch    : $($intg.categories.type_mismatch)"` (score 1)
- L69: `Write-Host "Artifacts:"` (score 1)
- L70: `Write-Host " - Rust NDJSON      : $rustNdjson"` (score 1)
- L71: `Write-Host " - Go   NDJSON      : $goNdjson"` (score 1)
- L72: `Write-Host " - Diff (json/md)   : go_rust_diff.json / GO_RUST_DIFF.md"` (score 1)
- L73: `Write-Host " - Integrity (json/md): PARSE_INTEGRITY.json / PARSE_INTEGRITY.md"` (score 1)

## tools\go_baseline\comprehensive_comparison.py  (score: 13, touchable: True)

- L65: `            f.write(line + '\n')` (score 1)
- L191: `    rust_ndjson_path = 'examples/pcap/decoded/dummy_parsed_all.ndjson'` (score 4)
- L192: `    go_output_path = 'examples/pcap/decoded/dummy_go_comprehensive.ndjson'` (score 2)
- L209: `    neutral_path = 'examples/pcap/decoded/dummy_neutral_comprehensive.ndjson'` (score 1)
- L212: `            f.write(line + '\n')` (score 1)
- L226: `        with open('examples/pcap/decoded/comparison_comprehensive.json', 'w') as f:` (score 1)
- L227: `            json.dump(comparison_results, f, indent=2)` (score 1)
- L253: `        with open('examples/pcap/decoded/comparison_comprehensive.json', 'w') as f:` (score 1)
- L254: `            json.dump(summary, f, indent=2)` (score 1)

## scripts\run_parity_iteration.sh  (score: 12, touchable: True)

- L45: `if [[ -f "examples/pcap/decoded/dummy_parsed_new.ndjson" && -f "examples/pcap/decoded/dummy_go.ndjson" ]]; then` (score 2)
- L60: `    python tools/diff_go_rust_parsed.py --rust examples/pcap/decoded/dummy_parsed_new.ndjson --go examples/pcap/decoded/dummy_go.ndjson --json-out go_rust_diff.json --md-out GO_RUST_DIFF.md || { echo "ERROR: Initial diff failed"; exit 1; }` (score 3)
- L79: `    "--go" "examples/pcap/decoded/dummy_go.ndjson"` (score 2)
- L80: `    "--rs" "examples/pcap/decoded/dummy_parsed_new.ndjson"` (score 1)
- L111: `python tools/diff_go_rust_parsed.py --rust examples/pcap/decoded/dummy_parsed_new.ndjson --go examples/pcap/decoded/dummy_go.ndjson --json-out go_rust_diff.json --md-out GO_RUST_DIFF.md || { echo "ERROR: Diff failed"; exit 1; }` (score 3)
- L178: `    json.dump(iteration_summary, f, indent=2)` (score 1)

## scripts\kill_placeholders.ps1  (score: 8, touchable: True)

- L18: `Write-Host "== Placeholder/Demo Cleaner ==" -ForegroundColor Cyan` (score 5)
- L19: `Write-Host "Repo: $root"` (score 1)
- L20: `Write-Host "Report will be written under .reports/" -ForegroundColor DarkGray` (score 1)
- L25: `Write-Host "Running: $py $($argsList -join ' ')" -ForegroundColor Yellow` (score 1)

## tools\go_baseline\main.go  (score: 8, touchable: True)

- L39: `		fmt.Fprintf(os.Stderr, "usage: %s <input_ndjson> <out_ndjson> <out_json>\n", filepath.Base(os.Args[0]))` (score 3)
- L110: `		w.Write(b)` (score 1)
- L118: `	// Also write pretty JSON array` (score 4)

## tools\go_baseline\main_strict.go  (score: 8, touchable: True)

- L39: `		fmt.Fprintf(os.Stderr, "usage: %s <input_ndjson> <out_ndjson> <out_json>\n", filepath.Base(os.Args[0]))` (score 3)
- L110: `		w.Write(b)` (score 1)
- L118: `	// Also write pretty JSON array` (score 4)

## scripts\run_dummy_parsing.ps1  (score: 7, touchable: True)

- L4: `$reass = Join-Path $repo "examples\pcap\decoded\dummy_reassembled.json"` (score 1)
- L5: `$parsed = Join-Path $repo "examples\pcap\decoded\dummy_parsed.json"` (score 1)
- L6: `$ndj = Join-Path $repo "examples\pcap\decoded\dummy_parsed.ndjson"` (score 1)
- L23: `Write-Host "`n=== Done ==="` (score 1)
- L24: `Write-Host "Reassembled:" $reass` (score 1)
- L25: `Write-Host "Parsed JSON :" $parsed` (score 1)
- L26: `Write-Host "NDJSON      :" $ndj` (score 1)

## tools\diff_go_rust_parsed.py  (score: 6, touchable: True)

- L269: `        json.dump(report, f, indent=2)` (score 1)
- L397: `                json.dumps(result.rust_parsed, indent=2) if result.rust_parsed else "null",` (score 2)
- L402: `                json.dumps(result.go_parsed, indent=2) if result.go_parsed else "null",` (score 2)
- L460: `        f.write('\n'.join(lines))` (score 1)

## tools\go_struct_discovery.py  (score: 6, touchable: True)

- L69: `        print(json.dumps({"error":"retroproto dir missing","path":str(RETRO)}))` (score 2)
- L78: `    OUTJSON.write_text(json.dumps({` (score 2)
- L83: `    print(json.dumps({"ok": True, "count": len(structs), "out": str(OUTJSON)}))` (score 2)

## tools\retroproto_porter_py\porter.py  (score: 6, touchable: True)

- L519: `        json.dumps(mapping, indent=2), encoding="utf-8"` (score 2)
- L522: `        json.dumps(report, indent=2), encoding="utf-8"` (score 2)
- L526: `    print(json.dumps({` (score 2)

## tools\verify_no_gaps.py  (score: 6, touchable: True)

- L268: `            f.write(report_content)` (score 1)
- L279: `        print("Example: python verify_no_gaps.py examples/pcap/decoded/dummy_parsed_all.ndjson")` (score 4)
- L303: `        json.dump(results, f, indent=2, ensure_ascii=False)` (score 1)

## scripts\run_go_strict.ps1  (score: 5, touchable: True)

- L3: `  [string]$Ndjson = "examples/pcap/decoded/dummy_go_strict.ndjson",` (score 2)
- L4: `  [string]$Json   = "examples/pcap/decoded/dummy_go_strict.json"` (score 1)
- L9: `  elseif (Test-Path "examples/pcap/decoded/dummy_parsed_new.ndjson") { $In = "examples/pcap/decoded/dummy_parsed_new.ndjson" }` (score 1)
- L16: `Write-Host "Strict baseline written to $Ndjson and $Json. Validation report: GO_BASELINE_VALIDATION.md"` (score 1)

## scripts\diagnose_repo.py  (score: 4, touchable: True)

- L122: `        "examples/pcap/decoded/dummy_reassembled.json",` (score 1)
- L182: `    reasm = repo / "examples/pcap/decoded/dummy_reassembled.json"` (score 1)
- L194: `    out_json.write_text(json.dumps(diag, indent=2), encoding="utf-8")` (score 2)

## scripts\run_go_baseline.sh  (score: 4, touchable: True)

- L28: `RUST_INPUT="$EXAMPLES_DIR/pcap/decoded/dummy_parsed_new.ndjson"` (score 1)
- L29: `GO_OUTPUT_NDJSON="$EXAMPLES_DIR/pcap/decoded/dummy_go.ndjson"` (score 2)
- L30: `GO_OUTPUT_JSON="$EXAMPLES_DIR/pcap/decoded/dummy_go.json"` (score 1)

## scripts\run_integrity_check.sh  (score: 4, touchable: True)

- L10: `INPUT_FILE="examples/pcap/decoded/dummy_parsed_all.ndjson"` (score 4)

## tools\align_structs_only.py  (score: 4, touchable: True)

- L57: `    CACHE_FILE.write_text(json.dumps(structs, indent=2), encoding="utf8")` (score 2)
- L164: `    print(json.dumps(report))` (score 2)

## tools\gen_full_parsers.py  (score: 4, touchable: True)

- L177: `        f.write(file_content)` (score 1)
- L244: `        f.write(mod_content)` (score 1)
- L260: `            f.write(actions_mod_content)` (score 1)
- L305: `        json.dump(report, f, indent=2, ensure_ascii=False)` (score 1)

## tools\gen_gameaction_subparsers.py  (score: 4, touchable: True)

- L208: `            f.write(content)` (score 1)
- L237: `            f.write(module_content)` (score 1)
- L247: `                f.write("// AUTO-GENERATED GameAction subparsers\n// Individual action parsers are organized as submodules\n\n")` (score 1)
- L306: `        json.dump(result, f, indent=2, ensure_ascii=False)` (score 1)

## tools\generate_missing_parsers_plan.py  (score: 4, touchable: True)

- L238: `    OUT_JSON.write_text(json.dumps({` (score 2)
- L288: `    print(json.dumps({` (score 2)

## tools\ids\ingest_ids.py  (score: 4, touchable: True)

- L56: `    s = json.dumps({str(k): v for k, v in sorted(data.items())}, ensure_ascii=False, indent=2)` (score 2)
- L74: `    print(json.dumps(meta, ensure_ascii=False))` (score 2)

## tools\parser_coverage_audit.py  (score: 4, touchable: True)

- L169: `    out_json.write_text(json.dumps({` (score 2)
- L229: `    print(json.dumps({` (score 2)

## tools\port_missing_parsers_from_go.py  (score: 4, touchable: True)

- L180: `        print(json.dumps({"error":"missing missing_parsers_plan.json"}))` (score 2)
- L211: `    print(json.dumps({"ported":ported, "filled":filled, "errors":errors}, indent=2))` (score 2)

## tools\retroproto_porter_py\run_porter.ps1  (score: 4, touchable: True)

- L7: `Write-Host "== Retroproto Python porter =="` (score 1)
- L8: `Write-Host "tp:" $Tp` (score 1)
- L9: `Write-Host "out:" $Out` (score 1)
- L12: `Write-Host "== Done =="` (score 1)

## tools\sync_action_parsers.py  (score: 4, touchable: True)

- L110: `        print(json.dumps({"error":"run go_struct_discovery first"}))` (score 2)
- L135: `    print(json.dumps({` (score 2)

## scripts\run_dummy_pipeline_verbose.ps1  (score: 3, touchable: True)

- L11: `Write-Host "Running pipeline with flags: $($flags -join ' ')" -ForegroundColor Cyan` (score 1)
- L12: `Write-Host "Command: python scripts\run_dummy_pipeline.py $($flags -join ' ')" -ForegroundColor Yellow` (score 1)
- L13: `Write-Host ""` (score 1)

## tools\generate_prefix_counts.py  (score: 3, touchable: True)

- L32: `        json.dump(dict(sorted_counts), f, indent=2, ensure_ascii=False)` (score 1)
- L38: `        'examples/pcap/decoded/flow_000_decoded.json',` (score 1)
- L39: `        'examples/pcap/decoded/prefix_counts_after_overrides.json'` (score 1)

## tools\parity\auto_refine_from_go.py  (score: 3, touchable: True)

- L145: `                    f.write(content)` (score 1)
- L232: `    write_text(f"{out_dir}/summary.txt", json.dumps(summary, indent=2))` (score 2)

## tools\parity\utils.py  (score: 3, touchable: True)

- L54: `        json.dump(obj, f, indent=2, ensure_ascii=False)` (score 1)
- L61: `        f.write(content)` (score 1)
- L298: `            f.write('\n'.join(new_lines))` (score 1)

## scripts\run_action_shims.ps1  (score: 2, touchable: True)

- L1: `Write-Host "== Generating action shims =="` (score 1)
- L4: `Write-Host "== Building core =="` (score 1)

## scripts\run_dummy_pipeline.py  (score: 2, touchable: True)

- L230: `            print(json.dumps(summary, indent=2))` (score 2)

## tools\ensure_action_shims.py  (score: 2, touchable: True)

- L127: `    print(json.dumps({` (score 2)

## tools\fix_parser_systematic.py  (score: 2, touchable: True)

- L118: `                f.write(content)` (score 1)
- L142: `            f.write(content)` (score 1)

## tools\fix_while_loop_parsing.py  (score: 2, touchable: True)

- L105: `                    f.write(content)` (score 1)
- L178: `            f.write(fixed_content)` (score 1)

## tools\gen_parser_registry.py  (score: 2, touchable: True)

- L125: `    print(json.dumps({"generated_count": len(stems), "actions_count": len([s for s in stems if s.startswith(("GameAction", "CliAction"))])}))` (score 2)

## tools\go_baseline\gen_go_registry.py  (score: 2, touchable: True)

- L261: `        f.write('\n'.join(lines))` (score 1)
- L312: `            json.dump(debug_info, f, indent=2)` (score 1)

## tools\introspect_action_exports.py  (score: 2, touchable: True)

- L37: `    print(json.dumps({` (score 2)

## tools\regen_and_parse.py  (score: 2, touchable: True)

- L122: `    print(json.dumps({` (score 2)

## scripts\ingest_ids.ps1  (score: 1, touchable: True)

- L4: `Write-Host "IDs ingested. JSON written to third_party/identifiants/json and mirrored into core/assets/ids"` (score 1)

## tools\align_rust_to_go.py  (score: 1, touchable: True)

- L165: `            json.dump(cache_data, f, indent=2)` (score 1)

## tools\find_go_structs.py  (score: 1, touchable: True)

- L170: `        json.dump(results, f, indent=2, ensure_ascii=False)` (score 1)

## tools\find_plaintext_flow.py  (score: 1, touchable: True)

- L91: `        json.dump(report, f, indent=2)` (score 1)

## tools\fix_all_function_closing.py  (score: 1, touchable: True)

- L39: `                    f.write(content)` (score 1)

## tools\fix_comprehensive_syntax.py  (score: 1, touchable: True)

- L161: `                f.write(content)` (score 1)

## tools\fix_delimiter_issues.py  (score: 1, touchable: True)

- L148: `                f.write(content)` (score 1)

## tools\fix_double_braces.py  (score: 1, touchable: True)

- L33: `                f.write(content)` (score 1)

## tools\fix_function_closing.py  (score: 1, touchable: True)

- L41: `                    f.write(content)` (score 1)

## tools\fix_malformed_structs.py  (score: 1, touchable: True)

- L52: `                f.write(content)` (score 1)

## tools\fix_reserved_keywords.py  (score: 1, touchable: True)

- L87: `                    f.write(fixed_content)` (score 1)

## tools\fix_specific_pattern.py  (score: 1, touchable: True)

- L32: `                f.write(content)` (score 1)

## tools\go_baseline\make_neutral_from_parsed.py  (score: 1, touchable: True)

- L49: `            f.write(line + '\n')` (score 1)

## tools\go_schema_index.py  (score: 1, touchable: True)

- L139: `        json.dump(output, f, indent=2, ensure_ascii=False)` (score 1)

## tools\go_to_rust_mapper.py  (score: 1, touchable: True)

- L240: `        json.dump(output, f, indent=2, ensure_ascii=False)` (score 1)

## tools\infer_retroproto_mapping.py  (score: 1, touchable: True)

- L86: `        json.dump(data, f, indent=2, ensure_ascii=False)` (score 1)

## repo_report_generator.py  (score: 60, touchable: False)

- L361: `# This script only Write-Hosts the actions that would be performed` (score 1)
- L363: `Write-Host "=== Repository Normalization Dry Run (PowerShell) ===" -ForegroundColor Green` (score 1)
- L364: `Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')" -ForegroundColor Gray` (score 1)
- L365: `Write-Host ""` (score 1)
- L368: `Write-Host "Phase 1: Directory Structure Normalization" -ForegroundColor Yellow` (score 1)
- L369: `Write-Host "===========================================" -ForegroundColor Yellow` (score 1)
- L371: `Write-Host "1.1 Consolidating Retroproto Trees..." -ForegroundColor Cyan` (score 1)
- L372: `Write-Host "  - Would copy unique files from dofus-retro-bot/third_party/retroproto/ to third_party/retroproto/" -ForegroundColor White` (score 1)
- L373: `Write-Host "  - Would remove dofus-retro-bot/third_party/retroproto/ directory" -ForegroundColor White` (score 1)
- L374: `Write-Host "  - Would update references to old path" -ForegroundColor White` (score 1)
- L376: `Write-Host ""` (score 1)
- L377: `Write-Host "1.2 Consolidating Example Paths..." -ForegroundColor Cyan` (score 1)
- L378: `Write-Host "  - Would merge unique files from dofus-retro-bot/examples/ to examples/" -ForegroundColor White` (score 1)
- L379: `Write-Host "  - Would remove redundant example directories" -ForegroundColor White` (score 1)
- L380: `Write-Host "  - Would update pipeline scripts to use canonical paths" -ForegroundColor White` (score 1)
- L383: `Write-Host ""` (score 1)
- L384: `Write-Host "Phase 2: Parser Module Structure Fixes" -ForegroundColor Yellow` (score 1)
- L385: `Write-Host "=======================================" -ForegroundColor Yellow` (score 1)
- L387: `Write-Host "2.1 Fixing mod.rs Declarations..." -ForegroundColor Cyan` (score 1)
- L388: `Write-Host "  - Would update core/src/retroproto_parsers/mod.rs" -ForegroundColor White` (score 1)
- L389: `Write-Host "  - Would ensure generated and handwritten modules are properly exposed" -ForegroundColor White` (score 1)
- L390: `Write-Host "  - Would verify all parser files are linked in module tree" -ForegroundColor White` (score 1)
- L392: `Write-Host ""` (score 1)
- L393: `Write-Host "2.2 Actions Submodule Integration..." -ForegroundColor Cyan` (score 1)
- L394: `Write-Host "  - Would create core/src/retroproto_parsers/generated/actions/ directory" -ForegroundColor White` (score 1)
- L395: `Write-Host "  - Would generate action-specific parser files" -ForegroundColor White` (score 1)
- L396: `Write-Host "  - Would update generated/mod.rs to include actions submodule" -ForegroundColor White` (score 1)
- L399: `Write-Host ""` (score 1)
- L400: `Write-Host "Phase 3: Registry Generation" -ForegroundColor Yellow` (score 1)
- L401: `Write-Host "===========================" -ForegroundColor Yellow` (score 1)
- … plus 30 more lines

## repo_norm_actions.ps1  (score: 52, touchable: False)

- L2: `# This script only Write-Hosts the actions that would be performed` (score 1)
- L4: `Write-Host "=== Repository Normalization Dry Run (PowerShell) ===" -ForegroundColor Green` (score 1)
- L5: `Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')" -ForegroundColor Gray` (score 1)
- L6: `Write-Host ""` (score 1)
- L9: `Write-Host "Phase 1: Directory Structure Normalization" -ForegroundColor Yellow` (score 1)
- L10: `Write-Host "===========================================" -ForegroundColor Yellow` (score 1)
- L12: `Write-Host "1.1 Consolidating Retroproto Trees..." -ForegroundColor Cyan` (score 1)
- L13: `Write-Host "  - Would copy unique files from dofus-retro-bot/third_party/retroproto/ to third_party/retroproto/" -ForegroundColor White` (score 1)
- L14: `Write-Host "  - Would remove dofus-retro-bot/third_party/retroproto/ directory" -ForegroundColor White` (score 1)
- L15: `Write-Host "  - Would update references to old path" -ForegroundColor White` (score 1)
- L17: `Write-Host ""` (score 1)
- L18: `Write-Host "1.2 Consolidating Example Paths..." -ForegroundColor Cyan` (score 1)
- L19: `Write-Host "  - Would merge unique files from dofus-retro-bot/examples/ to examples/" -ForegroundColor White` (score 1)
- L20: `Write-Host "  - Would remove redundant example directories" -ForegroundColor White` (score 1)
- L21: `Write-Host "  - Would update pipeline scripts to use canonical paths" -ForegroundColor White` (score 1)
- L24: `Write-Host ""` (score 1)
- L25: `Write-Host "Phase 2: Parser Module Structure Fixes" -ForegroundColor Yellow` (score 1)
- L26: `Write-Host "=======================================" -ForegroundColor Yellow` (score 1)
- L28: `Write-Host "2.1 Fixing mod.rs Declarations..." -ForegroundColor Cyan` (score 1)
- L29: `Write-Host "  - Would update core/src/retroproto_parsers/mod.rs" -ForegroundColor White` (score 1)
- L30: `Write-Host "  - Would ensure generated and handwritten modules are properly exposed" -ForegroundColor White` (score 1)
- L31: `Write-Host "  - Would verify all parser files are linked in module tree" -ForegroundColor White` (score 1)
- L33: `Write-Host ""` (score 1)
- L34: `Write-Host "2.2 Actions Submodule Integration..." -ForegroundColor Cyan` (score 1)
- L35: `Write-Host "  - Would create core/src/retroproto_parsers/generated/actions/ directory" -ForegroundColor White` (score 1)
- L36: `Write-Host "  - Would generate action-specific parser files" -ForegroundColor White` (score 1)
- L37: `Write-Host "  - Would update generated/mod.rs to include actions submodule" -ForegroundColor White` (score 1)
- L40: `Write-Host ""` (score 1)
- L41: `Write-Host "Phase 3: Registry Generation" -ForegroundColor Yellow` (score 1)
- L42: `Write-Host "===========================" -ForegroundColor Yellow` (score 1)
- … plus 22 more lines

## cleanup_mangled_files.py  (score: 7, touchable: False)

- L3: `Clean up files with placeholder text and fix them properly.` (score 2)
- L10: `    """Fix files that have been mangled with placeholder text."""` (score 2)
- L17: `        # Skip if file doesn't have placeholder text` (score 2)
- L69: `            f.write(clean_content)` (score 1)

## temp_script.py  (score: 5, touchable: False)

- L37: `open(out,"w",encoding="utf8").write(json.dumps(summary, indent=2))` (score 3)
- L38: `print(json.dumps(summary, indent=2))` (score 2)

## advanced_parser_fix.py  (score: 4, touchable: False)

- L75: `                f.write(content)` (score 1)
- L95: `            f.write(content)` (score 1)
- L131: `            f.write(content)` (score 1)
- L168: `                        f.write(content)` (score 1)

## temp_analyze.py  (score: 4, touchable: False)

- L145: `# Simulate a merge count: how many NONE would be "absorbed"` (score 2)
- L180: `    json.dump(stats, f, indent=2)` (score 1)
- L183: `    json.dump(examples, f, indent=2)` (score 1)

## temp_summary.py  (score: 4, touchable: False)

- L31: `json.dump(summ, open(out1,"w",encoding="utf8"), indent=2)` (score 1)
- L32: `json.dump(samples, open(out2,"w",encoding="utf8"), indent=2, ensure_ascii=False)` (score 1)
- L33: `print(json.dumps(summ, indent=2))` (score 2)

## comprehensive_syntax_fix_v2.py  (score: 3, touchable: False)

- L56: `                f.write(content)` (score 1)
- L75: `            f.write(mod_content)` (score 1)
- L101: `                f.write('\n'.join(cleaned_lines))` (score 1)

## core\fix_critical_syntax_errors.py  (score: 3, touchable: False)

- L22: `            f.write(content)` (score 1)
- L40: `            f.write(content)` (score 1)
- L81: `            f.write(content)` (score 1)

## fix_incomplete_files.py  (score: 3, touchable: False)

- L39: `                        # Replace the placeholder with actual function name` (score 2)
- L55: `                f.write(content)` (score 1)

## temp_parse.py  (score: 3, touchable: False)

- L3: `examples\pcap\decoded\_plaintext_flow_probe.json"""` (score 1)
- L19: `    f.write(chosen)` (score 1)
- L21: `    f.write(out)` (score 1)

## temp_py_script.py  (score: 3, touchable: False)

- L14: `print(json.dumps(summ, indent=2))` (score 2)
- L16: `json.dump(summ, open(out,"w",encoding="utf8"), indent=2)` (score 1)

## temp_validation.py  (score: 3, touchable: False)

- L4: `parsed = json.load(open('examples/pcap/decoded/dummy_parsed.json','r',encoding='utf8'))` (score 1)
- L22: `print(json.dumps(report,indent=2))` (score 2)

## comprehensive_fix.py  (score: 2, touchable: False)

- L50: `                f.write(content)` (score 1)
- L72: `                f.write(content)` (score 1)

## comprehensive_fix_all.py  (score: 2, touchable: False)

- L77: `                f.write(content)` (score 1)
- L97: `            f.write(content)` (score 1)

## core\fix_remaining_errors.py  (score: 2, touchable: False)

- L36: `                f.write(content)` (score 1)
- L112: `                f.write(content)` (score 1)

## core\fix_vec_generics_v2.py  (score: 2, touchable: False)

- L64: `                f.write(content)` (score 1)
- L98: `                f.write(content)` (score 1)

## fix_gameaction_syntax.py  (score: 2, touchable: False)

- L29: `                    f.write(content)` (score 1)
- L60: `                    f.write(content)` (score 1)

## fix_remaining_syntax.py  (score: 2, touchable: False)

- L49: `                f.write(content)` (score 1)
- L79: `                f.write(fixed_content)` (score 1)

## fix_simple_syntax.py  (score: 2, touchable: False)

- L39: `                f.write(content)` (score 1)
- L69: `                f.write(fixed_content)` (score 1)

## batch_fix.py  (score: 1, touchable: False)

- L24: `                f.write(new_content)` (score 1)

## batch_fix_empty_structs.py  (score: 1, touchable: False)

- L50: `                f.write(content)` (score 1)

## comprehensive_batch_fix.py  (score: 1, touchable: False)

- L43: `                f.write(content)` (score 1)

## comprehensive_cleanup.py  (score: 1, touchable: False)

- L41: `                f.write(content)` (score 1)

## comprehensive_syntax_fix.py  (score: 1, touchable: False)

- L59: `                    f.write(content)` (score 1)

## core\comprehensive_fix.py  (score: 1, touchable: False)

- L74: `                f.write(fixed_content)` (score 1)

## core\fix_all_syntax.py  (score: 1, touchable: False)

- L40: `                f.write(content)` (score 1)

## core\fix_double_braces.py  (score: 1, touchable: False)

- L42: `                f.write(content)` (score 1)

## core\fix_double_braces_simple.py  (score: 1, touchable: False)

- L27: `                f.write(content)` (score 1)

## core\fix_double_delimiters.py  (score: 1, touchable: False)

- L39: `                f.write(content)` (score 1)

## core\fix_extra_parentheses.py  (score: 1, touchable: False)

- L33: `                f.write(content)` (score 1)

## core\fix_final_vec_types.py  (score: 1, touchable: False)

- L38: `                f.write(content)` (score 1)

## core\fix_missing_braces.py  (score: 1, touchable: False)

- L42: `                f.write(content)` (score 1)

## core\fix_missing_parentheses_semicolons.py  (score: 1, touchable: False)

- L36: `                f.write(content)` (score 1)

## core\fix_missing_semicolons.py  (score: 1, touchable: False)

- L57: `                f.write(content)` (score 1)

## core\fix_ok_expressions.py  (score: 1, touchable: False)

- L36: `                f.write(content)` (score 1)

## core\fix_ok_expressions_precise.py  (score: 1, touchable: False)

- L42: `                f.write(content)` (score 1)

## core\fix_ok_expressions_v2.py  (score: 1, touchable: False)

- L47: `                f.write(content)` (score 1)

## core\fix_remaining_hash_fields.py  (score: 1, touchable: False)

- L51: `                    f.write(fixed_content)` (score 1)

## core\fix_specific_double_braces.py  (score: 1, touchable: False)

- L42: `                f.write(content)` (score 1)

## core\fix_unwrap_braces.py  (score: 1, touchable: False)

- L35: `                f.write(content)` (score 1)

## core\fix_vec_generics.py  (score: 1, touchable: False)

- L46: `                f.write(content)` (score 1)

## enhanced_fix_parsers.py  (score: 1, touchable: False)

- L47: `                f.write(content)` (score 1)

## exact_pattern_fix.py  (score: 1, touchable: False)

- L27: `                f.write(content)` (score 1)

## final_comprehensive_fix.py  (score: 1, touchable: False)

- L49: `                f.write(content)` (score 1)

## final_fix_all.py  (score: 1, touchable: False)

- L50: `                f.write(content)` (score 1)

## final_syntax_fix.py  (score: 1, touchable: False)

- L42: `                f.write(content)` (score 1)

## fix_action_function_names.py  (score: 1, touchable: False)

- L50: `                    f.write(content)` (score 1)

## fix_all_parser_files.py  (score: 1, touchable: False)

- L45: `                f.write(content)` (score 1)

## fix_all_parser_syntax.py  (score: 1, touchable: False)

- L62: `                    f.write(content)` (score 1)

## fix_all_syntax_errors.py  (score: 1, touchable: False)

- L45: `                        f.write(content)` (score 1)

## fix_brackets.py  (score: 1, touchable: False)

- L15: `            f.write(content)` (score 1)

## fix_closing_braces.py  (score: 1, touchable: False)

- L24: `                f.write(content)` (score 1)

## fix_comprehensive_syntax.py  (score: 1, touchable: False)

- L33: `                f.write(content)` (score 1)

## fix_corrupted_files.py  (score: 1, touchable: False)

- L39: `                f.write(content)` (score 1)

## fix_delimiters.py  (score: 1, touchable: False)

- L29: `                f.write(content)` (score 1)

## fix_delimiters_all.py  (score: 1, touchable: False)

- L37: `                f.write(content)` (score 1)

## fix_final_braces.py  (score: 1, touchable: False)

- L30: `                f.write(content)` (score 1)

## fix_final_syntax_errors.py  (score: 1, touchable: False)

- L42: `                            f.write(content)` (score 1)

## fix_generated_rust_files.py  (score: 1, touchable: False)

- L48: `                            f.write(content)` (score 1)

## fix_json_fields.py  (score: 1, touchable: False)

- L36: `                f.write(content)` (score 1)

## fix_json_quotes.py  (score: 1, touchable: False)

- L33: `                f.write(content)` (score 1)

## fix_json_references.py  (score: 1, touchable: False)

- L46: `                f.write(content)` (score 1)

## fix_parser_compilation_issues.py  (score: 1, touchable: False)

- L117: `                f.write(content)` (score 1)

## fix_remaining_braces.py  (score: 1, touchable: False)

- L52: `                f.write(content)` (score 1)

## fix_remaining_structs.py  (score: 1, touchable: False)

- L48: `                f.write(content)` (score 1)

## fix_remaining_syntax_errors.py  (score: 1, touchable: False)

- L34: `                            f.write(content)` (score 1)

## fix_reserved_keywords.py  (score: 1, touchable: False)

- L31: `                f.write(content)` (score 1)

## fix_specific_syntax.py  (score: 1, touchable: False)

- L74: `                f.write(content)` (score 1)

## fix_struct_syntax.py  (score: 1, touchable: False)

- L29: `                f.write(content)` (score 1)

## fix_syntax_errors.py  (score: 1, touchable: False)

- L43: `                f.write(content)` (score 1)

## fix_syntax_issues.py  (score: 1, touchable: False)

- L16: `                f.write(content)` (score 1)

## fix_type_mappings.py  (score: 1, touchable: False)

- L26: `                f.write(content)` (score 1)

## fix_unclosed_delimiters.py  (score: 1, touchable: False)

- L32: `                f.write(content)` (score 1)

## global_fix.py  (score: 1, touchable: False)

- L41: `                f.write(content)` (score 1)

## orchestrator\tools\extract_flows.py  (score: 1, touchable: False)

- L128: `            f.write(payload)` (score 1)

## repo_diagnostic_collector.py  (score: 1, touchable: False)

- L370: `        json.dump(results, f, indent=2, ensure_ascii=False)` (score 1)

## simple_fix.py  (score: 1, touchable: False)

- L60: `                f.write(new_content)` (score 1)

## simple_fix_brackets.py  (score: 1, touchable: False)

- L32: `                f.write(content)` (score 1)

## simple_parser_fix.py  (score: 1, touchable: False)

- L81: `                f.write(content)` (score 1)

## ultra_targeted_fix.py  (score: 1, touchable: False)

- L32: `                f.write(content)` (score 1)

