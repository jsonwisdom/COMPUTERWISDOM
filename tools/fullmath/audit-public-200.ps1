param(
  [string]$BaseUrl = "https://jsonwisdom.github.io/COMPUTERWISDOM/public/fullmath/",
  [string]$ReportRoot = "C:\Users\jsonw\github\_machine-sync\JASON_STORY_WORK_SYNC_20261005-210908",
  [int]$MaxWaitSeconds = 600,
  [int]$PollSeconds = 10
)

$ErrorActionPreference = "Stop"
$run = "FULLMATH_PUBLIC_AUDIT_" + (Get-Date -Format "yyyyMMdd-HHmmss")
$out = Join-Path $ReportRoot $run
New-Item -ItemType Directory -Force -Path $out | Out-Null

$targets = @(
  @{ id="HOME"; url=$BaseUrl },
  @{ id="MATRIX"; url=($BaseUrl + "matrix.html") },
  @{ id="PLAY"; url="https://jsonwisdom.github.io/COMPUTERWISDOM/public-record-verification/game.html" },
  @{ id="KERNEL"; url="https://jsonwisdom.github.io/COMPUTERWISDOM/docs/replay_kernel_v0_1.md" },
  @{ id="ZORA"; url="https://jsonwisdom.github.io/COMPUTERWISDOM/public/zora/CWAAS-FLYWHEEL-001_ZORA_DROP_RECEIPT.md" },
  @{ id="MACHINE"; url="https://jsonwisdom.github.io/COMPUTERWISDOM/docs/layered-machine-speed-scale-blueprint-v0-1.md" }
)

$started = Get-Date
$deadline = $started.AddSeconds($MaxWaitSeconds)
$attempt = 0
$home200 = $false

while((Get-Date) -lt $deadline -and -not $home200){
  $attempt++
  $elapsed = [int]((Get-Date) - $started).TotalSeconds
  $pct = [Math]::Min(99,[int](100 * $elapsed / $MaxWaitSeconds))
  Write-Progress -Activity "Waiting for public HTTP 200" -Status "Attempt $attempt : $BaseUrl" -PercentComplete $pct
  try {
    $r = Invoke-WebRequest -Uri $BaseUrl -Method Head -MaximumRedirection 5 -TimeoutSec 20
    if($r.StatusCode -eq 200){ $home200 = $true; break }
  } catch {}
  Start-Sleep -Seconds $PollSeconds
}
Write-Progress -Activity "Waiting for public HTTP 200" -Completed

$results = @()
for($i=0; $i -lt $targets.Count; $i++){
  $t = $targets[$i]
  Write-Progress -Activity "Auditing FULLMATH links" -Status "$($t.id) $($i+1)/$($targets.Count)" -PercentComplete ([int](100*($i+1)/$targets.Count))
  $status = $null
  $err = $null
  $final = $null
  try {
    $r = Invoke-WebRequest -Uri $t.url -Method Get -MaximumRedirection 5 -TimeoutSec 30
    $status = [int]$r.StatusCode
    $final = $r.BaseResponse.ResponseUri.AbsoluteUri
  } catch {
    if($_.Exception.Response){ $status = [int]$_.Exception.Response.StatusCode.value__ }
    $err = $_.Exception.Message
  }
  $results += [pscustomobject]@{
    id=$t.id; url=$t.url; status=$status; final_url=$final; pass=($status -eq 200); error=$err
  }
}
Write-Progress -Activity "Auditing FULLMATH links" -Completed

$all200 = (@($results | Where-Object { -not $_.pass }).Count -eq 0)
$receipt = [ordered]@{
  schema = "FULLMATH_PUBLIC_200_AUDIT_V0_1"
  run_at = (Get-Date).ToUniversalTime().ToString("o")
  base_url = $BaseUrl
  all_required_200 = $all200
  authority_created = $false
  identity_join = $false
  results = $results
}
$receipt | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 (Join-Path $out "audit.json")
$results | Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $out "links.csv")

$rows = ($results | ForEach-Object {
  "<tr><td>$($_.id)</td><td><a href='$($_.url)'>$($_.url)</a></td><td>$($_.status)</td><td>$($_.pass)</td></tr>"
}) -join [Environment]::NewLine

$proof = "<!doctype html><meta charset='utf-8'><title>FULLMATH Public Proof Audit</title><style>body{font-family:system-ui;max-width:1100px;margin:40px auto;padding:20px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #bbb;padding:8px}</style><h1>FULLMATH Public 200 Audit</h1><p><b>Run:</b> $($receipt.run_at)</p><p><b>ALL_REQUIRED_200:</b> $all200</p><table><tr><th>ID</th><th>URL</th><th>HTTP</th><th>PASS</th></tr>$rows</table><p>NO SOURCE REPO WAS MODIFIED.</p>"
$proof | Set-Content -Encoding UTF8 (Join-Path $out "proof.html")

Write-Host ""
Write-Host "FULLMATH PUBLIC AUDIT COMPLETE"
Write-Host "ALL_REQUIRED_200=$all200"
Write-Host "Report directory: $out"
Write-Host "NO SOURCE REPO WAS MODIFIED."
