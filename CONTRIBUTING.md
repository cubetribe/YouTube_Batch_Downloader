# Contributing to YouTube Batch Downloader

Erstmal: **Danke**, dass du dich für dieses Projekt interessierst! 🙏

Dieses Projekt ist aus dem Alltag entstanden und wird mit der Community geteilt. Feedback, Verbesserungen und neue Ideen sind herzlich willkommen!

## 🎯 Wie du beitragen kannst

### 1. 🐛 Bugs melden

Hast du einen Bug gefunden? Kein Problem!

1. Schau zuerst in den [Issues](https://github.com/cubetribe/YouTube_Batch_Downloader/issues), ob das Problem schon bekannt ist
2. Falls nicht, öffne ein neues Issue mit:
   - **Titel**: Kurze Beschreibung des Problems
   - **Beschreibung**: Was ist passiert? Was sollte passieren?
   - **Schritte zur Reproduktion**: Wie kann man den Bug nachstellen?
   - **System**: macOS/Linux/Windows, Python-Version
   - **Fehlermeldung**: Falls vorhanden, kopiere die komplette Fehlermeldung

### 2. 💡 Feature-Vorschläge

Du hast eine Idee für ein neues Feature?

1. Öffne ein [Issue](https://github.com/cubetribe/YouTube_Batch_Downloader/issues) mit dem Label `enhancement`
2. Beschreibe:
   - **Was** soll das Feature können?
   - **Warum** wäre es nützlich?
   - **Wie** könnte es funktionieren?
3. Eventuell gibt es schon eine Lösung oder jemand arbeitet daran!

### 3. 🔧 Code beitragen

Du willst selbst Code beisteuern? Großartig!

#### Setup für Entwicklung

```bash
# Repository forken und klonen
git clone https://github.com/DEIN-USERNAME/YouTube_Batch_Downloader.git
cd YouTube_Batch_Downloader

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Pull Request Prozess

1. **Fork** das Repository
2. **Branch** erstellen für dein Feature/Fix
   ```bash
   git checkout -b feature/dein-feature-name
   # oder
   git checkout -b fix/dein-bugfix-name
   ```
3. **Code** schreiben und testen
4. **Commit** mit aussagekräftiger Message
   ```bash
   git commit -m "feat: Neue Funktion XYZ hinzugefügt"
   # oder
   git commit -m "fix: Bug in URL-Extraktion behoben"
   ```
5. **Push** zu deinem Fork
   ```bash
   git push origin feature/dein-feature-name
   ```
6. **Pull Request** auf GitHub erstellen

#### Commit-Message-Konvention

Wir verwenden [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - Neues Feature
- `fix:` - Bugfix
- `docs:` - Dokumentation
- `style:` - Code-Formatierung
- `refactor:` - Code-Refactoring
- `test:` - Tests hinzufügen/ändern
- `chore:` - Maintenance-Tasks

Beispiele:
```
feat: Playlist-Download Support hinzugefügt
fix: URL-Extraktion für kurze YouTube-Links
docs: Installation Guide erweitert
```

### 4. 📖 Dokumentation verbessern

Auch Dokumentation ist wichtig!

- Tippfehler gefunden? → Mach einen PR!
- Etwas unklar? → Öffne ein Issue!
- Beispiele fehlen? → Ergänze sie!

## 🎨 Code-Style

- **Python**: Folge [PEP 8](https://pep8.org/)
- **Kommentare**: Auf Deutsch oder Englisch, Hauptsache verständlich
- **Docstrings**: Für Funktionen und Klassen
- **Type Hints**: Gerne verwenden, aber kein Muss

Beispiel:
```python
def extract_youtube_urls(text: str) -> list[str]:
    """
    Extract all YouTube URLs from text using regex

    Args:
        text: Input text containing YouTube URLs

    Returns:
        List of unique YouTube URLs
    """
    # Implementation...
```

## 🧪 Testing

Automatisierte Tests laufen mit:

```bash
python -m pytest -q
```

Downloader-, Netzwerk- und Cookie-Logik muss in Tests offline bleiben. Mocke `yt_dlp`, Browser-Cookies, Netzwerkzugriffe und echte Downloads, damit Tests reproduzierbar bleiben und keine Nutzerdaten oder lokalen Dateien beruehren.

Fuehre fuer repo-weite Checks bei Bedarf zusaetzlich aus:

```bash
python -m ruff check start.py src tests --select E9,F63,F7,F82 --target-version py310
python -m compileall -q start.py src gui download_4k.py download_best.py download_force_4k.py download_hd.py download_strict_hd.py download_ultimate.py
```

## 📋 Projekt-Struktur

```
YouTube_Batch_Downloader/
├── start.py              # Hauptmenü
├── simple_downloader.py  # Core Download-Logik
├── gui/                  # GUI-Komponenten (in Arbeit)
├── downloads/            # Standard-Download-Ordner
├── README.md             # Hauptdokumentation
├── CONTRIBUTING.md       # Diese Datei
├── LICENSE               # MIT License
└── requirements.txt      # Python Dependencies
```

## ❓ Fragen?

Bei Fragen:
- Öffne ein [Issue](https://github.com/cubetribe/YouTube_Batch_Downloader/issues)
- Schau in bestehende Discussions
- Kontaktiere mich über [aiEX Academy](https://www.goaiex.com)

## 🎓 Lerne mit uns

Interessiert an **AI-gestütztem Coding**?

Schau dir meine [Schulungsplattform aiEX Academy](https://www.goaiex.com) an! Dort lernst du, wie du mit Tools wie Claude Code, GitHub Copilot und mehr effizienter entwickelst.

## 🙏 Danke!

Jeder Beitrag, egal wie klein, hilft!

- ⭐️ **Star** das Projekt
- 🐛 **Bugs** melden
- 💡 **Ideen** teilen
- 🔧 **Code** beitragen
- 📖 **Docs** verbessern

**Let's build something great together!** 🚀

---

Made with ❤️ and Claude Code
