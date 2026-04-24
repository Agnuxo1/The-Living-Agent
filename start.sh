#!/usr/bin/env bash
# The Living Agent v1.0.0 - Chess-Grid Engine launcher (Linux/macOS)
set -e

echo "=================================================="
echo "      THE LIVING AGENT v1.0.0"
echo "      Chess-Grid Autonomous Research Engine"
echo "      P2PCLAW Silicon Layer"
echo "=================================================="
echo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate venv if present (supports `venv` and `.venv`).
if [ -f "venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

# Make sure the `living-agent` CLI is available.
if ! command -v living-agent >/dev/null 2>&1; then
    echo "[!] \`living-agent\` CLI not found. Installing package in editable mode..."
    pip install -e .
fi

if [ ! -f "knowledge/grid/cell_R0_C0.md" ]; then
    echo "[*] Knowledge grid not found. Initializing 16x16 grid..."
    living-agent init --grid-dir knowledge
fi

echo
echo "[*] Launching Chess-Grid Agent Engine..."
echo "[i] Expecting a KoboldCPP-compatible endpoint at http://localhost:5001"
echo
exec living-agent run --cycles 100 --endpoint http://localhost:5001/api/v1/generate
