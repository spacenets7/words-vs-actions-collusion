param(
    [string]$PythonExe = 'C:\Users\ussid\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe',
    [switch]$Reextract
)
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Push-Location $taskRoot
try {
    if ($Reextract) {
        & $PythonExe 'audit/scripts/extract_papers.py'
        if ($LASTEXITCODE -ne 0) { throw 'PDF extraction failed' }
        & 'audit/scripts/extract_layout.ps1'
    }
    & $PythonExe -u 'audit/scripts/verify_audit.py' | Out-File -LiteralPath 'audit/evidence/verification.log' -Encoding utf8
    if ($LASTEXITCODE -ne 0) { throw 'Offline verification failed' }
    & $PythonExe 'audit/scripts/build_reports.py'
    if ($LASTEXITCODE -ne 0) { throw 'Report generation failed' }
    & $PythonExe 'audit/scripts/validate_reports.py'
    if ($LASTEXITCODE -ne 0) { throw 'Report validation failed' }
} finally {
    Pop-Location
}
