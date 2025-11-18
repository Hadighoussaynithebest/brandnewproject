<#
build_exe.ps1

Packages `exterminator_gui.py` into a single executable using PyInstaller
and writes a ZIP `exterminator_windows.zip` containing the generated exe.

Usage (PowerShell):
  Set-Location "C:\path\to\project"
  .\build_exe.ps1

Requirements:
- Python 3.8+ installed and on PATH
- pip install pyinstaller
- This script must be run on the target platform (Windows) to produce a Windows exe.
#>

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $projectRoot

$gui = Join-Path $projectRoot 'downloads\exterminator_gui.py'
if (-not (Test-Path $gui)) {
    Write-Host "GUI source not found: $gui" -ForegroundColor Red
    exit 1
}

# Ensure PyInstaller is installed
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { Write-Host "Python not found on PATH" -ForegroundColor Red; exit 1 }

Write-Host "Installing PyInstaller (if necessary)..."
python -m pip install --user pyinstaller | Out-Null

# Run PyInstaller
Write-Host "Packaging with PyInstaller..."
# Call PyInstaller via the Python module to avoid requiring the `pyinstaller` entry on PATH
python -m PyInstaller --onefile --noconsole `"$gui`"

# Find the generated exe
$dist = Join-Path $projectRoot 'dist'
$exe = Get-ChildItem $dist -Filter 'exterminator_gui.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $exe) {
    Write-Host "Failed to find generated exe in dist/" -ForegroundColor Red
    exit 1
}

# Create a zip containing the exe and README
$zipName = Join-Path $projectRoot 'exterminator_windows.zip'
if (Test-Path $zipName) { Remove-Item $zipName }
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($dist, $zipName)

Write-Host "Created package: $zipName" -ForegroundColor Green
Write-Host "Reminder: Sign the executable and test on target machines before distribution." -ForegroundColor Yellow
