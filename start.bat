@echo off
TITLE The Living Agent v1.0.0 - Chess-Grid Engine
echo ==================================================
echo       THE LIVING AGENT v1.0.0
echo       Chess-Grid Autonomous Research Engine
echo       P2PCLAW Silicon Layer
echo ==================================================
echo.

IF NOT EXIST "venv" (
    echo [!] Virtual environment not found. Running installer...
    powershell -ExecutionPolicy Bypass -File install.ps1
)

IF EXIST "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Make sure the `living-agent` CLI is available.
where living-agent >nul 2>&1
IF ERRORLEVEL 1 (
    echo [!] `living-agent` CLI not found. Installing package in editable mode...
    pip install -e .
)

IF NOT EXIST "knowledge\grid\cell_R0_C0.md" (
    echo [*] Knowledge grid not found. Initializing 16x16 grid...
    living-agent init --grid-dir knowledge
)

echo.
echo [*] Launching Chess-Grid Agent Engine...
echo [i] Expecting a KoboldCPP-compatible endpoint at http://localhost:5001
echo.
living-agent run --cycles 100 --endpoint http://localhost:5001/api/v1/generate
pause
