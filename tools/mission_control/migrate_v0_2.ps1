param(
    [switch]$Execute
)

$ErrorActionPreference = 'Stop'

Write-Host 'MISSION_CONTROL MIGRATION v0.2'
Write-Host 'COPY != AUTHORITY'
Write-Host 'PROVENANCE_RECEIPT != AUTHORITY_GRANT'
Write-Host ''

if (-not $Execute) {
    python tools/mission_control/migrate_v0_2.py
    exit $LASTEXITCODE
}

if ($env:CW_MIGRATION_AUTHORIZED -ne 'TRUE') {
    Write-Error 'Execution denied: set CW_MIGRATION_AUTHORIZED=TRUE only after reviewing the migration plan and explicitly authorizing migration.'
    exit 2
}

python tools/mission_control/migrate_v0_2.py --execute
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python tools/mission_control/validate_migration_v0_2.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ''
Write-Host 'COPY_HASH_VERIFIED = TRUE'
Write-Host 'AUTHORITY_CREATED = FALSE'
Write-Host 'ORIGINAL_BRANCHES_DELETED = FALSE'
