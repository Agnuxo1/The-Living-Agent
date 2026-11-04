# The Living Agent - Autonomous Setup Script
# Project: The Living Agent
# Copyright (c) 2026 Francisco Angulo de Lafuente
# ORCID: https://orcid.org/0009-0001-1634-7063
# Attribution record: 2026-11-04
# SPDX-License-Identifier: Apache-2.0

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Setting up The Living Agent Environment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Python not found. Please install Python 3.10+ and add it to PATH." -ForegroundColor Red
    exit
}

# 2. Create Virtual Environment
Write-Host "[*] Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# 3. Install Dependencies
Write-Host "[*] Installing requirements (requests, colorama)..." -ForegroundColor Yellow
./venv/Scripts/pip install requests colorama

# 4. Success
Write-Host ""
Write-Host "[+] Setup Complete!" -ForegroundColor Green
Write-Host "[i] Remember to have KoboldCPP running with the Qwen model on http://localhost:5001" -ForegroundColor Gray
Write-Host "[i] Run start.bat to begin the research cycle." -ForegroundColor Gray
