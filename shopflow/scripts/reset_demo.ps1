# Resets the demo to a pristine state between runs.
#   1. Resets local code on `main` to a baseline tag (the buggy starting point).
#   2. Reopens any closed seeded issues (or recreates them if missing).
#
# It does NOT restart the app server: app data is in-memory, so just Ctrl+C the
# uvicorn window and re-run it to reset stock/orders.
#
# Prerequisite (run once during pre-flight, after your first commit):
#   git tag demo-baseline
#
# Usage:
#   .\scripts\reset_demo.ps1
#   .\scripts\reset_demo.ps1 -Tag demo-baseline -Repo "calstick/FactoryInterviewMock"
#   .\scripts\reset_demo.ps1 -SkipCode      # only fix up issues
#   .\scripts\reset_demo.ps1 -SkipIssues    # only reset code

param(
    [string]$Tag = "demo-baseline",
    [string]$Repo = "",
    [switch]$SkipCode,
    [switch]$SkipIssues
)

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$issuesDir = Join-Path $PSScriptRoot "..\issues"
$repoArgs = @()
if ($Repo -ne "") { $repoArgs = @("--repo", $Repo) }

function Get-LabelList($lines) {
    $line = ($lines | Where-Object { $_ -match "^labels:" } | Select-Object -First 1) -replace "^labels:\s*", ""
    return ($line -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" })
}

if (-not $SkipCode) {
    Write-Host "Resetting code on 'main' to tag '$Tag'..."
    Push-Location $repoRoot
    try {
        & git rev-parse --verify "$Tag" 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Tag '$Tag' not found. Create it during pre-flight: git tag $Tag"
        }
        & git checkout main | Out-Null
        & git reset --hard $Tag
    }
    finally {
        Pop-Location
    }
}

if (-not $SkipIssues) {
    Write-Host "Reconciling seeded issues..."
    $existing = & gh issue list --state all --limit 200 --json number,title,state @repoArgs | ConvertFrom-Json

    Get-ChildItem -Path $issuesDir -Filter "ISSUE-*.md" | Sort-Object Name | ForEach-Object {
        $lines = Get-Content $_.FullName
        $title = ($lines | Where-Object { $_ -match "^title:" } | Select-Object -First 1) -replace "^title:\s*", ""
        $match = $existing | Where-Object { $_.title -eq $title } | Select-Object -First 1

        if ($null -ne $match) {
            if ($match.state -eq "CLOSED") {
                Write-Host "  Reopening #$($match.number): $title"
                & gh issue reopen $match.number @repoArgs | Out-Null
            }
            else {
                Write-Host "  Already open #$($match.number): $title"
            }
        }
        else {
            $sepIndex = ($lines | Select-String -Pattern "^---$" | Select-Object -First 1).LineNumber
            $body = ($lines[$sepIndex..($lines.Count - 1)] -join "`n").Trim()
            $labelArgs = @()
            foreach ($l in (Get-LabelList $lines)) {
                & gh label create $l --force @repoArgs | Out-Null
                $labelArgs += @("--label", $l)
            }
            Write-Host "  Recreating: $title"
            & gh issue create --title $title --body $body @labelArgs @repoArgs
        }
    }
}

Write-Host ""
Write-Host "Reset complete."
Write-Host "Now restart the app to reset in-memory data: Ctrl+C in the uvicorn window, then re-run uvicorn."
