# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Fixed
- Video-Downloads versuchen HD/4K-Formate zuerst ohne Browser-Cookies, damit Cookie-bedingt unvollständige YouTube-Formatlisten nicht sofort zum Abbruch führen.

### Geplant
- GUI-Version mit tkinter
- Playlist-Support
- Qualitäts-Auswahl (4K, 1080p, 720p)
- Download-History
- Fortschritts-Wiederherstellung nach Abbruch
- Untertitel-Download
- Thumbnail-Download

## [2.1.0] - 2025-11-12

### ✨ Added
- **Download-Logging**: Alle Download-Operationen werden nun in `src/download_log.txt` protokolliert
- **Vereinfachtes Menü**: Übersichtlichere Benutzerführung mit klaren 4K/1080p Prioritäten
- **Verbesserte Batch-Funktionalität**: Zuverlässiger Batch-Download für mehrere Videos gleichzeitig

### Changed
- **Refactored Downloader**: `downloader_enhanced.py` wurde vollständig überarbeitet für bessere Zuverlässigkeit
- **Strikte Qualitätspriorisierung**: 4K → 1080p → Abbruch (kein Fallback auf niedrigere Qualitäten)
- **Optimiertes Start-Menü**: Entfernte komplexe Optionen zugunsten von Stabilität

### Fixed
- **FullHD Download**: FullHD (1080p) Downloads funktionieren jetzt zuverlässig
- **Batch Download Stabilität**: Batch-Downloads sind nun wesentlich stabiler und fehlerfrei

### Known Issues
- **4K Download**: 4K Downloads funktionieren nicht immer zuverlässig (wird in zukünftigen Versionen adressiert)
- 4K Fallback auf 1080p funktioniert jedoch problemlos

## [2.0.0] - 2025-11-12

### ✨ Added
- **Neue Start-Logik**: Ein zentrales Start-Menü (`start.py`) für alle Download-Optionen
- **Priorisierter HD/4K Download**: Neue Logik, die immer die beste verfügbare Qualität zwischen 4K und 1080p wählt
- **Strikte Qualitätskontrolle**: Downloads werden abgebrochen, wenn eine Mindestqualität von 1080p nicht verfügbar ist
- **Ultimate HD Downloader**: Eine neue Strategie, die mehrere Download-Methoden kombiniert
- **Automatische Cookie-Integration**: Nutzt automatisch Chrome-Cookies für angemeldete Sessions
- **Verbesserte Audio-Downloads**: Audio wird nun standardmäßig in 320kbps MP3-Qualität heruntergeladen

### Changed
- **Konsolidierte Skripte**: Die Funktionalität der alten `download_*.py` Skripte wurde zusammengefasst
- **Verbesserte Benutzerführung**: Übersichtlicheres Hauptmenü mit direktem Zugriff auf alle Funktionen

### Removed
- Veraltete und redundante Download-Skripte, die durch die neue, einheitliche Logik ersetzt wurden

## [1.0.0] - 2025-01-29

### 🎉 Initial Release

#### ✨ Features
- **Video Download**: YouTube-Videos in bester Qualität (MP4)
- **Audio Extraktion**: Konvertierung zu MP3 (192 kbps)
- **Batch Download**: Mehrere Videos/Audios auf einmal herunterladen
- **Smart URL Detection**: Automatische Erkennung von YouTube-URLs aus Text
- **Multi-Input Support**: URLs mehrfach einfügen möglich
- **Fortschrittsanzeige**: Detaillierte Progress-Informationen
- **Zusammenfassung**: Überprüfung aller URLs vor Download
- **Bestätigungsschritt**: Explizite Bestätigung vor Download-Start

#### 🛠 Technisch
- Python 3.9+ Support
- yt-dlp Integration mit Android client workaround
- Regex-basierte URL-Extraktion
- Terminal-basiertes interaktives Menü
- Fehlerbehandlung und Retry-Logik
- Multi-Command-Support (show, clear, file, start)

#### 📝 Dokumentation
- Umfassendes README.md
- CONTRIBUTING.md für Contributors
- GitHub Issue Templates (Bug Report, Feature Request)
- Pull Request Template
- MIT License

---

## Kategorien

- `Added` für neue Features
- `Changed` für Änderungen an bestehenden Features
- `Deprecated` für Features die bald entfernt werden
- `Removed` für entfernte Features
- `Fixed` für Bug Fixes
- `Security` für Sicherheits-Updates
