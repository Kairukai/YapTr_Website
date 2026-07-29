# Show how many times the YapTr installer has actually been downloaded.
#
#   powershell -ExecutionPolicy Bypass -File tools\downloads.ps1
#
# GitHub does NOT display download counts anywhere in its web UI - not on the
# release page, not in Insights - so the REST API is the only way to see them.
#
# Caveats on the number:
#   * It counts every download, including repeats, bots and mirrors. Treat it as
#     an upper bound on real people.
#   * It resets to zero if a release is deleted and re-created. Don't do that
#     once the figure is published anywhere.
#
# NOTE: keep this file ASCII-only. Windows PowerShell 5.1 reads .ps1 as ANSI,
# so smart quotes / em dashes get mangled and break parsing.

$ErrorActionPreference = 'Stop'
$repo = 'Kairukai/YapTr_Website'

try {
    $releases = Invoke-RestMethod "https://api.github.com/repos/$repo/releases"
} catch {
    Write-Host "Couldn't reach the GitHub API: $($_.Exception.Message)"
    Write-Host "(Unauthenticated requests are limited to 60/hour per IP.)"
    exit 1
}

if (-not $releases) {
    Write-Host "No releases published yet."
    exit 0
}

$total = 0
Write-Host ""
foreach ($rel in $releases) {
    foreach ($asset in $rel.assets) {
        # Skip GitHub's auto-attached source archives - they aren't the app.
        if ($asset.name -notlike '*.exe') { continue }
        $line = "{0,-30} {1,8}   ({2}, published {3:yyyy-MM-dd})" -f $asset.name, $asset.download_count, $rel.tag_name, [datetime]$rel.published_at
        Write-Host $line
        $total += $asset.download_count
    }
}

Write-Host ""
Write-Host "TOTAL INSTALLER DOWNLOADS: $total"

# The site's download counter stays off until this clears ~500. Below that a
# visible count reads as "nobody uses this". See PLAN.md roadmap Phase 7.
if ($total -lt 500) {
    Write-Host "(Threshold is 500 - not worth showing on the site yet.)"
} else {
    Write-Host "(Above threshold - the download counter is worth adding now.)"
}
Write-Host ""
