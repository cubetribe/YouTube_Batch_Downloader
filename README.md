# 🤓 Nerd Downloader

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)
[![Made with Claude Code](https://img.shields.io/badge/built%20with-Claude%20Code-5436DA.svg)](https://claude.ai/code)

> **Paste · Analyze · Download.** Eine kleine lokale Web-App für den Mac, mit der du
> YouTube-Videos (und perspektivisch mehr) per Link-Einfügen herunterlädst.
> Für den persönlichen Gebrauch.

Nerd Downloader läuft komplett lokal auf deinem Mac: Du startest die App per
Doppelklick, sie öffnet sich im Browser unter `http://127.0.0.1:8765`, du fügst
einen Link ein, siehst die Video-Infos, wählst den Zielordner und lädst herunter.
Kein Account, keine Cloud, kein Netzwerk-Zugriff von außen.

---

## ⚡️ Schnellstart

1. **`Nerd Downloader.command` doppelklicken.**
   - Beim **ersten Start** richtet sich die App selbst ein (virtuelle Umgebung +
     Abhängigkeiten). Das dauert einmalig ein paar Sekunden.
   - macOS blockt unsignierte Programme beim ersten Mal:
     **Rechtsklick auf die Datei → „Öffnen" → „Öffnen"** (nur einmal nötig).
     Alternativ: *Systemeinstellungen → Datenschutz & Sicherheit → „Trotzdem öffnen"*.
2. Der Browser öffnet sich automatisch.
3. Auf YouTube den Link kopieren → in der App oben auf das **Einfügen-Icon** 📋
   klicken (liest die Zwischenablage) → **Analysieren**.
4. Qualität & Zielordner wählen → **Download starten**.

Fertig. Die Datei landet im gewählten Ordner; per **„Im Finder zeigen"** springst
du direkt dorthin.

## ✨ Features

- 📋 **Paste-First** – Link einfügen, fertig. Das Icon oben liest deine Zwischenablage.
- 🔎 **Video-Infos vor dem Download** – Titel, Thumbnail, Kanal, Dauer, max. Qualität.
- 🎬 **HD / 4K** – beste Qualität bis 2160p, sauber zu MP4 zusammengeführt (ffmpeg).
- 🎵 **MP3** – Audio-Extraktion mit 320 kbps.
- 📁 **Nativer Ordner-Picker** – „Wählen…" öffnet den echten macOS-Dialog; plus
  Schnellwahl für Downloads / Desktop / Movies.
- 📊 **Live-Fortschritt** – Prozent, Tempo und ETA in Echtzeit.
- 🔒 **Lokal & privat** – Server lauscht nur auf `127.0.0.1`, nie im Netzwerk.
- 🧩 **Erweiterbar** – die Engine ist `yt-dlp`; das unterstützt 1000+ Seiten, also
  funktionieren perspektivisch auch andere Quellen ohne Code-Änderung.

## 🧰 Voraussetzungen

- **macOS** (für den nativen Ordner-Picker & „Im Finder zeigen"; der Rest läuft
  plattformübergreifend).
- **Python 3.10+** (`brew install python@3.12`, falls nötig).
- **ffmpeg** für HD/4K-Merge und MP3: `brew install ffmpeg`.

Der Launcher prüft Python/ffmpeg und installiert die Python-Abhängigkeiten
(`flask`, `yt-dlp`) automatisch in eine lokale `venv/`.

## 🏗️ Wie es funktioniert

```
Browser (Vanilla-JS UI)
   │  fetch /api/info, /api/download
   ▼
Flask (127.0.0.1)  ──►  yt-dlp Engine  ──►  ffmpeg (Merge / MP3)
   ▲  Server-Sent Events (Live-Fortschritt)
   │
Download läuft in einem Hintergrund-Thread; Fortschritt streamt per SSE zurück.
```

| Datei | Aufgabe |
|-------|---------|
| `nerd_downloader/__main__.py` | freien Port wählen, Server starten, Browser öffnen |
| `nerd_downloader/app.py` | Flask-Routen (`/api/info`, `/download`, `/progress`, `/choose-folder`, `/reveal`) |
| `nerd_downloader/engine.py` | `yt-dlp`: Metadaten + Download, mit Cookie-Fallback |
| `nerd_downloader/jobs.py` | Job-/Fortschritts-Verwaltung + SSE-Brücke |
| `nerd_downloader/macos.py` | nativer Ordner-Picker & Finder-Reveal via `osascript` |
| `nerd_downloader/static/` | UI (HTML/CSS/JS, kein Build-Schritt) |

**Robustheit:** Metadaten und Download werden zuerst **ohne** Browser-Cookies
versucht und bei Bedarf **mit** Chrome-Cookies wiederholt — das umgeht die
häufigen, cookie-bedingt unvollständigen YouTube-Formatlisten.

### Manuell starten (statt Doppelklick)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m nerd_downloader
```

---

## 🛠️ Entwicklung

```bash
pip install -r requirements-dev.txt
python -m ruff check nerd_downloader --select E9,F63,F7,F82 --target-version py310
python -m compileall -q nerd_downloader
python -m pytest -q
```

## 📟 Legacy: Terminal-CLI

Die ursprünglichen Terminal-Skripte bleiben erhalten und funktionieren weiter:

```bash
python3 start.py
```

Sie bieten Batch-Download und Audio/Video-Auswahl im Menü. Siehe
`download_*.py` und `gui/` für die alten Varianten.

## 📄 Lizenz

MIT — siehe [LICENSE](LICENSE).

---

*Built with [Claude Code](https://claude.ai/code). Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp).*
