@echo off
setlocal enabledelayedexpansion

REM Set the working directory to the directory of the batch file
cd /d "%~dp0"

REM Check if a folder is dragged and dropped
if "%~1"=="" (
    echo Please drag and drop a folder onto this script.
    pause
    exit /b 1
)

REM Get the full path of the dragged folder
set "folderPath=%~1"

REM Verify the folder exists
if not exist "%folderPath%\" (
    echo Error: The folder "%folderPath%" does not exist.
    pause
    exit /b 1
)

REM Activate conda environment (adjust 'base' if using a different environment)
call conda activate base

REM Run the Python script with the folder path
python main.py "%folderPath%"

if %ERRORLEVEL% neq 0 (
    echo Error: Python script failed with error code %ERRORLEVEL%.
    pause
    exit /b %ERRORLEVEL%
)

pause