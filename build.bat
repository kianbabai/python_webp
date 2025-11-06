@echo off
echo ========================================
echo  WebP Converter - Build EXE
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Removing obsolete pathlib package (if exists)...
pip uninstall pathlib -y >nul 2>&1
echo      Done!
echo.

echo [2/4] Installing required packages...
pip install Pillow pyinstaller --quiet
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)
echo      Done!
echo.

echo [3/4] Checking if webp_converter.py exists...
if not exist "webp_converter.py" (
    echo ERROR: webp_converter.py not found in current directory
    echo Please make sure the Python script is in the same folder as this batch file
    pause
    exit /b 1
)
echo      Found!
echo.

echo [4/4] Building EXE file (this may take a minute)...
pyinstaller --onefile --windowed --name "WebP_Converter" --icon=NONE webp_converter.py
if errorlevel 1 (
    echo ERROR: Failed to build EXE
    pause
    exit /b 1
)
echo      Done!
echo.

echo [4/4] Cleaning up build files...
if exist "build" rmdir /s /q build
if exist "WebP_Converter.spec" del /q WebP_Converter.spec
echo      Done!
echo.

echo ========================================
echo  BUILD SUCCESSFUL!
echo ========================================
echo.
echo Your EXE file is located at:
echo %CD%\dist\WebP_Converter.exe
echo.
echo You can copy this file anywhere and run it without Python installed.
echo.
pause