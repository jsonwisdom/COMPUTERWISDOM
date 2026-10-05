param(
    [string]$ProductPath = "commerce\products\PRODUCT_001.json"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $ProductPath)) {
    throw "PRODUCT_NOT_FOUND"
}

$p = Get-Content $ProductPath -Raw | ConvertFrom-Json
$Failures = @()

if ($p.creator -ne "JAY") {
    $Failures += "CREATOR_NOT_JAY"
}

if ($p.approval_state -ne "APPROVED") {
    $Failures += "PRODUCT_NOT_APPROVED"
}

if (@("PASS","NOT_APPLICABLE") -notcontains $p.consent_state) {
    $Failures += "CONSENT_NOT_RESOLVED"
}

if ($p.public_release_state -ne "APPROVED_FOR_PUBLIC") {
    $Failures += "PUBLIC_RELEASE_NOT_APPROVED"
}

if (-not $p.checkout_url) {
    $Failures += "CHECKOUT_NOT_BOUND"
}

if (-not $p.digital_asset -or $p.digital_asset -eq "UNBOUND") {
    $Failures += "DIGITAL_ASSET_NOT_BOUND"
}
elseif (-not (Test-Path $p.digital_asset)) {
    $Failures += "DIGITAL_ASSET_MISSING"
}
else {
    $ActualHash = (Get-FileHash $p.digital_asset -Algorithm SHA256).Hash.ToLower()

    if ($ActualHash -ne $p.digital_asset_sha256) {
        $Failures += "DIGITAL_ASSET_HASH_MISMATCH"
    }
}

if ($Failures.Count -gt 0) {
    [pscustomobject]@{
        verdict = "HOLD"
        product = $p.product_id
        failures = $Failures
        authority_created = $false
    } | ConvertTo-Json -Depth 6

    exit 2
}

[pscustomobject]@{
    verdict = "READY_FOR_FIRST_CUSTOMER"
    product = $p.product_id
    price_cents = $p.price_cents
    checkout_url = $p.checkout_url
    asset_sha256 = $p.digital_asset_sha256
    authority_created = $false
} | ConvertTo-Json -Depth 6
