Param(
  [string]$RepoRoot = (Resolve-Path ".").Path
)

$ErrorActionPreference = "Stop"

$setsIndexPath = Join-Path $RepoRoot "practice/data/sets.index.json"
$setsDir = Join-Path $RepoRoot "practice/data/sets"
$categoriesPath = Join-Path $RepoRoot "practice/data/categories.json"

if (-not (Test-Path $setsIndexPath)) { throw "Missing: $setsIndexPath" }
if (-not (Test-Path $setsDir)) { throw "Missing: $setsDir" }
if (-not (Test-Path $categoriesPath)) { throw "Missing: $categoriesPath" }

$setsIndex = Get-Content -Raw $setsIndexPath -Encoding UTF8 | ConvertFrom-Json
$categories = Get-Content -Raw $categoriesPath -Encoding UTF8 | ConvertFrom-Json
$categoryIds = @{}
foreach ($cat in $categories) { $categoryIds[$cat.id] = $true }

$errors = @()
$warnings = @()

foreach ($entry in $setsIndex) {
  $filePath = Join-Path $setsDir $entry.file
  if (-not (Test-Path $filePath)) {
    $errors += "Missing file: $($entry.file)"
    continue
  }

  if (-not $categoryIds.ContainsKey($entry.categoryId)) {
    $errors += "Unknown categoryId '$($entry.categoryId)' for file $($entry.file)"
  }

  $setJson = Get-Content -Raw $filePath -Encoding UTF8 | ConvertFrom-Json
  if (-not $setJson.problems) {
    $errors += "No problems array in $($entry.file)"
    continue
  }

  $count = $setJson.problems.Count
  if ($count -ne $entry.numProblems) {
    $errors += "numProblems mismatch for $($entry.file): index=$($entry.numProblems), actual=$count"
  }
}

if ($errors.Count -gt 0) {
  Write-Host "FAIL: issues found" -ForegroundColor Red
  $errors | ForEach-Object { Write-Host "- $_" -ForegroundColor Red }
  exit 1
}

if ($warnings.Count -gt 0) {
  Write-Host "WARN: $($warnings.Count) warnings" -ForegroundColor Yellow
  $warnings | ForEach-Object { Write-Host "- $_" -ForegroundColor Yellow }
}

Write-Host "OK: sets.index.json is consistent" -ForegroundColor Green
