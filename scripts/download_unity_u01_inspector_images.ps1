$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$outDir = Join-Path $root "practice/data/theory/images"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

$downloads = @(
    @{
        File = "unity_u01_inspector_editor_overview.png"
        Url  = "https://docs.unity3d.com/es/2019.4/uploads/Main/Editor-Breakdown.png"
    },
    @{
        File = "unity_u01_inspector_window_mapping.png"
        Url  = "https://docs.unity.cn/uploads/Main/project-window-context.png"
    },
    @{
        File = "unity_u01_inspector_static_tag_prefab.png"
        Url  = "https://docs.unity.cn/2017.4/Documentation/uploads/Main/GameObjectStaticDropDownMenu.png"
    },
    @{
        File = "unity_u01_inspector_external_script_editor.png"
        Url  = "https://docs.unity3d.com/es/2018.4/uploads/Main/PrefsExtTools.png"
    },
    @{
        File = "unity_u01_inspector_scene_tools.png"
        Url  = "https://docs.unity.cn/uploads/Main/game-objects-transform-modes.png"
    },
    @{
        File = "unity_u01_inspector_serializefield_compare.png"
        Url  = "https://docs.unity3d.com/es/2019.4/uploads/Main/InspectorExampleObjWithScripts.png"
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
