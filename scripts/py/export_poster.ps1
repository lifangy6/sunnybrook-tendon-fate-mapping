# Export the poster .pptx files to PDF (for submission) and PNG (for visual
# checking) via PowerPoint COM automation.
#
#   .\scripts\py\export_poster.ps1                  # the final poster
#   .\scripts\py\export_poster.ps1 -Variant Drafts  # the two frozen drafts
#   .\scripts\py\export_poster.ps1 -Variant All     # everything
#
# Final is the default: plan A was chosen, so the drafts are frozen references
# and re-exporting them is almost never what you want.
#
# Each PDF is written to a temp file and then moved into place. If the target
# PDF is open in a viewer it holds a write lock, which would otherwise abort the
# whole run; this way the export still succeeds and only the final move fails,
# leaving the new copy alongside.
param(
    [ValidateSet("Final", "A", "B", "Drafts", "All")]
    [string]$Variant = "Final",
    [int]$PngWidth = 3400
)

$root = (Get-Location).Path
$drafts = Join-Path $root "BINF6999\drafts"
$final = Join-Path $root "BINF6999\final"

$wantFinal = $Variant -eq "Final" -or $Variant -eq "All"
$wantA = $Variant -eq "A" -or $Variant -eq "Drafts" -or $Variant -eq "All"
$wantB = $Variant -eq "B" -or $Variant -eq "Drafts" -or $Variant -eq "All"

$targets = @()
if ($wantFinal) {
    $targets += [pscustomobject]@{
        Name = "FINAL (three-act narrative)"
        Pptx = Join-Path $final "LiF_BINF6999_Poster.pptx"
        Pdf  = Join-Path $final "LiF_BINF6999_Poster.pdf"
        Png  = Join-Path $final "poster_preview.png"
    }
}
if ($wantA) {
    $targets += [pscustomobject]@{
        Name = "draft A (three-act narrative, frozen)"
        Pptx = Join-Path $drafts "LiF_BINF6999_Poster_Draft_A.pptx"
        Pdf  = Join-Path $drafts "LiF_BINF6999_Poster_Draft_A.pdf"
        Png  = Join-Path $drafts "poster_a_preview.png"
    }
}
if ($wantB) {
    $targets += [pscustomobject]@{
        Name = "draft B (four-section, frozen)"
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
