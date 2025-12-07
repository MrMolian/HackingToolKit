@echo off
:: Vérifier les privilèges administrateur
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with admin privileges
) else (
    echo Requesting admin privileges...
    powershell -Command "Start-Process cmd -Verb RunAs -ArgumentList '/c cd /d %~dp0 && %0 %*'"
    exit /b
)

:: Créer un environnement virtuel
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

:: Installer les dépendances
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

:: Nettoyer les anciennes constructions
echo Cleaning old builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

