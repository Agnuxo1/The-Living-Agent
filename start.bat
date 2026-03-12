@echo off
TITLE The Living Agent - Launcher
echo ==========================================
echo       THE LIVING AGENT v2.0
echo       Autonomous Research Engine
echo ==========================================
echo.

IF NOT EXIST "venv" (
    echo [!] Virtual environment not found. Running installer...
    powershell -ExecutionPolicy Bypass -File install.ps1
)

echo [!] Starting Agent Engine...
call venv\Scripts\activate
python agent_v2_production.py
pause
