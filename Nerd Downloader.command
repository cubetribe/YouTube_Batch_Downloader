#!/bin/bash
#
# Nerd Downloader — double-click launcher for macOS.
# First run sets up a local virtual environment and installs dependencies;
# every run afterwards just starts the app and opens it in your browser.
#
# If macOS blocks the first launch ("not verified"), right-click this file
# and choose "Open" once.

set -e
# Keep the Terminal window open on any failure so the error is readable
# (a double-clicked .command otherwise closes instantly on error).
trap 'echo; echo "❌ Fehler beim Start — Details oben. Enter zum Schließen."; read -r _' ERR

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

PY="$DIR/venv/bin/python"

if [ ! -x "$PY" ]; then
  # Need to create the venv — make sure the available python3 is recent enough
  # (yt-dlp requires Python 3.10+). A friend's stock macOS python3 may be 3.9.
  if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
    echo "❌ Python 3.10+ wird benötigt (gefunden: $(python3 --version 2>&1))."
    echo "   Bitte installieren, z. B.:  brew install python@3.12"
    exit 1
  fi
  echo "→ Erstelle virtuelle Umgebung (einmalig)…"
  python3 -m venv venv
  PY="$DIR/venv/bin/python"
fi

if ! "$PY" -c "import flask, yt_dlp" >/dev/null 2>&1; then
  echo "→ Installiere Abhängigkeiten (einmalig)…"
  "$PY" -m pip install --quiet --upgrade pip
  "$PY" -m pip install --quiet -r "$DIR/nerd_downloader/requirements.txt"
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "⚠️  ffmpeg nicht gefunden — für HD/4K-Merge und MP3 bitte: brew install ffmpeg"
fi

exec "$PY" -m nerd_downloader
