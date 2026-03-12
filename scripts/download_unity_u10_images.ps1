$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$outDir = Join-Path $root "practice/data/theory/images"

Write-Host "U10 SVG Validation..."
$svgFiles = @(
    "unity_u10_material_color_renderer.svg"
)
foreach ($file in $svgFiles) {
    $targetPath = Join-Path $outDir $file
    if (Test-Path $targetPath) {
        Write-Host "[OK] $file (Generated via SVG)"
    } else {
        Write-Warning "[FAIL] $file is missing!"
    }
}

Write-Host "U10 script validation complete."
