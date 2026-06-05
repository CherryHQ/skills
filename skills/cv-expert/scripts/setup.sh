#!/usr/bin/env bash
# setup.sh — One-time dependency installer for cv-expert plugin
# Run once before first use: bash setup.sh

set -euo pipefail

echo "[cv-expert] Installing dependencies..."

# Install python-docx (required for docx parse/write)
pip install "python-docx>=1.2.0" --quiet

echo "[cv-expert] Verifying python-docx installation..."
python3 -c "from docx import Document; print('[cv-expert] python-docx OK')"

echo "[cv-expert] Setup complete. You can now run /cv-expert."
