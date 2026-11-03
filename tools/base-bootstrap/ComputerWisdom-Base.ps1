[CmdletBinding()]
param(
  [ValidateSet('check','address','balance','read','simulate','send','receipt')]
  [string]$Action = 'check',
  [ValidateSet('base','base-sepolia')][string]$Chain,
  [string]$To,
  [string]$Signature,
  [string[]]$Arguments = @(),
  [string]$Value = '0',
  [string]$Data = '0x',
  [string]$EnvFile = (Join-Path $PSScriptRoot '.env'),
  [string]$ReceiptId,
  [string]$ObservedAtUtc,
  [string]$ReceiptOut,
  [switch]$AllowSend
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Fail([string]$Message) { throw "COMPUTERWISDOM: $Message" }
function Need([string]$Name) {
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { Fail "'$Name' is required." }
}
function Import-SafeEnv([string]$Path) {
  $policyPath = Join-Path $PSScriptRoot 'config\allowed-environments.json'

  if (-not (Test-Path -LiteralPath $policyPath)) {
    Fail "DOTENV_POLICY: missing policy file '$policyPath'."
  }

  try {
    $policy = Get-Content -LiteralPath $policyPath -Raw | ConvertFrom-Json
  }
  catch {
    Fail 'DOTENV_POLICY: invalid policy JSON.'
  }

  $allowedKeys = @($policy.allowed_dotenv_keys)
  $allowedEnvNames = @($policy.allowed_env_names)
  $defaultEnvName = [string]$policy.default

  if (-not $defaultEnvName) {
    Fail 'DOTENV_POLICY: missing default ENV_NAME.'
  }

  if ($defaultEnvName -notin $allowedEnvNames) {
    Fail 'DOTENV_POLICY: invalid default ENV_NAME.'
  }

  $entries = [ordered]@{}
  $unknown = [System.Collections.Generic.List[string]]::new()

  if (Test-Path -LiteralPath $Path) {
    foreach ($line in Get-Content -LiteralPath $Path) {
      $s = $line.Trim()

      if (-not $s -or $s.StartsWith('#')) {
        continue
      }

      if ($s -notmatch '^([A-Z][A-Z0-9_]*)=(.*)$') {
        Fail 'DOTENV_POLICY: MALFORMED_LINE'
      }

      $name = $Matches[1]
      $value = $Matches[2].Trim()

      if (
        ($value.StartsWith('"') -and $value.EndsWith('"')) -or
        ($value.StartsWith("'") -and $value.EndsWith("'"))
      ) {
        if ($value.Length -ge 2) {
          $value = $value.Substring(1, $value.Length - 2)
        }
      }

      if ($entries.Contains($name)) {
        Fail "DOTENV_POLICY: DUPLICATE_KEY=$name"
      }

      if ($name -match '(PRIVATE|SECRET|MNEMONIC|SEED|PASSWORD|TOKEN)') {
        Fail "DOTENV_POLICY: SECRET_LIKE_KEY=$name"
      }

      if ($name -notin $allowedKeys) {
        $unknown.Add($name)
      }

      $entries[$name] = $value
    }
  }

  if ($unknown.Count -gt 0) {
    $unknownNames = ($unknown | Sort-Object -Unique) -join ','
    Fail "DOTENV_POLICY: UNKNOWN_KEYS=$unknownNames"
  }

  if ($entries.Contains('ENV_NAME')) {
    $envName = [string]$entries['ENV_NAME']
  }
  else {
    $envName = $defaultEnvName
  }

  if ($envName -notin $allowedEnvNames) {
    Fail "ENV_NAME_INVALID: $envName"
  }

  # Assignment happens only after the entire file passes policy validation.
  foreach ($name in $entries.Keys) {
    [Environment]::SetEnvironmentVariable(
      [string]$name,
      [string]$entries[$name],
      'Process'
    )
  }

  if (-not $entries.Contains('ENV_NAME')) {
    [Environment]::SetEnvironmentVariable(
      'ENV_NAME',
      $defaultEnvName,
      'Process'
    )
  }
}
function Env([string]$Name) { [Environment]::GetEnvironmentVariable($Name, 'Process') }
function Assert-Address([string]$Address, [string]$Label='address') {
  if ($Address -notmatch '^0x[0-9a-fA-F]{40}$') { Fail "$Label must be a 20-byte EVM address." }
}
function Get-WalletAddress {
  switch (Env 'CW_WALLET_MODE') {
    'keystore' {
      $keystore = Env 'CW_KEYSTORE'
      if (-not $keystore -or -not (Test-Path -LiteralPath $keystore)) { Fail 'CW_KEYSTORE must identify an encrypted keystore.' }
      $result = (& cast wallet address --keystore $keystore).Trim()
      if ($LASTEXITCODE -ne 0) { Fail 'Could not derive the keystore address.' }
      return $result
    }
    'hardware' {
      $result = Env 'CW_WALLET_ADDRESS'
      if (-not $result) { Fail 'CW_WALLET_ADDRESS is required for hardware mode.' }
      return $result
    }
    default { Fail "CW_WALLET_MODE must be 'keystore' or 'hardware'." }
  }
}
function Get-TxArgs([string]$From) {
  $tx = @('--from', $From, '--value', $Value)
  if ($Signature) { $tx += $Signature; $tx += $Arguments }
  elseif ($Data -ne '0x') { $tx += @('--data', $Data) }
  return $tx
}
function Get-SignerArgs {
  if ((Env 'CW_WALLET_MODE') -eq 'keystore') { return @('--keystore', (Env 'CW_KEYSTORE')) }
  $hardware = Env 'CW_HARDWARE_WALLET'
  if (-not $hardware) { $hardware = 'ledger' }
  if ($hardware -notin @('ledger','trezor')) { Fail 'CW_HARDWARE_WALLET must be ledger or trezor.' }
  return @("--$hardware")
}

Import-SafeEnv $EnvFile
Need cast
Need forge

if (-not $Chain) { $Chain = Env 'CW_CHAIN' }
if (-not $Chain) { $Chain = 'base-sepolia' }
$expectedId = if ($Chain -eq 'base') { '8453' } else { '84532' }
$rpcName = if ($Chain -eq 'base') { 'CW_BASE_RPC_URL' } else { 'CW_BASE_SEPOLIA_RPC_URL' }
$rpc = Env $rpcName
if (-not $rpc -or $rpc -match 'YOUR_') { Fail "Set $rpcName." }
$actualId = (& cast chain-id --rpc-url $rpc 2>$null).Trim()
if ($LASTEXITCODE -ne 0 -or $actualId -ne $expectedId) { Fail "RPC chain ID '$actualId' does not equal expected '$expectedId'." }

$address = $null
if ($Action -ne 'check') {
  $address = Get-WalletAddress
  Assert-Address $address 'wallet address'
}

switch ($Action) {
  'check' {
    [ordered]@{ action='check'; chain=$Chain; chain_id=[int]$actualId; forge=((& forge --version | Select-Object -First 1) -join ''); cast=((& cast --version | Select-Object -First 1) -join ''); transaction_sent=$false; authority_created=$false } | ConvertTo-Json -Compress
  }
  'address' { $address }
  'balance' { & cast balance $address --ether --rpc-url $rpc; if ($LASTEXITCODE -ne 0) { Fail 'Balance read failed.' } }
  'read' {
    Assert-Address $To 'contract address'
    if (-not $Signature) { Fail 'read requires -Signature.' }
    & cast call $To $Signature @Arguments --rpc-url $rpc
    if ($LASTEXITCODE -ne 0) { Fail 'Contract read failed.' }
  }
  'simulate' {
    Assert-Address $To 'destination address'
    $tx = Get-TxArgs $address
    & cast call $To @tx --rpc-url $rpc
    if ($LASTEXITCODE -ne 0) { Fail 'Simulation reverted or failed; nothing was sent.' }
    '{"action":"simulate","transaction_sent":false,"authority_created":false}'
  }
  'send' {
    Assert-Address $To 'destination address'
    if (-not $AllowSend) { Fail 'Send disabled: simulate first, then explicitly add -AllowSend.' }
    $confirmation = Read-Host "Type SEND $expectedId"
    if ($confirmation -cne "SEND $expectedId") { Fail 'Confirmation mismatch; nothing was sent.' }
    $tx = Get-TxArgs $address
    $signer = Get-SignerArgs
    & cast send $To @tx @signer --chain $expectedId --rpc-url $rpc
    if ($LASTEXITCODE -ne 0) { Fail 'Broadcast failed.' }
  }
  'receipt' {
    if ($ReceiptId -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$') { Fail 'receipt requires a stable -ReceiptId.' }
    $parsed = [DateTimeOffset]::MinValue
    if (-not [DateTimeOffset]::TryParse($ObservedAtUtc, [ref]$parsed) -or $parsed.Offset -ne [TimeSpan]::Zero) { Fail 'receipt requires -ObservedAtUtc with an explicit UTC offset.' }
    if (-not $ReceiptOut) { Fail 'receipt requires an explicit -ReceiptOut path.' }
    $record = [ordered]@{ schema='computerwisdom.base-bootstrap-receipt.v1'; receipt_id=$ReceiptId; observed_at_utc=$parsed.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'); chain=$Chain; chain_id=[int]$expectedId; wallet_address=$address.ToLowerInvariant(); action='boundary_check'; transaction_sent=$false; payment=$false; automatic_signing=$false; merge=$false; push=$false; authority_created=$false }
    $json = $record | ConvertTo-Json -Compress
    [IO.File]::WriteAllText([IO.Path]::GetFullPath($ReceiptOut), $json + "`n", [Text.UTF8Encoding]::new($false))
    $json
  }
}


