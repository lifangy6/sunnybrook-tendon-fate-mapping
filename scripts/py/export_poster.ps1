# Export the poster .pptx files to PDF (for submission) and PNG (for visual
# checking) via PowerPoint COM automation.
#
#   .\scripts\py\export_poster.ps1             # both variants
#   .\scripts\py\export_poster.ps1 -Variant A  # just plan A
#
# Each PDF is written to a temp file and then moved into place. If the target
# PDF is open in a viewer it holds a write lock, which would otherwise abort the
# whole run; this way the export still succeeds and only the final move fails,
# leaving the new copy alongside.
param(
    [ValidateSet("A", "B", "Both")]
    [string]$Variant = "Both",
    [int]$PngWidth = 3400
)

$root = (Get-Location).Path
$drafts = Join-Path $root "BINF6999\drafts"

$targets = @()
if ($Variant -eq "A" -or $Variant -eq "Both") {
    $targets += [pscustomobject]@{
        Name = "A (three-act narrative)"
        Pptx = Join-Path $drafts "LiF_BINF6999_Poster_Draft_A.pptx"
        Pdf  = Join-Path $drafts "LiF_BINF6999_Poster_Draft_A.pdf"
        Png  = Join-Path $drafts "poster_a_preview.png"
    }
}
if ($Variant -eq "B" -or $Variant -eq "Both") {
    $targets += [pscustomobject]@{
        Name = "B (four-section)"
        Pptx = Join-Path $drafts "LiF_BINF6999_Poster_Draft_B.pptx"
        Pdf  = Join-Path $drafts "LiF_BINF6999_Poster_Draft_B.pdf"
        Png  = Join-Path $drafts "poster_b_preview.png"
    }
}

foreach ($t in $targets) {
    if (-not (Test-Path $t.Pptx)) {
        throw "missing $($t.Pptx) - run the matching build script first"
    }
}

$ppt = New-Object -ComObject PowerPoint.Application
try {
    foreach ($t in $targets) {
        $tmp = [System.IO.Path]::ChangeExtension($t.Pdf, ".tmp.pdf")
        if (Test-Path $tmp) { Remove-Item $tmp -Force }

        $pres = $ppt.Presentations.Open($t.Pptx, $true, $false, $false)
        try {
            $pres.SaveAs($tmp, 32)                  # 32 = ppSaveAsPDF
            $h = [int]($PngWidth * $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth)
            $pres.Slides.Item(1).Export($t.Png, "PNG", $PngWidth, $h)
        } finally {
            $pres.Close()
        }

        Write-Output "poster $($t.Name)"
        try {
            Move-Item $tmp $t.Pdf -Force -ErrorAction Stop
            Write-Output "  PDF -> $($t.Pdf)"
        } catch {
            Write-Output "  PDF LOCKED (close it in your viewer) - new copy left at $tmp"
        }
        Write-Output "  PNG -> $($t.Png) ($PngWidth x $h)"
    }
} finally {
    $ppt.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
}
