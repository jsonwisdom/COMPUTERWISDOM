# Optional Windows Task Scheduler installer; explicitly requires -Install.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string[]]$Sources,
    [string]$VaultRoot = (Join-Path $env:USERPROFILE 'ComputerWisdom\Flywheel'),
    [Parameter(Mandatory=$true)][string]$MirrorRoot,
    [switch]$Install
)
$ErrorActionPreference='Stop'
if (-not $Install) {
    Write-Output 'PREVIEW ONLY: This would install CW-Flywheel-Ingest at user logon. Add -Install to register it.'
    return
}
$scriptPath = Join-Path $PSScriptRoot 'CW-Flywheel.ps1'
if (-not (Test-Path -LiteralPath $scriptPath)) { throw 'CW-Flywheel.ps1 not found beside installer.' }
function Q([string]$value) { return "'" + $value.Replace("'", "''") + "'" }
$src = '@(' + (($Sources | ForEach-Object { Q $_ }) -join ',') + ')'
$command = "& $(Q $scriptPath) -Sources $src -VaultRoot $(Q $VaultRoot) -MirrorRoot $(Q $MirrorRoot) -Apply"
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($command))
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -NonInteractive -EncodedCommand $encoded"
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 6)
Register-ScheduledTask -TaskName 'CW-Flywheel-Ingest' -Action $action -Trigger $trigger -Settings $settings -Description 'Computer Wisdom local source-to-vault verified copy only; no deletions or publication' -Force | Out-Null
Write-Output 'INSTALLED: CW-Flywheel-Ingest (at user logon only). No current ingestion was run.'