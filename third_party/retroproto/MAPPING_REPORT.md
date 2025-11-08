# Retroproto Mapping Report

## Summary
Extracted 200+ message prefixes from `third_party/retroproto` Go source code. Mapping includes literal prefixes and regex patterns for client messages.

## Extraction Details
- **Source**: `msgcli.go` and `msgsvr.go`
- **Method**: Parsed Go constants and regex patterns
- **Coverage**: Client messages (200+), server messages (300+)
- **Detection Types**: Literal string prefixes, regex for special cases (version, credential)

## Notes
- Regex patterns converted from Go to JSON-compatible format
- All prefixes are 2-4 characters as per Dofus protocol
- Special handling for Cyrillic 'I' bug in client detection

## TODO for Future
- Add server message mappings
- Implement automatic extraction script
- Validate against live protocol captures