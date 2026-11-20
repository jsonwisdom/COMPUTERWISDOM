# Isolated fixture; run on Windows in PowerShell, no user data touched.
$ErrorActionPreference='Stop'
$test = Join-Path ([IO.Path]::GetTempPath()) ('CW-test-' + [guid]::NewGuid().ToString('N'))
$source = Join-Path $test 'source'
$vault = Join-Path $test 'vault'
$mirror = Join-Path $test 'mirror'
New-Item -ItemType Directory -Path $source -Force | Out-Null
try {
    $photo = Join-Path $source 'test-photo.jpg'
    [IO.File]::WriteAllBytes($photo, [byte[]](0,1,2,3,4,5,6,7))
    $original = (Get-FileHash -LiteralPath $photo -Algorithm SHA256).Hash
    $script = Join-Path $PSScriptRoot 'CW-Flywheel.ps1'
    & $script -Sources @($source) -VaultRoot $vault -MirrorRoot $mirror -MinAgeMinutes 0
    if (Test-Path -LiteralPath $vault) { throw 'FAIL dry-run created vault' }
    & $script -Sources @($source) -VaultRoot $vault -MinAgeMinutes 0 -Apply
    $first = @(Get-Content -LiteralPath (Join-Path $vault 'receipts.jsonl') | ForEach-Object { $_ | ConvertFrom-Json })
    if ($first[-1].status -ne 'HOLD_SECOND_COPY') { throw 'FAIL no-mirror gate' }
    & $script -Sources @($source) -VaultRoot $vault -MirrorRoot $mirror -MinAgeMinutes 0 -Apply
    $second = @(Get-Content -LiteralPath (Join-Path $vault 'receipts.jsonl') | ForEach-Object { $_ | ConvertFrom-Json })
    if ($second[-1].status -ne 'PASS_2COPY') { throw 'FAIL mirror gate' }
    $audit = (& $script -VaultRoot $vault -Audit) -join "`n"
    if ($audit -notmatch 'PASS_2COPY=1 HOLD=0 FAIL=0') { throw "FAIL audit: $audit" }
    & $script -Sources @($source) -VaultRoot $vault -MirrorRoot $mirror -MinAgeMinutes 0 -Apply | Out-Null
    $thirdCount = @(Get-Content -LiteralPath (Join-Path $vault 'receipts.jsonl')).Count
    if ($thirdCount -ne 2) { throw 'FAIL idempotent receipt count' }
    if ((Get-FileHash -LiteralPath $photo -Algorithm SHA256).Hash -ne $original) { throw 'FAIL source modified' }
    $queueCount = @(Get-ChildItem -LiteralPath (Join-Path $vault 'queue') -Filter *.json).Count
    if ($queueCount -ne 1) { throw 'FAIL queue proposal count' }
    $jobFile = Get-ChildItem -LiteralPath (Join-Path $vault 'queue') -Filter *.json | Select-Object -First 1
    $job = Get-Content -LiteralPath $jobFile.FullName -Raw | ConvertFrom-Json
    if ($job.published -or $job.status -ne 'DRAFT_ONLY' -or -not $job.require_human_approval) { throw 'FAIL publication gate' }
    Write-Output 'SELFTEST PASS: dry-run, HOLD, two hashes, audit, idempotent, source unchanged, approval gate'
} finally {
    # Removes only isolated generated test fixtures.
    if (Test-Path -LiteralPath $test) { Remove-Item -LiteralPath $test -Recurse -Force }
}