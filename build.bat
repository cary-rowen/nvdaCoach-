@echo off
REM NVDA Coach - Build Script
REM Packages the add-on as an .nvda-addon file (which is just a zip archive).
REM Run this from the nvdaCoach directory.

set ADDON_NAME=nvdaCoach
REM Read the version from manifest.ini so it cannot drift from what the
REM add-on actually reports. Nothing is typed twice.
for /f "tokens=3" %%v in ('findstr /b /c:"version" manifest.ini') do set VERSION=%%v

echo Building %ADDON_NAME% version %VERSION%...

REM Remove any old build.
if exist "%ADDON_NAME%-%VERSION%.nvda-addon" del "%ADDON_NAME%-%VERSION%.nvda-addon"

REM Create the zip archive. Requires 7-Zip or PowerShell.
REM Using PowerShell (available on Windows 10+):
REM NOTE: The canonical build is the Python snippet in README.md, which excludes
REM __pycache__/*.pyc. Delete any globalPlugins\nvdaCoach\__pycache__ before running this.
powershell -Command "Compress-Archive -Path 'manifest.ini','globalPlugins','doc','locale' -DestinationPath '%ADDON_NAME%-%VERSION%.zip' -Force"
ren "%ADDON_NAME%-%VERSION%.zip" "%ADDON_NAME%-%VERSION%.nvda-addon"

echo.
echo Build complete: %ADDON_NAME%-%VERSION%.nvda-addon
echo You can install this file by opening it with NVDA.
pause
