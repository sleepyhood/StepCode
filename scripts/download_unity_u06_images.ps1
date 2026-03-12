$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$srcDir = Join-Path $root "practice/data/theory/unity/수정본/사진"
$outDir = Join-Path $root "practice/data/theory/images"

# 1. 파일 복사 및 이름 매핑 규칙 (적절한 이미지 검증 후 복사 진행)
$map = @{
    "Input_horizontal.png" = "unity_u06_input_horizontal.png"
}

Write-Host "Checking and copying valid images from user provided directory..."
foreach ($key in $map.Keys) {
    $srcPath = Join-Path $srcDir $key
    $targetPath = Join-Path $outDir $map[$key]
    
    if (Test-Path $srcPath) {
        Copy-Item $srcPath $targetPath -Force
        Write-Host "[OK] Copied valid image $key -> $($map[$key])"
    } else {
        Write-Warning "[FAIL] Source image not found: $srcPath"
    }
}

Write-Host "U06 SVG Validation..."
$svgFiles = @(
    "unity_u06_time_deltatime_flow.svg",
    "unity_u06_translate_vs_position.svg"
)
foreach ($file in $svgFiles) {
    $targetPath = Join-Path $outDir $file
    if (Test-Path $targetPath) {
        Write-Host "[OK] $file (Generated via SVG)"
    } else {
        Write-Warning "[FAIL] $file is missing!"
    }
}

Write-Host "U06 Image copy and script validation complete."
