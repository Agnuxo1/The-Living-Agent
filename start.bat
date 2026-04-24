@echo off
TITLE The Living Agent v3.0 - Chess-Grid Engine
echo ==================================================
echo       THE LIVING AGENT v3.0
echo       Chess-Grid Autonomous Research Engine
echo       P2PCLAW Silicon Layer
echo ==================================================
echo.

IF NOT EXIST "venv" (
    echo [!] Virtual environment not found. Running installer...
    powershell -ExecutionPolicy Bypass -File install.ps1
)

IF NOT EXIST "knowledge\grid\cell_R0_C0.md" (
    echo [!] Knowledge grid not found.
    call venv\Scripts\activate
    IF DEFINED HEYTING_ROOT IF EXIST "%HEYTING_ROOT%\lean_index\catalog.json" (
        echo [*] Rebuilding verified Heyting-backed grid...
        set VERIFIED_GRID_TMP=knowledge\verified_grid_artifact
        python heyting_bridge\living_agent_grid_builder.py --rows 16 --cols 16 --output-root "%VERIFIED_GRID_TMP%"
        IF EXIST "%VERIFIED_GRID_TMP%\grid\cell_R0_C0.md" (
            mkdir knowledge\grid 2>nul
            xcopy /E /I /Y "%VERIFIED_GRID_TMP%\grid\*" "knowledge\grid\" >nul
            copy /Y "%VERIFIED_GRID_TMP%\grid_index.md" "knowledge\grid_index.md" >nul
            copy /Y "%VERIFIED_GRID_TMP%\verified_grid_index.json" "knowledge\grid\verified_grid_index.json" >nul
        ) ELSE (
            echo [!] Verified grid build failed. Falling back to legacy placeholder grid.
            python grid_generator.py
        )
    ) ELSE (
        echo [!] HEYTING_ROOT not configured. Falling back to legacy placeholder grid.
        python grid_generator.py
    )
)

echo [*] Launching Chess-Grid Agent Engine...
call venv\Scripts\activate
python agent_v2_production.py
pause
