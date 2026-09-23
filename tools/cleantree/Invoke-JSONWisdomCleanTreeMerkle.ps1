#requires -Version 7.2
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$InventoryCsv,
    [Parameter(Mandatory)][string]$WorkspaceRoot,
    [string]$OutputRoot = (Join-Path $PWD.Path "JSONWisdom-CleanTree-Receipts"),
    [string]$PreviousInventoryCsv,
    [switch]$EnableSecretContainerHmac
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-Sha256Bytes {
    param([Parameter(Mandatory)][byte[]]$Bytes)
    return [System.Security.Cryptography.SHA256]::HashData($Bytes)
}

function Get-Sha256Hex {
    param([Parameter(Mandatory)][byte[]]$Bytes)
    return [Convert]::ToHexString((Get-Sha256Bytes $Bytes)).ToLowerInvariant()
}

function Get-Utf8Bytes {
    param([Parameter(Mandatory)][string]$Text)
    return [System.Text.UTF8Encoding]::new($false).GetBytes($Text)
}

function Get-Utf8OrdinalSortKey {
    param(
        [Parameter(Mandatory)][string]$Repository,
        [Parameter(Mandatory)][string]$RelativePath
    )
    # Hex encoding converts the exact UTF-8 byte sequence into an ASCII key.
    # Sorting this key is stable across Windows/Linux cultures and preserves
    # ordinal byte order, including uppercase/lowercase distinctions.
    return [Convert]::ToHexString(
        (Get-Utf8Bytes ($Repository + [char]0 + $RelativePath))
    )
}

function Get-MerkleRoot {
    param([Parameter(Mandatory)][byte[][]]$Leaves)
    if ($Leaves.Count -eq 0) {
        return Get-Sha256Hex (Get-Utf8Bytes "CLEANTREE_EMPTY_V1")
    }
    $level = [System.Collections.Generic.List[byte[]]]::new()
    foreach ($leaf in $Leaves) { $level.Add($leaf) }
    while ($level.Count -gt 1) {
        $next = [System.Collections.Generic.List[byte[]]]::new()
        for ($i = 0; $i -lt $level.Count; $i += 2) {
            $left = $level[$i]
            $right = if (($i + 1) -lt $level.Count) { $level[$i + 1] } else { $left }
            $combined = [byte[]]::new(64)
            [Array]::Copy($left, 0, $combined, 0, 32)
            [Array]::Copy($right, 0, $combined, 32, 32)
            $next.Add((Get-Sha256Bytes $combined))
        }
        $level = $next
    }
    return [Convert]::ToHexString($level[0]).ToLowerInvariant()
}

function Get-HardwareProfile {
    $cpuName = "UNKNOWN"
    $logicalProcessors = [Environment]::ProcessorCount
    $gpuNames = @()
    try {
        $cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
        if ($cpu) {
            $cpuName = [string]$cpu.Name
            $logicalProcessors = [int]$cpu.NumberOfLogicalProcessors
        }
        $gpuNames = @(Get-CimInstance Win32_VideoController | ForEach-Object { [string]$_.Name })
    } catch {
        # Hardware discovery is informational and must not block inventory proof.
    }
    return [pscustomobject][ordered]@{
        cpu_name = $cpuName
        logical_processors = $logicalProcessors
        ryzen_detected = ($cpuName -match "(?i)Ryzen")
        recommended_parallel_corridors = [Math]::Max(1, [Math]::Min(8, $logicalProcessors))
        gpu_names = $gpuNames
        radeon_detected = [bool]($gpuNames -match "(?i)Radeon")
        gpu_acceleration_used = $false
        computation_mode = "DETERMINISTIC_CPU"
    }
}

function Get-ReversePatchAction {
    param([Parameter(Mandatory)][string]$Classification)
    switch ($Classification) {
        "SECRET" { return "ROTATE_IF_LIVE_AND_REMOVE_FROM_FUTURE_COMMITS_AFTER_HUMAN_CONFIRMATION" }
        "PRIVATE_IP" { return "REVIEW_FOR_PRIVATE_IP_MIGRATION" }
        "QUARANTINE" { return "ISOLATE_FOR_HUMAN_PRIVACY_REVIEW" }
        "CONTROLLED" { return "VERIFY_PUBLIC_INTEROPERABILITY_MINIMUM" }
        default { return "NO_CHANGE_PROPOSED" }
    }
}

$inventoryFull = [IO.Path]::GetFullPath($InventoryCsv)
$workspaceFull = [IO.Path]::GetFullPath($WorkspaceRoot)
$outputFull = [IO.Path]::GetFullPath($OutputRoot)
if (-not (Test-Path -LiteralPath $inventoryFull -PathType Leaf)) { throw "Inventory not found: $inventoryFull" }
if (-not (Test-Path -LiteralPath $workspaceFull -PathType Container)) { throw "Workspace not found: $workspaceFull" }
New-Item -ItemType Directory -Path $outputFull -Force | Out-Null

$rows = @(Import-Csv -LiteralPath $inventoryFull)
$rows = @(
    $rows | Sort-Object @{
        Expression = {
            Get-Utf8OrdinalSortKey -Repository ([string]$_.repository) -RelativePath ([string]$_.relative_path)
        }
    }
)
$leafRecords = [System.Collections.Generic.List[object]]::new()
$leafBytes = [System.Collections.Generic.List[byte[]]]::new()
$reversePatch = [System.Collections.Generic.List[object]]::new()

