#Requires -Version 5.1
<#
.SYNOPSIS
    Create .venv and install ARGUS-Rerank in editable mode with dev dependencies.

.DESCRIPTION
    Run from this repository root (or via VS Code task "argus-rerank: setup").
    Safe to re-run; upgrades pip and reinstalls editable package.
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "==> ARGUS-Rerank dev setup (root: $Root)" -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "python not found on PATH. Install Python 3.10+ and try again."
    exit 1
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creating .venv ..." -ForegroundColor Yellow
    python -m venv .venv
}

$Py = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Py)) {
    Write-Error "Expected venv python at $Py"
    exit 1
}

& $Py -m pip install --upgrade pip
& $Py -m pip install -e ".[dev]"

Write-Host ""
Write-Host "Done. In Cursor/VS Code: select interpreter" -ForegroundColor Green
Write-Host "  $Py"
Write-Host "Then run tests: Terminal -> Run Task -> argus-rerank: pytest"
