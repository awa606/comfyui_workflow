param(
    [string[]]$Roots = @()
)

$ErrorActionPreference = "SilentlyContinue"

if ($Roots.Count -eq 0) {
    $user = $env:USERPROFILE
    $Roots = @(
        "$user\Downloads",
        "$user\Documents",
        "$user\Desktop",
        "D:\Models"
    )
}

$exts = @("*.safetensors","*.ckpt","*.pt","*.pth","*.bin","*.gguf","*.onnx","*.engine")
$files = New-Object System.Collections.Generic.List[Object]

function Guess-Type($path) {
    $p = $path.ToLower()
    if ($p -match "\\lora|\\loras|\\lycoris") { return "LoRA / LyCORIS" }
    if ($p -match "\\checkpoint|\\checkpoints|\\stable-diffusion|\\models\\stable-diffusion") { return "Checkpoint" }
    if ($p -match "\\vae") { return "VAE" }
    if ($p -match "\\controlnet|\\control-net") { return "ControlNet" }
    if ($p -match "\\upscale|\\upscaler|\\esrgan|\\realesrgan") { return "Upscaler" }
    if ($p -match "\\embeddings|\\textual_inversion") { return "Embedding / Textual Inversion" }
    if ($p -match "\\clip|\\text_encoders") { return "CLIP / Text Encoder" }
    if ($p -match "\\unet") { return "UNet" }
    if ($p -match "\\ollama|\.gguf$") { return "GGUF / LLM" }
    return "Unknown"
}

foreach ($root in $Roots) {
    if (!(Test-Path $root)) { continue }
    Write-Host "Scanning $root ..."
    foreach ($ext in $exts) {
        Get-ChildItem -Path $root -Filter $ext -File -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
            $sizeGB = [math]::Round($_.Length / 1GB, 3)
            $files.Add([PSCustomObject]@{
                Type = Guess-Type $_.FullName
                Name = $_.Name
                SizeGB = $sizeGB
                Modified = $_.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
                Path = $_.FullName
            })
        }
    }
}

$filesSorted = $files | Sort-Object Type, Name, SizeGB -Descending
$csv = Join-Path (Get-Location) "ai_asset_inventory.csv"
$md = Join-Path (Get-Location) "ai_asset_inventory.md"

$filesSorted | Export-Csv -Path $csv -NoTypeInformation -Encoding UTF8

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# AI Asset Inventory")
$lines.Add("")
$lines.Add("Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
$lines.Add("")
$lines.Add("| Type | Name | Size GB | Modified | Path |")
$lines.Add("|---|---:|---:|---|---|")

foreach ($f in $filesSorted) {
    $safePath = $f.Path.Replace("|", "\|")
    $safeName = $f.Name.Replace("|", "\|")
    $lines.Add("| $($f.Type) | $safeName | $($f.SizeGB) | $($f.Modified) | `$safePath` |")
}

$lines | Set-Content -Path $md -Encoding UTF8

Write-Host ""
Write-Host "Done."
Write-Host "CSV: $csv"
Write-Host "MD : $md"
Write-Host "Total files: $($filesSorted.Count)"
