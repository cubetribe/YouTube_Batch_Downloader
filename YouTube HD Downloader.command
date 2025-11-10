#!/bin/bash

# YouTube HD/4K Downloader - macOS Launch Script
# Downloads videos in HD/4K quality (minimum 1080p)

# Zum Verzeichnis des Scripts wechseln
cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment nicht gefunden!"
    echo "Erstelle venv..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install yt-dlp
else
    # Virtuelle Umgebung aktivieren
    source venv/bin/activate
fi

# Check for yt-dlp updates
echo "🔄 Prüfe auf yt-dlp Updates..."
pip install --upgrade yt-dlp --quiet

# Clear screen and start
clear
echo "============================================================"
echo "🎬 YOUTUBE HD/4K DOWNLOADER"
echo "============================================================"
echo "✅ Bereit für HD/4K Downloads!"
echo "ℹ️  Für beste Qualität: In Chrome bei YouTube anmelden"
echo "============================================================"
echo ""

# Python-Script starten
python start.py

# Terminal offen lassen
echo ""
echo "Drücke Enter zum Beenden..."
read