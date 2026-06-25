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

Get-ChildItem -Path $issuesDir -Filter "ISSUE-*.md" | Sort-Object Name | ForEach-Object {
    $lines = Get-Content $_.FullName
    $title  = ($lines | Where-Object { $_ -match "^title:" }    | Select-Object -First 1) -replace "^title:\s*", ""
    $labels = ($lines | Where-Object { $_ -match "^labels:" }   | Select-Object -First 1) -replace "^labels:\s*", ""

    $sepIndex = ($lines | Select-String -Pattern "^---$" | Select-Object -First 1).LineNumber
    $body = ($lines[$sepIndex..($lines.Count - 1)] -join "`n").Trim()

    Write-Host "Creating issue: $title"
    $args = @("issue", "create", "--title", $title, "--body", $body, "--label", $labels)
    if ($Repo -ne "") { $args += @("--repo", $Repo) }
    & gh @args
}

Write-Host "Done. All seeded issues created."
