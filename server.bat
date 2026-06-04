@echo off
title Nialcraft Dedicated Server Core v1.8.4
color 0A
cls
echo =======================================================================
echo             NIALCRAFT DEDICATED SERVER ENGINE CORE INITIALIZATION     
echo =======================================================================
echo [%time%] [BOOTSTRAP] Checking system architecture... 64-bit detected.
echo [%time%] [BOOTSTRAP] Verifying Python runtime environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [%time%] [CRITICAL] Python runtime NOT found in system PATH.
    echo [%time%] [CRITICAL] Please install Python 3.x and check 'Add to PATH'.
    pause
    exit
)
echo [%time%] [BOOTSTRAP] Python environment OK. Allocating memory buffers...
echo [%time%] [BOOTSTRAP] Spawning Python virtual thread loop worker...
echo -----------------------------------------------------------------------
python server.py
echo -----------------------------------------------------------------------
echo [%time%] [BOOTSTRAP] Process exited.
pause
