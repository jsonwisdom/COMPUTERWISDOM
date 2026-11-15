param(
  [string]$DriveMirrorPath = '',
  [switch]$Once
)
# CI-FIRST Computer Wisdom PC: read-only dual-route observation.
$ErrorActionPreference = 'Stop'
$intervalSeconds = 300
$logDir = Join-Path $PSScriptRoot 'cw-two-route-logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$targets = @(
  @{ Role = 'PRIMARY'; Worker = 'cw-ooda-emergency-50state-v01'; URL = 'https://emergency.jsonwisdom.com/api/v1/health' },
  @{ Role = 'REPLICA'; Worker = 'cw-ooda-emergency-50state-replica-v01'; URL = 'https://emergency.jsonwisdom.io/api/v1/health' }
)
while ($true) {
  $started = Get-Date
  $results = @(
    foreach ($t in $targets) {
      try {
        $resp = Invoke-WebRequest -Uri $t.URL -Method GET -UseBasicParsing -TimeoutSec 20
        $raw = [string]$resp.Content
        $json = $raw | ConvertFrom-Json
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($raw)
        $sha = [System.Security.Cryptography.SHA256]::Create()
        try {
          $digest = [BitConverter]::ToString($sha.ComputeHash($bytes)).Replace('-', '').ToLowerInvariant()
        } finally { $sha.Dispose() }
        $isPass = ($resp.StatusCode -eq 200 -and
          $json.schema -eq 'cw-ooda-emergency-estate/0.1' -and
          $json.state_count -eq 50 -and
          $json.authority_created -eq $false -and
          $json.live_alerts -eq $false)
        [pscustomobject]@{
          role = $t.Role; worker = $t.Worker; url = $t.URL
          http = [int]$resp.StatusCode; cf_ray = [string]$resp.Headers['CF-Ray']
          schema = $json.schema; states = $json.state_count
          verified_bundles = $json.source_bundles_verified
          body_sha256 = $digest; status = if ($isPass) { 'PASS' } else { 'HOLD' }
        }
      } catch {
        [pscustomobject]@{
          role = $t.Role; worker = $t.Worker; url = $t.URL
          status = 'UNKNOWN'; error = $_.Exception.Message
        }
      }
    }
  )
  $both = @($results | Where-Object { $_.status -eq 'PASS' }).Count -eq 2
  $parity = $both -and ($results[0].body_sha256 -eq $results[1].body_sha256)
  $receipt = [ordered]@{
    observed_utc = (Get-Date).ToUniversalTime().ToString('o')
    identity_label = 'Computer Wisdom PC'
    public_wallet_anchor = '0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0'
    wallet_signature = 'NOT_TESTED'
    dual_route_status = if ($both) { 'PASS' } else { 'UNKNOWN' }
    response_parity = if ($parity) { 'PASS' } else { 'UNKNOWN' }
    cross_provider_failover = 'NOT_ESTABLISHED'
    live_emergency_feed = 'NOT_ESTABLISHED'
    authority_created = $false
    routes = $results
  }
  $stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssfffZ')
  $file = Join-Path $logDir ("cw-ooda-" + $stamp + ".json")
  ($receipt | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $file -Encoding UTF8
  ($receipt | ConvertTo-Json -Depth 8 -Compress) | Add-Content -Path (Join-Path $logDir 'history.jsonl') -Encoding UTF8
  if (-not [string]::IsNullOrWhiteSpace($DriveMirrorPath)) {
    if (Test-Path -LiteralPath $DriveMirrorPath -PathType Container) {
      try {
        $folder = Join-Path $DriveMirrorPath ('ComputerWisdom-OODA-Emergency\' + (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd'))
        New-Item -ItemType Directory -Force -Path $folder | Out-Null
        Copy-Item -LiteralPath $file -Destination (Join-Path $folder (Split-Path $file -Leaf)) -ErrorAction Stop
        Write-Host "Copied locally to Google Drive sync folder; CLOUD_SYNC=UNKNOWN until Drive readback."
      } catch { Write-Warning ("Drive copy failed: " + $_.Exception.Message) }
    } else { Write-Warning 'DriveMirrorPath not mounted; mirror NOT_CONFIGURED' }
  }
  $results | Format-Table role, http, states, status, cf_ray -AutoSize
  Write-Host "Receipt: $file | Dual route: $($receipt.dual_route_status) | Parity: $($receipt.response_parity)"
  if ($Once) { break }
  $elapsed = ((Get-Date) - $started).TotalSeconds
  Start-Sleep -Seconds ([int][Math]::Max(0, 300 - [Math]::Ceiling($elapsed)))
}
