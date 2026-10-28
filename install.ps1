<#
.SYNOPSIS
    Installs native Windows ARM64 layoutlib binaries into Android Studio.
#>
param(
    [string]$StudioPath = ""
)

$ErrorActionPreference = "Stop"

Write-Host "=== Android Studio Windows ARM64 Layoutlib Installer ===" -ForegroundColor Cyan

# Autodetect Android Studio paths
$candidatePaths = @(
    $StudioPath,
    "C:\Program Files\Android\Android Studio",
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Android Studio",
    "C:\Users\$env:USERNAME\.gemini\antigravity\scratch\android-studio-dist\android-studio"
)

$targetDir = $null
foreach ($path in $candidatePaths) {
    if (-not [string]::IsNullOrWhiteSpace($path)) {
        $check = Join-Path $path "plugins\design-tools\resources\layoutlib\data\win\lib64"
        if (Test-Path $check) {
            $targetDir = $check
            Write-Host "Found Android Studio layoutlib at: $targetDir" -ForegroundColor Green
            break
        }
    }
}

if (-not $targetDir) {
    Write-Host "Could not automatically locate Android Studio." -ForegroundColor Yellow
    $userPath = Read-Host "Please enter the path to your Android Studio installation directory"
    $targetDir = Join-Path $userPath "plugins\design-tools\resources\layoutlib\data\win\lib64"
    if (-not (Test-Path $targetDir)) {
        Write-Error "Target directory does not exist: $targetDir"
        exit 1
    }
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$distDir = Join-Path $scriptDir "dist"
$backupDir = Join-Path $targetDir "..\lib64_x86_64_backup"

if (-not (Test-Path $backupDir)) {
    Write-Host "Backing up original x86_64 DLLs to: $backupDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    Copy-Item (Join-Path $targetDir "*") $backupDir -Force
}

Write-Host "Deploying ARM64 DLLs..." -ForegroundColor Cyan
Copy-Item (Join-Path $distDir "*.dll") $targetDir -Force

Write-Host "Verification:" -ForegroundColor Green
Get-ChildItem $targetDir -Filter "*.dll" | Format-Table Name, Length, LastWriteTime

Write-Host "`nSUCCESS: Windows ARM64 Layoutlib successfully installed!" -ForegroundColor Green
Write-Host "Restart Android Studio to enable native XML and Jetpack Compose Preview." -ForegroundColor Green
