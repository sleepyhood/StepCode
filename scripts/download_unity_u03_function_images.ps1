$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$outDir = Join-Path $root "practice/data/theory/images"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

# 웹에서 다운로드 받을 이미지 리스트 및 저장될 파일명
$downloads = @(
    @{
        File = "unity_u03_function_return_error.png"
        # Microsoft 공식 문서에는 IDE 오류 화면의 직접적인 고정 링크 이미지가 없으므로,
        # 시각적 테스트를 위해 임시 placeholder 이미지를 매핑해 둡니다. 실제 IDE 캡처본으로 교체하여 사용하실 수 있습니다.
        Url  = "https://placehold.co/800x200/png?text=IDE+Error+CS0161:+Not+all+code+paths+return+a+value"
    },
    @{
        File = "unity_u03_function_event_execution_order.png"
        # 유니티 이벤트 함수 흐름도의 최신 버전은 벡터 이미지(SVG) 형태로 제공되지만,
        # 마크다운 호환을 위해 PNG placeholder를 우선 배치했습니다.
        Url  = "https://placehold.co/800x600/png?text=Unity+Event+Execution+Order+Flowchart" 
    },
    @{
        File = "unity_u03_function_static_access_error.png"
        # static 접근 오류 역시 공식 문서의 고정 이미지 URL이 존재하지 않아 placeholder 적용
        Url  = "https://placehold.co/800x200/png?text=IDE+Error+CS0120:+An+object+reference+is+required"
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
