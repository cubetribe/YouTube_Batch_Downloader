#!/bin/bash

# YouTube Downloader - Doppelklick Script
# Dieses Script startet den YouTube Downloader per Doppelklick

# Wechsle ins Script-Verzeichnis
cd "$(dirname "$0")"

echo "🎬 YouTube Downloader wird gestartet..."
echo "📂 Arbeitsverzeichnis: $(pwd)"
echo ""

# Prüfe ob Virtual Environment existiert
if [ ! -d "venv" ]; then
    echo "❌ Virtual Environment nicht gefunden!"
    echo "Bitte erst das Setup ausführen:"
    echo "python3 -m venv venv"
    echo "source venv/bin/activate"
    echo "pip install yt-dlp"
    read -p "Enter drücken zum Beenden..."
    exit 1
fi

# Aktiviere Virtual Environment
echo "🔧 Aktiviere Virtual Environment..."
source venv/bin/activate

# Prüfe ob yt-dlp installiert ist
if ! python -c "import yt_dlp" 2>/dev/null; then
    echo "❌ yt-dlp nicht gefunden!"
    echo "Installiere yt-dlp..."
    pip install yt-dlp
fi

# Benutzer fragen: CLI oder GUI
echo "🎬 YouTube Downloader"
echo ""
echo "Welche Version möchten Sie starten?"
echo "1) GUI-Version (grafische Oberfläche)"
echo "2) CLI-Version (Terminal)"
echo ""
read -p "Auswahl (1-2): " choice

case $choice in
    1)
        echo "✅ Starte GUI-Version..."
        echo ""
        python start_gui.py
        ;;
    2)
        echo "✅ Starte CLI-Version..."
        echo ""
        python start.py
        ;;
    *)
        echo "❌ Ungültige Auswahl. Starte GUI-Version..."
        echo ""
        python start_gui.py
        ;;
esac

echo ""
echo "👋 Downloader beendet."
read -p "Enter drücken zum Schließen..."