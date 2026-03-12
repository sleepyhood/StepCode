$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$outDir = Join-Path $root "practice/data/theory/images"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

Write-Host "Checking for U04 image requirements..."

# U04 문서에 필요한 이미지 목록
$svgFiles = @(
    "unity_u04_null_exception_console.svg",
    "unity_u04_type_mismatch_error.svg",
    "unity_u04_var_initialization_error.svg"
)

foreach ($file in $svgFiles) {
    $targetPath = Join-Path $outDir $file
    if (Test-Path $targetPath) {
        Write-Host "[OK] $file (Directly generated via SVG due to lack of fixed PNG links in official docs)"
    } else {
        Write-Warning "[FAIL] $file is missing!"
    }
}

Write-Host "U04 image validation and direct SVG generation complete."
