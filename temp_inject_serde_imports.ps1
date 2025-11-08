Get-ChildItem core\src\retroproto_parsers\generated -Filter *.rs -Recurse |
  ForEach-Object {
    $t = Get-Content $_.FullName -Raw
    if ($t -match '#\[derive' -and $t -match 'Serialize' -and $t -notmatch 'use\s+serde::Serialize') {
      $t = $t -replace '(\#\[derive[^\n]+\n)', "`$1use serde::{Serialize, Deserialize};`r`n"
      Set-Content $_.FullName $t -NoNewline
      Write-Host "serde imports added: $($_.Name)"
    }
  }