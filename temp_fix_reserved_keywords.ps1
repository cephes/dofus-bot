Get-ChildItem core\src\retroproto_parsers\generated -Filter *.rs -Recurse |
  ForEach-Object {
    (Get-Content $_.FullName -Raw) `
    -replace '\bpub\s+type\b', 'pub r#type' `
    -replace '\blet\s+type\b', 'let r#type' `
    -replace '\btype,', 'r#type,' |
    Set-Content $_.FullName
  }