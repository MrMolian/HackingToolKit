@echo off
setlocal enabledelayedexpansion

echo Starting PyInstaller build for PROLOX...

REM Get the directory where this script is located
set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

REM Build the PyInstaller command
set "CMD=pyinstaller"
set "CMD=!CMD! --onefile"
set "CMD=!CMD! --noconsole"
set "CMD=!CMD! --clean"
set "CMD=!CMD! --name PROLOX"
set "CMD=!CMD! --icon=assets/logo.ico"
set "CMD=!CMD! --uac-admin"

REM Add hidden imports
set "CMD=!CMD! --hidden-import win32timezone"
set "CMD=!CMD! --hidden-import win32crypt"
set "CMD=!CMD! --hidden-import win32api"
set "CMD=!CMD! --hidden-import win32con"
set "CMD=!CMD! --hidden-import win32evtlog"
set "CMD=!CMD! --hidden-import win32evtlogutil"
set "CMD=!CMD! --hidden-import win32file"
set "CMD=!CMD! --hidden-import win32gui"
set "CMD=!CMD! --hidden-import win32process"
set "CMD=!CMD! --hidden-import win32security"
set "CMD=!CMD! --hidden-import win32service"
set "CMD=!CMD! --hidden-import win32serviceutil"
set "CMD=!CMD! --hidden-import win32ts"
set "CMD=!CMD! --hidden-import win32wnet"
set "CMD=!CMD! --hidden-import winxpgui"
set "CMD=!CMD! --hidden-import PySide6"
set "CMD=!CMD! --hidden-import PySide6.QtCore"
set "CMD=!CMD! --hidden-import PySide6.QtGui"
set "CMD=!CMD! --hidden-import PySide6.QtWidgets"

REM Add data files if they exist
if exist "venv\Lib\site-packages\PySide6\plugins" (
    set "CMD=!CMD! --add-data venv\Lib\site-packages\PySide6\plugins;PySide6\plugins"
    echo Found: PySide6 plugins
) else (
    echo Warning: Could not find venv\Lib\site-packages\PySide6\plugins
)

if exist "venv\Lib\site-packages\PySide6\resources" (
    set "CMD=!CMD! --add-data venv\Lib\site-packages\PySide6\resources;PySide6\resources"
    echo Found: PySide6 resources
) else (
    echo Warning: Could not find venv\Lib\site-packages\PySide6\resources
)

if exist "venv\Lib\site-packages\PySide6\styles" (
    set "CMD=!CMD! --add-data venv\Lib\site-packages\PySide6\styles;PySide6\styles"
    echo Found: PySide6 styles
) else (
    echo Warning: Could not find venv\Lib\site-packages\PySide6\styles
)

if exist "assets/logo.png" (
    set "CMD=!CMD! --add-data assets/logo.png;assets"
    echo Found: logo.png
) else (
    echo Warning: Could not find assets/logo.png
)

REM Add main.py at the end
set "CMD=!CMD! main.py"

echo.
echo Running PyInstaller with the following command:
echo !CMD!
echo.

REM Execute PyInstaller
!CMD!

if %errorlevel% equ 0 (
    echo.
    echo Build completed successfully!
    echo Executable can be found in: %BASE_DIR%dist\PROLOX.exe
) else (
    echo.
    echo Build failed with error code: %errorlevel%
)

:: Nettoyer
echo Cleaning up temporary files...
rmdir /s /q build 2>nul
rmdir /s /q "%TEMP%\_MEI*" 2>nul

pause