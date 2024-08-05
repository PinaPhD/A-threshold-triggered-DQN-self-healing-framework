@echo off
setlocal enabledelayedexpansion

:: Change to the directory where the script is located
cd C:\Users\amwangi254\Desktop\JP3\KnowledgePlane

:: Create the logs directory if it does not exist
if not exist logs (
    mkdir logs
)

:: Get current timestamp
for /F "tokens=1-4 delims=/ " %%a in ('date /t') do (
    set day=%%a
    set month=%%b
    set year=%%c
)
for /F "tokens=1-2 delims=: " %%a in ('time /t') do (
    set hour=%%a
    set minute=%%b
)

set timestamp=%year%-%month%-%day%_%hour%-%minute%

:: Run the Python script and log output with timestamp
python Observe.py > logs\observe_%timestamp%.log 2>&1

pause
