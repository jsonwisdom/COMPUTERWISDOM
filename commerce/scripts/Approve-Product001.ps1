$ErrorActionPreference = "Stop"

$ProductPath = "commerce\products\PRODUCT_001.json"
$ReceiptPath = "commerce\receipts\PRODUCT_001_APPROVAL.json"

$p = Get-Content $ProductPath -Raw | ConvertFrom-Json

if (-not (Test-Path $p.digital_asset)) {
    throw "DIGITAL_ASSET_MISSING"
}

$Hash = (Get-FileHash $p.digital_asset -Algorithm SHA256).Hash.ToLower()
$Bytes = (Get-Item $p.digital_asset).Length

Write-Host ""
Write-Host "========== JAY HUMAN REVIEW ==========" -ForegroundColor Cyan
Write-Host "PRODUCT: $($p.title)"
Write-Host "CREATOR: $($p.creator)"
Write-Host "PRICE:   $($p.price_cents) cents $($p.currency)"
Write-Host "ASSET:   $($p.digital_asset)"
Write-Host "BYTES:   $Bytes"
Write-Host "SHA256:  $Hash"
Write-Host ""
Write-Host "Review the product-source folder before approving:" -ForegroundColor Yellow
Write-Host "commerce\product-source\PRODUCT_001"
Write-Host ""

$Expected = "JAY APPROVES PRODUCT_001 FOR PUBLIC SALE"
$Answer = Read-Host "Type exactly: $Expected"

if ($Answer -cne $Expected) {
    Write-Host ""
    Write-Host "NO APPROVAL RECORDED" -ForegroundColor Yellow
    exit 3
}

$p.approval_state = "APPROVED"
$p.public_release_state = "APPROVED_FOR_PUBLIC"

$p |
    ConvertTo-Json -Depth 10 |
    Set-Content -Encoding UTF8 $ProductPath

$Receipt = [ordered]@{
    artifact             = "PRODUCT_001_APPROVAL"
    product_id           = $p.product_id
    creator              = "JAY"
    decision             = "APPROVED_FOR_PUBLIC_SALE"
    digital_asset        = $p.digital_asset
    digital_asset_bytes  = $Bytes
    digital_asset_sha256 = $Hash
    consent_state        = $p.consent_state
    human_input_required = $true
    machine_approved     = $false
    system_recorded_at   = (Get-Date).ToUniversalTime().ToString("o")
    authority_created    = $false
}

$Receipt |
    ConvertTo-Json -Depth 8 |
    Set-Content -Encoding UTF8 $ReceiptPath

Write-Host ""
Write-Host "HUMAN APPROVAL RECORDED" -ForegroundColor Green
Write-Host "Receipt: $ReceiptPath"
