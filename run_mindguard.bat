@echo off
title MindGuard AI - Mental Health Sentimental Analysis Platform
cd /d "%~dp0"

echo ======================================================================
echo MINDGUARD AI - BERT-BASED MENTAL HEALTH SENTIMENTAL ANALYSIS
echo Vishwakarma University Pune - Group 21 Minor Project (2026-2027)
echo Authors: Bhupesh Bhatia, Samruddhi Meher, Arnav Phuke, Sushrut Ingle, Saket Radke
echo Mentor: Prof. Richa Agnihotri
echo ======================================================================
echo.
echo [1/2] Verifying Python environment and packages...
python -c "import fastapi, uvicorn, sklearn, pandas; print('All core libraries verified!')"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Required packages missing. Installing fastapi uvicorn scikit-learn pandas...
    pip install fastapi uvicorn scikit-learn pandas
)

echo.
echo [2/2] Launching MindGuard AI Server on http://127.0.0.1:8000 ...
start "" http://127.0.0.1:8000
python server.py

pause
