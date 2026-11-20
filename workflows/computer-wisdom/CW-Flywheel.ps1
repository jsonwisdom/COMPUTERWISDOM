# Computer Wisdom Flywheel v1.0 — Windows PowerShell 5.1+
# Safe-by-default: preview unless -Apply; source folders are never modified.
[CmdletBinding()]
param(
    [string[]]$Sources = @(),
    [string]$VaultRoot = (Join-Path $env:USERPROFILE 'ComputerWisdom\Flywheel'),
    [string]$MirrorRoot = '',
    [int]$MinAgeMinutes = 10,
    [int]$MaxFiles = 250,
    [switch]$Apply,
    [switch]$Audit
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($MinAgeMinutes -lt 0 -or $MaxFiles -lt 1) { throw 'Invalid MinAgeMinutes or MaxFiles.' }

function FullPath([string]$P) { return [IO.Path]::GetFullPath($P).TrimEnd([char[]]@('\','/')) }
function Within([string]$Child, [string]$Parent) {
    $c = FullPath $Child; $p = FullPath $Parent
    return ($c.Equals($p, [StringComparison]::OrdinalIgnoreCase) -or
        $c.StartsWith($p + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase))
}
function Digest([string]$Path) { return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Json([object]$Value) { return (ConvertTo-Json -InputObject $Value -Depth 9 -Compress) }
function Record([object]$Event) {
    if (-not $Apply) { return }
    $line = Json $Event
    $writer = New-Object IO.StreamWriter($script:Journal, $true, (New-Object Text.UTF8Encoding($false)))
    try { $writer.WriteLine($line); $writer.Flush() } finally { $writer.Dispose() }
}
function Verify-Object([string]$Path, [string]$Hash) {
    return ((Test-Path -LiteralPath $Path -PathType Leaf) -and ((Digest $Path) -eq $Hash))
}
function Copy-Verified([string]$From, [string]$To, [string]$Hash) {
    if (Test-Path -LiteralPath $To) {
        if (-not (Verify-Object $To $Hash)) { throw "Existing object checksum mismatch: $To" }
        return
    }
    $dir = Split-Path -Parent $To
    [IO.Directory]::CreateDirectory($dir) | Out-Null
    $temp = Join-Path $dir ('.cw-partial-' + [guid]::NewGuid().ToString('N'))
    try {
        Copy-Item -LiteralPath $From -Destination $temp -ErrorAction Stop
        if (-not (Verify-Object $temp $Hash)) { throw "Copy checksum mismatch: $From" }
        Move-Item -LiteralPath $temp -Destination $To -ErrorAction Stop
        if (-not (Verify-Object $To $Hash)) { throw "Final checksum mismatch: $To" }
    } finally {
        # Only our own transient staging file may be removed; never source/archive originals.
        if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Force }
    }
}

$vault = FullPath $VaultRoot
$mirror = if ($MirrorRoot) { FullPath $MirrorRoot } else { '' }
if ($mirror -and ((Within $mirror $vault) -or (Within $vault $mirror))) {
    throw 'Vault and mirror must be different non-nested directories.'
}
foreach ($source in $Sources) {
    $s = FullPath $source
    if (-not (Test-Path -LiteralPath $s -PathType Container)) { throw "Source folder not found: $s" }
    if ((Within $vault $s) -or (Within $s $vault) -or
        ($mirror -and ((Within $mirror $s) -or (Within $s $mirror)))) {
        throw 'Source, vault and mirror must not overlap.'
    }
}
if (-not $Audit -and $Sources.Count -eq 0) { throw 'Specify -Sources for ingestion or -Audit to validate receipts.' }
$script:Journal = Join-Path $vault 'receipts.jsonl'
$queue = Join-Path $vault 'queue'
$allowed = @('.jpg','.jpeg','.png','.heic','.heif','.gif','.tif','.tiff','.webp','.mov','.mp4','.m4v','.pdf','.txt','.md','.json','.csv','.docx','.xlsx','.pptx','.wav','.mp3')
$media = @('.jpg','.jpeg','.png','.heic','.heif','.gif','.tif','.tiff','.webp','.mov','.mp4','.m4v')
$events = @()
if (Test-Path -LiteralPath $script:Journal) {
    $events = @(Get-Content -LiteralPath $script:Journal -Encoding UTF8 | Where-Object { $_.Trim() } | ForEach-Object { $_ | ConvertFrom-Json })
}

if ($Audit) {
    $targets = @($events | Where-Object { $_.status -in @('PASS_2COPY','HOLD_SECOND_COPY') } |
        Group-Object archive | ForEach-Object { $_.Group[-1] })
    $pass = 0; $hold = 0; $fail = 0
    foreach ($r in $targets) {
        try {
            if (-not (Verify-Object $r.archive $r.sha256)) { $fail++; Write-Output "FAIL vault: $($r.archive)"; continue }
            if (-not $r.mirror -or -not (Test-Path -LiteralPath $r.mirror)) { $hold++; Write-Output "HOLD second copy: $($r.archive)"; continue }
            if (-not (Verify-Object $r.mirror $r.sha256)) { $fail++; Write-Output "FAIL mirror: $($r.mirror)"; continue }
            $pass++
        } catch { $fail++; Write-Output "FAIL audit: $($_.Exception.Message)" }
    }
    Write-Output "AUDIT PASS_2COPY=$pass HOLD=$hold FAIL=$fail RECORDS=$($targets.Count)"
    return
}

if (-not $Apply) { Write-Output 'PREVIEW ONLY. No files, receipts or tasks will be created. Add -Apply to enable copying.' }
$lock = $null
if ($Apply) {
    [IO.Directory]::CreateDirectory($vault) | Out-Null
    [IO.Directory]::CreateDirectory($queue) | Out-Null
    $lockPath = Join-Path $vault '.ingest.lock'
    try { $lock = [IO.File]::Open($lockPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None) }
    catch { throw 'Another ingestion run may be active. Inspect the lock before removing it manually.' }
}
try {
    $known = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
    foreach ($r in $events) {
        if ($r.status -eq 'PASS_2COPY' -or ($r.status -eq 'HOLD_SECOND_COPY' -and -not $mirror)) {
            [void]$known.Add([string]$r.key)
        }
    }
    $seen = 0; $verified = 0; $held = 0; $failed = 0
    foreach ($source in $Sources) {
        $sourceBase = FullPath $source
        foreach ($item in @(Get-ChildItem -LiteralPath $sourceBase -Recurse -File -Force -ErrorAction Stop)) {
            if ($seen -ge $MaxFiles) { break }
            if ($allowed -notcontains $item.Extension.ToLowerInvariant()) { continue }
            if ($item.Length -eq 0 -or ( ([datetime]::UtcNow - $item.LastWriteTimeUtc).TotalMinutes -lt $MinAgeMinutes)) { continue }
            $rawPath = $item.FullName
            try {
                if (($item.Attributes -band [IO.FileAttributes]::Offline) -ne 0) {
                    $held++; Write-Output "HOLD cloud placeholder: $rawPath"; continue
                }
                if (-not $Apply) { $seen++; Write-Output "ELIGIBLE $($item.Length) bytes: $rawPath"; continue }
                $beforeSize = $item.Length
                $beforeWrite = $item.LastWriteTimeUtc
                $hash = Digest $rawPath
                $relative = Join-Path (Join-Path 'objects' $hash.Substring(0,2)) ($hash + $item.Extension.ToLowerInvariant())
                $archive = Join-Path $vault $relative
                $mirrorTarget = if ($mirror) { Join-Path $mirror $relative } else { '' }
                $key = $rawPath + '|' + $hash
                if ($known.Contains($key)) { continue }
                $seen++  # Limit *new* work, not already ingested objects; batches progress across logons.
                Copy-Verified $rawPath $archive $hash
                $refreshed = Get-Item -LiteralPath $rawPath
                if ($refreshed.Length -ne $beforeSize -or $refreshed.LastWriteTimeUtc -ne $beforeWrite -or (Digest $rawPath) -ne $hash) {
                    throw 'Source changed while ingesting; preserving existing archive and marking HOLD.'
                }
                if ($mirror) { Copy-Verified $archive $mirrorTarget $hash }
                $status = if ($mirror) { 'PASS_2COPY' } else { 'HOLD_SECOND_COPY' }
                $receipt = [ordered]@{
                    schema='cw.flywheel.receipt.v1'; utc=[datetime]::UtcNow.ToString('o'); status=$status
                    key=$key; source=$rawPath; bytes=$beforeSize; sha256=$hash
                    archive=$archive; mirror=$mirrorTarget; algorithm='SHA256'; published=$false
                }
                Record $receipt
                [void]$known.Add($key)
                if ($mirror) {
                    $verified++
                    if ($media -contains $item.Extension.ToLowerInvariant()) {
                        $job = [ordered]@{
                            schema='cw.flywheel.job.v1'; id=[guid]::NewGuid().ToString('N')
                            status='DRAFT_ONLY'; source_hash=$hash; archive=$archive
                            requested_outputs=@('cover-art','x-draft','zora-draft','tiktok-draft')
                            require_human_approval=$true; published=$false
                        }
                        $jobPath = Join-Path $queue ($job.id + '.json')
                        [IO.File]::WriteAllText($jobPath, (Json $job), (New-Object Text.UTF8Encoding($false)))
                    }
                } else { $held++ }
                Write-Output "$status $($item.Name) $hash"
            } catch {
                $failed++
                Write-Output "FAIL $rawPath : $($_.Exception.Message)"
                Record ([ordered]@{ schema='cw.flywheel.receipt.v1'; utc=[datetime]::UtcNow.ToString('o'); status='FAIL'; source=$rawPath; reason=$_.Exception.Message })
            }
        }
        if ($seen -ge $MaxFiles) { break }
    }
    Write-Output "SUMMARY ELIGIBLE=$seen TWO_COPIES_VERIFIED=$verified HOLD=$held FAIL=$failed APPLY=$([bool]$Apply)"
} finally {
    if ($lock) {
        $lock.Dispose()
        # Delete only our self-created lock; source and archived files remain untouched.
        Remove-Item -LiteralPath (Join-Path $vault '.ingest.lock') -Force
    }
}