[CmdletBinding()]
param(
    [string]$MissionOwner = "Jason Wisdom",
    [string]$IdentityAnchor = "jaywisdom.base.eth",
    [string[]]$Repos = @("COMPUTERWISDOM", "GPKMONSTER", "JOY"),
    [switch]$ReverseReplay,
    [switch]$RunMachineChecks,
    [switch]$EmitGeneralReceipt,
    [bool]$HumanTerminalGate = $true
)

$ErrorActionPreference = "Stop"
$FactoryRoot = $PSScriptRoot
$ControlRepo = Split-Path -Parent $FactoryRoot
$GithubRoot = Split-Path -Parent $ControlRepo
$ConfigPath = Join-Path $FactoryRoot "config\repositories.json"
$GatePath = Join-Path $FactoryRoot "config\gates.json"
$RuntimePath = Join-Path $FactoryRoot "config\runtime-hierarchy.json"
$ReceiptRoot = Join-Path $FactoryRoot "receipts"

function Invoke-CapturedCommand {
    param([string]$FilePath, [string[]]$Arguments, [string]$WorkingDirectory)
    Push-Location $WorkingDirectory
    try {
        $output = & $FilePath @Arguments 2>&1 | Out-String
        $exitCode = $LASTEXITCODE
        return [ordered]@{ exit_code = $exitCode; output = $output.Trim() }
    }
    catch {
        return [ordered]@{ exit_code = 127; output = $_.Exception.Message }
    }
    finally {
        Pop-Location
    }
}

if (-not (Test-Path -LiteralPath $ConfigPath)) {
    throw "Missing repository registry: $ConfigPath"
}

$registry = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
$gates = Get-Content -LiteralPath $GatePath -Raw | ConvertFrom-Json
$runtimeHierarchy = Get-Content -LiteralPath $RuntimePath -Raw | ConvertFrom-Json
$observations = @()

foreach ($repoName in $Repos) {
    $definition = $registry.repositories | Where-Object { $_.name -eq $repoName } | Select-Object -First 1
    if (-not $definition) {
        $observations += [ordered]@{ name = $repoName; state = "HOLD_UNREGISTERED" }
        continue
    }

    $repoPath = Join-Path $GithubRoot $definition.local_folder
    if (-not (Test-Path -LiteralPath (Join-Path $repoPath ".git"))) {
        $observations += [ordered]@{
            name = $repoName
            repository = $definition.repository
            path = $repoPath
            state = "HOLD_CHECKOUT_MISSING"
        }
        continue
    }

    $head = Invoke-CapturedCommand -FilePath "git" -Arguments @("rev-parse", "HEAD") -WorkingDirectory $repoPath
    $branch = Invoke-CapturedCommand -FilePath "git" -Arguments @("branch", "--show-current") -WorkingDirectory $repoPath
    $status = Invoke-CapturedCommand -FilePath "git" -Arguments @("status", "--porcelain") -WorkingDirectory $repoPath
    $check = [ordered]@{ state = "NOT_REQUESTED"; exit_code = $null; output = "" }

    if ($RunMachineChecks) {
        $result = Invoke-CapturedCommand -FilePath "git" -Arguments @("diff", "--check") -WorkingDirectory $repoPath
        $check = [ordered]@{
            state = $(if ($result.exit_code -eq 0) { "PASS_SCOPED_GIT_DIFF_CHECK" } else { "HOLD_CHECK_FAILED" })
            exit_code = $result.exit_code
            output = $result.output
        }
    }

    $observations += [ordered]@{
        name = $repoName
        repository = $definition.repository
        purpose = $definition.purpose
        path = $repoPath
        state = "OBSERVED"
        branch = $branch.output
        commit = $head.output
        dirty_entries = $(if ([string]::IsNullOrWhiteSpace($status.output)) { 0 } else { @($status.output -split "`n").Count })
        machine_check = $check
    }
}

$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$receipt = [ordered]@{
    receipt_type = "GARBAGE_GENERAL_REVERSE_REPLAY_V1"
    observed_at_utc = $timestamp
    mission_owner = $MissionOwner
    operator = "Jay Wisdom"
    identity_anchor = $IdentityAnchor
    commander = "Garbage Jason"
    orchestrator = "Garbage General"
    runtime_hierarchy = $runtimeHierarchy
    reverse_replay_requested = [bool]$ReverseReplay
    repositories = $observations
    gates = $gates
    human_surface = "TERMINAL"
    human_terminal_gate = [ordered]@{
        required = $HumanTerminalGate
        decision = "NOT_CAPTURED"
        operator = $MissionOwner
    }
    authority_created = $false
    external_write = $false
    merge = $false
    publication = $false
}

if ($ReverseReplay) {
    $bashCandidates = @(
        (Join-Path $env:ProgramFiles "Git\bin\bash.exe"),
        (Join-Path $env:ProgramFiles "Git\usr\bin\bash.exe"),
        $(if (${env:ProgramFiles(x86)}) { Join-Path ${env:ProgramFiles(x86)} "Git\bin\bash.exe" }),
        $((Get-Command bash.exe -ErrorAction SilentlyContinue).Source)
    ) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }
    $bashPath = $bashCandidates | Select-Object -First 1
    if ($bashPath) {
        $bashScript = (Join-Path $FactoryRoot "bash\reverse-replay.sh") -replace "\\", "/"
        $bashGithubRoot = $GithubRoot -replace "\\", "/"
        $bashResult = Invoke-CapturedCommand -FilePath $bashPath -Arguments @($bashScript, $bashGithubRoot) -WorkingDirectory $ControlRepo
        $receipt["bash_reverse_replay"] = $bashResult
    }
    else {
        $receipt["bash_reverse_replay"] = [ordered]@{
            exit_code = 127
            output = "Bash unavailable; PowerShell inventory remains valid."
        }
    }
}

Write-Host ""
Write-Host "GARBAGE JASON TERMINAL GATE"
Write-Host "Mission owner: $MissionOwner"
foreach ($observation in $observations) {
    Write-Host ("{0,-16} {1}" -f $observation.name, $observation.state)
}
Write-Host "Machine execution cannot merge or publish."

if ($HumanTerminalGate) {
    $decision = ""
    while ($decision -notin @("ACKNOWLEDGE", "HOLD", "STOP")) {
        $decision = (Read-Host "Jason decision [ACKNOWLEDGE/HOLD/STOP]").Trim().ToUpperInvariant()
    }
    $receipt.human_terminal_gate.decision = $decision
    $receipt.human_terminal_gate.captured_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
}

$json = $receipt | ConvertTo-Json -Depth 12
if ($EmitGeneralReceipt) {
    New-Item -ItemType Directory -Force -Path $ReceiptRoot | Out-Null
    $stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
    $receiptPath = Join-Path $ReceiptRoot "GARBAGE_GENERAL_$stamp.json"
    [System.IO.File]::WriteAllText($receiptPath, $json, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "RECEIPT=$receiptPath"
}

$json
