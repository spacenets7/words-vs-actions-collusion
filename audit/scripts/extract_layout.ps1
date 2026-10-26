$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$pdfTool = Join-Path $taskRoot 'audit\tools\poppler-26.09.0\Library\bin\pdftotext.exe'
if (-not (Test-Path -LiteralPath $pdfTool)) { $pdfTool = (Get-Command pdftotext).Source }
Get-ChildItem -LiteralPath (Join-Path $taskRoot 'papers') -Filter '*.pdf' | ForEach-Object {
    $destination = Join-Path $taskRoot ('audit\text\' + $_.BaseName + '.layout.txt')
    & $pdfTool -layout $_.FullName $destination
    if ($LASTEXITCODE -ne 0) { throw "pdftotext failed: $($_.Name)" }
    Write-Output $destination
}
$manifestPath = Join-Path $taskRoot 'audit\text\manifest.json'
if (Test-Path -LiteralPath $manifestPath) {
    $records = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    foreach ($record in $records) {
        $stem = [System.IO.Path]::GetFileNameWithoutExtension($record.file)
        $layoutFile = Join-Path $taskRoot ('audit\text\' + $stem + '.layout.txt')
        $record.pdftotext = Test-Path -LiteralPath $layoutFile
        $record | Add-Member -NotePropertyName layout_sha256 -NotePropertyValue ((Get-FileHash -LiteralPath $layoutFile -Algorithm SHA256).Hash.ToLower()) -Force
    }
    $records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding utf8
}
