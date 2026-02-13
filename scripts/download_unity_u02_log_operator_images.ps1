$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$outDir = Join-Path $root "practice/data/theory/images"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

$downloads = @(
    @{
        File = "unity_u02_log_operator_console.png"
        Url  = "https://docs.unity.cn/2018.2/Documentation/uploads/Main/Console.png"
    },
    @{
        File = "unity_u02_log_operator_console_stacktrace.png"
        Url  = "https://docs.unity.cn/2018.2/Documentation/uploads/Main/ConsoleStackTrace.png"
    },
    @{
        File = "unity_u02_log_operator_console_linecount.png"
        Url  = "https://docs.unity.cn/2018.2/Documentation/uploads/Main/AdjustLineCount.png"
    },
    @{
        File = "unity_u02_log_operator_monobehaviour_flow.svg"
        Url  = "https://docs.unity3d.com/es/2019.4/uploads/Main/monobehaviour_flowchart.svg"
    }
)

Write-Host "Downloading $($downloads.Count) images to: $outDir"

foreach ($item in $downloads) {
    $target = Join-Path $outDir $item.File
    try {
        Invoke-WebRequest -Uri $item.Url -OutFile $target -UseBasicParsing
        $size = (Get-Item $target).Length
        Write-Host ("[OK] {0} ({1} bytes)" -f $item.File, $size)
    }
    catch {
        Write-Warning ("[FAIL] {0} <= {1}" -f $item.File, $item.Url)
        Write-Warning $_.Exception.Message
    }
}

Write-Host "Done."
