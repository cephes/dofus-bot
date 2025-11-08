$repo = (Resolve-Path ".").Path
$pcap = Join-Path $repo "core\dummy.pcap"
$flow = Join-Path $repo "examples\pcap\flows\dummy_stream.bin"
# DEMO_DISABLED: $reass = Join-Path $repo "examples\pcap\decoded\dummy_reassembled.json"
# DEMO_DISABLED: $parsed = Join-Path $repo "examples\pcap\decoded\dummy_parsed.json"
# DEMO_DISABLED: $ndj = Join-Path $repo "examples\pcap\decoded\dummy_parsed.ndjson"

# 1) build
Push-Location core
cargo build --release
Pop-Location

# 2) extract flow from pcap
.\core\target\release\pcap2flow.exe --pcap "$pcap" --out "$flow"

# 3) reassemble logical messages (already present in repo)
.\core\target\release\reassemble.exe --input "$flow" --output "$reass"

# 4) parse with generated parsers
.\core\target\release\parse_messages.exe --in "$reass" --out "$parsed" --ndjson "$ndj"

# 5) small summary
# DEMO_DISABLED: Write-Host "`n=== Done ==="
# DEMO_DISABLED: Write-Host "Reassembled:" $reass
# DEMO_DISABLED: Write-Host "Parsed JSON :" $parsed
# DEMO_DISABLED: Write-Host "NDJSON      :" $ndj