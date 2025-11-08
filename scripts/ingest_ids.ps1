param()
$ErrorActionPreference = "Stop"
python tools/ids/ingest_ids.py
Write-Host "IDs ingested. JSON written to third_party/identifiants/json and mirrored into core/assets/ids"