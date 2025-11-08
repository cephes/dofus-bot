param(
  [string]$Tp = "third_party/retroproto",
  [string]$Out = "core/src/retroproto_parsers/generated",
  [string]$Map = "third_party/retroproto/mapping_overrides.json",
  [string]$Txt = "third_party/retroproto/mappings_go.txt"
)
Write-Host "== Retroproto Python porter =="
Write-Host "tp:" $Tp
Write-Host "out:" $Out
python -V
python tools/retroproto_porter_py/porter.py --tp $Tp --out $Out --mapping $Map --mappings_txt $Txt
Write-Host "== Done =="