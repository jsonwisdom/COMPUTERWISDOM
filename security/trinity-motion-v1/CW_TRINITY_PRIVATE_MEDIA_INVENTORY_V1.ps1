# CI-FIRST Trinity Media — PRIVATE Windows source inventory (candidate).
# READ-ONLY source access; writes one local private JSON receipt. No upload, signing or TPM change.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $SourceFolder,
    [ValidateRange(1, 1000)]
    [int] $MaxFiles = 100
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$dir = Get-Item -LiteralPath $SourceFolder -ErrorAction Stop
if (-not $dir.PSIsContainer) { throw "FAIL: SourceFolder must be an existing folder" }
if (-not $env:LOCALAPPDATA) { throw "FAIL: LOCALAPPDATA missing; no safe receipt location" }
$root = $dir.FullName.TrimEnd([char]'\')
$allowed = @(".jpg", ".jpeg", ".png", ".heic", ".webp", ".mp4", ".mov", ".mkv", ".webm", ".wav", ".mp3", ".flac")
$files = @(Get-ChildItem -LiteralPath $root -File -Recurse -ErrorAction Stop |
    Where-Object {
        $allowed -contains $_.Extension.ToLowerInvariant() -and
        -not (($_.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
    } |
    Select-Object -First $MaxFiles)
$items = @()
foreach ($f in $files) {
    $hash = Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256 -ErrorAction Stop
    $rel = $f.FullName.Substring($root.Length).TrimStart([char]'\')
    $items += [ordered]@{
        relative_path = $rel
        length_bytes = $f.Length
        source_sha256 = $hash.Hash.ToLowerInvariant()
        source_last_write_utc = $f.LastWriteTimeUtc.ToString("o")
    }
}
$receipt = [ordered]@{
    schema = "CW_TRINITY_LOCAL_MEDIA_MANIFEST_V1"
    authority = $false
    status = "SOURCE_FILES_HASHED_ONLY"
    created_utc = [DateTime]::UtcNow.ToString("o")
    source_scope = "USER_SELECTED_PRIVATE_FOLDER"
    max_files = $MaxFiles
    files_count = $items.Count
    possibly_truncated = ($items.Count -eq $MaxFiles)
    entries = $items
    timestamps_are_not_proof_of_capture_time = $true
    human_media_rights_and_consent = "UNKNOWN"
    tpm_quote_verified = $false
    sync_to_server = "NOT_PERFORMED"
    public_release = $false
}
$privateDir = Join-Path $env:LOCALAPPDATA "ComputerWisdom\Trinity\PrivateReceipts"
[void](New-Item -ItemType Directory -Path $privateDir -Force)
$unique = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ") + "_" + [guid]::NewGuid().ToString("N").Substring(0,8)
$out = Join-Path $privateDir ("CW_TRINITY_LOCAL_MEDIA_" + $unique + ".json")
$json = $receipt | ConvertTo-Json -Depth 6
[System.IO.File]::WriteAllText($out, $json + [Environment]::NewLine, (New-Object System.Text.UTF8Encoding($false)))
$receiptHash = (Get-FileHash -LiteralPath $out -Algorithm SHA256).Hash.ToLowerInvariant()
# Do not print private source paths or individual media filenames.
Write-Output ("CI_FIRST=PASS | files_hashed=" + $items.Count + " | possibly_truncated=" + $receipt.possibly_truncated + " | local_receipt_sha256=" + $receiptHash)
Write-Output "PC_SYNC=UNKNOWN | TPM_ATTESTATION=UNKNOWN | NO_MEDIA_UPLOADED"