$hmacKey = $null
if ($EnableSecretContainerHmac) {
    $keyText = [Environment]::GetEnvironmentVariable("CLEANTREE_HMAC_KEY_B64")
    if ([string]::IsNullOrWhiteSpace($keyText)) { throw "CLEANTREE_HMAC_KEY_B64 is required when HMAC is enabled." }
    try { $hmacKey = [Convert]::FromBase64String($keyText) } catch { throw "CLEANTREE_HMAC_KEY_B64 is not valid Base64." }
    if ($hmacKey.Length -lt 32) { throw "HMAC key must contain at least 32 bytes." }
}

foreach ($row in $rows) {
    $fields = @(
        "CLEANTREE_LEAF_V1", [string]$row.repository, [string]$row.commit_sha,
        [string]$row.relative_path, [string]$row.bytes, ([string]$row.sha256).ToLowerInvariant(),
        [string]$row.suggested_classification, [string]$row.rule_ids, [string]$row.content_scan_state
    )
    $canonical = $fields -join "`n"
    $leafHashBytes = Get-Sha256Bytes (Get-Utf8Bytes $canonical)
    $leafHash = [Convert]::ToHexString($leafHashBytes).ToLowerInvariant()
    $leafBytes.Add($leafHashBytes)

    $containerHmac = $null
    if ($EnableSecretContainerHmac -and $row.suggested_classification -eq "SECRET") {
        $repoName = ([string]$row.repository).Split("/")[-1]
        $filePath = Join-Path (Join-Path $workspaceFull $repoName) (([string]$row.relative_path) -replace "/", [IO.Path]::DirectorySeparatorChar)
        if (Test-Path -LiteralPath $filePath -PathType Leaf) {
            $hmac = [System.Security.Cryptography.HMACSHA256]::new($hmacKey)
            try {
                $stream = [IO.File]::OpenRead($filePath)
                try { $containerHmac = [Convert]::ToHexString($hmac.ComputeHash($stream)).ToLowerInvariant() }
                finally { $stream.Dispose() }
            } finally { $hmac.Dispose() }
        }
    }

    $leafRecords.Add([pscustomobject][ordered]@{
        repository = $row.repository
        relative_path = $row.relative_path
        leaf_sha256 = $leafHash
        secret_container_hmac_sha256 = $containerHmac
        raw_secret_recorded = $false
    })
    $reversePatch.Add([pscustomobject][ordered]@{
        repository = $row.repository
        relative_path = $row.relative_path
        current_classification = $row.suggested_classification
        proposed_action = Get-ReversePatchAction ([string]$row.suggested_classification)
        patch_applied = $false
        human_approval_required = $true
    })
}

$merkleRoot = Get-MerkleRoot -Leaves @($leafBytes)
$hardware = Get-HardwareProfile

$delta = [ordered]@{ previous_inventory_supplied = $false; added = 0; removed = 0; changed = 0; unchanged = 0 }
if ($PreviousInventoryCsv) {
    $previousFull = [IO.Path]::GetFullPath($PreviousInventoryCsv)
    if (-not (Test-Path -LiteralPath $previousFull -PathType Leaf)) { throw "Previous inventory not found: $previousFull" }
    $delta.previous_inventory_supplied = $true
    $old = @{}
    foreach ($r in @(Import-Csv $previousFull)) { $old["$($r.repository)|$($r.relative_path)"] = [string]$r.sha256 }
    $new = @{}
    foreach ($r in $rows) { $new["$($r.repository)|$($r.relative_path)"] = [string]$r.sha256 }
    foreach ($key in $new.Keys) {
        if (-not $old.ContainsKey($key)) { $delta.added++ }
        elseif ($old[$key] -ne $new[$key]) { $delta.changed++ }
        else { $delta.unchanged++ }
    }
    foreach ($key in $old.Keys) { if (-not $new.ContainsKey($key)) { $delta.removed++ } }
}

$runId = "CLEANTREE_MERKLE_" + (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
$leavesPath = Join-Path $outputFull "$runId.leaves.json"
$reversePatchPath = Join-Path $outputFull "$runId.reverse-patch-plan.csv"
$receiptPath = Join-Path $outputFull "$runId.receipt.json"

$leafRecords | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $leavesPath -Encoding utf8
$reversePatch | Export-Csv -LiteralPath $reversePatchPath -NoTypeInformation -Encoding utf8

$receipt = [pscustomobject][ordered]@{
    receipt_type = "SUPER_SECRET_SISTER_OS_CLEANTREE_MERKLE_V0_1"
    run_id = $runId
    inventory_source_sha256 = (Get-FileHash $inventoryFull -Algorithm SHA256).Hash.ToLowerInvariant()
    leaf_count = $leafRecords.Count
    merkle_algorithm = "BINARY_SHA256_DUPLICATE_ODD_V1"
    merkle_root_sha256 = $merkleRoot
    secret_container_hmac_enabled = [bool]$EnableSecretContainerHmac
    secret_values_recorded = $false
    hardware_profile = $hardware
    radical_flywheel_delta = [pscustomobject]$delta
    reverse_patch_plan = [IO.Path]::GetFileName($reversePatchPath)
    reverse_patch_applied = $false
    remote_mutation_performed = $false
    deletion_performed = $false
    authority_created = $false
    next_transition = "FAMILY_HUMAN_REVIEWS_MERKLE_INVENTORY"
}
$receipt | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $receiptPath -Encoding utf8
$receiptHash = (Get-FileHash $receiptPath -Algorithm SHA256).Hash.ToLowerInvariant()
"$receiptHash  $([IO.Path]::GetFileName($receiptPath))" | Set-Content "$receiptPath.sha256" -Encoding ascii

if ($null -ne $hmacKey) { [Array]::Clear($hmacKey, 0, $hmacKey.Length) }

Write-Host "Merkle inventory complete: $merkleRoot"
Write-Host "Receipt: $receiptPath"
Write-Host "Reverse patch is a plan only; no patch was applied."
