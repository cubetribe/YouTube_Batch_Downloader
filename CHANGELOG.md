# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Geplant
- GUI-Version mit tkinter
- Playlist-Support
- Qualitäts-Auswahl (4K, 1080p, 720p)
- Download-History
- Fortschritts-Wiederherstellung nach Abbruch
- Untertitel-Download
- Thumbnail-Download

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
