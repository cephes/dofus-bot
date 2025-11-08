#!/usr/bin/env bash
set -euo pipefail
python3 tools/ids/ingest_ids.py
echo "IDs ingested. JSON written to third_party/identifiants/json and mirrored into core/assets/ids"