# This script installs Partiels and its main plugins on Windows systems

[CmdletBinding()]
param (
    [string]$partiels_version,
    [string]$ircam_vamp_version = "2.1.0",
    [string]$vax_vamp_version = "1.0.0",
    [string]$crepe_vamp_version = "3.0.0",
    [string]$whisper_vamp_version = "3.0.0"
)

# Show help if requested
if ($args -contains "--help" -or $args -contains "-h") {
    Write-Host "Usage: .\install_partiels.ps1 [-partiels_version <version>] [-ircam_vamp_version <version>] [-vax_vamp_version <version>] [-crepe_vamp_version <version>] [-whisper_vamp_version <version>]"
    Write-Host "Default versions will be used if no arguments are provided."
    exit 0
}

# Script setup
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $PythonExe) {
    $PythonExe = (Get-Command py -ErrorAction SilentlyContinue).Source
    if (-not $PythonExe) {
        Write-Host "Python not found. Please install Python and try again." -ForegroundColor Red
        exit 1
    }
}

# Get default Partiels version from Python if not specified
if (-not $partiels_version) {
    try {
        $partiels_version = & $PythonExe "$ScriptDir\..\src\partielspy\version.py"
    }
    catch {
        Write-Host "Error getting Partiels version: $_" -ForegroundColor Red
        exit 1
    }
}

# Setup URLs
$PartielsUrl = "https://github.com/Ircam-Partiels/Partiels/releases/download"
$IrcamVampUrl = "https://github.com/Ircam-Partiels/ircam-vamp-plugins/releases/download"
$CrepeVampUrl = "https://github.com/Ircam-Partiels/crepe-vamp-plugin/releases/download"
$WhisperVampUrl = "https://github.com/Ircam-Partiels/whisper-vamp-plugin/releases/download"

# Create temporary directory
$TempDir = Join-Path $env:TEMP "PartielsInstall_$(Get-Random)"
Write-Host "Creating temporary directory: $TempDir" -ForegroundColor Cyan
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
Set-Location $TempDir

try {
    # Download files
    Write-Host "Downloading Partiels..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $PartielsUrl/$partiels_version/Partiels-Windows.exe -OutFile Partiels-Windows.exe
    Write-Host "Downloading Ircam Vamp Plugins..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $IrcamVampUrl/$ircam_vamp_version/Ircam-Vamp-Plugins-Windows.zip -OutFile "Ircam-Vamp-Plugins-Windows.zip"
    Write-Host "Downloading VAX Vamp Plugin..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $IrcamVampUrl/$ircam_vamp_version/VAX-Vamp-Plugin-v$vax_vamp_version-Windows.zip -OutFile "VAX-Vamp-Plugin-Windows.zip"
    Write-Host "Downloading Crepe Vamp Plugin..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $CrepeVampUrl/$crepe_vamp_version/Crepe-Windows.exe -OutFile "Crepe-Windows.exe"
    Write-Host "Downloading Whisper Vamp Plugin..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $WhisperVampUrl/$whisper_vamp_version/Whisper-Windows.exe -OutFile "Whisper-Windows.exe"
    Write-Host "All downloads complete." -ForegroundColor Green

    # Install Partiels
    Write-Host "Installing Partiels and plugins..." -ForegroundColor Cyan

    $signature = Get-AuthenticodeSignature .\Partiels-Windows.exe
    if ($signature.Status -ne 'Valid') {
        throw "The installer isn't signed or the signature is invalid"
    }
    $proc = Start-Process .\Partiels-Windows.exe -ArgumentList "/VERYSILENT /NORESTART /SP-" -Wait -PassThru
    if ($proc.ExitCode -ne 0) {
        throw "The installation failed with the exit code $($proc.ExitCode)"
    }
    
    Expand-Archive -Path "Ircam-Vamp-Plugins-Windows.zip" -DestinationPath "Ircam-Vamp-Plugins-Windows"
    Start-Process -FilePath "Ircam-Vamp-Plugins-Windows\Ircam Vamp Plugins-install.exe" -ArgumentList "/VERYSILENT" -Wait
    Expand-Archive -Path "VAX-Vamp-Plugin-Windows.zip" -DestinationPath "VAX-Vamp-Plugin"
    Start-Process -FilePath "VAX-Vamp-Plugin\VAX-Vamp-Plugin-Windows.exe" -ArgumentList "/VERYSILENT" -Wait
    Start-Process -FilePath ".\Crepe-Windows.exe" -ArgumentList "/VERYSILENT" -Wait
    Start-Process -FilePath ".\Whisper-Windows.exe" -ArgumentList "/VERYSILENT" -Wait
    
} catch {
    Write-Host "An error occurred during installation: $_" -ForegroundColor Red
    exit 1
} finally {
    # Clean up
    Set-Location $ScriptDir
    if (Test-Path $TempDir) {
        Write-Host "Cleaning up temporary files..." -ForegroundColor Cyan
        Remove-Item -Path $TempDir -Recurse -Force
    }
}
