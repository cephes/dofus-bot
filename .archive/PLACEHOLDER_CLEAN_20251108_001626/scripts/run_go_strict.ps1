param(
  [string]$In = "",
  [string]$Ndjson = "examples/pcap/decoded/dummy_go_strict.ndjson",
  [string]$Json   = "examples/pcap/decoded/dummy_go_strict.json"
)
$ErrorActionPreference = "Stop"
if (-not $In) {
  if (Test-Path "examples/pcap/flows/dummy_frames.ndjson") { $In = "examples/pcap/flows/dummy_frames.ndjson" }
  elseif (Test-Path "examples/pcap/decoded/dummy_parsed_new.ndjson") { $In = "examples/pcap/decoded/dummy_parsed_new.ndjson" }
  else { throw "No neutral input found" }
}
Set-Location tools\go_baseline
go run main_strict.go registry.go "../../$In" "../../$Ndjson" "../../$Json"
Set-Location ..
python ../tools/validate_go_baseline.py
Write-Host "Strict baseline written to $Ndjson and $Json. Validation report: GO_BASELINE_VALIDATION.md"