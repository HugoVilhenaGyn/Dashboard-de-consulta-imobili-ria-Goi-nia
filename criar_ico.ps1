Add-Type -AssemblyName System.Drawing

$src = 'C:\Users\loglo\.gemini\antigravity-ide\brain\bc2e12f7-2666-464e-9a97-32ce8ae88d0a\dashboard_icon_1781972330755.png'
$dst = 'c:\VS Code\upload_supabase.py\icon.ico'

$img = [System.Drawing.Image]::FromFile($src)

$sizes = @(16, 32, 48, 256)
$bitmaps = @()
$streams = @()

foreach ($sz in $sizes) {
    $bmp = New-Object System.Drawing.Bitmap($sz, $sz)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.DrawImage($img, 0, 0, $sz, $sz)
    $g.Dispose()
    $bitmaps += $bmp
}

$ms = New-Object System.IO.MemoryStream
$bw = New-Object System.IO.BinaryWriter($ms)

# ICO header
$bw.Write([int16]0)        # Reserved
$bw.Write([int16]1)        # Type: ICO
$bw.Write([int16]$sizes.Count)  # Number of images

# Calculate offset to image data
$headerSize = 6 + ($sizes.Count * 16)
$offset = $headerSize

# Collect PNG data for each size
$pngDatas = @()
foreach ($bmp in $bitmaps) {
    $pngMs = New-Object System.IO.MemoryStream
    $bmp.Save($pngMs, [System.Drawing.Imaging.ImageFormat]::Png)
    $pngDatas += $pngMs
}

# Write directory entries
for ($i = 0; $i -lt $bitmaps.Count; $i++) {
    $sz = $sizes[$i]
    $dataLen = $pngDatas[$i].Length
    $w = if ($sz -eq 256) { 0 } else { $sz }
    $h = if ($sz -eq 256) { 0 } else { $sz }
    $bw.Write([byte]$w)         # Width
    $bw.Write([byte]$h)         # Height
    $bw.Write([byte]0)          # Color count
    $bw.Write([byte]0)          # Reserved
    $bw.Write([int16]1)         # Color planes
    $bw.Write([int16]32)        # Bits per pixel
    $bw.Write([int32]$dataLen)  # Data size
    $bw.Write([int32]$offset)   # Data offset
    $offset += $dataLen
}

# Write image data
foreach ($pngMs in $pngDatas) {
    $bw.Write($pngMs.ToArray())
    $pngMs.Dispose()
}

$bw.Flush()
[System.IO.File]::WriteAllBytes($dst, $ms.ToArray())
$ms.Dispose()
$img.Dispose()

Write-Host "ICO criado em: $dst"
