# Creates the seeded ShopFlow backlog as real GitHub issues.
# Prerequisites: GitHub CLI (`gh`) installed and authenticated (`gh auth login`),
# run from inside the repo (or pass --repo owner/name to gh).
#
# Usage:  .\scripts\create_issues.ps1
#         .\scripts\create_issues.ps1 -Repo "your-org/shopflow"

param(
    [string]$Repo = ""
)

$ErrorActionPreference = "Stop"
$issuesDir = Join-Path $PSScriptRoot "..\issues"
$repoArgs = @()
if ($Repo -ne "") { $repoArgs = @("--repo", $Repo) }

$files = Get-ChildItem -Path $issuesDir -Filter "ISSUE-*.md" | Sort-Object Name

function Get-LabelList($lines) {
    $line = ($lines | Where-Object { $_ -match "^labels:" } | Select-Object -First 1) -replace "^labels:\s*", ""
    return ($line -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" })
}

# 1. Collect every unique label used across the issue files.
$allLabels = New-Object System.Collections.Generic.HashSet[string]
foreach ($f in $files) {
    foreach ($l in (Get-LabelList (Get-Content $f.FullName))) { [void]$allLabels.Add($l) }
}

# 2. Ensure each label exists. `--force` creates it, or updates it if present,
#    so this never errors on labels that already exist (e.g. bug, enhancement).
Write-Host "Ensuring $($allLabels.Count) labels exist..."
foreach ($label in $allLabels) {
    & gh label create $label --force @repoArgs | Out-Null
}

# 3. Create the issues, passing each label as its own --label flag.
foreach ($f in $files) {
    $lines = Get-Content $f.FullName
    $title = ($lines | Where-Object { $_ -match "^title:" } | Select-Object -First 1) -replace "^title:\s*", ""
    $sepIndex = ($lines | Select-String -Pattern "^---$" | Select-Object -First 1).LineNumber
    $body = ($lines[$sepIndex..($lines.Count - 1)] -join "`n").Trim()

    $labelArgs = @()
    foreach ($l in (Get-LabelList $lines)) { $labelArgs += @("--label", $l) }

    Write-Host "Creating issue: $title"
    & gh issue create --title $title --body $body @labelArgs @repoArgs
}

Write-Host "Done. All seeded issues created."
