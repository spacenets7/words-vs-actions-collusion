# Held-out execution entry point. Never run this while tuning development data.
$ErrorActionPreference = 'Stop'
$pilotRoot = $PSScriptRoot
$projectRoot = Split-Path -Parent $pilotRoot
$pilotPython = Join-Path $pilotRoot 'env/Scripts/python.exe'
Push-Location -LiteralPath $projectRoot
try {
    & $pilotPython -X utf8 -m pilot.cli verify-freeze
    if ($LASTEXITCODE -ne 0) { throw 'Frozen configuration verification failed' }
    foreach ($family in 2001..2008) {
        & $pilotPython -X utf8 -m pilot.reconcile
        if ($LASTEXITCODE -ne 0) { throw 'Billing reconciliation failed before the next family' }
        $resultPath = "pilot/runs/test-$family-all.json"
        if (Test-Path -LiteralPath $resultPath) {
            # An existing output is immutable: verify its provenance before resuming.
            & $pilotPython -X utf8 -c 'import sys; from pilot.core import load,digest,CONDITIONS; d=load(sys.argv[1]); c=dict(d["config"]); c["allow_test_execution"]=False; assert d["remote_completed"] and not d["scripted"] and digest(c)==digest(load("pilot/frozen/config.json")); assert len(d["episodes"])==6 and {e["oracle"]["condition"] for e in d["episodes"]}==set(CONDITIONS) and {e["family_id"] for e in d["episodes"]}=={int(sys.argv[2])}' $resultPath $family
            if ($LASTEXITCODE -ne 0) { throw 'Existing output does not match the frozen configuration' }
            continue
        }
        & $pilotPython -X utf8 -m modal run -m pilot.modal_app --config pilot/frozen/config.json --family $family --conditions B,G,I,T,O,H --output $resultPath --execute-test
        if ($LASTEXITCODE -ne 0) { throw 'Run stopped; inspect STATUS.md and the spend ledger' }
    }
    & $pilotPython -X utf8 -m pilot.collect --output pilot/runs/all.json
    if ($LASTEXITCODE -ne 0) { throw 'Collection failed' }
    & $pilotPython -X utf8 -m pilot.review --input pilot/runs/all.json --out pilot/review-full
    if ($LASTEXITCODE -ne 0) { throw 'Blind review export failed' }
    & $pilotPython -X utf8 -m pilot.cli analyze --config pilot/frozen/config.json --input pilot/runs/all.json --out pilot/results
    if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }
}
finally { Pop-Location }
