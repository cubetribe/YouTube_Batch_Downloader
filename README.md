# 🎬 YouTube Batch Downloader

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)
[![Made with Claude Code](https://img.shields.io/badge/built%20with-Claude%20Code-5436DA.svg)](https://claude.ai/code)

> **📖 Deutsche Version weiter unten** | **German version below**

A simple, powerful YouTube downloader with batch functionality for Windows, macOS, and Linux. Built with **100% Vibe-Coding** 🎵 – because sometimes the best tools emerge when you just start building.

## ✨ Features

- 🎬 **Video Download** - Downloads YouTube videos in best quality (MP4)
- 🎵 **Audio Extraction** - Converts videos directly to MP3 (192 kbps)
- 📦 **Batch Download** - Download multiple videos at once
- 🎯 **Smart URL Detection** - Automatically detects YouTube URLs from any text
- 🔄 **Multi-Input Support** - Paste URLs multiple times, as often as you want
- 📊 **Progress Display** - See exactly what's happening
- ✅ **Summary View** - Review all URLs before download
- 💻 **Terminal-based** - Simple operation, no setup required

> **📌 Note:** The GUI version is currently in development. If you'd like to help, you're warmly invited! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 🎯 Use Cases

- Create offline playlists for long journeys
- Backup important video tutorials
- Download podcast episodes as audio
- Create music collections from YouTube
- Batch download for course videos

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python Package Manager)

### Setup

```bash
# Clone repository
git clone https://github.com/cubetribe/YouTube_Batch_Downloader.git
cd YouTube_Batch_Downloader

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Start

```bash
python3 start.py
```

### Menu Options

```
==================================================
🎬 YOUTUBE DOWNLOADER 🎵
==================================================

1️⃣  Download Video (MP4)
2️⃣  Download Audio (MP3)
3️⃣  Batch Download - Videos (MP4)
4️⃣  Batch Download - Audios (MP3)
5️⃣  Exit

==================================================
```

### Batch Download - How it works

1. Select option **3** (Videos) or **4** (Audios)
2. Paste URLs – **multiple times possible!**
   ```
   >>> [Cmd+V - paste first URLs]
   ✅ 8 URL(s) detected

   >>> [Cmd+V - paste more URLs]
   ✅ 5 URL(s) detected

   >>> start
   ```
3. Review the summary
   ```
   📊 SUMMARY
   ✅ Total 13 YouTube URL(s) found:

   1. https://www.youtube.com/watch?v=...
   2. https://www.youtube.com/watch?v=...
   ...
   ```
4. Confirm with `ja` (yes) and let's go! 🚀

### Additional Commands (during URL input)

- `show` - Display all currently found URLs
- `clear` - Delete all URLs and start fresh
- `file` - Load URLs from a text file
- `start` / `fertig` - End input and show summary

### Direct Download (CLI)

```bash
# Single video
python3 src/downloader.py "https://youtube.com/watch?v=..."

# Audio only
python3 src/downloader.py "https://youtube.com/watch?v=..." audio
```

## 📁 Output

All downloads are saved to your **Downloads folder** (`~/Downloads`) by default.

## 🛠 Technology

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - The core engine for YouTube downloads
- **[Rich](https://github.com/Textualize/rich)** - For beautiful terminal output (GUI)
- **Python 3** - Because Python is simply amazing
- **Regex Magic** - For intelligent URL extraction

## 💡 The Story Behind

This project emerged from the daily need to download multiple YouTube videos. Instead of going through the same process 30 times, I built a batch downloader with **[Claude Code](https://claude.ai/code)** in no time.

**100% Vibe-Coding** 🎵 – I use AI tools daily for my projects. I use this tool every day, so I wanted to share it with the community.

## 🎓 Learn AI-Assisted Coding

Want to code like this too? Check out my **[training platform aiEX Academy](https://www.goaiex.com)**! There I show you how to develop more efficiently and faster with AI tools like Claude Code, Copilot, and more.

I've been doing this for a while and have implemented larger projects too – but this one is special because it's so practical in everyday life.

## 🤝 Contributing

Feedback, feature requests, and pull requests are **warmly welcome**!

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Feature Ideas?

Feel free to open an [Issue](https://github.com/cubetribe/YouTube_Batch_Downloader/issues) and describe:
- What you'd like
- Why it would be useful
- How it should work

## 📝 Roadmap

- [ ] **GUI Version** (tkinter foundation available, in development - help welcome!)
- [ ] Playlist support
- [ ] Quality selection (4K, 1080p, 720p, etc.)
- [ ] Download history
- [ ] Resume after interruption
- [ ] Subtitle download
- [ ] Thumbnail download

## 🐛 Known Issues

- Some YouTube videos might be blocked by regional restrictions
- Private videos cannot be downloaded
- Age-restricted videos may require additional authentication

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

## 🙏 Credits

- **yt-dlp Team** - For the amazing YouTube download tool
- **Claude (Anthropic)** - For coding support
- **Open Source Community** - For inspiration and support

## ⚠️ Disclaimer

This tool is intended exclusively for **downloading videos for personal, private use** in compliance with YouTube's terms of service and applicable copyright law.

Please note:
- Respect copyrights and content creators
- Use downloads for private use only
- Do not redistribute protected content
- Support creators on YouTube (likes, subscriptions, etc.)

## 💬 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/cubetribe/YouTube_Batch_Downloader/issues)
- **AI Training Platform:** [aiEX Academy](https://www.goaiex.com)

---

**Like the project?** Give it a ⭐️ on GitHub!

Made with ❤️ and Claude Code

---
---

<br>
<br>

# 🎬 YouTube Batch Downloader

**[🇬🇧 English version above](#-youtube-batch-downloader) | Deutsche Version**

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)
[![Made with Claude Code](https://img.shields.io/badge/built%20with-Claude%20Code-5436DA.svg)](https://claude.ai/code)

Ein einfacher, leistungsstarker YouTube-Downloader mit Batch-Funktion für Windows, macOS und Linux. Entwickelt mit **100% Vibe-Coding** 🎵 – weil manchmal die besten Tools entstehen, wenn man einfach mal macht.

## ✨ Features

- 🎬 **Video Download** - Lädt YouTube-Videos in bester Qualität (MP4)
- 🎵 **Audio Extraktion** - Konvertiert Videos direkt zu MP3 (192 kbps)
- 📦 **Batch Download** - Lade mehrere Videos auf einmal herunter
- 🎯 **Smart URL Detection** - Erkennt automatisch YouTube-URLs aus beliebigem Text
- 🔄 **Multi-Input Support** - Füge URLs mehrfach ein, beliebig oft
- 📊 **Fortschrittsanzeige** - Sehe genau was passiert
- ✅ **Zusammenfassung** - Überprüfe alle URLs vor dem Download
- 💻 **Terminal-basiert** - Einfache Bedienung, kein Setup nötig

> **📌 Hinweis:** Die GUI-Version ist aktuell in Entwicklung. Wenn du Lust hast mitzuhelfen, bist du herzlich eingeladen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md)

## 🎯 Use Cases

- Erstelle Offline-Playlists für lange Reisen
- Sichere wichtige Video-Tutorials
- Lade Podcast-Episoden als Audio
- Erstelle Musiksammlungen von YouTube
- Batch-Download für Kurs-Videos

## 📦 Installation

### Voraussetzungen

- Python 3.9 oder höher
- pip (Python Package Manager)

### Setup

```bash
# Repository klonen
git clone https://github.com/cubetribe/YouTube_Batch_Downloader.git
cd YouTube_Batch_Downloader

# Virtuelle Umgebung erstellen (empfohlen)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# oder
venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt
```

## 🚀 Verwendung

### Start

```bash
python3 start.py
```

### Menü-Optionen

```
==================================================
🎬 YOUTUBE DOWNLOADER 🎵
==================================================

1️⃣  Video herunterladen (MP4)
2️⃣  Audio herunterladen (MP3)
3️⃣  Batch Download - Videos (MP4)
4️⃣  Batch Download - Audios (MP3)
5️⃣  Beenden

==================================================
```

### Batch Download - So geht's

1. Wähle Option **3** (Videos) oder **4** (Audios)
2. Füge URLs ein – **mehrfach möglich!**
   ```
   >>> [Cmd+V - erste URLs einfügen]
   ✅ 8 URL(s) erkannt

   >>> [Cmd+V - noch mehr URLs einfügen]
   ✅ 5 URL(s) erkannt

   >>> start
   ```
3. Überprüfe die Zusammenfassung
   ```
   📊 ZUSAMMENFASSUNG
   ✅ Insgesamt 13 YouTube URL(s) gefunden:

   1. https://www.youtube.com/watch?v=...
   2. https://www.youtube.com/watch?v=...
   ...
   ```
4. Bestätige mit `ja` und los geht's! 🚀

### Weitere Befehle (während der URL-Eingabe)

- `show` - Zeigt alle bisher gefundenen URLs
- `clear` - Löscht alle URLs und startet neu
- `file` - Lädt URLs aus einer Textdatei
- `start` / `fertig` - Beendet Eingabe und zeigt Zusammenfassung

### Direkter Download (CLI)

```bash
# Einzelnes Video
python3 src/downloader.py "https://youtube.com/watch?v=..."

# Nur Audio
python3 src/downloader.py "https://youtube.com/watch?v=..." audio
```

## 📁 Output

Alle Downloads landen standardmäßig in deinem **Downloads-Ordner** (`~/Downloads`).

## 🛠 Technologie

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Das Herzstück für YouTube-Downloads
- **[Rich](https://github.com/Textualize/rich)** - Für schöne Terminal-Ausgaben (GUI)
- **Python 3** - Weil Python einfach großartig ist
- **Regex Magic** - Für intelligente URL-Extraktion

## 💡 Die Story dahinter

Dieses Projekt ist entstanden aus der Notwendigkeit, täglich mehrere YouTube-Videos herunterzuladen. Statt 30x den gleichen Prozess zu durchlaufen, habe ich mit **[Claude Code](https://claude.ai/code)** in kürzester Zeit einen Batch-Downloader gebaut.

**100% Vibe-Coding** 🎵 – Ich nutze KI-Tools täglich für meine Projekte. Dieses Tool verwende ich jeden Tag, deswegen wollte ich es mit der Community teilen.

## 🎓 Lerne KI-gestütztes Coding

Du willst auch so coden? Schau dir meine **[Schulungsplattform aiEX Academy](https://www.goaiex.com)** an! Dort zeige ich dir, wie du mit KI-Tools wie Claude Code, Copilot und mehr effizienter und schneller entwickelst.

Ich mache das schon länger und habe auch größere Projekte umgesetzt – aber dieses hier ist besonders, weil es so praktisch im Alltag ist.

## 🤝 Contributing

Feedback, Feature-Requests und Pull Requests sind **herzlich willkommen**!

Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Feature-Ideen?

Öffne gerne ein [Issue](https://github.com/cubetribe/YouTube_Batch_Downloader/issues) und beschreibe:
- Was du dir wünschst
- Warum es nützlich wäre
- Wie es funktionieren sollte

## 📝 Roadmap

- [ ] **GUI-Version** (tkinter-Grundgerüst vorhanden, in Entwicklung - Hilfe willkommen!)
- [ ] Playlist-Support
- [ ] Qualitäts-Auswahl (4K, 1080p, 720p, etc.)
- [ ] Download-History
- [ ] Fortschritts-Wiederherstellung nach Abbruch
- [ ] Untertitel-Download
- [ ] Thumbnail-Download

## 🐛 Known Issues

- Manche YouTube-Videos könnten durch regionale Einschränkungen blockiert sein
- Private Videos können nicht heruntergeladen werden
- Age-restricted Videos benötigen eventuell zusätzliche Authentifizierung

## 📄 License

Dieses Projekt ist lizenziert unter der **MIT License** - siehe [LICENSE](LICENSE) für Details.

## 🙏 Credits

- **yt-dlp Team** - Für das großartige YouTube-Download-Tool
- **Claude (Anthropic)** - Für die Unterstützung beim Coding
- **Open Source Community** - Für Inspiration und Support

## ⚠️ Disclaimer

Dieses Tool dient ausschließlich zum **Download von Videos für den persönlichen, privaten Gebrauch** unter Einhaltung der YouTube-Nutzungsbedingungen und geltenden Urheberrechts.

Bitte beachte:
- Respektiere Urheberrechte und Content-Creator
- Nutze Downloads nur für privaten Gebrauch
- Verbreite keine geschützten Inhalte weiter
- Unterstütze Creator auf YouTube (Likes, Abos, etc.)

## 💬 Kontakt & Support

- **Issues:** [GitHub Issues](https://github.com/cubetribe/YouTube_Batch_Downloader/issues)
- **Schulungsplattform:** [aiEX Academy](https://www.goaiex.com)

---

**Gefällt dir das Projekt?** Gib ihm einen ⭐️ auf GitHub!

Made with ❤️ and Claude Code
