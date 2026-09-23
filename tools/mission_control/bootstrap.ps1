$ErrorActionPreference = 'Stop'

Write-Host 'MISSION_CONTROL PHASE 1-4'
Write-Host 'DISCOVER -> CLASSIFY -> INDEX -> VALIDATE -> SCAFFOLD'
Write-Host 'MIGRATION_AUTHORIZED = FALSE'
Write-Host 'AUTHORITY_CREATED = FALSE'

python tools/mission_control/build_index.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python tools/mission_control/validate_index.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ''
Write-Host 'Dry-run scaffold:'
python tools/mission_control/scaffold.py --dry-run
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ''
Write-Host 'Every generated row begins PENDING_REVIEW and REVIEW_REQUIRED=TRUE.'
Write-Host 'Before marking an artifact REVIEWED, set explicit ARTIFACT_ID, SOURCE_PATHS, and DESTINATION_SUBDIR.'
Write-Host 'Split multi-artifact branches into multiple rows sharing DISCOVERY_ID/BRANCH/SOURCE_SHA.'
Write-Host ''
Write-Host 'Scaffold creation remains a separate explicit command:'
Write-Host '  python tools/mission_control/scaffold.py'
Write-Host ''
Write-Host 'No artifacts copied. No branches moved or deleted. No authority created.'
