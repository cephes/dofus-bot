Get-ChildItem core\src\retroproto_parsers\generated -Filter *.rs -Recurse |
  ForEach-Object {
    $p = $_.FullName
    $t = Get-Content $p -Raw
    if ($t -notmatch '#\s*\[\s*derive\s*\(\s*Debug\s*,\s*Clone\s*,\s*Default\s*,\s*Serialize\s*,\s*Deserialize\s*\)\s*\]') {
      $t = $t -replace '(?ms)^(pub\s+struct\s+\w+\s*\{)',
                      "#[derive(Debug, Clone, Default, Serialize, Deserialize)]`r`n`$1"
      Set-Content $p $t -NoNewline
      Write-Host "derive added: $p"
    }
  }